from api.infra.entities.pokemon.pokemon_api import PokemonEntity
import json


def test_get_pokemon():
    pokemon = PokemonEntity()
    responses = pokemon.get_pokemon()
    assert all(item.status_code == 200 for item in responses)
