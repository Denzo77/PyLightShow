from pylightshow import pylights
import numpy as np

"""This should go in test fixture?
name = 'base_light'
position = 10, 10
size = 50, 50
light = pylights.BaseLight('base_light', position, size)
"""

def test_name():
    print("Testing name is correct")
    assert light.name == name


def test_shape():
    print("Testing position and size are correct")
    assert light.position == position
    assert light.size == size


def test_on_off():
    print("Testing switching on and off")
    assert light.is_on == False
    light.toggle()
    assert light.is_on == True
    light.toggle()
    assert light.is_on == False


def test_enabling():
    print("Testing enabling light")
    assert light.is_enabled == True
    light.enable(False)
    assert light.is_enabled == False


def test_single():
    """
     Test single channel light class
    """
    position = 10, 10
    size = 50, 50
    channels = 1
    light = pylights.SingleLight('single_test', position, size)
    light.set(0.8, False)
    assert light.value_current == 0.8
    assert light.value_target == 0.8
    assert light.value_output == 0
    light.set(0.1)
    assert light.value_current == 0.8
    assert light.value_target == 0.1
    assert light.value_output == 0
    light.update()
    temp = (0.8 + light.damping * (0.1 - 0.8))
    assert light.value_current == temp
    assert light.value_target == 0.1
    assert light.value_output == int(0.8 * 255.0)
    light.update()
    assert light.value_output == int(temp * 255.0)


def test_RGB():
    """
    Test multi channel light class
    """
    position = 10, 10
    size = 50, 50
    channels = 3
    light = pylights.MultiLight('single_test', position, size, channels=channels)
    old_value = np.array([0.8, 0.3, 0.6])
    new_value = np.array([0.1, 0.1, 0.1])
    light.set(old_value, False)
    assert np.array_equiv(light.value_current, old_value)
    assert np.array_equiv(light.value_target, old_value)
    assert np.array_equiv(light.value_output, np.array([0, 0, 0]))
    light.set(new_value)
    assert np.array_equiv(light.value_current, old_value)
    assert np.array_equiv(light.value_target, new_value)
    assert np.array_equiv(light.value_output, np.array([0, 0, 0]))
    light.update()
    temp = (old_value + light.damping * (new_value - old_value))
    assert np.array_equiv(light.value_current, temp)
    assert np.array_equiv(light.value_target, new_value)
    assert np.array_equiv(light.value_output, (old_value * 255.0).astype(int))
    light.update()
    assert np.array_equiv(light.value_output, (temp * 255.0).astype(int))