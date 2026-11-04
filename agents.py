from typing import TypedDict,List,Optional,Dict,Any
from dataclasses import dataclass,field

@dataclass
class RigidAgentState(TypedDict):
    user: str
    steps: List[Any]
    contact: str | None
    contact_result: dict
    email_result: str | None

@dataclass
class ReactAgentState(TypedDict):
    flag: Optional[str] | None
    counter: int
    user_name: str | None
    details: dict | None
    error: str | None
    message: str | None
    email_content: str | None
