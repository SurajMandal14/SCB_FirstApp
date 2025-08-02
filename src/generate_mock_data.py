# import pandas as pd
# import numpy as np
# import random
# from datetime import datetime, timedelta

# # Configuration
# NUM_ROWS = 5000
# MERCHANTS = ['Amazon', 'Swiggy', 'Flipkart', 'IRCTC', 'Zomato', 'Myntra', 'BigBasket', 'Uber', 'Ola']
# CITIES = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
# TXN_TYPES = ['DEBIT', 'CREDIT']
# PAYMENT_METHODS = ['UPI', 'Card', 'Netbanking']

# def generate_mock_data():
#     """Generates a mock transaction dataset."""
#     data = []
#     start_date = datetime(2022, 1, 1)

#     for i in range(NUM_ROWS):
#         transaction_id = f"TXN{i+1:004}"
#         user_id = f"U{random.randint(1, 100):003}"
#         date = start_date + timedelta(days=random.randint(0, 365*2))
#         amount = round(random.uniform(10.0, 5000.0), 2)
#         merchant = random.choice(MERCHANTS)
#         city = random.choice(CITIES)
#         txn_type = random.choice(TXN_TYPES)
#         payment_method = random.choice(PAYMENT_METHODS)

#         data.append([
#             transaction_id,
#             user_id,
#             date.strftime('%Y-%m-%d'),
#             amount,
#             merchant,
#             city,
#             txn_type,
#             payment_method
#         ])

#     df = pd.DataFrame(data, columns=[
#         'transaction_id', 'user_id', 'date', 'amount', 'merchant',
#         'city', 'txn_type', 'payment_method'
#     ])
#     return df

# if __name__ == "__main__":
#     mock_df = generate_mock_data()
#     # Save to data directory
#     mock_df.to_csv('data/mock_transactions.csv', index=False)
#     print(f"Generated mock data with {NUM_ROWS} rows and saved to data/mock_transactions.csv")
