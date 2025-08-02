# Smart Transaction Insight Dashboard

This project provides a tool for analyzing transaction data, with both a web-based UI (Streamlit) and a desktop UI (PyQt5).

## Features

- **Upload CSV:** Load your own transaction data.
- **Basic Dashboard:** Visualize total spend, merchant-wise spend, and daily trends.
- **ML Insights:**
  - **Anomaly Detection:** Identify unusual transactions using Isolation Forest.
  - **User Segmentation:** Group users into segments using KMeans clustering.
  - **Fraud Detection:** Flag transactions based on predefined rules.
  - **Spend Forecasting:** Predict future spending using a simple linear regression model.
- **Download Reports:** Save the analysis results.

## How the Magic Works: A Simple Guide to the ML Models

Imagine you have a big box of transaction receipts. Our program is like a super-smart detective that reads all of them and tells you interesting things. Here’s how it does it, explained simply.

### 1. Getting the Data Ready (`preprocess_data`)
*   **What it does:** Before the detective can start, it needs to organize the receipts. It reads the date, the amount, the store name, etc., and turns them into a simple language of numbers that the computer can understand easily.
*   **Analogy:** It’s like turning a messy pile of colorful LEGO bricks into neat stacks of red, blue, and yellow bricks. It makes the next steps much easier.

### 2. Finding the Odd Ones Out (Anomaly Detection with `IsolationForest`)
*   **What it does:** This part looks for transactions that are really weird compared to all the others.
*   **Analogy:** Imagine playing a game of "Odd One Out". If everyone usually spends about ₹100 on snacks, but suddenly one receipt shows someone spent ₹10,000 on a single snack, the detective says, "Hey, this one is really different!" It *isolates* the weird ones from the normal ones. This is how it finds potential problems or **anomalies**.

### 3. Sorting Users into Groups (User Segmentation with `KMeans`)
*   **What it does:** This part looks at all the users and sorts them into different groups based on how they shop.
*   **Analogy:** Imagine you have a bunch of stickers. You decide to sort them. You put all the big, shiny stickers in one pile, all the small, animal stickers in another, and all the car stickers in a third. Our program does the same thing with users. It might create groups like:
    *   **"Big Spenders":** People who buy expensive things.
    *   **"Daily Shoppers":** People who buy something almost every day.
    *   **"Online Foodies":** People who mostly buy from Zomato and Swiggy.
*   This helps in understanding the different kinds of customers.

### 4. Checking for Simple Fraud Rules (`detect_fraud_rules`)
*   **What it does:** This is the simplest check. It just looks for things that we've told it are definitely suspicious.
*   **Analogy:** It’s like having a rule that says, "If you see anyone trying to buy 100 ice creams at once, tell me immediately!" In our code, the rule is simple: "If a transaction is for more than ₹4000, flag it as a potential **fraud signal**."

### 5. Guessing the Future (Forecasting with `LinearRegression`)
*   **What it does:** This part tries to predict how much money will be spent in the future.
*   **Analogy:** Imagine you've been getting 1 inch taller every year. Your friend could guess that next year, you'll be another inch taller. The program does something similar. It looks at the spending pattern from the past and draws a straight line to guess what the spending might look like in the next few days.

## Folder Structure

```
.
├── data/
│   └── mock_transactions.csv
├── models/
│   └── ml_models.py
├── src/
│   └── generate_mock_data.py
├── ui/
│   └── pyqt_app.py
├── outputs/
├── streamlit_app.py
├── requirements.txt
└── README.md
```

## How to Run

### 1. Setup a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate Mock Data (Optional)

If you don't have your own data, you can generate a mock dataset.

```bash
python src/generate_mock_data.py
```
This will create `mock_transactions.csv` in the `data` directory.

### 4. Run the Streamlit Web App

```bash
streamlit run streamlit_app.py
```

### 5. Run the PyQt5 Desktop App

```bash
python ui/pyqt_app.py
```

## How to Package into an Executable (.exe)

You can use PyInstaller to package both the Streamlit and PyQt5 applications into standalone executables.

### Packaging the PyQt5 App

This is the more straightforward of the two.

```bash
pyinstaller --onefile --windowed --name "TransactionDashboard" ui/pyqt_app.py
```

- `--onefile`: Creates a single executable file.
- `--windowed`: Prevents the console window from appearing.
- `--name`: Sets the name of the executable.

The executable will be located in the `dist` folder.

### Packaging the Streamlit App

Packaging a Streamlit app is more complex because it runs as a web server. A common approach is to wrap the Streamlit command in a batch or shell script and then package that script.

**1. Create a runner script (e.g., `run_streamlit.bat` on Windows):**

```batch
@echo off
streamlit run streamlit_app.py
```

**2. Package the script with PyInstaller:**

```bash
pyinstaller --onefile --name "TransactionDashboardWeb" run_streamlit.bat
```

This will create an executable that, when run, will start the Streamlit server and should open the application in the default web browser. Note that this method can sometimes be tricky and may require additional configuration depending on the system.
