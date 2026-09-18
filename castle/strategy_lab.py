"""Nightforce Strategy Lab.

Strategy definitions and research metadata live here.
Trade execution does not belong in this module.
"""

STRATEGIES = {
    "ma_trend": {
        "name": "MA Trend",
        "description": (
            "Existing Nightforce 10/30 moving-average trend strategy."
        ),
        "timeframe": "M15",
        "status": "ACTIVE_BASELINE",
    },
    "ma_trend_confirmed_3": {
        "name": "MA Trend - 3 Bar Confirmation",
        "description": (
            "Experimental 10/30 MA trend strategy requiring "
            "three consecutive matching completed-bar signals."
        ),
        "timeframe": "M15",
        "confirmation_bars": 3,
        "status": "EXPERIMENTAL",
    },
}


def get_strategy(strategy_id):
    """Return a Strategy Lab definition by its identifier."""

    return STRATEGIES.get(strategy_id)


def list_strategies():
    """Return all currently registered Strategy Lab definitions."""

    return STRATEGIES.copy()
