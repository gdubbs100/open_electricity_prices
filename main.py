import os

import pandas as pd
import numpy as np

from datetime import datetime, timedelta
from utils.data_processing import write_row
from utils.queries import query_price_by_region
from algo.battery import Battery


def threshold_policy(state):
    p = state[-1]
    ## sell up to 10 if p > 25
    if p > 25:
        return -10
    ## charge the battery if price is negative
    elif p < 0:
        return 10
    ## sell small amt if price is not too high
    else:
        return -1

if __name__ == "__main__":
    region = 'VIC1'
    date_start = datetime.now()-timedelta(days=1)
    capacity = 100
    loss_factor = 1
    scenario_name = 'test_battery'
    log_file = f'./logs/{scenario_name}.csv'
    if os.path.exists(log_file):
        df = pd.read_csv(f"{log_file}")
        previous_results = df.sort_values('timestamp').iloc[-1]
        previous_stored_energy = previous_results['stored_energy']
        previous_charge_decision = previous_results['charge_decision']
        previous_timestamp = previous_results['timestamp']
    else:
        previous_stored_energy = 0
        previous_charge_decision = 0
        previous_timestamp = None

    ## initialise Battery class with previous results
    battery = Battery(
        capacity=capacity,
        loss_factor=loss_factor,
        policy=threshold_policy
    )
    battery.stored_energy = previous_stored_energy

    df = query_price_by_region(
        region=region,
        interval='1h',
        date_start=date_start
    )

    latest_row = df.sort_values('timestamp').iloc[-1]
    latest_price, latest_timestamp = latest_row['value'], latest_row['timestamp']

    charge_decision = battery.make_charge_decision(exogenous_info=np.array([latest_price]))

    results = {
        'region': region,
        'timestamp': latest_timestamp,
        'stored_energy': battery.stored_energy,
        'price': latest_price,
        'charge_decision': charge_decision,
        'revenue': -previous_charge_decision * latest_price,
        'capacity': capacity,
        'loss_factor': loss_factor,
    }

    write_row(csv_path=f'{log_file}', row=results)
