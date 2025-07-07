import logging
import os

def setup_logging():
    logger = logging.getLogger("nova")

    # Determine logging level based on DEBUG environment variable
    debug_mode = os.getenv("DEBUG", "false").lower() == "true"
    if debug_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if debug_mode else logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    ch.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(ch)
    return logger

logger = setup_logging()
