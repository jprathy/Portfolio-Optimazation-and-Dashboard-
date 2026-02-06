#  Portfolio Optimisation Dashboard

An institutional-grade portfolio optimisation framework integrating machine learning, constrained optimisation, and dynamic asset allocation.

## Key Features

- Mean-Variance Optimisation (Minimum Variance & Maximum Sharpe)
- Machine Learning Expected Returns (Ridge Regression)
- Random Forest Market Regime Detection
- Dynamic Portfolio Switching
- Risk Decomposition
- Tail Risk (VaR & CVaR)
- Rolling Risk Metrics
- Interactive Streamlit Dashboard

## Methodological Contribution

Unlike traditional static portfolio construction approaches, this project implements a continuous reassessment framework in which portfolio allocations adapt to evolving market conditions using predictive machine learning models.

This mirrors real-world quantitative asset management practices.

## Tech Stack

Python  
Pandas  
Scikit-Learn  
SciPy  
Plotly  
Streamlit  

## My Complete Dashboard
## Equal Weight
### Overall Navigator ###
![Screenshot_6-2-2026_151214_localhost](https://github.com/user-attachments/assets/cbf99df0-a1ae-49d2-b4a0-2a07b8a97697)
It shows that the equal-weight portfolio is performing well overall, generating strong long-term returns (16.14%) with steady growth over time. However, the portfolio also carries moderate risk and large temporary losses (-38% drawdown), meaning investors must tolerate market fluctuations. The Sharpe ratio (0.89) suggests the returns are reasonably good for the level of risk taken.

### Performance Analysis ###
<img width="1290" height="576" alt="image" src="https://github.com/user-attachments/assets/68600969-d53d-4835-84c4-a8e4f1ed8eed" />
The ML Expected portfolio (red line) significantly outperforms all other strategies, indicating that machine learning–based return predictions can enhance portfolio growth.

A.The Max Sharpe strategy shows strong and stable improvement, suggesting good risk-adjusted performance.
B.Traditional approaches like Equal Weight and Min Variance grow more slowly, reflecting safer but lower-return strategies.
C.The ML Dynamic portfolio demonstrates consistent progress, highlighting the benefit of adaptive allocation.
D.The Market benchmark remains the lowest, meaning most optimized portfolios are beating the general market.

### Rolling Risk Continues reassessment ###
<img width="1288" height="566" alt="image" src="https://github.com/user-attachments/assets/7d290b92-49ca-4700-a6fd-1b8065c0d868" />
This chart shows the 6-month rolling Sharpe ratio, which measures how well the portfolio is performing relative to the risk taken over time.

🔹 What It Tells
A.When the Sharpe ratio is above 1, the portfolio is delivering good risk-adjusted returns.
B.Peaks around 3–5 indicate periods of very strong performance.
C.Drops below 0 suggest the portfolio experienced poor returns compared to its risk.
D.The fluctuations highlight that portfolio performance changes with market conditions, but overall it repeatedly returns to positive territory.

👉 Insight: The portfolio demonstrates the ability to recover after weaker periods and generate strong risk-adjusted returns, indicating resilience and effective long-term strategy.

###  Risk Contribution ###
<img width="1288" height="566" alt="image" src="https://github.com/user-attachments/assets/f2ef4ff8-a37b-4086-a0cb-8d8e887a6f59" />

This is a Risk Contribution chart, showing how much each asset in the portfolio contributes to the total portfolio risk.
🔹 What It Means
A.Each bar represents an individual stock or asset.
B.Taller bars indicate assets that contribute more risk, while shorter bars contribute less risk.
C.The spread suggests the risk is fairly diversified rather than concentrated in just a few assets.
👉 Insight: Monitoring risk contribution helps investors identify which assets are driving portfolio volatility and ensures better risk balancing for a more stable portfolio.

### Tail Risk ###
<img width="1289" height="276" alt="image" src="https://github.com/user-attachments/assets/d1b0be89-3f57-4788-8a48-b738ee382876" />

This section shows the Tail Risk metrics of your portfolio, which measure the potential for extreme losses during severe market conditions.
🔹 What It Tells
VaR (95%) = -1.63%
→ There is a 95% confidence that the portfolio will not lose more than 1.63% in a normal trading period.
CVaR (95%) = -2.71%
→ If losses exceed the VaR threshold, the average loss could be around 2.71%, representing worst-case scenarios.
👉 Insight: The portfolio has controlled downside risk, but in rare market shocks, losses can be higher — making tail risk analysis essential for strong risk management.









