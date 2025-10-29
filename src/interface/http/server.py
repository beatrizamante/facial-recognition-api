import logging
import uvicorn

def make_server():
    """
    Creates and configures a Uvicorn server instance for running a FastAPI application.
    Sets up logging with DEBUG level and a specific format, and initializes a logger named "uvicorn".
    Configures the Uvicorn server to run the application defined in "main:app" on host "0.0.0.0" and port 5000,
    using the specified SSL certificate and key files for HTTPS.
    Returns:
        tuple: A tuple containing the configured Uvicorn server instance and the logger.
    """

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(message)s")
    logger = logging.getLogger("uvicorn")

    config = uvicorn.Config("main:app",
                            host="0.0.0.0",
                            port=5000,
                            ssl_certfile="./agrariacoopbr.cert",
                            ssl_keyfile="./agrariacoopbr.key"
                            )
    server = uvicorn.Server(config)
    return server, logger
