# Import json for serializing data into prompt strings and the LLM client for validation
import json
from llmcouncil.client import LLMClient


class SupervisorAgent:
    # Validate and potentially revise the execution plan against market and risk data
    @staticmethod
    def validate_and_coordinate(
        state: dict,  # original conversation state (unused here but kept for pipeline consistency)
        market_data: dict,  # market analysis output from MarketAgent
        risk_data: dict,  # risk assessment output from RiskAgent
        execution_plan: dict,  # proposed trading plan from ExecutionAgent
    ):
        print(
            "\n[SupervisorAgent] Validating execution plan against market analysis and risk assessment..."
        )
        # Serialize all inputs to JSON so they can be embedded in the LLM prompt
        market_json = json.dumps(market_data, default=str)
        risk_json = json.dumps(risk_data, default=str)
        execution_json = json.dumps(execution_plan, default=str)
        print(
            "Market data, risk assessment, and execution plan prepared for supervisor validation."
        )
        # Ask the LLM to act as a supervisor and perform a final consistency check
        validation = LLMClient.generate(f"""
            You are a trading supervisor. Your job is to review and validate the proposed execution plan
            against the market analysis and risk assessment. Coordinate all inputs into a final, safe,
            and consistent trading decision.

            Market data: {market_json}
            Risk assessment: {risk_json}
            Execution plan: {execution_json}

            Validation checks:
            - Does the action direction align with the price predictions?
            - Are stop-loss and take-profit levels consistent with the risk limits?
            - Is the leverage within the max allowed?
            - Is the position sizing reasonable?
            - If any discrepancy is found, adjust the plan to the safest viable alternative.

            Return the FINAL coordinated trading plan as JSON. If the original plan is valid, return it unchanged with status "approved". If modifications were needed, return the revised plan and status "revised".

            Output JSON format:
            {{
                "final_action": "BUY" | "SELL" | "HOLD",
                "final_entry": number,
                "final_stop_loss": number,
                "final_take_profit": [list of numbers],
                "final_position_size": number,
                "final_leverage": integer,
                "validation_status": "approved" | "revised",
                "supervisor_comments": "string"
            }}
            """)
        print("Supervisor validation completed with the following output:")
        print(validation)
        # Return the supervisor's final validated (or revised) trading decision
        return validation
