from .agents.market_agent import MarketAgent
from .agents.risk_agent import RiskAgent
from .agents.execution_agent import ExecutionAgent


class LLMCouncil:

    @staticmethod
    def run(state: dict):
        analysis = MarketAgent.analyze(state)
        risk = RiskAgent.evaluate(analysis)
        execution = ExecutionAgent.plan(state, analysis, risk)

        return {
            "analysis": analysis,
            "risk": risk,
            "execution": execution,
        }
