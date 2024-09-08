# Options Pricing Calculator

This script calculates the price of European call and put options, using either the Black-Scholes formula or the binomial pricing model.
The models are based on the book "Options, Futures, and Other Derivatives" by John C. Hull (5th edition).

## Variables

- **s**: Spot price (current market price of the underlying asset)
- **k**: Strike price (price at which the option can be exercised)
- **t**: Time to expiration (in years)
- **r**: Risk-free rate (annualized), set as the current 10-year US Treasury yield by default, obtained from the alpha-vantage API
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

The binomial pricing model calculates the price of European call and put options using a binomial tree approach.

#### Steps:

1. **Set Up the Binomial Tree:**
    - **Number of Time Steps (n):** Defines the depth of the tree.
    - **Time Step Length (dt):** Time per step, calculated as \( \frac{t}{n} \).
    - **Up Factor (u):** Represents the factor by which the asset price increases in one time step, calculated as \( e^{v \cdot \sqrt{dt}} \).
    - **Down Factor (d):** Represents the factor by which the asset price decreases in one time step, calculated as \( e^{-v \cdot \sqrt{dt}} \).
    - **Risk-Neutral Probability (q):** Probability of an up move under the risk-neutral measure, calculated as \( \frac{e^{r \cdot dt} - d}{u - d} \).
    - **Discount Factor (disc):** Factor to discount future values to present value, calculated as \( e^{-r \cdot dt} \).

2. **Initialize Asset Prices at Maturity:**
    - Compute all possible asset prices at the option's maturity based on different paths through the tree.

3. **Initialize Option Values at Maturity:**
    - Compute the option values at maturity for call and put options based on the asset prices.

4. **Step Backwards Through the Tree:**
    - For each time step, calculate the option values by taking the risk-neutral expected value of the option values at the next step and discounting it to the current step.

#### Call Option Price:

$$
C = Discount Factor \times ( q \cdot \text{Call Value} + (1 - q) \cdot \text{Call Value}_{\text{down}})
$$

#### Put Option Price:

$$
P = Discount Factor \times ( q \cdot \text{Put Value}_{\text{up}} \plus (1 - q) \cdot \text{Put Value}_{\text{down}})
$$