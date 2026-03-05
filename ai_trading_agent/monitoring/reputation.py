from .models import TradeExecutionRecord, AgentReputation
from django.db.models import Count, Q


class ReputationEngine:

    @staticmethod
    def update(plan: dict, tx_hash: str):
        """
        Вызывается после исполнения сделки.
        Обновляет историю сделок и репутацию агентов.
        """
        # 1. Сохраняем запись о сделке
        record = TradeExecutionRecord.objects.create(
            user_id=plan.get("user"),
            asset_in=plan.get("asset_in"),
            asset_out=plan.get("asset_out"),
            amount=plan.get("amount"),
            slippage=plan.get("max_slippage"),
            confidence=plan.get("confidence"),
            risk_level=plan.get("risk_level", "medium"),
            tx_hash=tx_hash,
            status="filled",
        )

        # 2. Обновляем репутацию каждого агента
        for agent in ["MarketAgent", "RiskAgent", "ExecutionAgent"]:
            ReputationEngine._update_agent(agent)

    @staticmethod
    def _update_agent(agent_name: str):
        """
        Считаем success_rate как ratio filled/total
        """
        total = TradeExecutionRecord.objects.filter().count()
        filled = TradeExecutionRecord.objects.filter(status="filled").count()

        reputation, _ = AgentReputation.objects.get_or_create(agent_name=agent_name)
        reputation.success_rate = filled / max(total, 1)
        reputation.save()
