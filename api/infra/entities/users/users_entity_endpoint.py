from api.infra.requests.api_requests import ApiRequests
from api.infra.enums.urls import Urls
from api.infra.enums.end_points import EndPoints
from api.infra.enums.http_methods import HttpMethods


class UsersEntity(ApiRequests):
    __BASE_URL = Urls.GO_REST_API_URL.value
    __USERS_ENDPOINT = EndPoints.USERS_END_POINT.value
    __USERS_URL = f"{__BASE_URL}/{__USERS_ENDPOINT}"

    def get_inactive_users(self):
        params = {'status': 'inactive'}
        response = self.get(self.__USERS_URL, params=params, paginate=True)
        return response

    def delete_inactive_users(self):
        responses: list = []
        inactive_users = self.get_inactive_users()
        for user in inactive_users:
            user_id = user.get("id")
            response = self.delete(f"{self.__USERS_URL}/{user_id}", token_required=True)
            responses.append(response)
        return responses
