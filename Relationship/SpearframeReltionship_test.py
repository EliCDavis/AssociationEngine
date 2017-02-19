from .SpearframeRelationship import SpearframeRelationship
from.Variable import Variable


def test_should_initialize_empty_frames():
    rel = SpearframeRelationship(Variable(), Variable())
    assert len(rel.frames) == 0

"""
# These are 2 are no longer valid
def test_should_generate_values_after_ten_iterations():
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    # Simulate some time
    for time_step in range(10):
        var1.on_data(time_step)
        var2.on_data(-time_step)

    assert len(rel.frames) == 1


def test_should_have_last_pushed_value_after_ten_iterations():
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    # Simulate some time
    for time_step in range(10):
        var1.on_data(time_step)
        var2.on_data(-time_step)

    assert rel.last_pushed_value is not None

# These 2 are private and cannot be tested
def test_should_show_monotonic_change():
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    assert rel.__check_for_monotonic_change(5, 10, 5) is True


def test_should_not_show_monotonic_change():
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    assert rel.__check_for_monotonic_change(10, 5, 3) is False
"""
