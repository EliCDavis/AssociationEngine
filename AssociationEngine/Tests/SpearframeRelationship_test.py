import math
import os
import pytest

from AssociationEngine.Relationship.Variable import Variable
from AssociationEngine.Relationship.SpearframeRelationship import \
    SpearframeRelationship


def test_should_show_perfect_association():
    if os.path.exists("spearframe.db"):
        os.remove("spearframe.db")
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(180):
        var1.on_data(math.sin(math.radians(degree * 10)), degree, degree+1)
        var2.on_data(math.sin(math.radians(degree * 10)), degree, degree+1)

    assert rel.get_last_pushed_value() == 1


def test_should_show_strong_association():
    if os.path.exists("spearframe.db"):
        os.remove("spearframe.db")
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(180):
        var1.on_data(math.sin(math.radians(degree * 10)), degree, degree+1)
        var2.on_data(math.cos(math.radians(degree * 10) + (math.pi / 2.0)),
                     degree, degree+1)

    assert rel.get_correlation_coefficient() > .95


def test_should_show_weak_association():
    if os.path.exists("spearframe.db"):
        os.remove("spearframe.db")
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(180):
        var1.on_data(math.sin(math.radians(degree * 10)), degree, degree+1)
        var2.on_data(math.cos(math.radians(degree * 50)), degree, degree+1)

    assert rel.get_correlation_coefficient() < .1


def test_should_not_return_nan():
    if os.path.exists("spearframe.db"):
        os.remove("spearframe.db")
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(180):
        var1.on_data(math.sin(math.radians(degree * 10)), degree, degree+1)
        var2.on_data(math.sin(math.radians(degree * 100)), degree, degree+1)

    assert not math.isnan(rel.get_correlation_coefficient())


def test_should_create_db():
    if os.path.exists("spearframe.db"):
        os.remove("spearframe.db")

    var1 = Variable()
    var2 = Variable()
    SpearframeRelationship(var1, var2)

    assert os.path.exists("spearframe.db")


def test_should_delete_db():
    if os.path.exists("spearframe.db"):
        os.remove("spearframe.db")
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    if os.path.exists("spearframe.db"):
        rel.clean_up()

    assert not os.path.exists("spearframe.db")


def test_should_return_float():
    if os.path.exists("spearframe.db"):
        os.remove("spearframe.db")
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(50):
        var1.on_data(math.sin(math.radians(degree * 10)), degree, degree+1)
        var2.on_data(math.cos(math.radians(degree * 10)), degree, degree+1)

    assert isinstance(rel.get_correlation_coefficient(), float)


def test_should_return_float2():
    if os.path.exists("spearframe.db"):
        os.remove("spearframe.db")
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(50):
        if degree < 46:
            var1.on_data(math.sin(math.radians(degree * 10)), degree, degree+1)
        var2.on_data(math.cos(math.radians(degree * 10)), degree, degree+1)

    assert isinstance(rel.get_correlation_coefficient(), float)


def test_should_return_float3():
    if os.path.exists("spearframe.db"):
        os.remove("spearframe.db")
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(20):
        var1.on_data(math.sin(math.radians(degree * 10)), degree, degree+1)
        var2.on_data(math.cos(math.radians(degree * 10)), degree, degree+1)

    assert isinstance(rel.get_correlation_coefficient(), float)


def test_should_return_float_from_frame_db():
    if os.path.exists("spearframe.db"):
        os.remove("spearframe.db")
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)

    for degree in range(180):
        var1.on_data(math.sin(math.radians(degree * 10)), degree, degree+1)
        var2.on_data(math.cos(math.radians(degree * 10)), degree, degree+1)

    assert isinstance(rel.get_value_between_times(0, 90), float)


def test_should_raise_error_when_unknown_publisher_emits():
    var1 = Variable()
    var2 = Variable()
    rel = SpearframeRelationship(var1, var2)
    with pytest.raises(ValueError):
        rel.on_new_value(1, 4, 0, 1)

