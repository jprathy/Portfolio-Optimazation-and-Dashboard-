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

### Overall Analysis ###
![Screenshot_6-2-2026_151214_localhost](https://github.com/user-attachments/assets/cbf99df0-a1ae-49d2-b4a0-2a07b8a97697)
It shows that the equal-weight portfolio is performing well overall, generating strong long-term returns (16.14%) with steady growth over time. However, the portfolio also carries moderate risk and large temporary losses (-38% drawdown), meaning investors must tolerate market fluctuations. The Sharpe ratio (0.89) suggests the returns are reasonably good for the level of risk taken.

### Performance Analysis ###
<img width="1183" height="539" alt="image" src="https://github.com/user-attachments/assets/d194b9b8-9a8a-4f9a-bd0e-6064c7b6adee" />
This chart compares the performance of multiple portfolio strategies against the market over time.
🔹 What It Tells
The Max Sharpe and ML Expected portfolios show the highest growth, indicating superior return potential.
Minimum Variance and Equal Weight grow steadily with lower risk but more moderate returns.
Advanced strategies like Black-Litterman and ML Dynamic outperform the general market benchmark.
The market line remains the lowest, suggesting that optimized portfolios can deliver better long-term results.
👉 Insight: Data-driven and optimized strategies significantly enhance portfolio performance, proving that intelligent allocation methods can outperform traditional investing approaches.

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


## Markotwiz Method
### Min Variance ###

### Overall Analysis ###
<img width="1291" height="582" alt="image" src="https://github.com/user-attachments/assets/3c9f8bb2-ce74-4fb0-b3ca-afb395a64459" />
This dashboard presents the performance of the Minimum Variance portfolio, which focuses on reducing risk while maintaining stable returns.
🔹 What It Tells
Return: 12.24% → Solid long-term growth with a conservative strategy.
Volatility: 12.03% → Lower risk compared to aggressive portfolios.
Sharpe Ratio: 1.02 → Strong risk-adjusted performance (above 1 is considered very good).
Max Drawdown: -20.55% → Smaller losses during market downturns, indicating better capital protection.
👉 Insight: The Minimum Variance strategy prioritizes stability over high returns, making it suitable for risk-averse investors seeking consistent performance with reduced market shocks.

### Portfolio Contruction ###
<img width="1257" height="578" alt="image" src="https://github.com/user-attachments/assets/5d7fb6f6-656d-4d37-914e-a7dca297c53a" />
This chart displays the Top Holdings of the Minimum Variance portfolio, showing the assets with the highest allocation weights.
🔹 What It Tells
A.Each bar represents a stock and its percentage weight in the portfolio.
B.Assets like VZ, JNJ, and CBOE have the largest allocations, meaning they play a bigger role in maintaining portfolio stability.
The weights are relatively balanced, indicating strong diversification rather than heavy dependence on a single asset.
👉 Insight: The portfolio prioritizes lower-risk, stable stocks to reduce overall volatility while maintaining consistent returns.

### Rolling Risk Contniue Reassessment ###
<img width="991" height="537" alt="image" src="https://github.com/user-attachments/assets/be3ed040-b343-4a80-8af9-3084b723a75f" />
This chart shows the 6-month Rolling Sharpe Ratio of the portfolio, measuring how efficiently it generates returns relative to risk over time.
🔹 What It Tells
A.Values above 1 indicate strong risk-adjusted performance.
B.Peaks near 4–5 highlight periods of exceptional portfolio efficiency.
C.Temporary drops below 0 reflect short phases where risk outweighed returns.
D.The repeated recovery to positive levels suggests consistent long-term stability.
👉 Insight: Despite market fluctuations, the portfolio frequently achieves strong risk-adjusted returns, demonstrating effective portfolio management and resilience.

### Risk Contribution ###
<img width="1183" height="539" alt="image" src="https://github.com/user-attachments/assets/74ce86f1-c5d9-4e94-bb1d-d21194e90167" />
This chart shows the Risk Contribution of each asset in the Minimum Variance portfolio, explaining which stocks are driving overall portfolio risk.
🔹 What It Tells
A.Each bar represents how much a stock contributes to total volatility.
B.A few taller bars indicate that some assets contribute more risk than others.
C.Most bars are relatively small, suggesting the portfolio is well-diversified.
👉 Insight: The Minimum Variance strategy effectively spreads risk across assets, helping reduce the chance that one stock heavily impacts overall portfolio stability.

### Tail Risk ###
<img width="1183" height="539" alt="image" src="https://github.com/user-attachments/assets/b59af1c9-9009-4d22-b3d5-d05c6f4d8615" />
This section presents the Tail Risk for the Minimum Variance portfolio, measuring potential losses during extreme market events.
🔹 What It Tells
A.VaR = -1.07% → With 95% confidence, the portfolio is unlikely to lose more than 1.07% in a typical adverse period.
B.CVaR = -1.70% → If losses exceed VaR, the expected average loss is about 1.70%.
👉 Insight: The Minimum Variance portfolio has very controlled downside risk, confirming its defensive nature and suitability for investors who prioritize capital protection over aggressive returns.


## Max Variance ##
### Overall Performance ###
<img width="1273" height="585" alt="image" src="https://github.com/user-attachments/assets/f92a2c75-a02e-418e-8864-3bc804320261" />
This  shows the performance of the Max Sharpe portfolio, designed to maximize returns for each unit of risk.
🔹 What It Tells
Return: 34.81% → Very high growth compared to typical strategies.
Volatility: 18.47% → Higher risk, but taken strategically.
Sharpe Ratio: 1.88 → Excellent risk-adjusted performance, indicating efficient portfolio optimisation.
Max Drawdown: -25.00% → Moderate losses during downturns but manageable given the strong returns.
👉 Insight: The Max Sharpe strategy delivers the best balance between risk and return, making it attractive for investors seeking aggressive growth with efficient risk management.

### Portfolio Construction ###
<img width="1183" height="539" alt="image" src="https://github.com/user-attachments/assets/359fbe3b-ab85-4363-b5fb-302f32bb9682" />
This chart shows the Top Holdings of the Max Sharpe portfolio, highlighting the assets with the largest weights.
🔹 What It Tells
Stocks like LLY, PGR, and NVDA have the highest allocations, meaning they are key drivers of portfolio returns.
The portfolio is slightly more concentrated than a low-risk strategy, allowing for higher growth potential.
Smaller positions help maintain diversification while focusing on high-performing assets.
👉 Insight: The Max Sharpe portfolio strategically allocates more weight to strong-performing stocks to maximize risk-adjusted returns, balancing growth with controlled diversification.

### Rolling Risk Continues Reassessment ###
<img width="1183" height="539" alt="image" src="https://github.com/user-attachments/assets/8f91c296-e646-418e-b331-7fc5a7268313" />
This chart displays the 6-month Rolling Sharpe Ratio for the Max Sharpe portfolio, showing how efficiently the portfolio generates returns relative to risk over time.
🔹 What It Tells
Frequent values above 2 indicate very strong risk-adjusted performance.
Peaks near 5–6 highlight periods of exceptional efficiency.
Short dips below 0 reflect temporary market stress, but quick recoveries show resilience.
👉 Insight: The Max Sharpe portfolio consistently achieves high risk-adjusted returns, confirming it as a high-performing and efficiently optimized strategy despite periodic volatility.

### Risk Contribution ###
<img width="1183" height="539" alt="image" src="https://github.com/user-attachments/assets/f6340518-7428-471e-a227-c14a597290c6" />
This chart shows the Risk Contribution of assets in the Max Sharpe portfolio, identifying which stocks contribute most to overall portfolio volatility.
🔹 What It Tells
A few tall bars indicate that some assets drive a larger portion of the risk, meaning the portfolio is slightly concentrated.
Smaller bars show that many assets have limited impact on total volatility.
This structure is typical for high-return strategies that accept moderate concentration to enhance performance.
👉 Insight: The Max Sharpe portfolio takes calculated risk by allocating more weight to high-impact assets, helping maximize returns while still maintaining a level of diversification.

### Tail Risk ###
<img width="1183" height="539" alt="image" src="https://github.com/user-attachments/assets/8e8ea0e6-d2ca-4131-a7df-8b41fb28b7a7" />
This section shows the Tail Risk of the Max Sharpe portfolio, measuring potential losses during extreme market movements.
🔹 What It Tells
VaR = -1.67% → With 95% confidence, the portfolio is unlikely to lose more than 1.67% in a typical adverse period.
CVaR = -2.59% → If losses exceed this level, the expected average loss is about 2.59%.
👉 Insight: Although the Max Sharpe strategy targets higher returns, its downside risk remains reasonably controlled, indicating a strong balance between aggressive growth and risk management.

## Machine Learning Expected Return ##
<img width="1183" height="539" alt="image" src="https://github.com/user-attachments/assets/68fd8450-62c4-4b8d-8f62-3bacd5a9c300" />
This shows the performance of the ML Expected portfolio, which uses machine learning to predict returns and optimize allocation.
🔹 What It Tells
Return: 37.42% → Extremely high growth potential.
Volatility: 29.81% → Higher risk due to aggressive positioning.
Sharpe Ratio: 1.26 → Strong risk-adjusted returns despite the volatility.
Max Drawdown: -41.86% → Large temporary losses can occur during market stress.
👉 Insight: The ML-driven strategy delivers superior returns but comes with higher fluctuations, making it ideal for investors willing to accept more risk for greater long-term rewards.

### Portfolio Optimization ###
<img width="1183" height="539" alt="image" src="https://github.com/user-attachments/assets/88ac1ac0-d6e7-457e-8429-1b0dd092b8d2" />
This chart shows the Top Holdings of the ML Expected portfolio, highlighting where most of the investment is allocated.
🔹 What It Tells
A large portion of the portfolio is concentrated in a few assets like MSCI, MPWR, NVDA, and AZO.
Higher weights indicate the machine learning model strongly expects these stocks to generate superior returns.
The remaining assets have smaller allocations, providing some diversification.
👉 Insight: The ML Expected strategy is more concentrated and aggressive, focusing capital on high-prediction stocks to maximize returns, but this can also increase overall portfolio risk.
























