from api.infra.entities.pokemon.pokemon_api import PokemonEntity
import json


def test_get_pokemon():
    pokemon = PokemonEntity()
    responses = pokemon.get_pokemon_data()
    assert all(item is not None for item in responses)
