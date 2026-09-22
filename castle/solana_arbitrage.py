"""
Nightforce Castle - Solana Arbitrage Engine

Research and simulation module.

Phase 1:
- No wallet access
- No private keys
- No transaction signing
- No blockchain execution
"""

import json
import math
import urllib.error
import urllib.parse
import urllib.request


SIMULATION_MODE = True
WALLET_EXECUTION_ENABLED = False

DEFAULT_TRADE_SIZE_USDC = 100.0
DEFAULT_SLIPPAGE_BPS = 50
DEFAULT_TRANSACTION_COST_USDC = 0.01
DEFAULT_MIN_NET_PROFIT_USDC = 0.10


def validate_arbitrage_inputs(
    trade_size_usdc,
    buy_price_usdc,
    sell_price_usdc,
    buy_fee_bps,
    sell_fee_bps,
    slippage_bps,
    transaction_cost_usdc,
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


def calculate_arbitrage_opportunity(
    trade_size_usdc,
    buy_price_usdc,
    sell_price_usdc,
    buy_fee_bps=0,
    sell_fee_bps=0,
    slippage_bps=DEFAULT_SLIPPAGE_BPS,
    transaction_cost_usdc=DEFAULT_TRANSACTION_COST_USDC,
):
    validate_arbitrage_inputs(
        trade_size_usdc=trade_size_usdc,
        buy_price_usdc=buy_price_usdc,
        sell_price_usdc=sell_price_usdc,
        buy_fee_bps=buy_fee_bps,
        sell_fee_bps=sell_fee_bps,
        slippage_bps=slippage_bps,
        transaction_cost_usdc=transaction_cost_usdc,
    )

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


def compare_venue_quotes(
    venue_a_name,
    venue_a_price_usdc,
    venue_b_name,
    venue_b_price_usdc,
):
    quotes = {
        venue_a_name: venue_a_price_usdc,
        venue_b_name: venue_b_price_usdc,
    }

    for venue_name, price in quotes.items():
        if not venue_name or not venue_name.strip():
            raise ValueError("Venue names cannot be empty.")

        if not math.isfinite(price):
            raise ValueError(
                f"{venue_name} price must be a finite number."
            )

        if price <= 0:
            raise ValueError(
                f"{venue_name} price must be greater than zero."
            )

    if venue_a_name == venue_b_name:
        raise ValueError("Venue names must be different.")

    if venue_a_price_usdc == venue_b_price_usdc:
        buy_venue = None
        sell_venue = None
        buy_price_usdc = venue_a_price_usdc
        sell_price_usdc = venue_b_price_usdc
    else:
        buy_venue = min(quotes, key=quotes.get)
        sell_venue = max(quotes, key=quotes.get)
        buy_price_usdc = quotes[buy_venue]
        sell_price_usdc = quotes[sell_venue]

    gross_spread_usdc = sell_price_usdc - buy_price_usdc
    gross_spread_percent = (
        gross_spread_usdc / buy_price_usdc
    ) * 100.0

    return {
        "buy_venue": buy_venue,
        "buy_price_usdc": buy_price_usdc,
        "sell_venue": sell_venue,
        "sell_price_usdc": sell_price_usdc,
        "gross_spread_usdc": gross_spread_usdc,
        "gross_spread_percent": gross_spread_percent,
    }


def evaluate_two_venue_opportunity(
    venue_a_name,
    venue_a_price_usdc,
    venue_b_name,
    venue_b_price_usdc,
    trade_size_usdc=DEFAULT_TRADE_SIZE_USDC,
    buy_fee_bps=0,
    sell_fee_bps=0,
    slippage_bps=DEFAULT_SLIPPAGE_BPS,
    transaction_cost_usdc=DEFAULT_TRANSACTION_COST_USDC,
):
    route = compare_venue_quotes(
        venue_a_name=venue_a_name,
        venue_a_price_usdc=venue_a_price_usdc,
        venue_b_name=venue_b_name,
        venue_b_price_usdc=venue_b_price_usdc,
    )

    validate_arbitrage_inputs(
        trade_size_usdc=trade_size_usdc,
        buy_price_usdc=route["buy_price_usdc"],
        sell_price_usdc=route["sell_price_usdc"],
        buy_fee_bps=buy_fee_bps,
        sell_fee_bps=sell_fee_bps,
        slippage_bps=slippage_bps,
        transaction_cost_usdc=transaction_cost_usdc,
    )

    if route["buy_venue"] is None:
        return {
            **route,
            "trade_size_usdc": trade_size_usdc,
            "net_profit_usdc": None,
            "meets_minimum_profit": False,
            "opportunity": False,
        }

    calculation = calculate_arbitrage_opportunity(
        trade_size_usdc=trade_size_usdc,
        buy_price_usdc=route["buy_price_usdc"],
        sell_price_usdc=route["sell_price_usdc"],
        buy_fee_bps=buy_fee_bps,
        sell_fee_bps=sell_fee_bps,
        slippage_bps=slippage_bps,
        transaction_cost_usdc=transaction_cost_usdc,
    )

    return {
        **route,
        "trade_size_usdc": trade_size_usdc,
        "net_profit_usdc": calculation["net_profit_usdc"],
        "meets_minimum_profit": calculation["meets_minimum_profit"],
        "opportunity": calculation["meets_minimum_profit"],
    }


HTTP_TIMEOUT_SECONDS = 5


def fetch_json_read_only(url, timeout=HTTP_TIMEOUT_SECONDS):
    if not isinstance(url, str) or not url.strip():
        raise ValueError("url must be a non-empty string.")

    if not isinstance(timeout, (int, float)) or timeout <= 0:
        raise ValueError("timeout must be greater than zero.")

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "NightforceCastle-SolanaResearch/1.0",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:
            raw_body = response.read()

    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"Read-only HTTP request failed with status {exc.code}."
        ) from exc

    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Read-only HTTP request failed: {exc.reason}"
        ) from exc

    except TimeoutError as exc:
        raise RuntimeError(
            "Read-only HTTP request timed out."
        ) from exc

    try:
        return json.loads(raw_body.decode("utf-8"))

    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            "Read-only HTTP response was not valid JSON."
        ) from exc


