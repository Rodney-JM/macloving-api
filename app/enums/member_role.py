import enum

class MemberRole(str, enum.Enum):
    owner = "owner"
    partner = "partner"