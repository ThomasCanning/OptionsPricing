import tkinter as tk

from api_calls import ApiCalls
from pricing_models import PricingModels


class OptionsPriceCalculatorApp:
    def __init__(self, root):
        self.call_price_label = None
        self.put_price_label = None
        self.model_var = None
        self.risk_free_rate_entry = None
        self.time_to_expiration_entry = None
        self.strike_price_entry = None
        self.spot_price_entry = None
        self.volatility_entry = None
        
        self.root = root
        self.root.title("Options Price Calculator")

        self.api = ApiCalls()
        self.models = PricingModels()

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

        # Risk-Free Rate text entry, set with default value of the current US Treasury 10-year yield retrieved from the alpha-vantage API
        tk.Label(self.root, text="Risk-Free Rate:").grid(row=3, column=0)
        self.risk_free_rate_entry = tk.Entry(self.root)
        self.risk_free_rate_entry.insert(0, self.api.get_us_treasury_yield())
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
            s = float(self.spot_price_entry.get())
            k = float(self.strike_price_entry.get())
            t = float(self.time_to_expiration_entry.get())
            r = float(self.risk_free_rate_entry.get())
            v = float(self.volatility_entry.get())

            model = self.model_var.get()
            self.models.update_parameters(s, k, t, r, v)

            values = None
            if model == "Black-Scholes":
                values = self.models.calculate_black_scholes()
            elif model == "Binomial":
                values = self.models.calculate_binomial()

            self.call_price_label.config(text=f"Call Price: {values[0]:.2f}")
            self.put_price_label.config(text=f"Put Price: {values[1]:.2f}")

        except ValueError:
            self.call_price_label.config(text="Invalid input to calculate call price")
            self.put_price_label.config(text="Invalid input to calculate put price")


if __name__ == "__main__":
    window = tk.Tk()
    app = OptionsPriceCalculatorApp(window)
    window.mainloop()
