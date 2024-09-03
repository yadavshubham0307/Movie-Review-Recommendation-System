
# Movie Recommendation and Review Project

A Django-based movie recommendation and review system using Django REST Framework (DRF) integrates with a publicly available
movie database API (such as The Movie Database API) to fetch movie data and allows users to create, read, update, and delete reviews. Additionally, implemented a recommendation system based on user reviews and movie ratings.



## Technologies
- **Django:** Web framework.  
- **Django REST Framework:** API toolkit.  
- **Simple JWT:** Token.
- **SQLite:** Database (development).  
- **TMDB API:** Fetches movie data.
## Installation
*1.  Clone the Repository*
```sh
git clone https://github.com/yadavshubham0307/Movie-Review-Recommendation-System.git
cd Movie-Review-Recommendation-System
```  

*2. Set Up Environment*  

```sh
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

*3. Configure Environment*  
Create a .env file with: 

```sh
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=db_name
TMDB_API_KEY=your_tmdb_api_key
SIMPLE_JWT_SECRET_KEY=your_jwt_secret_key
```

*4. Apply Migrations and Start Server*  
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
## API Endpoints
- **Movies**: GET hostname/api/movies/, POST /api/movies/, etc.
- **Reviews:** GET hostname/api/reviews/, POST hostname/api/reviews/, etc.
- **Recommendations:** GET hostname/api/recommendations/

## API Artifacts
[Postman API Documentation](https://documenter.getpostman.com/view/38071239/2sAXjNWqFq)  
[Postman API Requests Collection](https://api.postman.com/collections/38071239-2ed21e2b-1a02-4aeb-9778-cb36f5e6486b?access_key=PMAT-01J6VEEQFYXVF4CJV71DF138JP)
## Fetching Movies from TMDB
```sh
python manage.py fetch_movies
```
Ensure TMDB API key is set in .env.

## Contributing
1. Fork the repo.
2. Create a feature branch.
3. Commit changes.
4. Push and create a Pull Request.
## License
MIT License - see [LICENSE](https://github.com/yadavshubham0307/Movie-Review-Recommendation-System?tab=MIT-1-ov-file#readme).
## Contact
**Email:** [yadavshubham0307@gmail.com](yadavshubham0307@gmail.com)  
**GitHub:** [yadavshubham0307](https://github.com/yadavshubham0307)
