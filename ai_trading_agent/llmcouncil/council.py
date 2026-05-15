# Import agents that perform distinct steps in the council's pipeline
from .agents.market_agent import MarketAgent
from .agents.risk_agent import RiskAgent
from .agents.execution_agent import ExecutionAgent
from .agents.supervisor_agent import SupervisorAgent


class LLMCouncil:

    # Run the full council pipeline: market → risk → execution → supervisor validation
    @staticmethod
    def run(state: dict):
        # Step 1: Analyze market data from the current state
        print("\n[LLMCouncil] Starting council processing with the following state:")
        market_data = MarketAgent.analyze(
            state,
        )
        # Step 2: Evaluate risk based on the market analysis
        risk_data = RiskAgent.evaluate(
            market_data,
        )
        # Step 3: Create an execution plan using the original state, market data, and risk assessment
        execution_plan = ExecutionAgent.plan(
            state,
            market_data,
            risk_data,
        )
        # Step 4: Have the supervisor validate and coordinate all intermediate results
        validation = SupervisorAgent.validate_and_coordinate(
            state,
            market_data,
            risk_data,
            execution_plan,
        )

        # Return a structured output combining all steps
        return {
            "market_analysis": market_data,
            "risk_assessment": risk_data,
            "execution_plan": execution_plan,
            "supervisor_validation": validation,
        }
