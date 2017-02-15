from .Relationship import Relationship
from .Variable import Variable


def test_should_have_personal_uuid():
    relationship = Relationship(Variable(), Variable())
    relationship.get_uuid() is not None


def test_should_automatically_subscribe_to_variables():
    var1 = Variable()
    var2 = Variable()
    relationship = Relationship(var1, var2)
    assert var1.subscribers[relationship.get_uuid()] is not None
    assert var2.subscribers[relationship.get_uuid()] is not None
