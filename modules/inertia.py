from typing import Union

class InertialNumber:
    def __init__(self, initial_value: Union[int, float] = 0, minimum: Union[int, float] = 0,
                 maximum: Union[int, float] = 86400, friction: float = 0.95, force_multiplier:float = 10.0) -> None:

        self._value = initial_value % (maximum - minimum)
        self._minimum = minimum
        self._maximum = maximum
        self._velocity = 0
        self._friction = friction
        self._target_value = None
        self._force_multiplier = force_multiplier

    def apply_force(self, force: int, dt: int = 1):
        self._velocity += force * dt

    def update(self, dt: int = 1):
        if self._target_value is not None:
            difference = self._target_value - self._value
            self.apply_force(difference * self._force_multiplier, dt)

        self._value += self._velocity * dt
        self._value %= self._maximum

        self._velocity *= (self._friction ** dt)

        if abs(self._velocity) < 0.01:
            self._velocity = 0

        self._value = self._value % (self._maximum - self._minimum)
        if self._value < self._minimum:
            self._value += (self._maximum - self._minimum)

    def get_value(self):
        return self._value

    def set_value(self, new_value: int):
       self._value = new_value % (self._maximum - self._minimum)

    def set_target_value(self, new_target_value: int):
        self._target_value = new_target_value % (self._maximum- self._minimum)

    def clear_target_value(self):
        self._target_value = None
