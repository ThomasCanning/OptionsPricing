import math
import numpy as np
from scipy.stats import norm


class PricingModels:

    def __init__(self):
        self.s = None
        self.k = None
        self.t = None
        self.r = None
        self.v = None

    def update_parameters(self, s, k, t, r, v):
        self.s = s
        self.k = k
        self.t = t
        self.r = r
        self.v = v

    def calculate_black_scholes(self):
        s, k, t, r, v = self.s, self.k, self.t, self.r, self.v

        d1 = (math.log(s / k) + (r + (v ** 2) / 2) * t) / (v * math.sqrt(t))
        d2 = d1 - v * math.sqrt(t)
        call_price = s * norm.cdf(d1) - k * math.exp(-r * t) * norm.cdf(d2)
        put_price = k * math.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)

        return call_price, put_price

    def calculate_binomial(self):
        s, k, t, r, v = self.s, self.k, self.t, self.r, self.v

        n = 1000  # Number of time steps = depth of binomial tree

        dt = t / n
        u = np.exp(v * np.sqrt(dt))  # Up factor = factor by which the underlying asset price increases
        d = np.exp(-v * np.sqrt(dt))  # Down factor = factor by which the underlying asset price decreases
        q = (np.exp(r * dt) - d) / (u - d)
        disc = np.exp(-r * dt)

        # Initialize asset prices at maturity
        asset_prices = s * d ** np.arange(n, -1, -1) * u ** np.arange(0, n + 1, 1)

        # Initialize option values at maturity
        call_values = np.maximum(asset_prices - k, 0)
        put_values = np.maximum(k - asset_prices, 0)

        # Step backwards through the tree
        for i in range(n, 0, -1):
            call_values = disc * (q * call_values[1:i + 1] + (1 - q) * call_values[0:i])
            put_values = disc * (q * put_values[1:i + 1] + (1 - q) * put_values[0:i])

        call_price = call_values[0]
        put_price = put_values[0]

        return call_price, put_price
