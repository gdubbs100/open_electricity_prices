import pandas as pd
from openelectricity.models.timeseries import TimeSeriesResponse

def convert_response_to_pandas(response: TimeSeriesResponse) -> pd.DataFrame:
    # TODO: monitor to make sure can handle queries generally
    data = []

    for timeseries in response.data:

        for result in timeseries.results:
            region = result.name.split("_")[-1] 
            for data_point in result.data:
                data.append({
                    "region": region,
                    "timestamp": data_point.timestamp,
                    "metric": timeseries.metric,
                    "value": data_point.value,
                    "unit": timeseries.unit
                })

    return pd.DataFrame(data)