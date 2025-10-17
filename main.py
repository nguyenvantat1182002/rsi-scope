import MetaTrader5 as mt5
mt5.initialize(path=r'C:\Program Files\MetaTrader 5 EXNESS 2\terminal64.exe')

from detector import RSIDivergence


def main():
    rsi = RSIDivergence('EURUSDm', mt5.TIMEFRAME_M5)

    df = rsi.create_dataframe()
    rsi.create_market_struct(df)

    print(df.tail(10))


if __name__ == "__main__":
    main()
