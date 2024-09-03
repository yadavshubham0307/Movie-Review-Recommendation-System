import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from movies.models import Movie

class Command(BaseCommand):
    help = 'Fetch movies from TMDb and update the database'

    def handle(self, *args, **kwargs):
        api_key = settings.TMDB_API_KEY
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            movies = data.get('results', [])

            for movie_data in movies:
                genres = movie_data.get('genre_ids', [])
                genre_names = ', '.join(map(str, genres))
                Movie.objects.update_or_create(
                    tmdb_id=movie_data['id'],
                    defaults={
                        'title': movie_data.get('title', ''),
                        'description': movie_data.get('overview', ''),
                        'release_date': movie_data.get('release_date', '1900-01-01'),
                        'genre': genre_names,
                        'poster': f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}"
                    }
                )
            self.stdout.write(self.style.SUCCESS('Successfully fetched and updated movies.'))
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error fetching data from TMDb: {e}'))
