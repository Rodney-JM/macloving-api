import enum

class NightSessionStatus(str, enum.Enum):
    WAITING = "waiting"
    ACTIVE = "active"
    ENDED = "ended"