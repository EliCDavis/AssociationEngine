from Snapper.AssociationMatrix import AssociationMatrix
from Relationship.Relationship import Relationship
from Relationship.Variable import Variable


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


def test_should_return_values_in_range():
    """not sure how to test with artificial correlations
    """
    pass
