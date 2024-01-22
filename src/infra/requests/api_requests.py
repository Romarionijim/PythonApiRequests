import requests
import os
from typing import Dict, TypeVar, Optional, List, Union
from dotenv import load_dotenv
from PythonApiRequests.src.infra.enums.http_methods import HttpMethods
from PythonApiRequests.src.infra.utils.interfaces.request_options import RequestOptions
import logging
from PythonApiRequests.src.infra.utils.custom_exceptions.exceptions import PaginationError

load_dotenv()

T = TypeVar("T")


class ApiRequests:

    def __init__(self):
        self.requests = requests.Session()
        self.logger = logging.getLogger(__name__)

    def __is_token_required(self, headers: Dict[str, str], options: RequestOptions = RequestOptions()):
        if options.token_required:
            headers["Authorization"] = f"Bearer {os.getenv('TOKEN')}"

    def __make_request(self, method: HttpMethods, url: str, data: Optional[Dict[str, T]] = None,
                       params: Optional[Dict[str, str]] = None, options: RequestOptions = RequestOptions()):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.__is_token_required(headers, options)
        response = None

        match method:
            case HttpMethods.GET:
                response = self.requests.get(url, headers=headers, params=params)
            case HttpMethods.POST:
                response = self.requests.post(url, headers=headers, data=data)
            case HttpMethods.PUT:
                response = self.requests.put(url, headers=headers, data=data)
            case HttpMethods.PATCH:
                response = self.requests.patch(url, headers=headers, data=data)
            case HttpMethods.DELETE:
                response = self.requests.delete(url)

        return response

    def __get_specific_response_key(self, key: str, json_data: Dict[str, T]):
        """this is a helper function that retrieves a specific key from the json response after making a request"""
        if key is None:
            raise ValueError(f" the key {key} was not found or may be None")
        response_key = json_data[key]
        return response_key

    def __paginate_request(self, method: HttpMethods, url: str, data: Optional[Dict[str, T]] = None,
                           params: Optional[Dict[str, T]] = None, options: RequestOptions = RequestOptions()):
        """helper function that provides pagination options - either by page pagination or by offset and limit
        pagination"""

        current_params = params.copy() if params else {}
        response_data_list: list = []
        while True:
            if options.page is not None:
                current_params['page'] = options.page
                response = self.__make_request(method, url, data=data, params=current_params,
                                               options=options)
                response_json_data = response.json()
                if options.request_key is not None:
                    response_key = self.__get_specific_response_key(options.request_key, response_json_data)
                    if not response_key:
                        break
                else:
                    if not response_json_data or len(response_json_data) == 0:
                        break
                response_data_list.extend(response_json_data)
                options.page += 1
            # ==========================================================================
            elif options.limit is not None and options.offset is not None:
                current_params.update({'limit': options.limit, 'offset': options.offset})
                response = self.__make_request(method, url, data=data, params=current_params,
                                               options=options)
                response_json_data = response.json()

                if options.request_key is not None:
                    request_key = self.__get_specific_response_key(options.request_key, response_json_data)
                    if not request_key:
                        break
                    response_data_list.extend(request_key)
                else:
                    if not response_json_data or len(response_json_data) == 0:
                        break
                    response_data_list.extend(response_json_data)
                options.offset += options.limit
            # ==========================================================================
            else:
                raise PaginationError("none of the pagination options were provided")

        return response_data_list

    def __make_http_request(self, method: HttpMethods, url: str,
                            params: Optional[Dict[str, T]] = None,
                            data: Optional[Dict[str, T]] = None,
                            options: RequestOptions = RequestOptions()):
        """helper method that sends http request which can include pagination - this method is encapsulated and is
        used by the public CRUD methods below"""
        if options.paginate:
            return self.__paginate_request(method, url, params=params, data=data, options=options)
        else:
            return self.__make_request(method, url, data=data, params=params, options=options)

    def get(self, url: str, params: Optional[Dict[str, str]] = None, options: RequestOptions = RequestOptions()):
        return self.__make_http_request(HttpMethods.GET, url, params=params, options=options)

    def post(self, url: str, data: Dict[str, T], options: RequestOptions):
        return self.__make_http_request(HttpMethods.POST, url, data=data, options=options)

    def put(self, url: str, data: Dict[str, T], options: RequestOptions = RequestOptions()):
        return self.__make_http_request(HttpMethods.PUT, url, data=data, options=options)

    def patch(self, url: str, data: Dict[str, T], options: RequestOptions = RequestOptions()):
        return self.__make_http_request(HttpMethods.PATCH, url, data=data, options=options)

    def delete(self, url, options: RequestOptions = RequestOptions()):
        return self.__make_http_request(HttpMethods.DELETE, url, options=options)
