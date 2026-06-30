from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AxisInput:
    """Normalized movement intent for one frame."""

    forward: int = 0
    strafe: int = 0
    vertical: int = 0
    turn: int = 0
    pitch: int = 0


def bool_axis(positive: bool, negative: bool) -> int:
    """Convert two directional key states into -1, 0, or 1."""
    return int(positive) - int(negative)


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def scaled_delta(axis_value: int, speed: float, dt: float) -> float:
    return axis_value * speed * dt


def pitch_with_limits(current_pitch: float, delta: float, limit: float = 70.0) -> float:
    return clamp(current_pitch + delta, -limit, limit)

