import pylights


def test_single():
    position = 10, 10
    size = 50, 50
    channels = 1
    light = pylights.Light('single_test', position, size)
    light.set_value(0.8, False)
    assert light.value_current == 0.8
    assert light.value_target == 0.8
    assert light.value_output == 0
    light.set_value(0.1)
    assert light.value_current == 0.8
    assert light.value_target == 0.1
    assert light.value_output == 0
    light.update()
    temp = (0.8 + light.damping * (0.1 - 0.8))
    assert light.value_current == temp
    assert light.value_target == 0.1
    assert light.value_output == int(temp * 255.0)