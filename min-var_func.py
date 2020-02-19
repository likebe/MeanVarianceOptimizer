from __future__ import division
import numpy as np
from scipy.optimize import minimize
import pandas as pd
import pandas_datareader as web
import xlrd
import statsmodels.stats.moment_helpers as models


# calculate portfolio variance
def calculate_portfolio_var(w,V):
	w = np.matrix(w)
	return np.sqrt(w*V*w.T)*np.sqrt(252)


# the min-var optimization tool
def min_var(V, method = 'SLSQP'):

	""" takes in a covariance matrix and returns a vector of weights"""

	V = np.matrix(V)
	size = V.shape[0]
	# have an initial guess of the weight
	init_guess = np.ones(size) * (1.0 / size)

	# constrained portfolio variance minimizer
	bounds = ((0.0, 1.0),) * size
	cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0})
	res = minimize(calculate_portfolio_var, init_guess, args=V, method=method, constraints=cons, bounds=bounds)

	w_g = res.x
	print('Optimal Portfolio weights are: ' + np.array2string(w_g))
	return w_g


if __name__ == '__main__':
	data = pd.read_excel('covar.xlsx', header=0, index_col=0)
	header = list(data.columns)
	#data = pd.read_excel('test.xlsx', header = None)
	print(data)
	min_var(data)
	#data = models.cov2corr(data, return_std=True)
	#print(data)

