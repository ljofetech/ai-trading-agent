from llmcouncil.orchestrator import LangGraphOrchestrator


class ConversationService:

    @staticmethod
    def process_message(conversation_id: str, message: str):
        """
        Обрабатывает сообщение пользователя и возвращает торговый план.
        """

        plan_result = LangGraphOrchestrator.run(
            conversation_id=conversation_id, user_message=message
        )

        return {
            "plan": plan_result["plan"],
            "market": plan_result["market"],
        }
