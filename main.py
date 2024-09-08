import math
from scipy.stats import norm

s = 42   # Spot price         = current market price of underlying asset
k = 40   # Strike price       = price option can be exercised for at expiration
t = 0.5   # Time to expiration = years until option expires and can be exercised
r = 0.1  # Risk-free rate     = return that can be make risk-free
v = 0.2   # Volatility         = standard deviation of the underlying asset's price

# Black-Scholes formula
d1 = (math.log(s / k) + (r + (v ** 2) / 2) * t) / (v * math.sqrt(t))
d2 = d1 - v * math.sqrt(t)
call_price = s * norm.cdf(d1) - k * math.exp(-r * t) * norm.cdf(d2)
put_price = k * math.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)

# Output
print("The value of d1 is: ", d1)
print("The value of d2 is: ", d2)
print("The price of the call option is: ", call_price)
print("The price of the put option is: ", put_price)
