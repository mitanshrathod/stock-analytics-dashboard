import requests
import pandas as pd

def GetData(company="IBM"):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={company}&interval=5min&apikey=VIG3ZY2A30IJ35PJ"
    res = requests.get(url)
    data = res.json()

    if "Time Series (5min)" in data:
        time_series = data["Time Series (5min)"]
        df = pd.DataFrame.from_dict(time_series, orient="index")
        df.columns = [col.split('. ')[1] for col in df.columns]  # Clean column names
        df.index.name = "timestamp"  # Name the index
        df.to_csv(f"./Data/{company}_Data.csv")
        return df
    else:
        print("Error or Limit reached. Response:", data)
        return None

if __name__ == "__main__":
    df = GetData("TSLA")
    print(df)