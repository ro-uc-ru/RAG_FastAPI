import logging


logger= logging.getLogger(__name__)

formatter = logging.Formatter(
    fmt = "%(asctime)s - %(levelname)s - %(message)s "
)

fileHandler = logging.FileHandler("app.log")

fileHandler.setFormatter(formatter)


logger.handlers = [fileHandler]

logger.setLevel(logging.INFO)