from typing import Optional


class RequestOptions:
    """class that serves as an interface with reusable api optional params - this class needs to be instantiated and
    passed as a dependency injection to provide the optional params in the 'options' key when calling one of the crud
    functions"""
    token_required: bool = False
    paginate: bool = False,
    page: Optional[int] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
    request_key: Optional[str] = None

    def __init__(self, token_required: bool = False, paginate: bool = False,
                 page: int = None, offset: int = None, limit: int = None, request_key: str = None):
        self.token_required = token_required
        self.paginate = paginate
        self.page = page
        self.offset = offset
        self.limit = limit
        self.request_key = request_key
