from scene_explorer.movement import bool_axis, clamp, pitch_with_limits, scaled_delta


def test_bool_axis_returns_directional_intent():
    assert bool_axis(True, False) == 1
    assert bool_axis(False, True) == -1
    assert bool_axis(False, False) == 0
    assert bool_axis(True, True) == 0


def test_clamp_limits_values():
    assert clamp(5, 0, 10) == 5
    assert clamp(-2, 0, 10) == 0
    assert clamp(12, 0, 10) == 10


def test_scaled_delta_uses_speed_and_frame_time():
    assert scaled_delta(1, 18.0, 0.5) == 9.0
    assert scaled_delta(-1, 18.0, 0.5) == -9.0
    assert scaled_delta(0, 18.0, 0.5) == 0


def test_pitch_with_limits_prevents_over_rotation():
    assert pitch_with_limits(65, 10) == 70.0
    assert pitch_with_limits(-65, -10) == -70.0
    assert pitch_with_limits(10, 5) == 15

