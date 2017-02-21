import math
from .SpearframeRelationship import SpearframeRelationship, check_for_monotonic_change, generate_association
from.Variable import Variable


def test_should_initialize_empty_frames():
    rel = SpearframeRelationship(Variable(), Variable())
    assert len(rel.frames) == 0


def test_should_show_monotonic_change():
    assert check_for_monotonic_change(1, 2, 1) is True


def test_should_show_no_monotonic_change():
    assert check_for_monotonic_change(1, 2, 3) is False


def test_should_show_strong_association():
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(720):
        var1.on_data(math.sin(math.radians(degree)))
        var2.on_data(math.cos(math.radians(degree)))

    assert rel.get_last_pushed_value() > .95


def test_should_show_weak_association():
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(720):
        var1.on_data(math.sin(math.radians(degree*5)))
        var2.on_data(math.sin(math.radians(degree)))

    assert rel.get_last_pushed_value() < .2
