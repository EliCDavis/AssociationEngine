from AssociationEngine.Relationship.Relationship import Relationship
from AssociationEngine.Relationship.Variable import Variable
import pytest


def test_should_have_last_pushed_value_as_none_on_initialization():
    relationship = Relationship(Variable(), Variable())
    assert relationship.get_last_pushed_value() is None


def test_should_should_throw_error_trying_to_grab_coefficient():
    with pytest.raises(NotImplementedError) as excinfo:
        Relationship(Variable(), Variable()).get_correlation_coefficient()
    assert "Underlying algorithm should implement this" in str(excinfo.value)


def test_should_should_throw_error_trying_get_new_value_from_variables():
    with pytest.raises(NotImplementedError) as excinfo:
        Relationship(Variable(), Variable()).on_new_value(1, 1)
    assert "Underlying algorithm should implement this" in str(excinfo.value)


def test_should_should_throw_error_trying_to_get_value_between_times():
    with pytest.raises(NotImplementedError) as excinfo:
        Relationship(Variable(), Variable()).get_value_between_times()
    assert "Underlying algorithm should implement this" in str(excinfo.value)


def test_should_should_throw_error_trying_clean_up():
    with pytest.raises(NotImplementedError) as excinfo:
        Relationship(Variable(), Variable()).clean_up()
    assert "Underlying algorithm should implement this" in str(excinfo.value)


def test_should_have_personal_uuid():
    relationship = Relationship(Variable(), Variable())
    assert relationship.get_uuid() is not None


def test_should_automatically_subscribe_to_variables():
    var1 = Variable()
    var2 = Variable()
    relationship = Relationship(var1, var2)
    assert var1.subscribers[relationship.get_uuid()] is not None
    assert var2.subscribers[relationship.get_uuid()] is not None


def test_should_update_last_pushed_value_on_push():
    relationship = Relationship(Variable(), Variable())
    relationship._push_to_subscribers(1)
    assert relationship.get_last_pushed_value() is 1
