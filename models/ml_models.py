import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def preprocess_data(df):
    """Preprocesses the transaction data for ML models."""
    df['date'] = pd.to_datetime(df['date'])
    
    # Feature Engineering
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['hour'] = df['date'].dt.hour if 'hour' in df['date'].dt.__dict__ else 0 # Handle date only

    # Define categorical and numerical features
    categorical_features = ['merchant', 'city', 'txn_type', 'payment_method']
    numerical_features = ['amount', 'day_of_week', 'month', 'hour']

    # Create preprocessing pipelines for both numerical and categorical data
    numerical_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    return preprocessor, df

def detect_anomalies(df):
    """Detects anomalies using Isolation Forest."""
    preprocessor, df_processed = preprocess_data(df.copy())
    
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', IsolationForest(contamination=0.01, random_state=42))])
    
    pipeline.fit(df_processed)
    df['anomaly_score'] = pipeline.decision_function(df_processed)
    df['is_anomaly'] = pipeline.predict(df_processed)
    df['is_anomaly'] = df['is_anomaly'].apply(lambda x: 'Yes' if x == -1 else 'No')
    
    return df[df['is_anomaly'] == 'Yes']

def segment_users(df):
    """Segments users using KMeans clustering."""
    preprocessor, df_processed = preprocess_data(df.copy())
    
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('clusterer', KMeans(n_clusters=4, random_state=42, n_init=10))])
    
    pipeline.fit(df_processed)
    df['segment'] = pipeline.predict(df_processed)
    
    return df

def detect_fraud_rules(df):
    """Detects potential fraud based on simple rules."""
    # Rule 1: High amount transactions
    df['fraud_signal'] = (df['amount'] > 4000)
    
    # Rule 2: Multiple transactions in a short period (placeholder)
    # In a real scenario, this would require more complex logic
    
    return df[df['fraud_signal'] == True]

def train_forecasting_model(df):
    """Trains a simple linear regression model for spend forecasting."""
    from sklearn.linear_model import LinearRegression
    
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_year'] = df['date'].dt.dayofyear
    
    daily_spend = df.groupby('day_of_year')['amount'].sum().reset_index()
    
    X = daily_spend[['day_of_year']]
    y = daily_spend['amount']
    
    model = LinearRegression()
    model.fit(X, y)
    
    return model
