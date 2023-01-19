import pandas as pd
import yfinance as yf
from keras.layers import Dense
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# download the stock prices for Yahoo
stock_data = yf.download("SPY")

# split into input (X) and output (y) variables
X = stock_data.drop(columns=["Close"])
y = stock_data["Close"]

# split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# https://www.youtube.com/watch?v=fhBw3j_O9LE

# scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# define the model
model = Sequential()
model.add(Dense(12, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='linear'))

# compile the model
model.compile(loss='mean_squared_error', optimizer='adam')

# fit the model to the training data
model.fit(X_train, y_train, epochs=150, batch_size=10)
