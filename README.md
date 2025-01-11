# **ini-Ticker**

A lightweight, fullscreen stock ticker built with Python and Tkinter. Ideal for Raspberry Pi or any Python-compatible system. Powered by the [Finnhub API](https://finnhub.io/).

## **Features**
- Real-time tracking for multiple stocks.
- Minimalistic, fullscreen design for small screens.
- Performance-based coloring (green for gains, red for losses).
- Fully customizable via `config.json`.

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/mini-ticker.git
   cd mini-ticker
   ```

2. Install dependencies:
   ```bash
   pip install requests
   ```

3. Add your [Finnhub API key](https://finnhub.io/dashboard) to `config.json`.

4. Run the app:
   ```bash
   python3 main.py
   ```

---

## **Configuration**

Customize `config.json`:
- **Stocks**: Add tickers under `stocks`.
- **Colors**: Set `highlight_positive` (green) and `highlight_negative` (red).
- **Update Interval**: Set in seconds with `update_interval`.

Example:
```json
{
  "stocks": [
    {"name": "Apple", "symbol": "AAPL"},
    {"name": "Tesla", "symbol": "TSLA"}
  ],
  "update_interval": 300,
  "highlight_positive": "green",
  "highlight_negative": "red"
}
```

---

## **Usage**

1. Start the ticker:
   ```bash
   python3 main.py
   ```

2. Exit fullscreen with `Ctrl+Q`.

---

## **Planned Features**
- Auto-scroll for long stock lists.
- Historical trend sparklines.

---

## **Contributing**

1. Fork the repo, create a branch, make changes, and submit a pull request.

---

## **License**
Licensed under the MIT License.