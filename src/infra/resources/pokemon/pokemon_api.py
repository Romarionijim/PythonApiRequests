import json

from PythonApiRequests.src.infra.clients.api_client import ApiClient, RequestOptions
import pytest


class PokemonApi(ApiClient):
    __base_url = 'https://pokeapi.co/api/v2/pokemon'

    def get_pokemon_data_length(self):
        response = self.get(self.__base_url,
                            options=RequestOptions(paginate=True, offset=0, limit=100, request_key='results'))
        return len(response)

    def get_pokemon_data(self):
        response = self.get(self.__base_url)
        return response
