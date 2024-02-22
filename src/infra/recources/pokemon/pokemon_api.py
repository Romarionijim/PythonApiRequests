import json

from PythonApiRequests.src.infra.requests.api_requests import ApiRequests, RequestOptions
import pytest


class PokemonApi(ApiRequests):
    __base_url = 'https://pokeapi.co/api/v2/pokemon'

    def get_pokemon_data_length(self):
        response = self.get(self.__base_url,
                            options=RequestOptions(paginate=True, offset=0, limit=100, request_key='results'))
        return len(response)

    def get_pokemon_data(self):
        response = self.get(self.__base_url)
        return response


