# Dataset: Kaggle — Store Sales — Time Series Forecasting

This project uses the **Store Sales — Time Series Forecasting** competition
dataset from Kaggle. It contains daily grocery sales for Corporación Favorita
(Ecuador), broken down by store and product family.

- Competition page: <https://www.kaggle.com/competitions/store-sales-time-series-forecasting>
- Data page: <https://www.kaggle.com/competitions/store-sales-time-series-forecasting/data>

## Why this dataset

- Real, widely used retail sales data with genuine temporal structure
  (weekly seasonality, holidays, promotions).
- Small enough to run on a laptop but rich enough to demonstrate calendar,
  lag and rolling features.
- Well documented, which makes the results easy to interpret and defend.

## How to download (manual step)

The dataset is **not** stored in this repository (see *Terms and attribution*
below). To reproduce the project you must download it yourself:

1. Create a free Kaggle account: <https://www.kaggle.com/account/login>.
2. Open the competition **Data** tab and click **Join Competition**, then
   accept the competition rules. Downloading the files requires this step.
3. Download the data (either the "Download All" button or the individual
   CSVs) and extract it.
4. Place these files directly inside `data/raw/`:

   ```
   data/raw/train.csv
   data/raw/test.csv
   data/raw/stores.csv
   data/raw/transactions.csv
   data/raw/oil.csv
   data/raw/holidays_events.csv
   ```

5. Confirm the files are present by running:

   ```powershell
   python -m src.data_loader
   ```

   You should see the available files listed and a row/column summary for
   each table. If a required file is missing, the command raises a clear
   error telling you what to download.

### Optional: Kaggle CLI

If you prefer the command line, install the Kaggle API
(`pip install kaggle`), save your API token as described in the
[Kaggle API docs](https://www.kaggle.com/docs/api), accept the competition
rules, then run:

```powershell
kaggle competitions download -c store-sales-time-series-forecasting -p data/raw
```

The download is a zip; extract it so the CSVs sit directly in `data/raw/`.

## Expected schema (to be verified after download)

The following is the documented structure. It is treated as an expectation
until `python -m src.data_loader` is run against the real files and the
output is recorded.

| File | Columns (expected) |
|------|--------------------|
| `train.csv` | `id`, `date`, `store_nbr`, `family`, `sales`, `onpromotion` |
| `test.csv` | `id`, `date`, `store_nbr`, `family`, `onpromotion` |
| `stores.csv` | `store_nbr`, `city`, `state`, `type`, `cluster` |
| `transactions.csv` | `date`, `store_nbr`, `transactions` |
| `oil.csv` | `date`, `dcoilwtico` |
| `holidays_events.csv` | `date`, `type`, `locale`, `locale_name`, `description`, `transferred` |

- **Target:** `sales` (units sold for a given store/family/date).
- **Granularity:** daily.
- **Documented training range:** 2013-01-01 to 2017-08-31 (verify on download).

## Terms and attribution

- The dataset is provided by Kaggle for the competition and is subject to the
  competition rules and Kaggle's terms of use.
- **Do not redistribute the raw CSVs** in this repository. `data/raw/` is
  excluded via `.gitignore`; only this documentation is committed.
- Cite the competition when presenting results:

  > Kaggle. *Store Sales — Time Series Forecasting*.
  > <https://www.kaggle.com/competitions/store-sales-time-series-forecasting>

## Verification status

- [ ] Real files downloaded to `data/raw/`
- [ ] `python -m src.data_loader` run and output recorded
- [ ] Schema, date range and row counts confirmed against the expectations above
