from ibmlnn.judge import LNNJudge
from .council import LLMCouncil
from .schemas import TradePlan


class LangGraphOrchestrator:

    @staticmethod
    def run(conversation_id: str, user_message: str):

        state = {
            "conversation_id": conversation_id,
            "user_input": user_message,
        }

        council_output = LLMCouncil.run(state)

        if "execution" not in council_output:
            raise Exception("Council did not return execution plan")

        plan = TradePlan(**council_output["execution"])

        validated_plan = LNNJudge.validate(plan, council_output["analysis"])

        return {
            "plan": validated_plan.dict(),
            "market": council_output["analysis"],
        }
