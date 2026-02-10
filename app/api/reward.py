from fastapi import APIRouter
from app.models.schemas import RewardRequest, RewardResponse
from app.cache.factory import get_cache
from app.services.reward import RewardService
from app.utils.config_loader import load_policy


router = APIRouter()
policy = load_policy()


@router.post("/reward/decide", response_model=RewardResponse)
async def decide_reward(req: RewardRequest):
    """
    Decide reward for a given transaction.

    This endpoint is idempotent and deterministic.
    Repeated requests with the same idempotency key
    will return the same response.

    :param req: RewardRequest payload
    :return: RewardResponse
    """
    cache = await get_cache()
    service = RewardService(cache, policy)
    return await service.decide(req)
