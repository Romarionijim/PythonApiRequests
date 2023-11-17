import json

from api.infra.requests.api_requests import ApiRequests
import pytest


class PokemonEntity(ApiRequests):
    __base_url = 'https://pokeapi.co/api/v2/pokemon'

    def get_pokemon_data(self):
        response = self.get(self.__base_url, paginate=True, offset=0, limit=100, request_key='results')
        return response

    def get_pokemon_total_count(self):
        response = self.get(self.__base_url)
        if response.status_code == 200:
            response_json = response.json()
            pokemon_count = response_json['count']
            return pokemon_count
