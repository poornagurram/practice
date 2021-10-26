import pandas as pd
from matplotlib import pyplot
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

data = pd.read_csv("auto_fuel.csv")


#Missing values across columns are as follows
print(data.isna().sum())

# Plots to check the distribution of features
for i in data.columns[:-1]:
    pyplot.hist(data[i], label=i)
    pyplot.savefig(f"{i}")
    pyplot.clf()

# Impute missing data with mean
data['horsepower'] = data['horsepower'].fillna(data['horsepower'].mean())
data['weight'] = data['weight'].fillna(data['weight'].mean())
data['cylinders'] = data['cylinders'].fillna(data['cylinders'].mean())
data['displacement'] = data['displacement'].fillna(data['displacement'].mean())

# Features
X = data.drop('mpg', axis=1)
# Target Variable
y = data['mpg']

# Divide the training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Normalize the data using standard scaler
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)

# Metrics being used to measure are mean_absolute_error [lesser the better], r2_score [best possible score is 1,
# negative is due to bad performance]

best_model = ""
max_mae = 2147483647 # INT_MAX
max_reg_score = -2147483648 # INT_MIN
best_degree = None
# considering 1,2,3,4,5 degree features
for deg in range(1, 5):
    poly_feat = PolynomialFeatures(degree=deg)
    X_train = poly_feat.fit_transform(X_train, y_train)
    X_test = poly_feat.fit_transform(X_test, y_test)

    reg_model = LinearRegression()
    reg_model.fit(X_train, y_train)
    y_pred = reg_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2s = r2_score(y_test, y_pred)
    if max_mae > mae and max_reg_score < r2s:
        max_mae = mae
        max_reg_score = r2s
        best_model = reg_model
        best_degree = deg
    print(f"for degree {deg} the mean absolute error is  {mae}")
    print(f"for degree {deg} the regression score is {r2s}")

# We can see that degree 2 is performing the best with the scores
# mean absolute error is  2.756251124667085 [lesser is better]
# regression score is  0.7557990710267817 [nearer to 1 is better]

print(f"Best degree is {best_degree} with metrics MAE: {max_mae} Regression Score: {max_reg_score}")

