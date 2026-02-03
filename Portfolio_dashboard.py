
# =================================================
# PORTFOLIO OPTIMISATION DASHBOARD (CLEAN VERSION)
# =================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Portfolio Optimisation Dashboard",
    layout="wide"
)

st.title("📊 Portfolio Optimisation & Continuous Reassessment Dashboard")

TRADING_DAYS = 252

# =================================================
# LOAD DATA
# =================================================
@st.cache_data
def load_data():
    returns = pd.read_excel(
        "sp500_daily_returns.xlsx",
        index_col=0,
        parse_dates=True
    )
    return returns

returns = load_data()
assets = returns.columns
n_assets = len(assets)

# =================================================
# PORTFOLIO WEIGHTS (CLEAN & SAFE)
# =================================================
w_eq = np.ones(n_assets) / n_assets

cov = returns.cov() * TRADING_DAYS
inv_cov = np.linalg.pinv(cov)
ones = np.ones(n_assets)

# Minimum Variance (Unconstrained)
w_mvp = inv_cov @ ones
w_mvp /= ones.T @ inv_cov @ ones

# Maximum Sharpe (Unconstrained, rf = 0)
mu = returns.mean() * TRADING_DAYS
w_ms = inv_cov @ mu
w_ms /= np.sum(w_ms)

# =================================================
# HELPER FUNCTIONS
# =================================================
def annualised_return(r):
    return r.mean() * TRADING_DAYS

def annualised_volatility(r):
    return r.std() * np.sqrt(TRADING_DAYS)

def sharpe_ratio(r):
    return annualised_return(r) / annualised_volatility(r)

def max_drawdown(cum_ret):
    running_max = np.maximum.accumulate(cum_ret)
    drawdown = (cum_ret - running_max) / running_max
    return drawdown.min()

# =================================================
# COLOUR MAP
# =================================================
COLOR_MAP = {
    "Equal Weight": "#1f77b4",
    "Min Variance": "#2ca02c",
    "Max Sharpe": "#9467bd"
}

# =================================================
# SIDEBAR
# =================================================
st.sidebar.header("📌 Navigation")

section = st.sidebar.radio(
    "Select Section",
    [
        "Overview",
        "Data & Returns",
        "Portfolio Construction",
        "Risk Analysis",
        "Performance Analysis",
        "Continuous Reassessment"
    ]
)

portfolio_choice = st.sidebar.selectbox(
    "Select Portfolio",
    ["Equal Weight", "Min Variance", "Max Sharpe"]
)

# =================================================
# SELECT PORTFOLIO
# =================================================
if portfolio_choice == "Equal Weight":
    weights = w_eq
elif portfolio_choice == "Min Variance":
    weights = w_mvp
else:
    weights = w_ms

port_returns = returns @ weights
cum_returns = (1 + port_returns).cumprod()
color = COLOR_MAP[portfolio_choice]

# =================================================
# OVERVIEW
# =================================================
if section == "Overview":
    st.subheader("📌 Portfolio Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Annual Return", f"{annualised_return(port_returns):.2%}")
    c2.metric("Volatility", f"{annualised_volatility(port_returns):.2%}")
    c3.metric("Sharpe Ratio", f"{sharpe_ratio(port_returns):.2f}")
    c4.metric("Max Drawdown", f"{max_drawdown(cum_returns):.2%}")

    fig = px.line(
        cum_returns,
        title=f"Cumulative Returns – {portfolio_choice}",
        labels={"value": "Cumulative Return", "index": "Date"}
    )
    fig.update_traces(line=dict(color=color, width=3))
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# DATA & RETURNS
# =================================================
elif section == "Data & Returns":
    st.subheader("📈 Data & Return Characteristics")

    fig = px.histogram(
        returns,
        nbins=40,
        title="Distribution of Asset Returns"
    )
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    corr = returns.corr()
    fig = px.imshow(
        corr,
        title="Correlation Matrix",
        color_continuous_scale="RdBu_r"
    )
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# PORTFOLIO CONSTRUCTION
# =================================================
elif section == "Portfolio Construction":
    st.subheader("🧮 Portfolio Weights")

    weights_df = pd.DataFrame(
        weights,
        index=assets,
        columns=["Weight"]
    )

    fig = px.bar(
        weights_df,
        y="Weight",
        title=f"Portfolio Weights – {portfolio_choice}",
        color_discrete_sequence=[color]
    )
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# RISK ANALYSIS
# =================================================
elif section == "Risk Analysis":
    st.subheader("⚠️ Risk Contribution Analysis")

    port_var = weights.T @ cov @ weights
    marginal = cov @ weights
    risk_contrib = weights * marginal / port_var

    rc_df = pd.DataFrame(
        risk_contrib,
        index=assets,
        columns=["Risk Contribution"]
    )

    fig = px.bar(
        rc_df,
        y="Risk Contribution",
        title="Asset-Level Risk Contributions",
        color_discrete_sequence=["#d62728"]
    )
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# PERFORMANCE ANALYSIS
# =================================================
elif section == "Performance Analysis":
    st.subheader("📉 Drawdown Analysis")

    running_max = np.maximum.accumulate(cum_returns)
    drawdown = (cum_returns - running_max) / running_max

    fig = px.line(
        drawdown,
        title="Portfolio Drawdown",
        labels={"value": "Drawdown", "index": "Date"}
    )
    fig.update_traces(line=dict(color="#d62728"))
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# CONTINUOUS REASSESSMENT
# =================================================
elif section == "Continuous Reassessment":
    st.subheader("🔄 Rolling Performance Analysis")

    rolling_sharpe = (
        port_returns.rolling(252).mean()
        / port_returns.rolling(252).std()
    ) * np.sqrt(TRADING_DAYS)

    fig = px.line(
        rolling_sharpe,
        title="Rolling Sharpe Ratio (12-Month Window)"
    )
    fig.update_traces(line=dict(color=color))
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

