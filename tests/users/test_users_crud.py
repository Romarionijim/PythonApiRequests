import json

import pytest
from requests2.api.infra.requests.api_requests import ApiRequests
from requests2.api.infra.entities.users.users_entity_endpoint import UsersEntity


def test_get_users():
    api_requests = ApiRequests()
    response = api_requests.get("https://gorest.co.in/public/v2/users?page=1&status=inactive")
    response_json = response.json()
    if response.status_code == 200:
        with open('info_file.json', 'w+') as my_f:
            dump_json = json.dumps(response_json)
            my_f.write(dump_json)


def test_get_user_json_file_response():
    file_path = 'info_file.json'
    with open(file_path, 'r') as file:
        file_content = json.load(file)
        expected_data = {
            "id": 5822018,
            "name": "Nalini Chattopadhyay",
            "email": "nalini_chattopadhyay@morar.example",
            "gender": "female",
            "status": "inactive"
        }

        assert expected_data in file_content


def test_delete_inactive_users():
    users = UsersEntity()
    responses = users.delete_inactive_users()
    assert all(response.status_code == 204 for response in responses)
    inactive_users = users.get_inactive_users()
    assert inactive_users == []
