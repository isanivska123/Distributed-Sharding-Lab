from pydantic import BaseModel
from typing import Dict, Any

class Record(BaseModel):
    partition_key_value: str
    sort_key_value: str
    data: Dict[str, Any]

class ShardRecord(BaseModel):
    composite_key: str
    value: Any