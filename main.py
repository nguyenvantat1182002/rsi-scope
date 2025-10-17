import MetaTrader5 as mt5
mt5.initialize()

from detector import RSIDivergence


def main():
    rsi = RSIDivergence('BTCUSDm', mt5.TIMEFRAME_M5)

    df = rsi.create_dataframe()
    rsi.create_market_struct(df)

    print(df.tail(10))


if __name__ == "__main__":
    main()
