from .AssociationMatrix import AssociationMatrix

def test_should_have_relationships_field_as_empty_dictionary_on_init():
    associationMatrix = AssociationMatrix()
    assert associationMatrix.relationships is {}