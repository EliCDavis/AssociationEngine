import math

from Relationship.SpearframeRelationship import SpearframeRelationship
from Relationship.Variable import Variable


def test_should_initialize_empty_frames():
    rel = SpearframeRelationship(Variable(), Variable())
    assert len(rel.frames) == 0


def test_should_show_strong_association():
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(180):
        var1.on_data(math.sin(math.radians(degree * 10)))
        var2.on_data(math.cos(math.radians(degree * 10) + (math.pi / 2.0)))

    assert rel.get_last_pushed_value() > .95


def test_should_show_weak_association():
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(180):
        var1.on_data(math.sin(math.radians(degree * 10)))
        var2.on_data(math.cos(math.radians(degree * 10)))

    assert rel.get_last_pushed_value() < .1


def test_should_not_return_nan():
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(180):
        var1.on_data(math.sin(math.radians(degree * 10)))
        var2.on_data(math.sin(math.radians(degree * 100)))

    assert not math.isnan(rel.get_last_pushed_value())
