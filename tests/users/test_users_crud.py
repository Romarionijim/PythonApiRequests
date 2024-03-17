import json
from PythonApiRequests.src.infra.utils.test_steps.steps import Step

import pytest
from PythonApiRequests.src.infra.clients.api_client import ApiClient
from PythonApiRequests.src.infra.recources.users.users_api import UsersApi


@pytest.fixture()
def entity_class_object_creation():
    users = UsersApi()
    yield users


def test_get_users():
    api_requests = ApiClient()
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


def test_delete_inactive_users(entity_class_object_creation):
    users = entity_class_object_creation
    responses = users.delete_inactive_users()
    assert responses, "no responses received"
    assert all(response.status_code == 204 for response in responses)
    inactive_users = users.get_inactive_users()
    assert inactive_users == []


def test_replace_email_extension_for_each_user(entity_class_object_creation):
    """replace email extension for each user with .co.il extension"""
    users = entity_class_object_creation
    response_list = users.replace_extension_for_each_user()
    assert response_list, "no responses received"
    assert all(response.status_code == 204 for response in response_list)
    users_email_extension = users.get_current_user_email_extensions()
    assert all(extension == 'co.il' for extension in users_email_extension)


def test_make_male_and_female_gender_even(entity_class_object_creation):
    users = entity_class_object_creation
    responses = users.make_genders_even()
    assert all(response.status_code == 200 for response in responses)
    male_gender = users.get_male_gender_count()
    female_gender = users.get_female_gender_count()
    assert male_gender == female_gender
