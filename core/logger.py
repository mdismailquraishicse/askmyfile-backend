import logging



logging.basicConfig(
    level = logging.INFO,
    format = "%(acstime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)