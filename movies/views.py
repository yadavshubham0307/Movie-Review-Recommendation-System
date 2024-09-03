from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied,  ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from .models import Movie, Review
from .serializers import MovieSerializer, ReviewSerializer
from django_filters import rest_framework as django_filters
from .filters import MovieFilter, ReviewFilter
from .recommendations import recommend_movies



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class MovieListCreateAPIView(generics.ListCreateAPIView):
    """
    Fetch List of movies from DB and perform search, filter and create new movie
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = MovieFilter
    search_fields = ('title', 'genre')
    ordering_fields = ('release_date', 'title')
    ordering = ('title',)


class MovieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a movie.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer



class ReviewListCreateAPIView(generics.ListCreateAPIView):
    """
    Fetch List of reviews from DB and perform search, filter and create new reviews
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = ReviewFilter
    search_fields = ('movie__title', 'comment')
    ordering_fields = ('rating', 'created_at')
    ordering = ('created_at',)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        movie = serializer.validated_data['movie']

        # Check if the user has already reviewed this movie
        existing_review = Review.objects.filter(user=user, movie=movie).first()
        if existing_review:

            raise ValidationError("You have already reviewed this movie. Please use the PUT or PATCH method to update your existing review.")
        
        # Create a new review if no existing review is not found
        serializer.save(user=user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        movie = serializer.validated_data['movie']
        
        # Check if the user has already reviewed this movie
        existing_review = Review.objects.filter(user=user, movie=movie).first()
        if existing_review:
            
            return Response({
                'message': 'You have already reviewed this movie. Please use the PUT or PATCH method to update your existing review.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new review if no existing review is not found
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        
        return Response({
            'count': response.data['count'],
            'results': response.data['results']
        })

      
class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a review.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        review = super().get_object()
        if review.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this review.")
        return review

    def get(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = self.get_serializer(review)
        data = serializer.data
        # Remove user and movie from the response data
        data.pop('user', None)
        data.pop('movie', None)
        return Response(data)

    def put(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            raise PermissionDenied("You do not have permission to update this review.")
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            raise PermissionDenied("You do not have permission to update this review.")
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            raise PermissionDenied("You do not have permission to delete this review.")
        review.delete()
        return Response({"message": "Review deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    
class UserRecommendationsAPIView(generics.GenericAPIView):
    """
    Get movie recommendations based on user reviews.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        
        # Fetch recommended movies for the user
        recommended_movies = recommend_movies(user_id)
        
        if not recommended_movies:
            return Response({'recommendations': []}, status=200)
   
        serializer = MovieSerializer(recommended_movies, many=True)
        
        return Response({'recommendations': serializer.data})
