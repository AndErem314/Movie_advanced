import json
import os

DATA_FILE = "data.json"


def get_movies():
    """Returns a dictionary of dictionaries that contains the movies information.
    Loads from JSON file, returns empty dict if file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}


def save_movies(movies):
    """Saves movies dictionary to JSON file"""
    with open(DATA_FILE, 'w') as file:
        json.dump(movies, file, indent=4)


def add_movie(title, rating, year):
    """Adds a movie to the database"""
    movies = get_movies()
    movies[title] = {"rating": rating, "year": year}
    save_movies(movies)


def delete_movie(title):
    """Deletes a movie from the database"""
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)


def update_movie(title, rating):
    """Updates a movie's rating"""
    movies = get_movies()
    if title in movies:
        movies[title]["rating"] = rating
        save_movies(movies)