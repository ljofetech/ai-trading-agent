from ..llmcouncil.orchestrator import LangGraphOrchestrator
from ..execution.tasks import execute_trade_task


class ConversationService:

    @staticmethod
    def process_message(conversation_id, message):
        """
        Обрабатывает сообщение пользователя и возвращает торговый план.
        """

        plan_result = LangGraphOrchestrator.run(
            conversation_id=conversation_id, user_message=message
        )

        return {
            "status": "plan_generated",
            "plan": plan_result["plan"],
            "market": plan_result["market"],
            "reasoning": plan_result.get("council_reasoning"),
        }

    @staticmethod
    def approve_trade(plan, user_address, chain_id):
        """
        Запускает асинхронное исполнение сделки.
        """

        task = execute_trade_task.delay(
            plan_data=plan, user_address=user_address, chain_id=chain_id
        )

        return {"status": "execution_started", "task_id": task.id}
