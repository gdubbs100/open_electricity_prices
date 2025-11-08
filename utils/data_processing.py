import csv
import os
import pandas as pd
from openelectricity.models.timeseries import TimeSeriesResponse


def write_row(csv_path: str, row: dict):
    """Append a single dictionary row to a CSV file, writing headers if file is empty."""
    file_exists = os.path.exists(csv_path)
    
    with open(csv_path, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        # Write header only if file is new or empty
        if not file_exists or os.stat(csv_path).st_size == 0:
            writer.writeheader()
        writer.writerow(row)


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