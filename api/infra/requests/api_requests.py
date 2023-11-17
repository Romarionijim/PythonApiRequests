import requests
import os
from typing import Dict, TypeVar, Optional, List, Union
from dotenv import load_dotenv
from enum import Enum
import logging
import json
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

load_dotenv()

T = TypeVar("T")


class HttpMethods(Enum):
    GET = "GET",
    POST = "POST",
    PUT = "PUT",
    PATCH = "PATCH",
    DELETE = "DELETE"


class ApiRequests:

    def __init__(self):
        self.requests = requests.Session()
        self.logger = logging.getLogger(__name__)

    def __is_token_required(self, headers: Dict[str, str], token_required: bool = None):
        if token_required:
            headers["Authorization"] = f"Bearer {os.getenv('TOKEN')}"

    def __make_request(self, method: HttpMethods, url: str, data: Optional[Dict[str, T]] = None,
                       params: Optional[Dict[str, str]] = None, token_required: bool = None):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.__is_token_required(headers, token_required)
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

    def __paginate_request(self, method: HttpMethods, url: str, data: Optional[Dict[str, T]] = None,
                           params: Optional[Dict[str, T]] = None, token_required: bool = None, page: int = None,
                           limit: int = None, offset: int = None, request_key: str = None):
        response_data: list = []
        while True:
            if page is not None:
                current_params = params.copy() if params else {}
                current_params['page'] = page

                response = self.__make_request(method, url, data=data, params=current_params,
                                               token_required=token_required)
                json_result = response.json()
                if not json_result or len(json_result) == 0:
                    break
                response_data.extend(json_result)
                page += 1

            elif limit is not None and offset is not None:
                current_params = params.copy() if params else {}
                current_params.update({'limit': limit, 'offset': offset})
                response = self.__make_request(method, url, data=data, params=current_params,
                                               token_required=token_required)
                json_data = response.json()
                if request_key is not None:
                    specific_key = json_data[request_key]
                    if len(specific_key) == 0:
                        break
                    response_data.extend(specific_key)
                    offset += limit
                else:
                    if not json_data or len(json_data) == 0:
                        break
                    response_data.extend(json_data)
                    offset += limit

        return response_data

    def __request_api_with_or_without_pagination(self, method: HttpMethods, url: str,
                                                 params: Optional[Dict[str, T]] = None,
                                                 data: Optional[Dict[str, T]] = None, paginate: bool = False,
                                                 token_required: bool = False, page: int = None, offset: int = None,
                                                 limit: int = None, request_key: str = None):
        """make a regular http request or paginate in case of pagination mechanism"""
        if paginate:
            return self.__paginate_request(method, url, params=params, data=data, token_required=token_required,
                                           page=page, offset=offset, limit=limit, request_key=request_key)
        else:
            return self.__make_request(method, url, data=data, params=params, token_required=token_required)

    def get(self, url: str, params: Optional[Dict[str, str]] = None, paginate: Optional[bool] = False, page: int = None,
            offset: int = None,
            limit: int = None, request_key: str = None):
        return self.__request_api_with_or_without_pagination(HttpMethods.GET, url, params=params, paginate=paginate,
                                                             page=page, offset=offset, limit=limit,
                                                             request_key=request_key)

    def post(self, url: str, data: Dict[str, T], token_required: bool = None, paginate: Optional[bool] = False,
             page: int = None, offset: int = None,
             limit: int = None):
        return self.__request_api_with_or_without_pagination(HttpMethods.POST, url, data=data,
                                                             token_required=token_required,
                                                             paginate=paginate,
                                                             page=page, offset=offset, limit=limit)

    def put(self, url: str, data: Dict[str, T], token_required: bool = None, paginate: Optional[bool] = False,
            page: int = None, offset: int = None,
            limit: int = None):
        return self.__request_api_with_or_without_pagination(HttpMethods.PUT, url, data=data,
                                                             token_required=token_required,
                                                             paginate=paginate,
                                                             page=page, offset=offset, limit=limit)

    def patch(self, url: str, data: Dict[str, T], token_required: bool = None, paginate: Optional[bool] = False,
              page: int = None, offset: int = None,
              limit: int = None):
        return self.__request_api_with_or_without_pagination(HttpMethods.PATCH, url, data=data,
                                                             token_required=token_required,
                                                             paginate=paginate,
                                                             page=page, offset=offset, limit=limit)

    def delete(self, url, paginate: Optional[bool] = False, token_required: bool = False, page: int = None,
               offset: int = None,
               limit: int = None):
        return self.__request_api_with_or_without_pagination(HttpMethods.DELETE, url, paginate=paginate,
                                                             token_required=token_required,
                                                             page=page, offset=offset, limit=limit)
