from enum import Enum


class JobStatusType(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class LayerTypeEnum(str, Enum):
    PARAGRAPH = "paragraph"
    SECTION = "section"
    CHAPTER = "chapter"


class ComponentStatusType(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"


class IterationStatusType(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"