from app import fetch_ohlcv

def rsi_strategy(symbol, period=14):
    df = fetch_ohlcv(symbol)
    if df is None:
        return 'hold'
    
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    if rsi.iloc[-1] < 30:
        return 'buy'
    elif rsi.iloc[-1] > 70:
        return 'sell'
    else:
        return 'hold'
