
import numpy as np
## TODO: validate expected behaviour
class Battery:

    def __init__(
            self, 
            capacity: float, 
            loss_factor: float,
            policy: callable,
        ):

        self.capacity = capacity
        self.loss_factor = loss_factor
        self.remaining_capacity = np.array([capacity])
        self.policy = policy

    def apply_constraints(self, raw_charge_decision: float) -> float:
        upper = 1/self.loss_factor * (self.capacity - (self.remaining_capacity-raw_charge_decision))
        lower = 1/self.loss_factor * (self.remaining_capacity-raw_charge_decision)
        return np.clip(raw_charge_decision, lower, upper)
    
    def make_charge_decision(self, exogenous_info: np.ndarray[float]) -> float:
        state = np.concat([self.remaining_capacity, exogenous_info])
        raw_charge_decision = self.policy(state)
        charge_decision = self.apply_constraints(raw_charge_decision)
        self.remaining_capacity = self.remaining_capacity - charge_decision
        return charge_decision