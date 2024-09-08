# Black-Scholes Option Pricing Model

This script calculates the price of European call and put options, using either the Black-Scholes formula or the binomial pricing model.

## Variables

- **s**: Spot price (current market price of the underlying asset) = 42
- **k**: Strike price (price at which the option can be exercised) = 40
- **t**: Time to expiration (in years) = 0.5
- **r**: Risk-free rate (annualized) = 0.1
- **v**: Volatility (standard deviation of the underlying asset's price) = 0.2

## Pricing models

### Black-Scholes Formula

The Black-Scholes formula calculates the price of a European call and put option.

#### Formula for \(d_1\) and \(d_2\):

$$
d_1 = \frac{\ln(\frac{s}{k}) + (r + \frac{v^2}{2}) \cdot t}{v \cdot \sqrt{t}}
$$

$$
d_2 = d_1 - v \cdot \sqrt{t}
$$

Where:

- \(s\) is the spot price
- \(k\) is the strike price
- \(t\) is the time to expiration
- \(r\) is the risk-free interest rate
- \(v\) is the volatility (standard deviation of returns)

#### Call Option Price:

$$
C = s \cdot N(d_1) - k \cdot e^{-rt} \cdot N(d_2)
$$

Where:

- \(N(d_1)\) and \(N(d_2)\) are the cumulative distribution functions of the standard normal distribution.

#### Put Option Price:

$$
P = k \cdot e^{-rt} \cdot N(-d_2) - s \cdot N(-d_1)
$$

### Binomial Pricing Model

