import logging


def get_logger(name):
    try:
        logger = logging.getLogger(name)
        if not logger.handlers:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s %(levelname)s %(name)s %(message)s"
            )
        return logger
    except Exception as exc:
        raise RuntimeError(f"Failed to get logger: {exc}")
