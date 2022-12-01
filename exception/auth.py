from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
from exception.base import BaseHTTPException

class AuthException(BaseHTTPException):
    def __init__(self,status_code, detail: str = None, headers: Optional[Dict[str, Any]] = None ,**kwargs):
        self.status_code =status_code
        self.detail = detail
        self.headers = headers

        for k, v in kwargs.items():
            setattr(self, k, v)

async def auth_exception_handler(request: Request, exc: AuthException):
    return JSONResponse(
            status_code = exc.status_code,
            content = exc.to_dict(),
            headers=exc.headers
        )

class FieldValidationException(Exception):
    def __init__(self, field, description):
        self.field = field
        self.description = description
