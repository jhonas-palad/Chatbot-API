from typing import Optional, Any, Dict

class BaseHTTPException(Exception):
    def __init__(self, status_code, detail: str = None, headers: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers
    def to_dict(self):
        clone_dict = self.__dict__.copy()
        clone_dict.pop('status_code', None)
        clone_dict.pop('headers', None)
        return clone_dict