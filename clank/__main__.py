"""
Main entry point for the personal AI assistant, Clank
"""
import logging
import tensorflow as tf

from keras import mixed_precision
from .api import app
from .config import app_config
from .utils.logging import setup_logging


def main():
    """
    entry point for Clank
    """
    # Set up logging
    setup_logging()

    # Configure gpus
    print("tf.version: ", tf.__version__)
    gpus = tf.config.experimental.list_physical_devices('GPU')
    print("[init] ", gpus)

    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

    # Configure mixed precision
    policy = mixed_precision.Policy('mixed_float16')
    mixed_precision.set_global_policy(policy)

    # Start the Flask app
    logging.info("Starting the Clank API server...")
    app.run(host='0.0.0.0', port=app_config["api_port"],debug=True)


if __name__ == "__main__":
    main()
