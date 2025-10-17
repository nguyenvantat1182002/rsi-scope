import numpy as np
import pandas as pd
import MetaTrader5 as mt5
import talib


class RSIDivergence:
    def __init__(self, symbol: str, timeframe: int, lookback: int = 200):
        self.symbol = symbol
        self.timeframe = timeframe
        self.lookback = lookback
        
    def create_market_struct(self, df: pd.DataFrame):
        df['pivot_type'] = 0
        df['pivot_index'] = 0
        
        prev_candle = df.iloc[0]
        prev_candle_i = 0
        
        up_move = True
        
        for i in range(1, len(df)):
            curr_candle = df.iloc[i]
            
            if up_move:
                if curr_candle['high'] > prev_candle['high']:
                    prev_candle = curr_candle
                    prev_candle_i = i
                elif curr_candle['low'] < prev_candle['low']:
                    df.at[i, 'pivot_type'] = 1
                    df.at[i, 'pivot_index'] = prev_candle_i
                    
                    prev_candle = curr_candle
                    prev_candle_i = i
                    
                    up_move = False
            else:
                if curr_candle['low'] < prev_candle['low']:
                    prev_candle = curr_candle
                    prev_candle_i = i
                elif curr_candle['high'] > prev_candle['high']:
                    df.at[i, 'pivot_type'] = -1
                    df.at[i, 'pivot_index'] = prev_candle_i
                    
                    prev_candle = curr_candle
                    prev_candle_i = i
                    
                    up_move = True
                    
    def create_dataframe(self, source: str = 'close', start: int = 0, count: int = 500) -> pd.DataFrame:
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, start, count)
        
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        if source == 'ohlc4':
            df['ohlc4'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
        
        source = df[source].to_numpy()
        df['rsi'] = np.round(talib.RSI(source), 2)

        c = df['close'].to_numpy()
        _, _, hist = talib.MACD(c)
        
        sym_info = mt5.symbol_info(self.symbol)
        df['macd_hist'] = np.round(hist / sym_info.point) * sym_info.point
        
        df.drop(columns=['tick_volume', 'spread', 'real_volume'], inplace=True)
        df.dropna(subset=['rsi'], inplace=True, ignore_index=True)
        
        return df
    