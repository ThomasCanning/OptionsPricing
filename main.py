import tkinter as tk
import math
import numpy as np
from scipy.stats import norm


class OptionsPriceCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Options Price Calculator")

        self.create_widgets()

    def create_widgets(self):

        # Spot Price text entry
        tk.Label(self.root, text="Spot Price:").grid(row=0, column=0)
        self.spot_price_entry = tk.Entry(self.root)
        self.spot_price_entry.grid(row=0, column=1, columnspan=2)

        # Strike Price text entry
        tk.Label(self.root, text="Strike Price:").grid(row=1, column=0)
        self.strike_price_entry = tk.Entry(self.root)
        self.strike_price_entry.grid(row=1, column=1, columnspan=2)

        # Time to Expiration text entry
        tk.Label(self.root, text="Time to Expiration:").grid(row=2, column=0)
        self.time_to_expiration_entry = tk.Entry(self.root)
        self.time_to_expiration_entry.grid(row=2, column=1, columnspan=2)

        # Risk-Free Rate text entry
        tk.Label(self.root, text="Risk-Free Rate:").grid(row=3, column=0)
        self.risk_free_rate_entry = tk.Entry(self.root)
        self.risk_free_rate_entry.grid(row=3, column=1, columnspan=2)

        # Volatility text entry
        tk.Label(self.root, text="Volatility:").grid(row=4, column=0)
        self.volatility_entry = tk.Entry(self.root)
        self.volatility_entry.grid(row=4, column=1, columnspan=2)

        # Model Selection
        tk.Label(self.root, text="Select Model:").grid(row=5, column=0)
        self.model_var = tk.StringVar(value="Black-Scholes")
        tk.Radiobutton(self.root, text="Black-Scholes", variable=self.model_var, value="Black-Scholes").grid(row=5, column=1)
        tk.Radiobutton(self.root, text="Binomial", variable=self.model_var, value="Binomial").grid(row=5, column=2)

        # Calculate button
        calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate_prices)
        calculate_button.grid(row=7, column=0, columnspan=2)

        # Results labels
        self.call_price_label = tk.Label(self.root, text="Call Price: ")
        self.call_price_label.grid(row=8, column=0, columnspan=2)

        self.put_price_label = tk.Label(self.root, text="Put Price: ")
        self.put_price_label.grid(row=9, column=0, columnspan=2)

    def calculate_prices(self):
        try:
            s = float(self.spot_price_entry.get())          # Spot price = current market price of underlying asset
            k = float(self.strike_price_entry.get())        # Strike price = price option can be exercised for at expiration
            t = float(self.time_to_expiration_entry.get())  # Time to expiration = years until option expires and can be exercised
            r = float(self.risk_free_rate_entry.get())      # Risk-free rate = return that can be made risk-free
            v = float(self.volatility_entry.get())          # Volatility = standard deviation of the underlying asset's price

            model = self.model_var.get()

            if model == "Black-Scholes":
                self.calculate_black_scholes(s, k, t, r, v)
            elif model == "Binomial":
                self.calculate_binomial(s, k, t, r, v)

        except ValueError:
            self.call_price_label.config(text="Invalid input to calculate call price")
            self.put_price_label.config(text="Invalid input to calculate put price")

    def calculate_black_scholes(self, s, k, t, r, v):
        d1 = (math.log(s / k) + (r + (v ** 2) / 2) * t) / (v * math.sqrt(t))
        d2 = d1 - v * math.sqrt(t)
        call_price = s * norm.cdf(d1) - k * math.exp(-r * t) * norm.cdf(d2)
        put_price = k * math.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)

        self.call_price_label.config(text=f"Call Price: {round(call_price, 4)}")
        self.put_price_label.config(text=f"Put Price: {round(put_price, 4)}")

    def calculate_binomial(self, s, k, t, r, v):
        # Placeholder for Binomial model calculation
        self.call_price_label.config(text="Call Price: [Binomial result]")
        self.put_price_label.config(text="Put Price: [Binomial result]")


if __name__ == "__main__":
    window = tk.Tk()
    app = OptionsPriceCalculatorApp(window)
    window.mainloop()
