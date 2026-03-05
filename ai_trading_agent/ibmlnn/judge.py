from lnn import Model
from .rules import apply_rules


class LNNJudge:

    @staticmethod
    def validate(plan, market_data):

        model = Model()
        apply_rules(model, plan, market_data)
        model.infer()

        return plan
