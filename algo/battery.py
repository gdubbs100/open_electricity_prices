import numpy as np

from typing import Callable

class Battery:

    def __init__(
            self, 
            capacity: float, 
            loss_factor: float,
            policy: Callable[np.ndarray[float], np.ndarray[float]],
        ):

        self.capacity = capacity
        self.loss_factor = loss_factor
        self.stored_energy = 0
        self.policy = policy

    def apply_constraints(self, raw_charge_decision: float) -> float:
        upper = 1/self.loss_factor * (self.capacity - self.stored_energy)
        lower = -1/self.loss_factor * self.stored_energy
        return np.clip(raw_charge_decision, lower, upper)
    
    def make_charge_decision(self, exogenous_info: np.ndarray[float]) -> float:
        state = np.concat([np.array([self.stored_energy]), exogenous_info])
        raw_charge_decision = self.policy(state)
        charge_decision = self.apply_constraints(raw_charge_decision)
        self.stored_energy += self.loss_factor * charge_decision
        assert (self.stored_energy <= self.capacity), f"Cannot store more energy then {self.capacity}, recorded {self.stored_energy}"
        assert (self.stored_energy >= 0.0), f"Cannot store negative energy, recorded {self.stored_energy}"
        return charge_decision.item()