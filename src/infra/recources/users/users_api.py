from PythonApiRequests.src.infra.requests.api_requests import ApiRequests
from PythonApiRequests.src.infra.enums.urls import Urls
from PythonApiRequests.src.infra.enums.end_points import EndPoints
from PythonApiRequests.src.infra.utils.interfaces.request_options import RequestOptions
from PythonApiRequests.src.infra.utils.faker.fake_data_generator import FakeDataGenerator


class UsersApi(ApiRequests):
    URL = Urls.GO_REST_API_URL.value
    USERS_ENDPOINT = EndPoints.USERS_END_POINT.value

    def get_users(self):
        users_end_point = self.get(f'{self.URL}/{self.USERS_ENDPOINT}')
        if users_end_point.status_code != 200:
            raise Exception('GET users did not get 200 status code response')
        users_json_object = users_end_point.json()
        return users_json_object

    def get_inactive_users(self):
        params = {'status': 'inactive'}
        response = self.get(f'{self.URL}/{self.USERS_ENDPOINT}', params=params)
        response_data = response.json()
        return response_data

    def delete_inactive_users(self):
        responses: list = []
        inactive_users = self.get_inactive_users()
        for user in inactive_users:
            user_id = user.get("id")
            response = self.delete(f'{self.URL}/{self.USERS_ENDPOINT}/{user_id}',
                                   options=RequestOptions(token_required=True))
            responses.append(response)
        return responses

    def __get_gender(self, gender: str):
        gender_params = {'gender': gender}
        response = self.get(f'{self.URL}/{self.USERS_ENDPOINT}', params=gender_params)
        response_data = response.json()
        return response_data

    def get_male_gender_count(self):
        male_gender = self.__get_gender('male')
        return len(male_gender)

    def get_female_gender_count(self):
        female_gender = self.__get_gender('female')
        return len(female_gender)

    def make_genders_even(self):
        """function that takes the gender difference and makes males and females even"""
        male_gender_count = self.get_male_gender_count()
        female_gender_count = self.get_female_gender_count()
        count_difference = abs(male_gender_count - female_gender_count)
        responses = []
        if male_gender_count == female_gender_count:
            return responses
        elif male_gender_count > female_gender_count:
            for i in range(count_difference):
                female_data = {
                    "id": FakeDataGenerator.get_random_number(),
                    "name": FakeDataGenerator.get_random_female_last_name(),
                    "email": FakeDataGenerator.get_random_email(),
                    "gender": "female",
                    "status": "active"
                }
                response = self.post(f'{self.URL}/{self.USERS_ENDPOINT}', female_data,
                                     options=RequestOptions(token_required=True))
                responses.append(response)
        else:
            for i in range(count_difference):
                male_data = {
                    "id": FakeDataGenerator.get_random_number(),
                    "name": FakeDataGenerator.get_random_male_first_name(),
                    "email": FakeDataGenerator.get_random_email(),
                    "gender": "male",
                    "status": "active"
                }
                response = self.post(f'{self.URL}/{self.USERS_ENDPOINT}', male_data,
                                     options=RequestOptions(token_required=True))
                responses.append(response)

        return responses

    def replace_extension_for_each_user(self):
        """replaces the email extension for all users to '.co.il'"""
        user_objects = self.get_users()
        responses: list = []
        for user in user_objects:
            email = user.get("email")
            email_extension = self.__get_email_extension(email)
            if email_extension != 'co.il':
                new_extension = email.replace(email_extension, 'co.il')
                user_id = user.get("id")
                new_email = {
                    "email": new_extension
                }
                response = self.patch(f'{self.URL}/{self.USERS_ENDPOINT}/{user_id}', new_email,
                                      options=RequestOptions(token_required=True))
                responses.append(response)
        return responses

    def __get_email_extension(self, email: str):
        domain = email.split('@').pop()
        extension = domain.split('.')[-1]
        return extension

    def get_current_user_email_extensions(self):
        email_extension_list: list = []
        users = self.get_users()
        for user in users:
            user_email = user.get("email")
            email_extensions = self.__get_email_extension(user_email)
            email_extension_list.append(email_extensions)
        return email_extension_list
