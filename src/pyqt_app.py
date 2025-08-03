import sys
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QFileDialog, QLabel, QTableView, QHeaderView, QMessageBox)
from PyQt5.QtCore import QAbstractTableModel, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from ml_models import detect_anomalies, segment_users, detect_fraud_rules, train_forecasting_model

class PandasModel(QAbstractTableModel):
    """A model to interface a pandas DataFrame with QTableView."""
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Smart Transaction Insight Dashboard'
        self.left = 100
        self.top = 100
        self.width = 1200
        self.height = 800
        self.df = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QVBoxLayout()

        self.load_button = QPushButton('Load CSV File', self)
        self.load_button.clicked.connect(self.load_csv)
        layout.addWidget(self.load_button)

        self.run_ml_button = QPushButton('Run ML Analysis', self)
        self.run_ml_button.clicked.connect(self.run_ml_analysis)
        self.run_ml_button.setEnabled(False)
        layout.addWidget(self.run_ml_button)

        self.table_view = QTableView()
        layout.addWidget(self.table_view)

        self.plot_canvas = FigureCanvas(Figure(figsize=(15, 10)))
        layout.addWidget(self.plot_canvas)

        self.setLayout(layout)
        self.show()

    def load_csv(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            self.df = pd.read_csv(fileName)
            model = PandasModel(self.df.head())
            self.table_view.setModel(model)
            self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.run_ml_button.setEnabled(True)
            self.plot_basic_dashboard()

    def plot_basic_dashboard(self):
        self.plot_canvas.figure.clear()
        
        # Merchant Spend
        ax1 = self.plot_canvas.figure.add_subplot(221)
        merchant_spend = self.df[self.df['txn_type'] == 'DEBIT'].groupby('merchant')['amount'].sum().sort_values(ascending=False)
        merchant_spend.plot(kind='bar', ax=ax1)
        ax1.set_title('Spend by Merchant')
        ax1.tick_params(axis='x', rotation=45)

        # Daily Spend
        ax2 = self.plot_canvas.figure.add_subplot(222)
        self.df['date'] = pd.to_datetime(self.df['date'])
        daily_spend = self.df[self.df['txn_type'] == 'DEBIT'].groupby('date')['amount'].sum()
        daily_spend.plot(kind='line', ax=ax2)
        ax2.set_title('Daily Spend')
        ax2.tick_params(axis='x', rotation=45)

        # Payment Method
        ax3 = self.plot_canvas.figure.add_subplot(223)
        payment_methods = self.df['payment_method'].value_counts()
        payment_methods.plot(kind='pie', ax=ax3, autopct='%1.1f%%')
        ax3.set_title('Payment Method Usage')
        ax3.set_ylabel('')

        self.plot_canvas.figure.tight_layout()
        self.plot_canvas.draw()

    def run_ml_analysis(self):
        if self.df is not None:
            # Anomaly Detection
            anomalies = detect_anomalies(self.df.copy())
            QMessageBox.information(self, "Anomalies", f"Found {len(anomalies)} anomalous transactions.")
            self.show_data_in_new_window(anomalies, "Anomalous Transactions")

            # User Segmentation
            segmented_df = segment_users(self.df.copy())
            self.show_data_in_new_window(segmented_df, "User Segments")

            # Fraud Signals
            fraud_signals = detect_fraud_rules(self.df.copy())
            QMessageBox.information(self, "Fraud Signals", f"Found {len(fraud_signals)} transactions with fraud signals.")
            self.show_data_in_new_window(fraud_signals, "Fraudulent Transactions")
            
            # Forecasting
            self.plot_forecast()

    def show_data_in_new_window(self, df, title):
        win = QWidget()
        win.setWindowTitle(title)
        layout = QVBoxLayout()
        table = QTableView()
        model = PandasModel(df)
        table.setModel(model)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(table)
        win.setLayout(layout)
        win.show()
        # Keep a reference to the window
        setattr(self, f"{title.replace(' ', '_')}_window", win)

    def plot_forecast(self):
        forecasting_model = train_forecasting_model(self.df.copy())
        future_days = np.array(range(1, 366))[-30:].reshape(-1, 1)
        predictions = forecasting_model.predict(future_days)
        
        ax4 = self.plot_canvas.figure.add_subplot(224)
        ax4.plot(future_days, predictions, label="Forecasted Spend")
        ax4.set_xlabel("Day of Year")
        ax4.set_ylabel("Predicted Spend")
        ax4.set_title("Spend Forecast (Next 30 Days)")
        ax4.legend()
        self.plot_canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
