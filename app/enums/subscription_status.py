import enum

class SubscriptionStatus(enum.Enum):
    free = "free"
    active = "active"
    canceled = "canceled"
    expired = "expired"