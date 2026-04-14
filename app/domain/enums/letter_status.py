import enum

class LetterStatus(str, enum.Enum): 
    DRAFT = "draft"
    SENT = "sent"
    READ = "read"