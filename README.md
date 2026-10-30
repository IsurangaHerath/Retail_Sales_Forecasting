# Retail Sales Forecasting Using Machine Learning

A reproducible time-series forecasting pipeline comparing simple forecasting baselines with a Random Forest regression model. Built for educational and portfolio demonstration purposes.

## Project Goal
Analyze historical retail grocery sales, identify temporal patterns, and produce 14-day daily sales forecasts using chronological validation to prevent future-data leakage.

## Dataset Source
- **Competition:** [Kaggle — Store Sales — Time Series Forecasting](https://www.kaggle.com/competitions/store-sales-time-series-forecasting)
- **Files:** `train.csv`, `test.csv`, `stores.csv`, `transactions.csv`, `oil.csv`, `holidays_events.csv`
- **Target:** `sales`
- **Note:** The raw dataset is excluded from this repository due to Kaggle licensing. Follow the download instructions below to reproduce results.

## Setup (Reproduction Instructions)
1. Clone this repository:
   ```powershell
   git clone https://github.com/IsurangaHerath/Retail_Sales_Forecasting.git
   cd Retail_Sales_Forecasting
   ```
2. Create a virtual environment (recommended):
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Download the dataset from Kaggle (requires account and competition acceptance):
   - Visit: https://www.kaggle.com/competitions/store-sales-time-series-forecasting/data
   - Place downloaded files in `data/raw/`

## Repository Structure
```
retail-sales-forecasting/
    README.md
    requirements.txt
    .gitignore
    data/
        raw/         (downloaded dataset — excluded from git)
        processed/
    notebooks/
        01_sales_eda.ipynb
    src/
        data_loader.py
        preprocessing.py
        features.py
        baselines.py
        train.py
        evaluate.py
        visualize.py
    tests/
    reports/
        figures/
    models/
```

## Forecasting Approach (Overview)
- **Baselines:** Naive, seasonal-naive (7-day lag), moving average (7-day).
- **Machine Learning:** Random Forest regression with calendar, lag, and rolling-window features.
- **Validation:** Chronological train / validation / test split (no random shuffling).
- **Metrics:** MAE, RMSE.

## Current Status
- [x] Repository initialized
- [x] Directory structure and `.gitignore` set
- [x] Requirements documented
- [ ] Dataset acquired and inspected
- [ ] Data cleaning and EDA
- [ ] Baseline forecasts
- [ ] Feature engineering and leakage tests
- [ ] Machine Learning model and evaluation
- [ ] Final documentation and results

## Limitations and Future Improvements
- Forecast horizon is currently set to 14 days; could be adjusted.
- Feature engineering can be expanded with external economic indicators.
- Optional Streamlit dashboard may be added after core pipeline is complete.

## License
MIT (recommended — to be added in a future milestone).

---
*This project is a learning portfolio piece. All results are based on verified data only; no fabricated metrics are reported.*
