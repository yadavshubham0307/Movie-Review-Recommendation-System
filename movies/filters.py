import django_filters
from .models import Movie, Review

class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    genre = django_filters.CharFilter(lookup_expr='icontains')
    release_date = django_filters.DateFilter(lookup_expr='exact')
    min_release_date = django_filters.DateFilter(field_name='release_date', lookup_expr='gte')
    max_release_date = django_filters.DateFilter(field_name='release_date', lookup_expr='lte')

    class Meta:
        model = Movie
        fields = ['title', 'genre', 'release_date', 'min_release_date', 'max_release_date']

class ReviewFilter(django_filters.FilterSet):
    movie_title = django_filters.CharFilter(field_name='movie__title', lookup_expr='icontains')
    comment = django_filters.CharFilter(lookup_expr='icontains')
    rating = django_filters.NumberFilter(lookup_expr='exact')
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    max_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='lte')
    created_at = django_filters.DateTimeFilter(lookup_expr='exact')
    min_created_at = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    max_created_at = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Review
        fields = ['movie_title', 'comment', 'rating', 'min_rating', 'max_rating', 'created_at', 'min_created_at', 'max_created_at']
