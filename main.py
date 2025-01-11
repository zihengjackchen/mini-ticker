import tkinter as tk
import json
import time
import requests

def remove_prefix(string):
    # Partition the string into three parts: before the first ':', the ':', and the rest
    if ':' not in string:
        return string
    remainder = string.replace('BINANCE:', '')
    return remainder.replace('USDC', '')

# Load configuration from config.json
def load_config():
    try:
        with open("config.json", "r") as file:
            print("[DEBUG] Loading configuration...")
            return json.load(file)
    except Exception as e:
        print(f"[ERROR] Failed to load configuration: {e}")
        exit(1)

# Fetch asset data (mocked with random values for testing)
latest_data_cache = {}
last_price_update_time = 0


def fetch_asset_data():
    global last_price_update_time, latest_data_cache
    
    current_time = time.time()
    if current_time - last_price_update_time >= CONFIG["update_interval"]:
        try:
            print("[DEBUG] Fetching latest data for all assets...")
            api_key = CONFIG.get("api_key")
            if not api_key:
                raise ValueError("API key not found in configuration.")

            for _, symbols in CONFIG["assets"].items():
                for symbol in symbols:
                    response = requests.get(
                        f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
                    )
                    if response.status_code == 200:
                        data = response.json()
                        latest_data_cache[symbol] = {
                            "price": data.get("c", 0),  # Current price
                            "change_percent": data.get("dp", 0)  # Percentage change
                        }
                    else:
                        print(f"[ERROR] Failed to fetch data for {symbol}: {response.text}")

            last_price_update_time = current_time
            print("[DEBUG] Data updated successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to fetch asset data: {e}")

# Display assets for the current group
def display_assets():
    global current_group, last_updated_label

    canvas.delete("all")

    y_offset = 20

    # Add the asset class header
    canvas.create_text(
        10, y_offset, anchor="nw",
        text=f"{current_group}", font=(CONFIG["font"], CONFIG["header_font_size"], "bold"),
        fill=CONFIG["text_color"]
    )
    y_offset += 50
    canvas.create_line(
        0, y_offset, CONFIG["window_size"][0], y_offset,
        fill=CONFIG["text_color"]
    )
    y_offset += 20

    # Add the assets
    for asset_ticker in CONFIG["assets"][current_group]:

        data = latest_data_cache.get(asset_ticker, {})

        change_color = CONFIG["highlight_positive"] if data["change_percent"] >= 0 else CONFIG["highlight_negative"]

        # Render data in three columns
        canvas.create_text(
            10, y_offset, anchor="w",
            text=remove_prefix(asset_ticker), font=(CONFIG["font"], CONFIG["asset_font_size"]), fill=CONFIG["text_color"]
        )
        canvas.create_text(
            120, y_offset, anchor="w",
            text=f"${data['price']:.2f}", font=(CONFIG["font"], CONFIG["asset_font_size"]), fill=CONFIG["text_color"]
        )
        canvas.create_text(
            245, y_offset, anchor="w",
            text=f"{data['change_percent']:.1f}%", font=(CONFIG["font"], CONFIG["asset_font_size"]), fill=change_color
        )
        y_offset += 30

    # Update last updated label with the time of the last price fetch
    last_updated_label.config(text=f"Last updated: {time.strftime('%H:%M:%S', time.localtime(last_price_update_time))}")

    # Schedule switch to the next group with a transition effect
    root.after(CONFIG["asset_jumping_time"] * 1000, start_transition)

# Smooth scrolling transition effect when switching groups
def start_transition():
    global current_group

    groups = list(CONFIG["assets"].keys())
    current_index = groups.index(current_group)
    next_group = groups[(current_index + 1) % len(groups)]

    frame_width = CONFIG["window_size"][0]
    step_size = frame_width // (CONFIG["asset_jumping_time"] * 3)

    for offset in range(0, frame_width + 1, step_size):
        canvas.delete("all")

        # Render current group sliding left
        render_group_with_offset(current_group, -offset)

        # Render next group entering from the right
        render_group_with_offset(next_group, frame_width - offset)

        canvas.update()
        time.sleep(0.03)

    current_group = next_group
    fetch_asset_data()  # Update data before displaying the next group
    display_assets()

# Render a group with an offset for transition effects
def render_group_with_offset(group, x_offset):
    y_offset = 20

    # Render header
    canvas.create_text(
        10 + x_offset, y_offset, anchor="nw",
        text=f"{group}", font=(CONFIG["font"], CONFIG["header_font_size"], "bold"),
        fill=CONFIG["text_color"]
    )
    y_offset += 50
    canvas.create_line(
        0, y_offset, CONFIG["window_size"][0], y_offset,
        fill=CONFIG["text_color"]
    )
    y_offset += 20

    # Render assets
    for asset_ticker in CONFIG["assets"][group]:
        data = latest_data_cache.get(asset_ticker)
        if not data:
            continue

        change_color = CONFIG["highlight_positive"] if data["change_percent"] >= 0 else CONFIG["highlight_negative"]

        canvas.create_text(
            10 + x_offset, y_offset, anchor="w",
            text=remove_prefix(asset_ticker), font=(CONFIG["font"], CONFIG["asset_font_size"]), fill=CONFIG["text_color"]
        )
        canvas.create_text(
            120 + x_offset, y_offset, anchor="w",
            text=f"${data['price']:.2f}", font=(CONFIG["font"], CONFIG["asset_font_size"]), fill=CONFIG["text_color"]
        )
        canvas.create_text(
            245 + x_offset, y_offset, anchor="w",
            text=f"{data['change_percent']:.1f}%", font=(CONFIG["font"], CONFIG["asset_font_size"]), fill=change_color
        )
        y_offset += 30

# Exit the application
def exit_app():
    print("[DEBUG] Exiting application...")
    root.destroy()

# Initialize the application
try:
    print("[DEBUG] Initializing application...")
    CONFIG = load_config()

    root = tk.Tk()
    root.title("Mini Ticker")

    width, height = CONFIG.get("window_size", [320, 480])
    if CONFIG["fullscreen"]:
        root.attributes("-fullscreen", True)
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()

    root.geometry(f"{width}x{height}")
    root.configure(bg=CONFIG["bg_color"])

    # Create a canvas for displaying content
    canvas = tk.Canvas(root, bg=CONFIG["bg_color"], width=width, height=height - 50)
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Add a bottom frame for the exit button and last updated label
    bottom_frame = tk.Frame(root, bg=CONFIG["bg_color"])
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # Add last updated label
    last_updated_label = tk.Label(
        bottom_frame, text="", font=(CONFIG["font"], 12), bg=CONFIG["bg_color"], fg=CONFIG["text_color"]
    )
    last_updated_label.pack(side=tk.LEFT, padx=10)

    # Add an exit button
    exit_button = tk.Button(
        bottom_frame, text="Exit", command=exit_app,
        font=(CONFIG["font"], 14), bg="red", fg="white", width=10
    )
    exit_button.pack(side=tk.RIGHT, padx=10)

    # Initial state
    current_group = list(CONFIG["assets"].keys())[0]

    fetch_asset_data()  # Initial data fetch
    print("[DEBUG] Starting asset updates...")
    display_assets()
    root.mainloop()
except Exception as e:
    print(f"[ERROR] Application failed to start: {e}")
