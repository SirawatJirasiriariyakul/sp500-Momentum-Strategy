import pandas as pd
import numpy as np


def calculate_cagr(returns):
    """
    Calculate compound annual growth rate (CAGR).

    Parameters
    ----------
    returns : pandas.Series
        Periodic investment returns.

    Returns
    -------
    float
        Annualized compound growth rate.
    """

    cumulative_return = (1 + returns).prod()

    years = (returns.index[-1] - returns.index[0]).days / 365.25

    cagr = cumulative_return ** (1 / years) - 1

    return cagr

def calculate_annualized_volatility(returns):
    """
    Calculate annualized volatility.

    Assumes monthly returns.
    """

    return returns.std() * np.sqrt(12)

def calculate_sharpe_ratio(returns, risk_free_rate=0.0):
    """
    Calculate annualized Sharpe ratio.

    Assumes monthly returns.
    """

    monthly_rf = (1 + risk_free_rate) ** (1 / 12) - 1

    excess_returns = returns - monthly_rf

    return (
        excess_returns.mean()
        / excess_returns.std()
        * np.sqrt(12)
    )

def calculate_max_drawdown(returns):
    """
    Calculate maximum drawdown.

    Returns
    -------
    float
        Largest peak-to-trough decline.
    """

    wealth_index = (1 + returns).cumprod()

    running_peak = wealth_index.cummax()

    drawdown = wealth_index / running_peak - 1

    return drawdown.min()