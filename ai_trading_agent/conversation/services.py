from llmcouncil.orchestrator import LangGraphOrchestrator


class ConversationService:

    @staticmethod
    def process_message(conversation_id: str, message: str):
        plan_result = LangGraphOrchestrator.run(
            conversation_id=conversation_id,
            user_message=message,
        )
        return plan_result
