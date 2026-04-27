import enum

class BillingInterval(str, enum.Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"