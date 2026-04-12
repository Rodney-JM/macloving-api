import enum 

class MoodType(str, enum.Enum):
    HAPPY = "happy"
    IN_LOVE = "in_love"
    MISSING = "missing"
    TIRED = "tired"
    STRESSED = "stressed"
    EXCITED = "excited"