import requests
import os
from typing import Dict, TypeVar, Optional, List, Union
from dotenv import load_dotenv
from requests2.api.infra.enums.http_methods import HttpMethods
from requests2.api.infra.utils.interfaces.request_options import RequestOptions
import logging

load_dotenv()

T = TypeVar("T")


class ApiRequests:

    def __init__(self):
        self.requests = requests.Session()
        self.logger = logging.getLogger(__name__)

    def __is_token_required(self, headers: Dict[str, str], options: RequestOptions):
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

    def __process_response_key(self, key, json_data):
        if key is not None:
            response_key = json_data[key]
            return response_key
        raise ValueError(f" the key {key} might be None")

    def __paginate_request(self, method: HttpMethods, url: str, data: Optional[Dict[str, T]] = None,
                           params: Optional[Dict[str, T]] = None, options: RequestOptions = RequestOptions()):
        response_data: list = []
        while True:
            if options.page is not None:
                current_params = params.copy() if params else {}
                current_params['page'] = options.page

                response = self.__make_request(method, url, data=data, params=current_params,
                                               options=options)
                json_result = response.json()
                if options.request_key is not None:
                    response_key = self.__process_response_key(options.request_key, json_result)
                    if not response_key:
                        break
                else:
                    if not json_result or len(json_result) == 0:
                        break
                response_data.extend(json_result)
                options.page += 1

            elif options.limit is not None and options.offset is not None:
                current_params = params.copy() if params else {}
                current_params.update({'limit': options.limit, 'offset': options.offset})
                response = self.__make_request(method, url, data=data, params=current_params,
                                               options=options)
                json_data = response.json()
                if options.request_key is not None:
                    specific_key = json_data[options.request_key]
                    if len(specific_key) == 0:
                        break
                    response_data.extend(specific_key)
                    options.offset += options.limit
                else:
                    if not json_data or len(json_data) == 0:
                        break
                    response_data.extend(json_data)
                    options.offset += options.limit

        return response_data

    def __make_http_request(self, method: HttpMethods, url: str,
                            params: Optional[Dict[str, T]] = None,
                            data: Optional[Dict[str, T]] = None,
                            options: RequestOptions = RequestOptions()):
        """make a regular request or make a request by using pagination by passing the paginate parameter if to
        paginate or not"""
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
