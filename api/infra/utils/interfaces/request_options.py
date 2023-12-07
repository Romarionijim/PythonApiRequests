class RequestOptions:
    """class that serves as an interface with reusable api optional  params - this class needs to be instantiated and passed
    as a dependency injection"""

    def __init__(self, token_required: bool = False, paginate: bool = False,
                 page: int = None, offset: int = None, limit: int = None, request_key: str = None):
        self.token_required = token_required
        self.paginate = paginate
        self.page = page
        self.offset = offset
        self.limit = limit
        self.request_key = request_key
