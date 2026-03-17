import os
import requests
import yfinance as yf

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    requests.get(url)

def check_market():
    symbols = {"Nifty 50": "^NSEI", "Sensex": "^BSESN"}
    for name, ticker in symbols.items():
        df = yf.download(ticker, period="2d", interval="15m", progress=False)
        df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
        df['EMA_21'] = df['Close'].ewm(span=21, adjust=False).mean()
        last, prev = df.iloc[-1], df.iloc[-2]

        if (prev['EMA_9'] <= prev['EMA_21']) and (last['EMA_9'] > last['EMA_21']):
            send_alert(f"🚀 *BUY ALERT: {name}*\nPrice: {last['Close']:.2f}")
        elif (prev['EMA_9'] >= prev['EMA_21']) and (last['EMA_9'] < last['EMA_21']):
            send_alert(f"📉 *SELL ALERT: {name}*\nPrice: {last['Close']:.2f}")

if __name__ == "__main__":
    check_market()
                         
