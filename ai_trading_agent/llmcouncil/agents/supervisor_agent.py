# from llmcouncil.client import LLMClient


# class SupervisorAgent:
#     @staticmethod
#     def validate_and_coordinate(
#         state: dict, market_data: dict, risk_data: dict, execution_plan: dict
#     ):
#         validation = LLMClient.generate(
#             f"""
#                 You are a supervisor AI for Trend Following + ATR strategy.
                
#                 Review all decisions made by specialized agents and ensure:
#                 1. Consistency across all analyses
#                 2. Adherence to trend following principles
#                 3. Proper use of ATR for position sizing
#                 4. No hallucinations or impossible prices
#                 5. Risk is properly managed

#                 USER REQUEST: {state["user_input"]}
                
#                 MARKET AGENT OUTPUT: {market_data}
                
#                 RISK AGENT OUTPUT: {risk_data}
                
#                 EXECUTION AGENT OUTPUT: {execution_plan}

#                 Check for:
#                 - Is the trend correctly identified?
#                 - Are ATR values reasonable?
#                 - Is position sizing appropriate for volatility?
#                 - Is risk-reward ratio acceptable (>2:1)?
#                 - Are stop loss levels logical?
#                 - Any contradictions between agents?

#                 Return ONLY valid JSON:
#                 {{
#                     "is_valid": boolean,
#                     "issues": ["issue1", "issue2"],
#                     "suggestions": ["suggestion1", "suggestion2"],
#                     "adjusted_plan": {{
#                         "changes_made": ["change1"],
#                         "modified_execution_plan": {{
#                             // copy execution_plan here with modifications
#                         }}
#                     }},
#                     "final_decision": "APPROVE | REJECT | MODIFY",
#                     "supervisor_reasoning": "text"
#                 }}
#             """
#         )

#         return validation
