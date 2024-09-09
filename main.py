import tkinter as tk
from api_calls import ApiCalls
from pricing_models import PricingModels
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class OptionsPriceCalculatorApp:
    def __init__(self, root):
        self.canvas = None
        self.ax = None
        self.fig = None
        self.volatility_slider = None
        self.risk_free_rate_slider = None
        self.strike_price_slider = None
        self.spot_price_slider = None
        self.time_to_expiration_slider = None

        self.call_price_label = None
        self.put_price_label = None
        self.model_var = None
        self.param_var = None
        self.price_type_var = None

        self.root = root
        self.root.title("Options Price Calculator")

        self.api = ApiCalls()
        self.models = PricingModels()

        self.create_widgets()
        self.create_plot()

    def create_widgets(self):
        tk.Label(self.root, text="Spot Price:").grid(row=0, column=0)
        self.spot_price_slider = tk.Scale(self.root, from_= 10, to= 200, orient='horizontal', command=self.update_plot)
        self.spot_price_slider.set(100)
        self.spot_price_slider.grid(row=0, column=1, columnspan=2)

        tk.Label(self.root, text="Strike Price:").grid(row=1, column=0)
        self.strike_price_slider = tk.Scale(self.root, from_=10, to=200, orient='horizontal', command=self.update_plot)
        self.strike_price_slider.set(100)
        self.strike_price_slider.grid(row=1, column=1, columnspan=2)

        tk.Label(self.root, text="Time to Expiration (Years):").grid(row=2, column=0)
        self.time_to_expiration_slider = tk.Scale(self.root, from_=0.01, to=3, resolution=0.01, orient='horizontal', command=self.update_plot)
        self.time_to_expiration_slider.set(1)
        self.time_to_expiration_slider.grid(row=2, column=1, columnspan=2)

        tk.Label(self.root, text="Risk-Free Rate (%):").grid(row=3, column=0)
        self.risk_free_rate_slider = tk.Scale(self.root, from_=0, to=10, resolution=0.01, orient='horizontal', command=self.update_plot)
        self.risk_free_rate_slider.set(self.api.get_us_treasury_yield() * 100)
        self.risk_free_rate_slider.grid(row=3, column=1, columnspan=2)

        tk.Label(self.root, text="Volatility (%):").grid(row=4, column=0)
        self.volatility_slider = tk.Scale(self.root, from_=1, to=100, orient='horizontal', command=self.update_plot)
        self.volatility_slider.set(30)
        self.volatility_slider.grid(row=4, column=1, columnspan=2)

        tk.Label(self.root, text="Select Model:").grid(row=5, column=0)
        self.model_var = tk.StringVar(value="Black-Scholes")
        tk.Radiobutton(self.root, text="Black-Scholes", variable=self.model_var, value="Black-Scholes", command=self.update_plot).grid(row=5, column=1)
        tk.Radiobutton(self.root, text="Binomial", variable=self.model_var, value="Binomial", command=self.update_plot).grid(row=5, column=2)

        self.call_price_label = tk.Label(self.root, text="Call Price: ")
        self.call_price_label.grid(row=6, column=0, columnspan=2)

        self.put_price_label = tk.Label(self.root, text="Put Price: ")
        self.put_price_label.grid(row=7, column=0, columnspan=2)

        tk.Label(self.root, text="Select Parameter for Plot:").grid(row=8, column=0)
        self.param_var = tk.StringVar(value="Spot Price")
        tk.OptionMenu(self.root, self.param_var, "Spot Price", "Strike Price", "Time to Expiration", "Risk-Free Rate", "Volatility", command=self.update_plot).grid(row=8, column=1, columnspan=2)

        tk.Label(self.root, text="Select Option Type for Plot:").grid(row=9, column=0)
        self.price_type_var = tk.StringVar(value="Call Price")
        tk.OptionMenu(self.root, self.price_type_var, "Call Price", "Put Price", command=self.update_plot).grid(row=9, column=1, columnspan=2)

    def create_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=10, column=0, columnspan=3)
        self.update_plot()

    def update_plot(self, *_):

        s = self.spot_price_slider.get()
        k = self.strike_price_slider.get()
        t = self.time_to_expiration_slider.get()
        r = self.risk_free_rate_slider.get() / 100
        v = self.volatility_slider.get() / 100

        model = self.model_var.get()
        self.models.update_parameters(s, k, t, r, v)

        if model == "Black-Scholes":
            values = self.models.calculate_black_scholes()
        else:
            values = self.models.calculate_binomial()

        self.call_price_label.config(text=f"Call Price: {values[0]:.2f}")
        self.put_price_label.config(text=f"Put Price: {values[1]:.2f}")

        selected_param = self.param_var.get()
        price_type = self.price_type_var.get()

        param_range,prices,x_label = range(1,100),range(1,100),"X-axis"
        if selected_param == "Spot Price":
            param_range = range(50, 201, 10)
            prices = [self.calculate_price(param, k, t, r, v, model, price_type) for param in param_range]
            x_label = "Spot Price"
        elif selected_param == "Strike Price":
            param_range = range(50, 201, 10)
            prices = [self.calculate_price(s, param, t, r, v, model, price_type) for param in param_range]
            x_label = "Strike Price"
        elif selected_param == "Time to Expiration":
            param_range = [i / 100.0 for i in range(1, 301)]
            prices = [self.calculate_price(s, k, param, r, v, model, price_type) for param in param_range]
            x_label = "Time to Expiration (Years)"
        elif selected_param == "Risk-Free Rate":
            param_range = [i / 100.0 for i in range(0, 1001)]
            prices = [self.calculate_price(s, k, t, param, v, model, price_type) for param in param_range]
            x_label = "Risk-Free Rate (%)"
        elif selected_param == "Volatility":
            param_range = range(1, 101)
            prices = [self.calculate_price(s, k, t, r, param / 100.0, model, price_type) for param in param_range]
            x_label = "Volatility (%)"

        self.ax.clear()
        self.ax.plot(param_range, prices, label=f"{price_type}")
        self.ax.set_title(f"{price_type} vs {x_label}")
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(price_type)
        self.ax.legend()
        self.canvas.draw()

    def calculate_price(self, s, k, t, r, v, model, price_type):
        self.models.update_parameters(s, k, t, r, v)
        if model == "Black-Scholes":
            return self.models.calculate_black_scholes()[0] if price_type == "Call Price" else self.models.calculate_black_scholes()[1]
        else:
            return self.models.calculate_binomial()[0] if price_type == "Call Price" else self.models.calculate_binomial()[1]

if __name__ == "__main__":
    window = tk.Tk()
    app = OptionsPriceCalculatorApp(window)
    window.mainloop()
