# =================================================
# MASTER PORTFOLIO OPTIMISATION DASHBOARD
# =================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestClassifier
from scipy.optimize import minimize

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(page_title="Portfolio Optimisation Dashboard",
                   layout="wide")

st.title("📊 Portfolio Optimisation & Intelligent Allocation Dashboard")

TRADING_DAYS = 252
RF = 0.02
ALPHA = 0.05


# =================================================
# LOAD DATA
# =================================================
@st.cache_data
def load_data():
    df = pd.read_excel(
        "sp500_daily_returns.xlsx",
        index_col=0,
        parse_dates=True
    )
    return df.dropna()

returns = load_data()
assets = returns.columns
n_assets = len(assets)


# =================================================
# HELPER FUNCTIONS
# =================================================
def annualised_return(r):
    return r.mean() * TRADING_DAYS

def annualised_volatility(r):
    return r.std() * np.sqrt(TRADING_DAYS)

def sharpe_ratio(r):
    return annualised_return(r) / annualised_volatility(r)

def max_drawdown(r):
    cum = (1+r).cumprod()
    peak = np.maximum.accumulate(cum)
    return ((cum-peak)/peak).min()

def risk_contribution(w, cov):
    return w * (cov @ w) / (w.T @ cov @ w)

def historical_var(r, a):
    return np.quantile(r, a)

def historical_cvar(r, a):
    return r[r <= historical_var(r, a)].mean()


# =================================================
# OPTIMISERS
# =================================================
def min_variance(cov):

    n = len(cov)

    def vol(w):
        return np.sqrt(w @ cov @ w)

    constraints = ({'type':'eq','fun':lambda w: np.sum(w)-1})
    bounds = tuple((0,1) for _ in range(n))
    w0 = np.ones(n)/n

    result = minimize(vol, w0,
                      bounds=bounds,
                      constraints=constraints)

    return result.x


def max_sharpe_constrained(mu, cov):

    n = len(mu)

    def neg_sharpe(w):
        ret = w @ mu
        vol = np.sqrt(w @ cov @ w)
        return -(ret / vol)

    constraints = ({'type':'eq','fun':lambda w: np.sum(w)-1})
    bounds = tuple((0,1) for _ in range(n))
    w0 = np.ones(n)/n

    result = minimize(neg_sharpe, w0,
                      bounds=bounds,
                      constraints=constraints)

    return result.x


# =================================================
# COVARIANCE
# =================================================
cov = returns.cov() * TRADING_DAYS
cov += np.eye(len(cov)) * 1e-5



mu_hist = returns.mean() * TRADING_DAYS


# =================================================
# STATIC PORTFOLIOS
# =================================================
benchmark = returns.mean(axis=1)
market_return = benchmark.mean() * TRADING_DAYS

w_eq = np.ones(n_assets)/n_assets
ret_eq = returns @ w_eq

w_mvp = min_variance(cov)
ret_mvp = returns @ w_mvp

w_ms = max_sharpe_constrained(mu_hist.values, cov)
ret_ms = returns @ w_ms


# =================================================
# ML EXPECTED RETURNS (RIDGE WITH TIME SPLIT)
# =================================================
@st.cache_data
def ml_expected_returns(returns):

    X = returns.shift(1).dropna()
    y = returns.loc[X.index]

    split = int(len(X)*0.7)

    X_train = X.iloc[:split]
    y_train = y.iloc[:split]
    X_test  = X.iloc[split:]

    model = Ridge(alpha=10)

    preds = {}

    for asset in returns.columns:
        model.fit(X_train, y_train[asset])
        preds[asset] = model.predict(X_test.tail(1))[0]

    mu_ml = pd.Series(preds) * TRADING_DAYS
    mu_ml -= mu_ml.mean()

    return mu_ml

mu_ml = ml_expected_returns(returns)

w_ml = max_sharpe_constrained(mu_ml.values, cov)
ret_ml = returns @ w_ml


# =================================================
# CAPM EXPECTED RETURNS
# =================================================
@st.cache_data
def capm_expected_returns(returns, benchmark, rf):

    market_var = np.var(benchmark)

    betas = returns.apply(
        lambda x: np.cov(x, benchmark)[0,1] / market_var
    )

    expected = rf + betas * (market_return - rf)

    return expected

mu_capm = capm_expected_returns(returns, benchmark, RF)

w_capm = max_sharpe_constrained(mu_capm.values, cov)
ret_capm = returns @ w_capm


# =================================================
# BLACK-LITTERMAN
# =================================================
@st.cache_data
def black_litterman(mu_capm, mu_ml, cov, tau=0.05):

    # convert to numpy
    cov_np = cov.values

    pi = mu_capm.values.reshape(-1,1)
    Q  = mu_ml.values.reshape(-1,1)

    n = len(pi)

    P = np.eye(n)

    omega = tau * cov_np   # MUCH safer

    inv_tau_cov = np.linalg.inv(tau * cov_np)
    inv_omega   = np.linalg.inv(omega)

    posterior = np.linalg.inv(
        inv_tau_cov + P.T @ inv_omega @ P
    ) @ (
        inv_tau_cov @ pi +
        P.T @ inv_omega @ Q
    )

    return pd.Series(
        posterior.flatten(),
        index=mu_capm.index
    )

try:
    mu_bl = black_litterman(mu_capm, mu_ml, cov)
    w_bl = max_sharpe_constrained(mu_bl.values, cov)
    ret_bl = returns @ w_bl
except Exception as e:
    # Fallback to CAPM if Black-Litterman fails
    print(f"Warning: Black-Litterman calculation failed: {e}")
    print("Using CAPM as fallback for Black-Litterman portfolio")
    mu_bl = mu_capm
    w_bl = w_capm
    ret_bl = ret_capm


