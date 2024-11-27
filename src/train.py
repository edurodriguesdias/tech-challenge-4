from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import numpy as np
import yfinance as yf
import pandas as pd
import joblib
import pickle

def create_dataset(data, time_step=60):
    X, y = [], []
    for i in range(time_step, len(data)):
        X.append(data[i-time_step:i, 0])  
        y.append(data[i, 0])              
    return np.array(X), np.array(y)



def data_preparation(ticker):
    start_date = '2018-01-01'
    end_date = '2024-07-20'

    df = yf.download(ticker, start=start_date, end=end_date)

    df = df[['Close']]

    scaler = MinMaxScaler(feature_range=(0, 1))

    scaled_data = scaler.fit_transform(df[['Close']])

    pickle.dump(scaled_data,open("src/data/scaled_data.pkl","wb"))

    time_step = 60
    X, y = create_dataset(scaled_data, time_step)

    X = X.reshape(X.shape[0], X.shape[1], 1)

    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    return X_train,X_test,y_train,y_test,scaler

def train_model(ticker):

    X_train,X_test,y_train,y_test,scaler = data_preparation(ticker)

    model = Sequential()

    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))  

    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(X_train, y_train, epochs=10, batch_size=32)

    model.save(f'data/{ticker}_modelo.h5')
    joblib.dump(scaler, f'data/{ticker}_scaler.pkl')  
    print(f"Modelo para {ticker} salvo.")

def generate(tickers):
    for ticker in tickers:
        train_model(ticker)

tickers = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'ABEV3.SA']
generate(tickers)