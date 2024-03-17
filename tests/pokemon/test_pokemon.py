from PythonApiRequests.src.infra.resources.pokemon.pokemon_api import PokemonApi
import json


def test_get_pokemon_data_length():
    pokemon = PokemonApi()
    responses = pokemon.get_pokemon_data_length()
    assert responses == 1302


def test_get_pokemon_data():
    pokemon = PokemonApi()
    response = pokemon.get_pokemon_data()
    response_data = response.json()
    assert response.status_code == 200
    assert response is not None
    assert response_data['count'] == 1302
    assert isinstance(response_data['results'], list) == True
