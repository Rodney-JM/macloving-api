import enum

class SurpriseType(str, enum.Enum):
    PHOTO_ALBUM = "photo_album"
    PLAYLIST = "playlist"
    LETTER = "letter"
    VIDEO = "video"
    CUSTOM = "custom"
    
class SurpriseStatus(str, enum.Enum):
    PENDING = "pending"
    LOCKED = "locked"
    DELIVERED = "delivered"
    OPENED = "opened"