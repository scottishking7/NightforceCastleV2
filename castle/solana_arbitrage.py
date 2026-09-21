"""
Nightforce Castle - Solana Arbitrage Engine

Research and simulation module.

Phase 1:
- No wallet access
- No private keys
- No transaction signing
- No blockchain execution
"""

import math


SIMULATION_MODE = True
WALLET_EXECUTION_ENABLED = False

DEFAULT_TRADE_SIZE_USDC = 100.0
DEFAULT_SLIPPAGE_BPS = 50
DEFAULT_TRANSACTION_COST_USDC = 0.01
DEFAULT_MIN_NET_PROFIT_USDC = 0.10


def calculate_arbitrage_opportunity(
    trade_size_usdc,
    buy_price_usdc,
    sell_price_usdc,
    buy_fee_bps=0,
    sell_fee_bps=0,
    slippage_bps=DEFAULT_SLIPPAGE_BPS,
    transaction_cost_usdc=DEFAULT_TRANSACTION_COST_USDC,
):
    values = {
        "trade_size_usdc": trade_size_usdc,
        "buy_price_usdc": buy_price_usdc,
        "sell_price_usdc": sell_price_usdc,
        "buy_fee_bps": buy_fee_bps,
        "sell_fee_bps": sell_fee_bps,
        "slippage_bps": slippage_bps,
        "transaction_cost_usdc": transaction_cost_usdc,
    }

    for name, value in values.items():
        if not math.isfinite(value):
            raise ValueError(f"{name} must be a finite number.")

        if value < 0:
            raise ValueError(f"{name} cannot be negative.")

    if trade_size_usdc == 0:
        raise ValueError("trade_size_usdc must be greater than zero.")

    if buy_price_usdc == 0:
        raise ValueError("buy_price_usdc must be greater than zero.")

    if sell_price_usdc == 0:
        raise ValueError("sell_price_usdc must be greater than zero.")

    buy_fee_rate = buy_fee_bps / 10000.0
    sell_fee_rate = sell_fee_bps / 10000.0
    slippage_rate = slippage_bps / 10000.0

    effective_buy_price = buy_price_usdc * (1 + slippage_rate)
    effective_sell_price = sell_price_usdc * (1 - slippage_rate)

    sol_bought = trade_size_usdc / effective_buy_price

    buy_fee_usdc = trade_size_usdc * buy_fee_rate
    gross_sale_usdc = sol_bought * effective_sell_price
    sell_fee_usdc = gross_sale_usdc * sell_fee_rate

    final_usdc = (
        gross_sale_usdc
        - buy_fee_usdc
        - sell_fee_usdc
        - transaction_cost_usdc
    )
    net_profit_usdc = final_usdc - trade_size_usdc

    gross_spread_percent = (
        (sell_price_usdc - buy_price_usdc) / buy_price_usdc
    ) * 100.0

    return {
        "trade_size_usdc": trade_size_usdc,
        "buy_price_usdc": buy_price_usdc,
        "sell_price_usdc": sell_price_usdc,
        "gross_spread_percent": gross_spread_percent,
        "effective_buy_price": effective_buy_price,
        "effective_sell_price": effective_sell_price,
        "sol_bought": sol_bought,
        "buy_fee_usdc": buy_fee_usdc,
        "sell_fee_usdc": sell_fee_usdc,
        "transaction_cost_usdc": transaction_cost_usdc,
        "final_usdc": final_usdc,
        "net_profit_usdc": net_profit_usdc,
        "meets_minimum_profit": (
            net_profit_usdc >= DEFAULT_MIN_NET_PROFIT_USDC
        ),
    }


def engine_status():
    return {
        "simulation_mode": SIMULATION_MODE,
        "wallet_execution_enabled": WALLET_EXECUTION_ENABLED,
        "default_trade_size_usdc": DEFAULT_TRADE_SIZE_USDC,
        "default_slippage_bps": DEFAULT_SLIPPAGE_BPS,
        "default_transaction_cost_usdc": DEFAULT_TRANSACTION_COST_USDC,
        "minimum_net_profit_usdc": DEFAULT_MIN_NET_PROFIT_USDC,
    }
