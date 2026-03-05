from django.db import models


class TradeExecutionRecord(models.Model):
    """
    Хранит данные по каждой исполненной сделке.
    """

    user_id = models.UUIDField()
    asset_in = models.CharField(max_length=20)
    asset_out = models.CharField(max_length=20)
    amount = models.FloatField()
    slippage = models.FloatField()
    confidence = models.FloatField()
    risk_level = models.CharField(max_length=10)
    tx_hash = models.CharField(max_length=66, blank=True, null=True)
    status = models.CharField(
        max_length=20, default="pending"
    )  # pending / filled / failed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AgentReputation(models.Model):
    """
    Репутация LLM-агентов (Market, Risk, Execution)
    """

    agent_name = models.CharField(max_length=50)
    success_rate = models.FloatField(default=1.0)  # filled / total
    last_activity = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