#----------------------------------------------------------------#
# ============================================================
# REAL-WORLD CONSTRAINED & ROBUST PORTFOLIO ANALYSIS
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(layout="wide")
st.title("📊 Real-World Portfolio Analysis: Benchmark vs Optimised")

TRADING_DAYS = 252

# ============================================================
# LOAD DATA
# ============================================================
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

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def annualised_return(r):
    return r.mean() * TRADING_DAYS

def annualised_volatility(r):
    return r.std() * np.sqrt(TRADING_DAYS)

def sharpe_ratio(r):
    return annualised_return(r) / annualised_volatility(r)

def max_drawdown(r):
    cum = (1 + r).cumprod()
    peak = np.maximum.accumulate(cum)
    return ((cum - peak) / peak).min()

def min_variance_unconstrained(cov):
    inv_cov = np.linalg.pinv(cov)
    ones = np.ones(len(cov))
    w = inv_cov @ ones
    return w / (ones.T @ inv_cov @ ones)

def min_variance_long_only(cov):
    w = np.ones(len(cov)) / len(cov)
    lr = 0.01
    for _ in range(800):
        grad = 2 * cov @ w
        w -= lr * grad
        w = np.maximum(w, 0)
        w /= w.sum()
    return w

# ============================================================
# PORTFOLIO CONSTRUCTION
# ============================================================
cov = returns.cov() * TRADING_DAYS

# 1️⃣ Equal-weight (benchmark)
w_eq = np.ones(n_assets) / n_assets
ret_eq = returns @ w_eq

# 2️⃣ Unconstrained MVP (theoretical)
w_uc = min_variance_unconstrained(cov)
ret_uc = returns @ w_uc

# 3️⃣ Long-only MVP (real-world)
w_lo = min_variance_long_only(cov)
ret_lo = returns @ w_lo

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.header("📌 Analysis Menu")

view = st.sidebar.radio(
    "Select Analysis",
    [
        "Cumulative Performance",
        "Risk-Return Comparison",
        "Real-World Robustness"
    ],
    key="main_view"
)

# ============================================================
# VIEW 1: CUMULATIVE PERFORMANCE
# ============================================================
if view == "Cumulative Performance":

    st.subheader("📈 Cumulative Performance Comparison")

    cum_df = pd.DataFrame({
        "Equal Weight (Benchmark)": (1 + ret_eq).cumprod(),
        "Unconstrained MVP": (1 + ret_uc).cumprod(),
        "Long-Only MVP": (1 + ret_lo).cumprod()
    })

    fig = px.line(
        cum_df,
        title="Cumulative Portfolio Performance",
        labels={"value": "Cumulative Value", "index": "Date"}
    )
    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, use_container_width=True, key="cum_perf")

    st.markdown("""
    **Interpretation:**  
    The equal-weight portfolio provides a naïve diversification benchmark.
    The unconstrained MVP often achieves lower volatility but may rely on
    extreme short positions. The long-only MVP delivers smoother performance
    while remaining implementable in real markets.
    """)

