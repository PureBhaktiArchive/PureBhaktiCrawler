
from flask import Blueprint

from flask_restful import (Resource, Api, fields, marshal, reqparse, marshal_with)
import models
from resources.api_fields import movie_field
from remove_words import remove_stop_words


class MovieList(Resource):
    def get(self):
        return {
            'movies': [
                marshal(movie, movie_field)
                for movie in models.Movie.select()
            ]
        }


class MovieSearch(Resource):
    def get(self, query):
        if len(query.split(" ")) > 1:
            return {
                'movies': [
                    marshal(movie, movie_field)
                    for movie in models.Movie.select().where(
                        models.Movie.title.regexp(
                            r"[-\s_]+".join(remove_stop_words(query.lower().split(" ")))
                        )
                    )
                ]
            }
        return {
            'movies': [
                marshal(movie, movie_field)
                for movie in models.Movie.select().where(
                    models.Movie.title.contains(query)
                )
            ]
        }

movie_api = Blueprint('resources.movies', __name__)
api = Api(movie_api)
api.add_resource(
    MovieList,
    '/movies',
    endpoint="movies"
)
api.add_resource(
    MovieSearch,
    '/search/movies/<query>',
    endpoint='search_movies'
)
