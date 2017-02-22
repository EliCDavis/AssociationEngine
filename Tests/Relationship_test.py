from Relationship.Relationship import Relationship
from Relationship.Variable import Variable


def test_should_have_last_pushed_value_as_none_on_initialization():
    relationship = Relationship(Variable(), Variable())
    assert relationship.get_last_pushed_value() is None


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
