import pytest

from app.models.schemas import RewardRequest
from app.services.reward import RewardService
from app.cache.memory import InMemoryCache
from app.utils.config_loader import load_policy


def setup_service():
    cache = InMemoryCache()
    policy = load_policy()
    return RewardService(
        cache=cache,
        policy=policy,
    )


@pytest.mark.asyncio
async def test_reward_decision_logic():
    service = setup_service()

    req = RewardRequest(
        txn_id="t100",
        user_id="u1",
        merchant_id="m1",
        amount=100,
        txn_type="PAY",
        ts="2024-01-01",
    )

    result = await service.decide(req)

    assert result["xp"] > 0
    assert result["reward_type"] in ["XP", "CHECKOUT", "GOLD"]


@pytest.mark.asyncio
async def test_idempotency_behavior():
    service = setup_service()

    req = RewardRequest(
        txn_id="t101",
        user_id="u1",
        merchant_id="m1",
        amount=200,
        txn_type="PAY",
        ts="2024-01-01",
    )

    r1 = await service.decide(req)
    r2 = await service.decide(req)

    assert r1 == r2


@pytest.mark.asyncio
async def test_cac_cap_enforcement():
    service = setup_service()

    # Exceed CAC cap deliberately
    for i in range(20):
        req = RewardRequest(
            txn_id=f"t{i}",
            user_id="u1",
            merchant_id="m1",
            amount=100,
            txn_type="PAY",
            ts="2024-01-01",
        )
        result = await service.decide(req)

    assert result["reward_type"] == "XP"

