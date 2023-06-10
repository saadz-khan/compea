import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectFromModel
from sklearn import metrics
from sklearn.metrics import mean_squared_error, r2_score

import keras
from keras.layers import Dense, LSTM, Dropout
from keras.models import Sequential
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping
from keras.utils import np_utils, to_categorical

import itertools
from scipy.stats import randint
from statsmodels.tsa.arima.model import ARIMA

try:
    df = pd.read_csv('household_power_consumption.csv')

except:
    df = pd.read_csv('household_power_consumption.txt', sep=';', 
		parse_dates={'dt' : ['Date', 'Time']}, infer_datetime_format=True, 
		low_memory=False, na_values=['nan','?'], index_col='dt')

def pre_process_data(df):
    droping_list_all=[]
    for j in range(0,7):
        if not df.iloc[:, j].notnull().all():
            droping_list_all.append(j)        
            #print(df.iloc[:,j].unique())
    droping_list_all
    # filling nan with mean in any columns

    for j in range(0,7):        
            df.iloc[:,j]=df.iloc[:,j].fillna(df.iloc[:,j].mean())

    # another sanity check to make sure that there are not more any nan
    df.isnull().sum()
    return df


def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	dff = pd.DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(dff.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(dff.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = pd.concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg


def resampling(df):
	## resampling of data over hour
	df_resample = df.resample('h').mean() 
	df_resample.shape
	## * Note: I scale all features in range of [0,1].

	## If you would like to train based on the resampled data (over hour), then used below
	values = df_resample.values 

	# normalize features
	scaler = MinMaxScaler(feature_range=(0, 1))
	scaled = scaler.fit_transform(values)
	# frame as supervised learning
	reframed = series_to_supervised(scaled, 1, 1)

	# drop columns we don't want to predict
	reframed.drop(reframed.columns[[8,9,10,11,12,13]], axis=1, inplace=True)
	print(reframed.head()) 
	return reframed, values, scaler


def split_and_normalize_data(df, train_ratio=0.8):
	# split into train and test sets
	values = reframed.values
	n_train_time = 365*24
	train = values[:n_train_time, :]
	test = values[n_train_time:, :]
	##test = values[n_train_time:n_test_time, :]
	# split into input and outputs
	train_X, train_y = train[:, :-1], train[:, -1]
	test_X, test_y = test[:, :-1], test[:, -1]
	# reshape input to be 3D [samples, timesteps, features]
	train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
	test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
	print(train_X.shape, train_y.shape, test_X.shape, test_y.shape) 
	# We reshaped the input into the 3D format as expected by LSTMs, namely [samples, timesteps, features].
	return train_X,train_y,test_X,test_y


def build_and_train_LSTM_model(train_X, train_y, test_X, test_y, window_size,scaler, learning_rate=0.001, epochs=2, batch_size=70):
	model = Sequential()
	model.add(LSTM(100, input_shape=(train_X.shape[1], train_X.shape[2])))
	model.add(Dropout(0.2))
	#model.add(LSTM(70))
	#model.add(Dropout(0.3))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')

	# fit network
	history = model.fit(train_X, train_y, epochs=epochs, batch_size=batch_size, validation_data=(test_X, test_y), verbose=2, shuffle=False)

	# summarize history for loss
	plt.figure(figsize=(25,10))
	plt.plot(history.history['loss'])
	plt.plot(history.history['val_loss'])
	plt.title('model loss')
	plt.ylabel('loss')
	plt.xlabel('epoch')
	plt.legend(['train', 'test'], loc='upper right')
	plt.show()

	# make a prediction
	yhat = model.predict(test_X)
	test_X = test_X.reshape((test_X.shape[0], 7))
	# invert scaling for forecast
	inv_yhat = np.concatenate((yhat, test_X[:, -6:]), axis=1)
	inv_yhat = scaler.inverse_transform(inv_yhat)
	inv_yhat = inv_yhat[:,0]
	# invert scaling for actual
	test_y = test_y.reshape((len(test_y), 1))
	inv_y = np.concatenate((test_y, test_X[:, -6:]), axis=1)
	inv_y = scaler.inverse_transform(inv_y)
	inv_y = inv_y[:,0]
	# calculate RMSE
	rmse = np.sqrt(mean_squared_error(inv_y, inv_yhat))
	print('Test RMSE: %.3f' % rmse)
	aa=[x for x in range(200)]
	plt.figure(figsize=(25,10))
	plt.plot(aa, inv_y[:200], marker='.', label="actual")
	plt.plot(aa, inv_yhat[:200], 'r', label="prediction")
	plt.ylabel('Global_active_power', size=15)
	plt.xlabel('Time step', size=15)
	plt.legend(fontsize=15)
	plt.show()
	return model,history,inv_y,inv_yhat


def forecast(df):
	# Resample the data to daily frequency
	daily_data = df.resample('D').sum()

	# Split the data into train and test sets
	train_size = int(len(daily_data) * 0.8)
	train, test = daily_data[0:train_size], daily_data[train_size:]

	# Fit the ARIMA model
	model = ARIMA(train['Global_active_power'], order=(3,1,2))
	model_fit = model.fit()

	# Forecast for the next two days
	forecast = model_fit.forecast(steps=2)

	# concatenate train and test indices
	index = pd.concat([train.index.to_series(), test.index.to_series()])

	# concatenate train and test Global_active_power columns
	global_active_power = pd.concat([train['Global_active_power'], test['Global_active_power']])

	# create a new DataFrame with the concatenated indices and Global_active_power columns
	df = pd.DataFrame({'index': index, 'Global_active_power': global_active_power})

	df.to_csv('predictions.csv', index=False)

	plt.plot(train.index, train['Global_active_power'], label='Training Data')
	plt.plot(test.index, test['Global_active_power'], label='Forecast')
	pd.DataFrame()
	#plt.plot(forecast.index, forecast, label='Forecast')
	plt.xlabel('Date')
	plt.ylabel('Global Active Power (kilowatts)')
	plt.title('Global Active Power Forecast')


	plt.legend()
	plt.show()

# Pre-process data
df = pre_process_data(df)

# Resample and normalize data
reframed, values, scaler = resampling(df)

# Split data into train and test sets
train_X, train_y, test_X, test_y = split_and_normalize_data(reframed)

# Build and train LSTM model
model, history, inv_y, inv_yhat = build_and_train_LSTM_model(train_X, train_y, test_X, test_y, 1, scaler)

# Forecast Global Active Power
forecast(df)