# ============================================================
# VIEW 2: RISK–RETURN COMPARISON
# ============================================================
elif view == "Risk-Return Comparison":

    st.subheader("⚖️ Risk–Return Trade-off")

    summary = pd.DataFrame({
        "Portfolio": [
            "Equal Weight",
            "Unconstrained MVP",
            "Long-Only MVP"
        ],
        "Annual Return": [
            annualised_return(ret_eq),
            annualised_return(ret_uc),
            annualised_return(ret_lo)
        ],
        "Volatility": [
            annualised_volatility(ret_eq),
            annualised_volatility(ret_uc),
            annualised_volatility(ret_lo)
        ],
        "Sharpe Ratio": [
            sharpe_ratio(ret_eq),
            sharpe_ratio(ret_uc),
            sharpe_ratio(ret_lo)
        ]
    })

    st.dataframe(
        summary.style.format({
            "Annual Return": "{:.2%}",
            "Volatility": "{:.2%}",
            "Sharpe Ratio": "{:.2f}"
        }),
        use_container_width=True
    )

    st.markdown("""
    **Interpretation:**  
    While the unconstrained MVP often exhibits superior volatility reduction,
    its Sharpe ratio advantage may be driven by unrealistic leverage and short
    selling. The long-only MVP offers a more balanced and investable risk–return
    profile compared to both the benchmark and the unconstrained solution.
    """)

# ============================================================
# VIEW 3: REAL-WORLD ROBUSTNESS
# ============================================================
elif view == "Real-World Robustness":

    st.subheader("🛡️ Downside Risk & Robustness")

    robustness = pd.DataFrame({
        "Portfolio": [
            "Equal Weight",
            "Unconstrained MVP",
            "Long-Only MVP"
        ],
        "Max Drawdown": [
            max_drawdown(ret_eq),
            max_drawdown(ret_uc),
            max_drawdown(ret_lo)
        ]
    })

    st.dataframe(
        robustness.style.format({
            "Max Drawdown": "{:.2%}"
        }),
        use_container_width=True
    )

    st.markdown("""
    **Real-World Insight:**  
    Maximum drawdown captures investor experience during market stress.
    Although the unconstrained MVP may minimise variance in theory, it
    can suffer severe drawdowns due to leveraged exposures. The long-only
    MVP reduces downside risk while remaining feasible for institutional
    implementation.
    """)

# ============================================================
# FINAL CONCLUSION
# ============================================================
st.markdown("""
### ✅ Overall Conclusion

This analysis demonstrates that **portfolio optimisation must be evaluated
relative to both a naïve benchmark and real-world constraints**. While
unconstrained optimisation performs well theoretically, its reliance on
short selling limits practical usability. The long-only minimum variance
portfolio provides a robust compromise between diversification, risk
control, and real-world implementability.
""")
#--------------------------------------------------------------------------------#
# ============================================================
# RISK CONTRIBUTION & TAIL RISK ANALYSIS
# Equal Weight vs MVP vs Max Sharpe
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(layout="wide")
st.title("📊 Risk Contribution & Tail Risk: Three-Portfolio Comparison")

TRADING_DAYS = 252
ALPHA = 0.05   # 95% VaR / CVaR
RF = 0.0       # Risk-free rate

# ============================================================
# LOAD DATA
# ============================================================
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

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def annualised_return(r):
    return r.mean() * TRADING_DAYS

def annualised_volatility(r):
    return r.std() * np.sqrt(TRADING_DAYS)

def sharpe_ratio(r):
    return (annualised_return(r) - RF) / annualised_volatility(r)

def min_variance(cov):
    inv_cov = np.linalg.pinv(cov)
    ones = np.ones(len(cov))
    w = inv_cov @ ones
    return w / (ones.T @ inv_cov @ ones)

def max_sharpe(mu, cov):
    inv_cov = np.linalg.pinv(cov)
    w = inv_cov @ mu
    return w / np.sum(w)

def risk_contribution(weights, cov):
    port_var = weights.T @ cov @ weights
    marginal = cov @ weights
    return weights * marginal / port_var

def risk_concentration(rc):
    return np.sum(rc ** 2)

def effective_bets(rc):
    return 1 / np.sum(rc ** 2)

def historical_var(r, alpha):
    return np.quantile(r, alpha)

def historical_cvar(r, alpha):
    var = historical_var(r, alpha)
    return r[r <= var].mean()

# ============================================================
# PORTFOLIOS
# ============================================================
cov = returns.cov() * TRADING_DAYS
mu = returns.mean() * TRADING_DAYS

# 1️⃣ Equal Weight
w_eq = np.ones(n_assets) / n_assets
ret_eq = returns @ w_eq

