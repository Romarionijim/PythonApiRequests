from typing import Optional
from dataclasses import dataclass


@dataclass
class RequestOptions:
    """Data class to specify optional parameters for API requests."""
    token_required: bool = False
    paginate: bool = False,
    page: Optional[int] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
    request_key: Optional[str] = None
