from typing import TypedDict,List,Optional,Dict,Any
from dataclasses import dataclass,field

@dataclass
class RigidAgentState(TypedDict):
    user: str
    steps: List[Any]
    contact: str | None
    contact_result: dict
    email_result: str | None
