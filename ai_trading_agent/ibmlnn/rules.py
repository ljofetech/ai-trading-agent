from lnn import Predicate, Proposition


def define_predicates():
    """
    Определяем логические переменные.
    """

    LiquidityHigh = Proposition("LiquidityHigh")
    VolatilityLow = Proposition("VolatilityLow")
    ConfidenceAcceptable = Proposition("ConfidenceAcceptable")
    RiskAcceptable = Proposition("RiskAcceptable")
    TradeAllowed = Proposition("TradeAllowed")

    return {
        "LiquidityHigh": LiquidityHigh,
        "VolatilityLow": VolatilityLow,
        "ConfidenceAcceptable": ConfidenceAcceptable,
        "RiskAcceptable": RiskAcceptable,
        "TradeAllowed": TradeAllowed,
    }


def add_facts_from_plan(model, predicates, plan, market_data):
    """
    Преобразуем числовые параметры в логические факты.
    """

    if market_data["liquidity"] > 5_000_000:
        model.add_data({predicates["LiquidityHigh"]: True})
    else:
        model.add_data({predicates["LiquidityHigh"]: False})

    if market_data["volatility"] < 0.05:
        model.add_data({predicates["VolatilityLow"]: True})
    else:
        model.add_data({predicates["VolatilityLow"]: False})

    if plan.confidence > 0.6:
        model.add_data({predicates["ConfidenceAcceptable"]: True})
    else:
        model.add_data({predicates["ConfidenceAcceptable"]: False})


def add_logic_rules(model, predicates):
    """
    Определяем формальные ограничения.
    """

    LiquidityHigh = predicates["LiquidityHigh"]
    VolatilityLow = predicates["VolatilityLow"]
    ConfidenceAcceptable = predicates["ConfidenceAcceptable"]
    TradeAllowed = predicates["TradeAllowed"]

    # Если ликвидность высокая И волатильность низкая И confidence приемлемый → сделка разрешена
    rule = (LiquidityHigh & VolatilityLow & ConfidenceAcceptable) >> TradeAllowed

    model.add_knowledge(rule)


def apply_rules(model, plan, market_data):
    """
    Главная функция, вызываемая LNNJudge.
    """

    predicates = define_predicates()

    add_facts_from_plan(model, predicates, plan, market_data)
    add_logic_rules(model, predicates)

    model.infer()

    trade_allowed = model[predicates["TradeAllowed"]].state()

    if not trade_allowed:
        raise Exception("Trade rejected by LNN validation")
