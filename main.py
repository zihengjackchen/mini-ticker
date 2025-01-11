import tkinter as tk
import requests
import json
import time

# Load configuration from config.json
def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

# Fetch stock data from Finnhub
def fetch_stock_data(symbol, api_key):
    BASE_URL = "https://finnhub.io/api/v1/quote"
    try:
        response = requests.get(BASE_URL, params={"symbol": symbol, "token": api_key})
        response.raise_for_status()
        data = response.json()
        return {
            "price": data["c"],
            "change_percent": data["dp"]
        }
    except requests.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Update stock data in the UI
def update_stocks():
    for widget in frame.winfo_children():
        widget.destroy()

    for stock in CONFIG["stocks"]:
        data = fetch_stock_data(stock["symbol"], CONFIG["api_key"])
        if not data:
            continue

        # Create a row for each stock
        row = tk.Frame(frame, bg=CONFIG["bg_color"])
        row.pack(fill=tk.X, pady=5)

        # Ticker name
        tk.Label(
            row,
            text=stock["name"],
            font=tuple(CONFIG["font"]),
            fg=CONFIG["text_color"],
            bg=CONFIG["bg_color"]
        ).pack(side=tk.LEFT, padx=10)

        # Current price
        tk.Label(
            row,
            text=f"${data['price']:.2f}",
            font=tuple(CONFIG["font"]),
            fg=CONFIG["text_color"],
            bg=CONFIG["bg_color"]
        ).pack(side=tk.LEFT, padx=10)

        # Daily percent change with color
        change_color = CONFIG["highlight_positive"] if data["change_percent"] >= 0 else CONFIG["highlight_negative"]
        tk.Label(
            row,
            text=f"{data['change_percent']:.2f}%",
            font=tuple(CONFIG["font"]),
            fg=change_color,
            bg=CONFIG["bg_color"]
        ).pack(side=tk.LEFT, padx=10)

    # Schedule the next update
    root.after(CONFIG["update_interval"] * 1000, update_stocks)

# Initialize the application
CONFIG = load_config()
root = tk.Tk()
root.title("Stock Ticker")
root.attributes("-fullscreen", True)
root.configure(bg=CONFIG["bg_color"])

canvas = tk.Canvas(root, bg=CONFIG["bg_color"], highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

frame = tk.Frame(canvas, bg=CONFIG["bg_color"])
canvas.create_window((0, 0), window=frame, anchor="nw")

# Start updating
update_stocks()
root.mainloop()
