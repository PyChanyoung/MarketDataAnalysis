# Stock Data Analysis

## 1. Project Objective

The primary aim of this project is to provide a comprehensive view of key stock indicators for investors. I fetch stock data using the yfinance library, targeting specific stock tickers, and visualize the results in Grafana.

## 2. Technical Stack

- **Programming Language**
  - Python: I use it for data collection, processing, and analysis.
- **Data Integration & Processing**
  - Airflow: Orchestrates my data pipeline.
  - yfinance: Helps me gather stock data.
  - PostgreSQL: My choice for data warehousing.
  - Grafana: I use it to visualize the stock indicators.
- **Containerization & Orchestration**
  - Docker: Houses the images for Airflow, PostgreSQL, Grafana, Redis, and Flower.
- **Cache & Monitoring**
  - Redis: Assists in task caching.
  - Flower: For monitoring tasks.

### 2.1 Data Sources

yfinance library: It provides me access to financial data available from Yahoo Finance.

## 3. Key Features

- **View Stock Indicators**:
  - I can monitor open, low, high, and close prices (OLHC).
  - Analyze 5-day moving averages.
  - Dive into volume analysis for tickers.
  - Understand daily price volatility.
  - Delve deep into quarterly daily returns.

## 4. Project Challenges & Solutions

- **Situation**: I needed consistent and streamlined data fetching to ensure I had the most up-to-date stock information.

  - **Task**: I aimed to establish an efficient data retrieval mechanism without redundancies using Airflow and yfinance.
  - **Action**: I implemented Airflow's DAG capabilities to orchestrate a seamless and consistent data retrieval process from yfinance.
  - **Result**: I achieved a reliable and efficient data pipeline, ensuring up-to-date stock indicators without redundancies.

- **Situation**: I wanted an effective visualization without the need for extensive data preprocessing.

  - **Task**: My goal was to directly use the fetched data for visualization.
  - **Action**: Recognizing that specific columns from yfinance data were straightforward, I used them directly in Grafana without additional processing.
  - **Result**: I was able to offer direct and meaningful visualizations without the need for time-consuming preprocessing.

- **Situation**: I faced the challenge of housing multiple tools within a single Docker container.
  - **Task**: My task was to consolidate multiple tools into a single environment for ease of deployment.
  - **Action**: I integrated tools like Airflow, PostgreSQL, Grafana, Redis, and Flower into one unified Docker container using docker-compose.
  - **Result**: The project's setup and deployment became more straightforward, with all tools cohesively working in one environment.

## 5. Screenshots & Demo Video

(I will add relevant screenshots and links to any demo video later.)

## 6. Learning Points from the Project

- I gained valuable experience in Docker containerization and orchestration.
- I understood the nuances of crafting a real-time data visualization dashboard.
- I experienced the collaboration of multiple tools like Airflow, PostgreSQL, and Grafana within a cohesive workflow.
