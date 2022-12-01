from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
from exception.base import BaseHTTPException

class IntentException(BaseHTTPException):
    def __init__(self,status_code, detail: str = None, headers: Optional[Dict[str, Any]] = None ,**kwargs):
        super().__init__(status_code, detail, headers)

        for k, v in kwargs.items():
            setattr(self, k, v)

async def intent_exception_handler(request: Request, exc: IntentException):
    return JSONResponse(
        status_code = exc.status_code,
        content = exc.to_dict(),
        headers=exc.headers
    )
