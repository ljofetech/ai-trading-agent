from .council import LLMCouncil


class LangGraphOrchestrator:

    @staticmethod
    def run(conversation_id: str, user_message: str):
        state = {
            "conversation_id": conversation_id,
            "user_input": user_message,
        }
        council_output = LLMCouncil.run(state)
        return council_output
