# Stock Data Analysis

## 1. Project Objective

This project seeks to facilitate data-driven decision-making by providing actionable insights on key stock indicators. Through the yfinance library, we extract data from targeted stock tickers and present this data in a user-friendly format using Grafana, aiding analysts in their assessments.

## 2. Technical Stack

- **Data Collection & Analysis**
  - Python: The backbone of our data analysis, making sense of raw stock data.
  - yfinance: A reliable source for fetching our financial data.
  - Airflow: Ensures a timely and consistent data collection process.
  - PostgreSQL: Provides a robust database for storing and querying the financial data.
- **Data Visualization & Reporting**
  - Grafana: Enables interactive and easily digestible visuals on stock performance indicators.
- **Infrastructure & Monitoring**
  - Docker: Streamlines the deployment of our entire data infrastructure.
  - Redis & Flower: Together, they ensure smooth operation by caching tasks and monitoring their execution, respectively.

### 2.1 Data Sources

yfinance library: This connects us to the wealth of financial data housed by Yahoo Finance.

## 3. Analytical Features

- **Stock Performance Overview**:
  - Track the OLHC (Open, Low, High, Close) prices to gauge stock momentum.
  - Study the 5-day moving averages for trend analysis.
  - Scrutinize volume metrics to infer investor interest in specific tickers.
  - Evaluate daily price volatility to inform risk assessments.
  - Compare quarterly daily returns for mid-term performance.

## 4. Analytical Challenges & Solutions

### 4-1. OLHC (Open, Low, High, Close Prices)

- **Situation**: I wanted to understand the daily fluctuations in stock prices.
  - **Task**: I aimed to provide an accurate representation of daily stock price movements.
  - **Action**: I focused on displaying the OLHC data.
  - **Result**: I was able to gain insights into daily stock price movements.

### 4-2. 5-day Moving Averages for Short-term Trends

- **Situation**: I found it difficult to understand.
  - **Task**: I decided to use the 5-day moving average to capture short-term stock trends.
  - **Action**: I integrated the 5-day moving average into the analysis.
  - **Result**: I was able to identify and understand short-term stock price trends.

### 4-3. Volume Analysis for Market Interest and Liquidity

- **Situation**: I believed that volume is an essential indicator.
  - **Task**: I wanted to relate market interest with volume.
  - **Action**: Thinking that market interest might be related to volume, I attempted to analyze the trading volume.
  - **Result**: I gained a better understanding of market interest and liquidity.

### 4-4. Daily Price Volatility for Risk Assessment

- **Situation**: I wondered if there might be some inherent risks.
  - **Task**: I aimed to evaluate risks based on daily price volatility.
  - **Action**: I delved deep into analyzing daily price fluctuations.
  - **Result**: I was able to assess potential risks in stock investments.

### 4-5. Quarterly Daily Returns for Long-term Performance

- **Situation**: I believed that while short-term insights are essential, it's important to understand the mid-to-long-term trajectory by quarter.
  - **Task**: I aimed to analyze daily returns on a quarterly basis to gain long-term insights.
  - **Action**: I incorporated quarterly daily returns into the analysis.
  - **Result**: I obtained a clearer picture of the stock's long-term performance.

## 5. Screenshots & Demo Video

(I will add relevant screenshots and links to any demo video later.)

## 6. Learning Points from the Project

- **Data Engineering and Orchestration**: I gained hands-on experience in crafting and orchestrating data pipelines using tools like Airflow and Docker, ensuring seamless data flow for analysis.

- **Analytical Tools and Visualization**: I delved deep into understanding the capabilities of PostgreSQL for data storage and manipulation. Moreover, I refined my skills in crafting insightful dashboards using Grafana, enabling more informed decision-making based on the analyzed data.

- **Interplay of Tools in Analysis**: I realized the importance of integrating various tools and platforms. The synergy between Airflow, PostgreSQL, and Grafana allowed me to create a cohesive workflow that enhanced the accuracy and efficiency of my analysis.
