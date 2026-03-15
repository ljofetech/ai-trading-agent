from lnn import Model
from .rules import apply_rules


class LNNJudge:

    @staticmethod
    def validate(plan: dict, market_data: dict):

        model = Model()
        apply_rules(model, plan, market_data)
        model.infer()

        return plan
