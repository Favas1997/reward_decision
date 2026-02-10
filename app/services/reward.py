import uuid
from app.cache.keys import *
from app.services.persona import PersonaService



class RewardService:

    def __init__(self, cache, policy):
        """
        Initialize service.

        :param cache: Cache implementation
        :param policy: Policy configuration
        """
        self.cache = cache
        self.policy = policy
        self.persona_service = PersonaService()

    async def decide(self, req):
        """
        Decide reward outcome for a transaction.

        :param req: RewardRequest
        :return: Reward decision dict
        """
        idem = idem_key(req.txn_id, req.user_id, req.merchant_id)

        cached = await self.cache.get(idem)
        if cached:
            return cached

        persona = await self.cache.get(persona_key(req.user_id))
        if not persona:
            persona = self.persona_service.get_persona(req.user_id)
            await self.cache.set(persona_key(req.user_id), persona, 86400)

        multiplier = self.policy["persona_multipliers"][persona]
        xp = min(
            int(req.amount * self.policy["xp_per_rupee"] * multiplier),
            self.policy["max_xp_per_txn"]
        )

        reward_type = "XP"
        reward_value = 0
        reasons = []

        cac_spent = await self.cache.get(cac_key(req.user_id)) or 0
        cap = self.policy["daily_cac_cap"][persona]

        if cac_spent < cap:
            reward_type = "CHECKOUT"
            reward_value = min(50, cap - cac_spent)
            await self.cache.incr(cac_key(req.user_id), reward_value, 86400)
        else:
            reasons.append("CAC_CAP_EXCEEDED")

        response = {
            "decision_id": str(uuid.uuid4()),
            "policy_version": self.policy["policy_version"],
            "reward_type": reward_type,
            "reward_value": reward_value,
            "xp": xp,
            "reason_codes": reasons,
            "meta": {"persona": persona}
        }

        await self.cache.set(idem, response, 86400)
        return response
