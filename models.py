from pydantic import BaseModel
from typing import List

class Observation(BaseModel):
    message: str
    history: List[str]
    urgency: int
    user_awareness: int
    step: int


class Action(BaseModel):
    action: str  # warn, block, ignore, verify, educate


class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool