# S&P 500 Portfolio Analysis Results

## Overview
This analysis compares two portfolio optimization strategies applied to S&P 500 stocks:
- **MVP (Minimum Variance Portfolio)**: Optimized to minimize portfolio risk
- **Max-Sharpe Portfolio**: Optimized to maximize the Sharpe ratio (risk-adjusted returns)

**Data Period**: January 5, 2015 to January 2, 2026 (2,766 trading days)  
**Number of Assets**: 463 S&P 500 stocks

---

## Key Findings

### 1. Portfolio Concentration (Herfindahl Index)

The Herfindahl Index measures portfolio concentration, where:
- **Lower values** indicate more diversified portfolios
- **Higher values** indicate more concentrated portfolios

| Portfolio | Herfindahl Index | Interpretation |
|-----------|------------------|----------------|
| MVP | 0.2337 | Well diversified |
| Max-Sharpe | 2.9114 | Highly concentrated |

**Key Insight**: The Max-Sharpe portfolio is **12.46x more concentrated** than the MVP portfolio. This means the Max-Sharpe strategy takes larger positions in fewer assets to maximize returns, while MVP spreads risk across many assets.

---

### 2. Portfolio Risk Metrics

| Metric | MVP | Max-Sharpe |
|--------|-----|------------|
| Portfolio Variance | 0.0069 | 0.0684 |
| Portfolio Volatility (Annual) | 8.33% | 26.15% |

**Key Insight**: The MVP achieves its objective of minimizing risk with only **8.33% volatility**, while the Max-Sharpe portfolio accepts **3.14x higher volatility** (26.15%) in pursuit of higher risk-adjusted returns.

---

### 3. Portfolio Composition

| Metric | MVP | Max-Sharpe |
|--------|-----|------------|
| Max Weight | 10.51% | 28.05% |
| Min Weight | -9.39% | -29.12% |
| Long Positions | 238 | 237 |
| Short Positions | 206 | 220 |
| Sum of Absolute Weights | 7.78 | 28.11 |

**Key Insights**:
- Both portfolios use **long-short strategies** (allowing negative weights/short selling)
- Max-Sharpe has much larger position sizes (max weight of 28% vs 10.5%)
- Max-Sharpe has higher leverage (sum of absolute weights = 28.11 vs 7.78)

---

### 4. Top Holdings Comparison

#### MVP Top 5 Holdings (by absolute weight):
1. **ED** (Consolidated Edison): 10.51%
2. **UNP** (Union Pacific): 9.54%
3. **PH** (Parker-Hannifin): 9.33%
4. **GI** (Gildan): 6.90%
5. **CAT** (Caterpillar): 6.74%

#### Max-Sharpe Top 5 Holdings (by absolute weight):
1. **LIN** (Linde): 28.05%
2. **UNP** (Union Pacific): 24.38%
3. **PH** (Parker-Hannifin): 22.82%
4. **CAT** (Caterpillar): 21.69%
5. **GI** (Gildan): 20.65%

**Note**: Both portfolios favor similar stocks but with very different position sizes.

---

### 5. Risk Contribution Analysis

Risk contribution measures how much each asset contributes to the overall portfolio variance.

#### MVP Risk Contributors:
- Risk is **well-distributed** across many assets
- Top 20 contributors account for a moderate share of total risk
- Weights and risk contributions are relatively balanced

#### Max-Sharpe Risk Contributors:
- Risk is **highly concentrated** in top holdings
- Large positions like LIN, CAT, GOOG, and NVDA dominate risk contribution
- Some assets have negative risk contributions (hedging positions)

---

## Visualizations Generated

1. **sp500_weight_comparison.png**: Bar chart showing top 30 asset weights for both portfolios
2. **sp500_concentration_hhi.png**: Herfindahl Index comparison
3. **sp500_mvp_risk_contributions.png**: MVP weight vs risk contribution for top 20 assets
4. **sp500_sharpe_risk_contributions.png**: Max-Sharpe weight vs risk contribution for top 20 assets

---

## Interpretation & Recommendations

### When to Use MVP:
- **Conservative investors** seeking minimal volatility
- **Risk-averse** portfolios (e.g., pension funds, capital preservation)
- Markets with high uncertainty
- When **stability** is more important than returns

### When to Use Max-Sharpe:
- **Aggressive investors** seeking maximum risk-adjusted returns
- Portfolios that can tolerate **higher volatility** (26% annual)
- Strong conviction in return forecasts
- When **performance** is the primary objective

### Trade-offs:
- **MVP**: Lower risk (8.33% vol) but potentially lower returns
- **Max-Sharpe**: Higher expected returns but 3x higher risk (26.15% vol)
- **Diversification**: MVP is much more diversified (HHI = 0.23 vs 2.91)
- **Leverage**: Max-Sharpe uses significantly more leverage (28.11 vs 7.78)

---

## Files Generated

### Data Files:
- `sp500_portfolio_summary.xlsx`: Summary statistics table
- `sp500_detailed_risk_contributions.xlsx`: Detailed risk contribution for all 463 assets

### Visualization Files:
- `sp500_weight_comparison.png`
- `sp500_concentration_hhi.png`
- `sp500_mvp_risk_contributions.png`
- `sp500_sharpe_risk_contributions.png`

### Code Files:
- `sp500_portfolio_analysis.py`: Full analysis script
- `sp500_analysis_notebook_cell.py`: Notebook-ready version

---

## How to Run the Analysis

### Option 1: Run the Python script
```python
python sp500_portfolio_analysis.py
```

### Option 2: Copy code into Jupyter Notebook
Copy the contents of `sp500_analysis_notebook_cell.py` into a Jupyter notebook cell and run it.

### Required Files:
- `sp500_mvp_weights.xlsx`
- `sp500_max_sharpe_weights.xlsx`
- `sp500_daily_returns.xlsx`

---

## Technical Notes

- **Covariance Matrix**: Computed from daily returns and annualized (×252 trading days)
- **Risk Contribution Formula**: `RC_i = w_i × (Σw)_i / σ_p²`
  - Where `w_i` is the weight of asset i
  - `(Σw)_i` is the marginal contribution to risk
  - `σ_p²` is portfolio variance
- **Herfindahl Index**: `HHI = Σ(w_i²)` for all assets

---

*Analysis completed on January 7, 2026*
