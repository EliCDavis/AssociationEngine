from Relationship.MockRelationship import MockRelationship
from Relationship.Variable import Variable


def test_should_have_correlation_coefficient_as_none_on_initialization():
    relationship = MockRelationship(Variable(), Variable())
    assert relationship.get_correlation_coefficient() is None


def test_should_update_correlation_coefficient():
    relationship = MockRelationship(Variable(), Variable())
    relationship.set_correlation_coefficient(1)
    assert relationship.get_correlation_coefficient() is 1
