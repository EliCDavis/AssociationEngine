from Snapper.AssociationMatrix import AssociationMatrix
from Relationship.Relationship import Relationship
from Relationship.Variable import Variable
from unittest.mock import MagicMock
import pytest


@pytest.fixture()
def rel_25():
    rel = Relationship(Variable(), Variable())
    rel.get_correlation_coefficient = MagicMock(return_value=0.25)
    return rel


@pytest.fixture()
def rel_50():
    rel = Relationship(Variable(), Variable())
    rel.get_correlation_coefficient = MagicMock(return_value=0.5)
    return rel


@pytest.fixture()
def rel_75():
    rel = Relationship(Variable(), Variable())
    rel.get_correlation_coefficient = MagicMock(return_value=0.75)
    return rel


def test_should_have_relationships_field_as_empty_dictionary_on_init():
    associationMatrix = AssociationMatrix()
    assert associationMatrix.relationships == dict()


def test_should_add_relationship_to_relationships():
    Vx = Variable()
    Vy = Variable()
    Rxy = Relationship(Vx, Vy)
    Am = AssociationMatrix()
    Am.add_relationship(Rxy)
    assert Am.relationships == {frozenset((Vx.uuid, Vy.uuid)): Rxy}


def test_should_remove_specified_relationship():
    Vx = Variable()
    Vy = Variable()
    Rxy = Relationship(Vx, Vy)
    Rwz = Relationship(Variable(), Variable())
    Am = AssociationMatrix()
    Am.add_relationship(Rxy)
    Am.add_relationship(Rwz)
    Am.remove_relationship(Rwz)
    assert Am.relationships == {frozenset((Vx.uuid, Vy.uuid)): Rxy}


def test_should_return_whole_dict():
    Rxy = Relationship(Variable(), Variable())
    Rwz = Relationship(Variable(), Variable())
    Am = AssociationMatrix()
    Am.add_relationship(Rxy)
    Am.add_relationship(Rwz)
    key1 = frozenset((Rxy.sensor_x.get_uuid(), Rxy.sensor_y.get_uuid()))
    key2 = frozenset((Rwz.sensor_x.get_uuid(), Rwz.sensor_y.get_uuid()))
    a = Am.get_value_matrix()
    assert a == {key1: None, key2: None}


def test_should_return_values_in_range(rel_25, rel_50, rel_75):
    association_matrix = AssociationMatrix()
    association_matrix.add_relationship(rel_25)
    association_matrix.add_relationship(rel_50)
    association_matrix.add_relationship(rel_75)
    min_val = 0.1
    max_val = 0.6
    sensor_pairs_in_range = \
        association_matrix.get_relationships_by_value_range(min_val, max_val)
    for key, value in sensor_pairs_in_range.items():
        assert min_val <= value <= max_val
