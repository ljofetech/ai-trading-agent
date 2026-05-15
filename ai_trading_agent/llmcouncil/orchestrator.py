# Import the LLMCouncil that handles the core LLM processing
from .council import LLMCouncil


class LangGraphOrchestrator:

    # Entry point to run the orchestrator with a conversation context
    @staticmethod
    def run(conversation_id: str, user_message: str):
        # Prepare the initial state containing the conversation ID and user input
        state = {
            "conversation_id": conversation_id,
            "user_input": user_message,
        }
        # Delegate to LLMCouncil to process the state and produce the final output
        council_output = LLMCouncil.run(state)
        return council_output
