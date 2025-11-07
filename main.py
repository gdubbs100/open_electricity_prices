
import pandas as pd
from datetime import datetime, timedelta
from utils.queries import query_price_by_region

## inputs := market, metric, interval, start_date
if __name__ == "__main__":

    df = query_price_by_region(
        region='VIC1',
        interval='1h',
        date_start=datetime.now()-timedelta(days=1)
    )

    latest_price = df.sort_values('timestamp')['value'].iloc[-1].item()
    # df.to_csv('./tmp2.csv')