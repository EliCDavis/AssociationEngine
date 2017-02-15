from .Relationship import Relationship
from .Variable import Variable


def test_should_have_last_pushed_value_as_none_on_initialization():
    relationship = Relationship(Variable(), Variable())
    assert relationship.last_pushed_value is None

def test_should_have_personal_uuid():
    relationship = Relationship(Variable(), Variable())
    assert relationship.get_uuid() is not None

def test_should_automatically_subscribe_to_variables():
    var1 = Variable()
    var2 = Variable()
    relationship = Relationship(var1, var2)
    assert var1.subscribers[relationship.get_uuid()] is not None
    assert var2.subscribers[relationship.get_uuid()] is not None
