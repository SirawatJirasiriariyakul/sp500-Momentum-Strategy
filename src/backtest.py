import pandas as pd
import numpy as np


def calculate_momentum(monthly_prices, lookback=12, skip=1):
    """
    Calculate momentum returns.
    """

    momentum = (
        monthly_prices.shift(skip)
        / monthly_prices.shift(lookback)
        - 1
    )

    return momentum


def select_top_stocks(momentum, top_pct=0.10):
    """
    Select the top percentage of stocks based on momentum.
    """

    ranks = momentum.rank(
        axis=1,
        ascending=False,
        pct=True
    )

    selected = ranks <= top_pct

    return selected


def calculate_weights(selected):
    """
    Equal-weight the selected stocks.
    """

    weights = selected.astype(float)

    weights = weights.div(
        weights.sum(axis=1),
        axis=0
    )

    return weights

def calculate_strategy_returns(weights, monthly_returns):
    """
    Calculate next-month strategy returns.

    The portfolio formed at month t is held during month t+1.
    The final month is excluded because there is no following
    month in the dataset.
    """

    next_month_returns = monthly_returns.shift(-1)

    # Exclude the final month because there is no next month.
    valid_backtest = weights.index < weights.index[-1]

    strategy_returns = (
        weights.loc[valid_backtest]
        * next_month_returns.loc[valid_backtest]
    ).sum(axis=1)

    return strategy_returns