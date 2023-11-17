from api.infra.entities.pokemon.pokemon_api import PokemonEntity
import json


def test_get_pokemon():
    pokemon = PokemonEntity()
    pokemon.get_pokemon()
