from scipy.stats import lognorm
from scipy import stats as st
from math import log, sqrt, e
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('WebAgg')


def get_dist_params(mu_x, sig_x):
    mu_dist = log(mu_x**2/sqrt(mu_x**2+sig_x**2))
    sig_dist = sqrt(log(1+sig_x**2/mu_x**2))
    return mu_dist, sig_dist


if __name__ == '__main__':
    mu_dist, sig_dist = get_dist_params(45, 10)
    vals = lognorm.rvs(sig_dist, scale=e**mu_dist, size=100)
    print(f"95% confidence interval: {st.t.interval(alpha=0.95, df=len(vals) - 1, loc=vals.mean(), scale=st.sem(vals))}")
    print(f"mean {vals.mean()}, standard deviation : {vals.std()}")
    plt.hist(vals, 15)
    plt.show()