# =================================================
# RANDOM FOREST DYNAMIC SWITCHING
# =================================================
@st.cache_data
def ml_switching_strategy(returns, w_mvp, w_ms):

    index_ret = returns.mean(axis=1)
    df = pd.DataFrame(index_ret, columns=["Index"])

    df["lag1"] = df["Index"].shift(1)
    df["vol"] = df["Index"].rolling(21).std()

    df["Target"] = (df["Index"].shift(-1) > 0).astype(int)
    df = df.dropna()

    X = df[["lag1","vol"]]
    y = df["Target"]

    split = int(len(df)*0.7)

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=6,
        random_state=42
    )

    model.fit(X.iloc[:split], y.iloc[:split])

    probs = model.predict_proba(X.iloc[split:])[:,1]

    test_dates = df.index[split:]
    returns_test = returns.loc[test_dates]

    ret_mvp = returns_test @ w_mvp
    ret_ms  = returns_test @ w_ms

    dynamic = np.where(probs>0.55, ret_ms, ret_mvp)

    return pd.Series(dynamic, index=test_dates)

ret_dynamic = ml_switching_strategy(returns, w_mvp, w_ms)


# =================================================
# SIDEBAR
# =================================================
st.sidebar.header("Navigation")

section = st.sidebar.selectbox(
    "Select Section",
    ["Overview",
     "Portfolio Construction",
     "Performance Analysis",
     "Rolling Risk",
     "Risk Contribution",
     "Tail Risk"]
)

portfolio_choice = st.sidebar.selectbox(
    "Select Portfolio",
    ["Equal Weight",
     "Min Variance",
     "Max Sharpe",
     "ML Expected",
     "CAPM",
     "Black-Litterman",
     "ML Dynamic"]
)


# =================================================
# SELECT PORTFOLIO
# =================================================
weights = None

if portfolio_choice == "Equal Weight":
    weights, port_returns = w_eq, ret_eq

elif portfolio_choice == "Min Variance":
    weights, port_returns = w_mvp, ret_mvp

elif portfolio_choice == "Max Sharpe":
    weights, port_returns = w_ms, ret_ms

elif portfolio_choice == "ML Expected":
    weights, port_returns = w_ml, ret_ml

elif portfolio_choice == "CAPM":
    weights, port_returns = w_capm, ret_capm

elif portfolio_choice == "Black-Litterman":
    weights, port_returns = w_bl, ret_bl

else:
    port_returns = ret_dynamic


cum_returns = (1+port_returns).cumprod()


# =================================================
# OVERVIEW
# =================================================
if section == "Overview":

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Return", f"{annualised_return(port_returns):.2%}")
    c2.metric("Volatility", f"{annualised_volatility(port_returns):.2%}")
    c3.metric("Sharpe", f"{sharpe_ratio(port_returns):.2f}")
    c4.metric("Max Drawdown", f"{max_drawdown(port_returns):.2%}")

    fig = px.line(cum_returns,
                  title=f"Cumulative Returns — {portfolio_choice}")

    st.plotly_chart(fig, use_container_width=True)


# =================================================
# PORTFOLIO CONSTRUCTION
# =================================================
elif section == "Portfolio Construction":

    if weights is None:
        st.info("Dynamic strategy — weights vary through time.")
        st.stop()

    w_df = (pd.DataFrame(weights,
                         index=assets,
                         columns=["Weight"])
            .sort_values("Weight",
                         ascending=False)
            .head(15))

    fig = px.bar(w_df,
                 y="Weight",
                 title=f"Top Holdings — {portfolio_choice}")

    st.plotly_chart(fig, use_container_width=True)


# =================================================
# PERFORMANCE ANALYSIS
# =================================================
elif section == "Performance Analysis":

    # Combine first
    perf_df = pd.concat({

        "Equal Weight": (1+ret_eq).cumprod(),
        "Min Variance": (1+ret_mvp).cumprod(),
        "Max Sharpe": (1+ret_ms).cumprod(),
        "ML Expected": (1+ret_ml).cumprod(),
        "CAPM": (1+ret_capm).cumprod(),
        "Black-Litterman": (1+ret_bl).cumprod(),
        "ML Dynamic": (1+ret_dynamic).cumprod(),
        "Market": (1+benchmark).cumprod()

    }, axis=1)

    # ALIGN DATA PROPERLY
    perf_df = perf_df.dropna(how="all")

    fig = px.line(
        perf_df,
        title="Portfolio Performance Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

    perf_df = perf_df.ffill()
    ret_dynamic = ml_switching_strategy(returns, w_mvp, w_ms)


# =================================================
# ROLLING RISK
# =================================================
elif section == "Rolling Risk":

    rolling = (port_returns.rolling(126).mean() /
               port_returns.rolling(126).std()) * np.sqrt(252)

    fig = px.line(rolling,
                  title="Rolling Sharpe (6 Months)")

    st.plotly_chart(fig, use_container_width=True)


# =================================================
# RISK CONTRIBUTION
# =================================================
elif section == "Risk Contribution":

    if weights is None:
        st.info("Unavailable for dynamic strategy.")
        st.stop()

    rc = risk_contribution(weights, cov)

    rc_df = pd.DataFrame(rc,
                         index=assets,
                         columns=["Risk Contribution"])

    fig = px.bar(rc_df, y="Risk Contribution")

    st.plotly_chart(fig, use_container_width=True)


# =================================================
# TAIL RISK
# =================================================
elif section == "Tail Risk":

    tail = pd.DataFrame({

        "VaR":[historical_var(port_returns, ALPHA)],
        "CVaR":[historical_cvar(port_returns, ALPHA)]

    }, index=[portfolio_choice])

    st.dataframe(tail.style.format("{:.2%}"),
                 use_container_width=True)