# 2️⃣ Minimum Variance
w_mvp = min_variance(cov)
ret_mvp = returns @ w_mvp

# 3️⃣ Maximum Sharpe
w_ms = max_sharpe(mu.values, cov)
ret_ms = returns @ w_ms

# ============================================================
# RISK CONTRIBUTIONS
# ============================================================
rc_eq = risk_contribution(w_eq, cov)
rc_mvp = risk_contribution(w_mvp, cov)
rc_ms = risk_contribution(w_ms, cov)

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.header("📌 Risk Analysis Menu")

view = st.sidebar.radio(
    "Select Analysis",
    [
        "Risk Contribution (Structure)",
        "Diversification Metrics",
        "Tail Risk (VaR & CVaR)"
    ],
    key="risk_view"
)

# ============================================================
# 1️⃣ RISK CONTRIBUTION STRUCTURE
# ============================================================
if view == "Risk Contribution (Structure)":

    st.subheader("⚠️ Asset-Level Risk Contribution")

    rc_df = pd.DataFrame({
        "Equal Weight": rc_eq,
        "Min Variance": rc_mvp,
        "Max Sharpe": rc_ms
    }, index=assets)

    fig = px.bar(
        rc_df,
        barmode="group",
        title="Risk Contribution by Asset (Three Portfolios)"
    )
    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, use_container_width=True, key="rc_structure")

    st.markdown("""
    **Meaningful interpretation:**  
    - Equal-weight portfolios typically exhibit *uneven risk contributions*
      due to correlation and volatility differences.  
    - The minimum variance portfolio deliberately concentrates risk in
      low-volatility assets.  
    - The maximum Sharpe portfolio often shows *strong risk concentration*,
      reflecting aggressive exposure to high-return assets.
    """)

# ============================================================
# 2️⃣ DIVERSIFICATION METRICS
# ============================================================
elif view == "Diversification Metrics":

    st.subheader("📊 Risk Concentration & Effective Number of Bets")

    div_df = pd.DataFrame({
        "Portfolio": ["Equal Weight", "Min Variance", "Max Sharpe"],
        "Risk Concentration (H)": [
            risk_concentration(rc_eq),
            risk_concentration(rc_mvp),
            risk_concentration(rc_ms)
        ],
        "Effective Number of Bets": [
            effective_bets(rc_eq),
            effective_bets(rc_mvp),
            effective_bets(rc_ms)
        ]
    })

    st.dataframe(
        div_df.style.format({
            "Risk Concentration (H)": "{:.3f}",
            "Effective Number of Bets": "{:.2f}"
        }),
        use_container_width=True
    )

    st.markdown("""
    **What this tells us:**  
    - A *lower* concentration index and *higher* effective number of bets
      indicate superior diversification.  
    - Equal-weight portfolios are not necessarily well-diversified in risk terms.  
    - Maximum Sharpe portfolios typically sacrifice diversification for return.
    """)

# ============================================================
# 3️⃣ TAIL RISK
# ============================================================
elif view == "Tail Risk (VaR & CVaR)":

    st.subheader("📉 Tail Risk Comparison")

    tail_df = pd.DataFrame({
        "Portfolio": ["Equal Weight", "Min Variance", "Max Sharpe"],
        "VaR (95%)": [
            historical_var(ret_eq, ALPHA),
            historical_var(ret_mvp, ALPHA),
            historical_var(ret_ms, ALPHA)
        ],
        "CVaR (95%)": [
            historical_cvar(ret_eq, ALPHA),
            historical_cvar(ret_mvp, ALPHA),
            historical_cvar(ret_ms, ALPHA)
        ]
    })

    st.dataframe(
        tail_df.style.format({
            "VaR (95%)": "{:.2%}",
            "CVaR (95%)": "{:.2%}"
        }),
        use_container_width=True
    )

    fig = px.histogram(
        pd.DataFrame({
            "Equal Weight": ret_eq,
            "Min Variance": ret_mvp,
            "Max Sharpe": ret_ms
        }),
        nbins=60,
        title="Return Distribution – Tail Risk Comparison"
    )
    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, use_container_width=True, key="tail_hist")

    st.markdown("""
    **Real-world interpretation:**  
    - The minimum variance portfolio exhibits the smallest extreme losses,
      confirming its defensive nature.  
    - The maximum Sharpe portfolio shows the most severe tail risk, reflecting
      aggressive return targeting.  
    - Equal-weight portfolios lie between these extremes, offering robustness
      without optimisation assumptions.
    """)



