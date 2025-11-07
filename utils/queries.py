import pandas as pd
import datetime

from openelectricity import OEClient
from openelectricity.types import MarketMetric

from utils.data_processing import convert_response_to_pandas



def query_price_by_region(
        region: str, 
        interval: str, 
        date_start: datetime.datetime
    ) -> pd.DataFrame:

    with OEClient() as client:
        response = client.get_market(
            network_code="NEM",
            metrics=[MarketMetric.PRICE],
            interval=interval,
            date_start=date_start,
            network_region = region
        )

    return convert_response_to_pandas(response)

