from collections import defaultdict
import logging


# INFO WARN WARNING
FORMAT = '{asctime} - [{levelname}] {filename}:{lineno} {name} - {message}'
LOG_FILE = "log.log"
LEVEL = logging.INFO


class CooldownFilter(logging.Filter):
    """Do not print same line if time after previous line less or equal <COOLDOWN> seconds. Defaults to 5 seconds"""
    def __init__(self, cooldown=5):
        """
        Initialize a filter.

        Do not print same line if time after previous line less or equal <COOLDOWN> seconds. Defaults to 5 seconds
        """
        self.cooldown = cooldown
    
    last_events: dict[str, float] = defaultdict(float)
    
    def filter(self, record) -> bool:
        prev_time = self.last_events[record.name]
        if prev_time + self.cooldown <= record.created:
            self.last_events[record.name] = record.created
            return True
        else:
            return False

stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
tempfile_handler = logging.FileHandler(f"temp{LOG_FILE}", encoding='utf-8', mode="w")
logging.basicConfig(format=FORMAT, level=LEVEL, handlers=[stream_handler, file_handler, tempfile_handler], style="{")

stream_handler.setLevel(LEVEL)
file_handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

MUTEDICT = {
    "httpx": logging.WARNING, 
    "asyncio": logging.ERROR, 
    "pyrogram.session.session": logging.WARNING, 
    "pyrogram.dispatcher": logging.WARNING, 
    "pyrogram.connection.transport.tcp.tcp": logging.WARNING, 
    "pyrogram.connection.connection": logging.WARNING
}

for _name, _value in MUTEDICT.items():
    _l = logging.getLogger(_name)
    _l.setLevel(_value)
    _l.addFilter(CooldownFilter())
