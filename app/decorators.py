import logging

logger = logging.getLogger(__name__)


def bool_on_error(func):
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            logger.exception(str(err))
            return False
    return decorator