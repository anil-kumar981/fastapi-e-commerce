import uvicorn
from app import create_app
from app.core.config import settings

# Initialize the FastAPI application using the factory function
app = create_app()


def main():
    """
    Entry point for running the application locally via 'python main.py'.
    We use the string format "main:app" to allow uvicorn's reload feature
    to work correctly when enabled.
    """
    # Note: Running via 'uvicorn main:app --reload' is preferred for development
    uvicorn.run(
        "main:app",
        host=settings.IP_ADDRESS,
        port=settings.PORT,
        reload=True if settings.ENV == "development" else False,
    )


if __name__ == "__main__":
    main()
