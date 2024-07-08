from app import fetch_ohlcv

def calculate_bollinger_bands(data, window=20, num_of_std=2):
    rolling_mean = data['close'].rolling(window=window).mean()
    rolling_std = data['close'].rolling(window=window).std()
    
    data['bollinger_high'] = rolling_mean + (rolling_std * num_of_std)
    data['bollinger_low'] = rolling_mean - (rolling_std * num_of_std)
    
    return data

def bollinger_bands_strategy(symbol):
    df = fetch_ohlcv(symbol)
    df = calculate_bollinger_bands(df)
    
    if df['close'].iloc[-1] < df['bollinger_low'].iloc[-1]:
        return 'buy'
    elif df['close'].iloc[-1] > df['bollinger_high'].iloc[-1]:
        return 'sell'
    else:
        return 'hold'
