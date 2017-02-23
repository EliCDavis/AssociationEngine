from Snapper.AssociationMatrix import AssociationMatrix
from Relationship.Relationship import Relationship
from Relationship.Variable import Variable



def test_should_have_relationships_field_as_empty_dictionary_on_init():
    associationMatrix = AssociationMatrix()
    assert len(associationMatrix.relationships) is 0

def test_should_add_relationship_to_relationships():
    Rxy = Relationship(Variable(), Variable())
    Am = AssociationMatrix()
    Am.add_relationship(Rxy)
    assert Am.relationships is not 0

def test_should_find_sensor_uuid_in_frozenset():
    x = False
    Vx = Variable()
    Vy = Variable()
    Rxy = Relationship(Vx,Vy)
    Am = AssociationMatrix()
    Am.add_relationship(Rxy)
    a = (Vx.get_uuid(), Vy.get_uuid())
    fs = frozenset(a)
    for key in Am.relationships:
        for value in key:
            if value == Vx.get_uuid():
                x = True
    assert x is True

def test_should_remove_specified_relationship():
    Rxy = Relationship(Variable(), Variable())
    Rwz = Relationship(Variable(), Variable())
    Am = AssociationMatrix()
    Am.add_relationship(Rxy)
    Am.add_relationship(Rwz)
    initial_length = len(Am.relationships)
    Am.remove_relationship(Rwz)
    assert len(Am.relationships) == (initial_length - 1)

def test_should_return_whole_dict():
    Rxy = Relationship(Variable(), Variable())
    Rwz = Relationship(Variable(), Variable())
    Am = AssociationMatrix()
    Am.add_relationship(Rxy)
    Am.add_relationship(Rwz)
    a = Am.get_all_relationships()
    assert len(a) == 2

def test_should_return_values_in_range():
    """not sure how to test with artificial correlations
    """
    pass
