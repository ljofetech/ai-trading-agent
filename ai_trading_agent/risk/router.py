from django.conf import settings


class RiskException(Exception):
    pass


class RiskPolicy:
    """
    Статические правила риск-политики.
    В продакшене это может храниться в БД.
    """

    MAX_TRADE_USD = 50_000
    MIN_CONFIDENCE = 0.6
    MAX_SLIPPAGE = 0.02
    MAX_EXPOSURE_PER_ASSET = 100_000


class RiskRouter:

    @staticmethod
    def route(intent: dict, portfolio: dict = None):
        """
        Проверяет intent перед исполнением.
        """

        RiskRouter._check_confidence(intent)
        RiskRouter._check_trade_size(intent)
        RiskRouter._check_slippage(intent)
        RiskRouter._check_exposure(intent, portfolio)

        return True

    @staticmethod
    def _check_confidence(intent):
        if intent["confidence"] < RiskPolicy.MIN_CONFIDENCE:
            raise RiskException("Confidence below threshold")

    @staticmethod
    def _check_trade_size(intent):
        usd_value = RiskRouter._estimate_usd_value(intent)

        if usd_value > RiskPolicy.MAX_TRADE_USD:
            raise RiskException("Trade size exceeds limit")

    @staticmethod
    def _check_slippage(intent):
        slippage = intent["max_slippage"] / 10_000

        if slippage > RiskPolicy.MAX_SLIPPAGE:
            raise RiskException("Slippage too high")

    @staticmethod
    def _check_exposure(intent, portfolio):
        if not portfolio:
            return

        asset = intent["asset_out"]
        current_exposure = portfolio.get(asset, 0)

        if current_exposure > RiskPolicy.MAX_EXPOSURE_PER_ASSET:
            raise RiskException("Asset exposure limit reached")

    @staticmethod
    def _estimate_usd_value(intent):
        # В реальном проекте берём price oracle
        return intent["amount"] / 10**6
