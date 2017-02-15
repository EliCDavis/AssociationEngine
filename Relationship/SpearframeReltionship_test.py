from .SpearframeRelationship import SpearframeRelationship
from.Variable import Variable


def test_should_initialize_empty_frames():
    rel = SpearframeRelationship(Variable(), Variable())
    assert len(rel.frames) == 0

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