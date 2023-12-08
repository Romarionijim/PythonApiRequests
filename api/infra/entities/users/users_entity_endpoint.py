from requests2.api.infra.requests.api_requests import ApiRequests
from requests2.api.infra.enums.urls import Urls
from requests2.api.infra.enums.end_points import EndPoints
from requests2.api.infra.utils.interfaces.request_options import RequestOptions
from requests2.api.infra.enums.http_methods import HttpMethods


class UsersEntity(ApiRequests):
    URL = Urls.GO_REST_API_URL.value
    USERS_ENDPOINT = EndPoints.USERS_END_POINT.value

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
                                   RequestOptions(token_required=True))
            responses.append(response)
        return responses
