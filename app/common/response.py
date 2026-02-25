from typing import TypeVar, Generic, Optional
from fastapi.responses import JSONResponse
from fastapi import status

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

        Args:
            data (Optional[T]): The data to include in the response payload.
            message (str): A descriptive message about the success.
            status_code (int): The HTTP status code (default: 200 OK).

        Returns:
            JSONResponse: A FastAPI JSONResponse with a standardized structure.
        """
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "success",
                "message": message,
                "data": data,
            },
        )

    @staticmethod
    def error(
        message: str = "Error",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: Optional[T] = None,
    ) -> JSONResponse:
        """
        Return a standardized error response.

        Args:
            message (str): A descriptive message about the error.
            status_code (int): The HTTP status code (default: 400 Bad Request).
            data (Optional[T]): Optional additional data about the error.

        Returns:
            JSONResponse: A FastAPI JSONResponse with a standardized structure.
        """
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "error",
                "message": message,
                "data": data,
            },
        )
