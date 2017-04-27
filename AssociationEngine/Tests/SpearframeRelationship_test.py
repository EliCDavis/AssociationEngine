import math
import os
import time

from AssociationEngine.Relationship.Variable import Variable
from AssociationEngine.Relationship.SpearframeRelationship import \
    SpearframeRelationship


def test_should_initialize_empty_frames():
    rel = SpearframeRelationship(Variable(), Variable())
    assert len(rel.frames) == 0


def test_should_show_strong_association():
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(180):
        var1.on_data(math.sin(math.radians(degree * 10)), degree, degree+1)
        var2.on_data(math.cos(math.radians(degree * 10) + (math.pi / 2.0)), degree, degree+1)

    assert rel.get_last_pushed_value() > .95


def test_should_show_weak_association():
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(180):
        var1.on_data(math.sin(math.radians(degree * 10)), degree, degree+1)
        var2.on_data(math.cos(math.radians(degree * 10)), degree, degree+1)

    assert rel.get_last_pushed_value() < .1


def test_should_not_return_nan():
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(180):
        var1.on_data(math.sin(math.radians(degree * 10)), degree, degree+1)
        var2.on_data(math.sin(math.radians(degree * 100)), degree, degree+1)

    assert not math.isnan(rel.get_last_pushed_value())


def test_should_create_db():
    if os.path.exists("spearframe.db"):
        os.remove("spearframe.db")

    var1 = Variable()
    var2 = Variable()
    SpearframeRelationship(var1, var2)

    assert os.path.exists("spearframe.db")


def test_should_delete_db():
    var1 = Variable()
    var2 = Variable()
    SpearframeRelationship(var1, var2)

    if os.path.exists("spearframe.db"):
        os.remove("spearframe.db")

    assert not os.path.exists("spearframe.db")
