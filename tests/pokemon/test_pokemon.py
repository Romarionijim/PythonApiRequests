from requests2.api.infra.entities.pokemon.pokemon_api import PokemonEntity
import json


def test_get_pokemon_data_length():
    pokemon = PokemonEntity()
    responses = pokemon.get_pokemon_data_length()
    assert responses == 1292


def test_get_pokemon_data():
    pokemon = PokemonEntity()
    response = pokemon.get_pokemon_data()
    assert response.status_code == 200
    assert response is not None