JUPITER_ORDER_URL = "https://api.jup.ag/swap/v2/order"


def fetch_jupiter_quote(
    input_mint,
    output_mint,
    amount,
    timeout=HTTP_TIMEOUT_SECONDS,
):
    if not isinstance(input_mint, str) or not input_mint.strip():
        raise ValueError("input_mint must be a non-empty string.")

    if not isinstance(output_mint, str) or not output_mint.strip():
        raise ValueError("output_mint must be a non-empty string.")

    input_mint = input_mint.strip()
    output_mint = output_mint.strip()

    if input_mint == output_mint:
        raise ValueError("input_mint and output_mint must be different.")

    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise ValueError("amount must be a positive integer.")

    query = urllib.parse.urlencode(
        {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": amount,
        }
    )
    data = fetch_json_read_only(
        f"{JUPITER_ORDER_URL}?{query}",
        timeout=timeout,
    )

    if not isinstance(data, dict):
        raise RuntimeError("Jupiter quote response must be a JSON object.")

    if data.get("errorCode") is not None:
        raise RuntimeError(
            f"Jupiter quote error: {data.get('errorMessage') or data['errorCode']}"
        )

    if data.get("inputMint") != input_mint:
        raise RuntimeError(
            "Jupiter quote response input mint does not match the request."
        )

    if data.get("outputMint") != output_mint:
        raise RuntimeError(
            "Jupiter quote response output mint does not match the request."
        )

    try:
        in_amount = int(data["inAmount"])
        out_amount = int(data["outAmount"])
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError(
            "Jupiter quote response contained invalid amounts."
        ) from exc

    if in_amount <= 0 or out_amount <= 0:
        raise RuntimeError(
            "Jupiter quote response amounts must be greater than zero."
        )

    if data.get("transaction") is not None:
        raise RuntimeError(
            "Jupiter returned transaction material in read-only mode."
        )

    return {
        "source": "Jupiter",
        "router": data.get("router"),
        "input_mint": data.get("inputMint"),
        "output_mint": data.get("outputMint"),
        "in_amount": in_amount,
        "out_amount": out_amount,
        "in_usd_value": data.get("inUsdValue"),
        "out_usd_value": data.get("outUsdValue"),
        "price_impact_pct": data.get("priceImpactPct"),
        "slippage_bps": data.get("slippageBps"),
        "route_plan": data.get("routePlan"),
        "transaction_present": data.get("transaction") is not None,
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
