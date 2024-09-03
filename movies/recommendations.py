from movies.models import Review, Movie
from django.db.models import Avg

def get_user_reviews(user_id):
    # Fetch all reviews by the user
    return Review.objects.filter(user_id=user_id).values_list('movie_id', 'rating')

def get_movie_reviews(movie_id):
    # Fetch all reviews for a movie
    return Review.objects.filter(movie_id=movie_id).values_list('user_id', 'rating')

def calculate_similarity(user_reviews, other_user_reviews):
    # Calculate similarity based on common rated movies
    common_movies = set(user_reviews.keys()).intersection(set(other_user_reviews.keys()))
    if not common_movies:
        return 0

    return len(common_movies)


def recommend_movies(user_id):
    user_reviews = dict(get_user_reviews(user_id))
    
    # No reviews by the user, no recommendations
    if not user_reviews:
        return []  

    # Fetch all users
    all_users = Review.objects.values_list('user_id', flat=True).distinct()
    
    # Remove the current user from the list
    all_users = set(all_users) - {user_id}

    # Find similar users
    user_similarities = {}
    for other_user_id in all_users:
        other_user_reviews = dict(get_user_reviews(other_user_id))
        similarity = calculate_similarity(user_reviews, other_user_reviews)
        if similarity > 0:
            user_similarities[other_user_id] = similarity

    # Find recommended movies
    recommended_movies = {}
    for similar_user, similarity in user_similarities.items():
        other_user_reviews = dict(get_user_reviews(similar_user))
        for movie_id, rating in other_user_reviews.items():
            if movie_id not in user_reviews:  # Only recommend movies not rated by the user
                if movie_id not in recommended_movies:
                    recommended_movies[movie_id] = 0
                recommended_movies[movie_id] += similarity * rating
    
    # Sort movies by recommendation score
    sorted_movies = sorted(recommended_movies.items(), key=lambda x: x[1], reverse=True)
    
    # Get top 5 movie IDs
    top_movie_ids = [movie_id for movie_id, _ in sorted_movies[:5]]
    
    # Fetch movie details
    movies = Movie.objects.filter(id__in=top_movie_ids)
    
    return movies
