from typing import TypeVar, Generic, Optional
from fastapi.responses import JSONResponse
from fastapi import status

from fastapi.encoders import jsonable_encoder

T = TypeVar("T")


class ResponseFactory(Generic[T]):
    """
    Standardized response factory for consistent API responses.
    """

    @staticmethod
    def success(
        data: Optional[T] = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK,
    ) -> JSONResponse:
        """
        Return a standardized success response.
        """
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(
                {
                    "status": "success",
                    "message": message,
                    "data": data,
                }
            ),
        )

    @staticmethod
    def error(
        message: str = "Error",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: Optional[T] = None,
    ) -> JSONResponse:
        """
        Return a standardized error response.
        """
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(
                {
                    "status": "error",
                    "message": message,
                    "data": data,
                }
            ),
        )
