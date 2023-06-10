import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam

# Final training_eval.py
def preprocess_data(df):
    df = df[['DATE_TIME', 'DC_POWER', 'AC_POWER', 'AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION', 'DAILY_YIELD']]
    df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'])
    df.set_index('DATE_TIME', inplace=True)
    df.dropna(inplace=True) 
    return df


def split_and_normalize_data(df, train_ratio=0.8):
    train_size = int(len(df) * train_ratio)
    train_data = df[:train_size].values
    test_data = df[train_size:].values

    scaler = MinMaxScaler(feature_range=(0, 1))
    train_data = scaler.fit_transform(train_data)
    test_data = scaler.transform(test_data)

    return train_data, test_data, scaler

def create_dataset(data, window_size):
    X = []
    y = []
    for i in range(window_size, len(data)):
        X.append(data[i-window_size:i])
        y.append(data[i, -1])
    return np.array(X), np.array(y)

def build_and_train_lstm_model(train_X, train_y, test_X, test_y, window_size, learning_rate=0.001, epochs=50, batch_size=32):
    model = Sequential()
    model.add(LSTM(units=50, input_shape=(window_size, train_X.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    optimizer = Adam(learning_rate=learning_rate)
    model.compile(loss='mean_squared_error', optimizer=optimizer)

    history = model.fit(train_X, train_y, epochs=epochs, batch_size=batch_size, validation_data=(test_X, test_y), verbose=1)
    
    return model, history

def plot_predicted_vs_actual(test_X, test_y, test_pred, df, train_size, window_size, scaler, future_df=None):
    test_pred = scaler.inverse_transform(np.concatenate((test_X[:, -1, :-1], test_pred), axis=1))[:, -1]
    test_y = scaler.inverse_transform(np.concatenate((test_X[:, -1, :-1], test_y.reshape(-1, 1)), axis=1))[:, -1]

    test_df = pd.DataFrame({'DATE_TIME': df.index[train_size + window_size:], 'Predicted': test_pred, 'Actual': test_y})
    test_df.set_index('DATE_TIME', inplace=True)

    plt.figure(figsize=(15, 5))
    plt.plot(test_df.index, test_df['Predicted'], label='Predicted')
    plt.plot(test_df.index, test_df['Actual'], label='Actual')
    if future_df is not None:
        plt.plot(future_df.index, future_df['Predicted'], label='Future Predicted')
    plt.title('Predicted vs Actual Daily Yield')
    plt.xlabel('Date')
    plt.ylabel('Daily Yield')
    plt.legend()
    plt.show()


def train_and_evaluate():
    # Preprocess data
    df = pd.read_csv('final_data.csv')
    df = preprocess_data(df)

    # Split and normalize data
    train_data, test_data, scaler = split_and_normalize_data(df)

    # Create windowed dataset
    window_size = 24
    train_X, train_y = create_dataset(train_data, window_size)
    test_X, test_y = create_dataset(test_data, window_size)

    # Build and train LSTM model
    model, history = build_and_train_lstm_model(train_X, train_y, test_X, test_y, window_size)

    # Make predictions on test data
    test_pred = model.predict(test_X)

    # Create test_df DataFrame
    train_size = int(len(df) * 0.8)
    test_pred_transformed = scaler.inverse_transform(np.concatenate((test_X[:, -1, :-1], test_pred), axis=1))[:, -1]
    test_y_transformed = scaler.inverse_transform(np.concatenate((test_X[:, -1, :-1], test_y.reshape(-1, 1)), axis=1))[:, -1]
    test_df = pd.DataFrame({'DATE_TIME': df.index[train_size + window_size:], 'Predicted': test_pred_transformed, 'Actual': test_y_transformed})
    test_df.set_index('DATE_TIME', inplace=True)

    # Get the last 24 hours of the test data
    last_24_hours = df[-96:]

    # Normalize the last 24 hours of the test data
    last_24_hours = scaler.transform(last_24_hours)

    # Create a windowed dataset with a window size of 24
    future_X, _ = create_dataset(last_24_hours, window_size)

    # Make predictions on the future dataset
    future_pred = model.predict(future_X)

    # Inverse transform the predictions to get the original values
    future_pred = scaler.inverse_transform(np.concatenate((future_X[:, -1, :-1], future_pred), axis=1))[:, -1]

    # Create a datetime range for the next day with the same frequency as the data
    date_range = pd.date_range(start=df.index[-1], periods=96, freq='15min')

    # Create a new date range with a smaller number of periods
    future_range = pd.date_range(start=date_range[-1], periods=len(future_pred)+1, freq='15min')[1:]

    # Create a dataframe with the predicted values and the datetime range
    future_df = pd.DataFrame({'DATE_TIME': future_range, 'Predicted': future_pred})
    future_power_generation = future_df['Predicted'].sum()
    
    # Set DATE_TIME as index
    future_df.set_index('DATE_TIME', inplace=True)

    # Concatenate the two dataframes
    future_df_fin = pd.concat([test_df.tail(1), future_df], axis=0)
    another_df = pd.concat ([test_df, future_df], axis=0)
    
    # Plot the results
    plot_predicted_vs_actual(test_X, test_y, test_pred, df, train_size, window_size, scaler, future_df=future_df_fin)

    # Add a new column 'col3' with None values (or any other desired default value)
    another_df['Forecast'] = np.NaN

    # Set the zero index value of the new column to the single value variable
    another_df.loc[0, 'Forecast'] = future_power_generation
    another_df.to_csv('predictions.csv')

    future_df_fin.to_csv('future_predictions.csv')

    return test_df, test_pred, future_df_fin

test_df, test_pred, future_df = train_and_evaluate()