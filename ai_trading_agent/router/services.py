# Import the orchestrator that handles LLM-based conversation planning
from llmcouncil.orchestrator import LangGraphOrchestrator


# Service class that provides conversation processing functionality
class ConversationService:

    # Static method to process a user message within a given conversation
    @staticmethod
    def process_message(conversation_id: str, message: str):
        # Call the orchestrator to get a plan/response based on conversation history and user input
        plan_result = LangGraphOrchestrator.run(
            conversation_id=conversation_id,
            user_message=message,
        )
        # Return the orchestrator's result (could be a response, plan, or intermediate step)
        return plan_result
