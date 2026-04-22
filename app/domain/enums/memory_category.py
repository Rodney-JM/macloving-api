import enum

class MemoryCategory(str, enum.Enum):
    TRAVEL = "travel"
    ROUTINE = "routine"
    ANNIVERSARY = "anniversary"
    NATURE = "nature"
    FOOD = "food"
    NIGHT = "night"
    SELFIE = "selfie"
    OTHER = "other"