from celery import shared_task

from execution.pipeline import ExecutionPipeline
from monitoring.reputation import ReputationEngine


@shared_task(bind=True, max_retries=3)
def execute_trade_task(self, plan_data, user_address, chain_id):
    """
    Асинхронное исполнение сделки.
    """

    try:
        tx_hash = ExecutionPipeline.execute(plan_data, user_address, chain_id)

        ReputationEngine.update(plan_data, tx_hash)

        return tx_hash

    except Exception as e:
        raise self.retry(exc=e, countdown=5)
