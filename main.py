import logging
from pathlib import Path

from dotenv import load_dotenv
import uvicorn

from backend.server.server import app


logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # File handler for general application logs
        logging.FileHandler('logs/app.log'),
        # Stream handler for console output
        logging.StreamHandler()
    ]
)

load_dotenv(override=True)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    """
    Main entry point for the application.
    """
    logger.info("Starting the application...")
    # Run the app
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
        logger.info("Application started successfully.")
    except Exception as e:
        logger.error(f"An error occurred while starting the app: {e}")
    