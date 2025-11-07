from openelectricity import OEClient
from openelectricity.types import MarketMetric
from datetime import datetime, timedelta

import pandas as pd

if __name__ == "__main__":
    with OEClient() as client:
        response = client.get_market(
            network_code="NEM",
            metrics=[MarketMetric.PRICE, MarketMetric.DEMAND_ENERGY],
            interval="1h",
            date_start=datetime.now() - timedelta(days=31),
            primary_grouping="network_region"
        )
    # Convert to DataFrame
data = []
# breakpoint()
for timeseries in response.data:
    for result in timeseries.results:
        region = result.name.split("_")[-1] 
        for data_point in result.data:
            data.append({
                "name": region,
                "timestamp": data_point.timestamp,
                "metric": timeseries.metric,
                "value": data_point.value,
                "unit": timeseries.unit
            })

    df = pd.DataFrame(data)
    df.to_csv('./tmp.csv')