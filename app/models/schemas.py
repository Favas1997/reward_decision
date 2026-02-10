from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime


class RewardRequest(BaseModel):
    """Incoming reward decision request."""
    txn_id: str
    user_id: str
    merchant_id: str
    amount: float
    txn_type: str
    ts: datetime


class RewardResponse(BaseModel):
    """Reward decision response."""
    decision_id: str
    policy_version: str
    reward_type: str
    reward_value: int
    xp: int
    reason_codes: List[str]
    meta: Dict[str, Any]