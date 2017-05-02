from unittest.mock import MagicMock, Mock
from AssociationEngine.Relationship.Variable import Variable


def test_variable_can_add_and_remove_subscribers():
    var = Variable()
    rel = Mock()
    rel.get_uuid = MagicMock(return_value="abcd")
    var.add_subscriber(rel)
    assert var.subscribers["abcd"] is rel
    var.remove_subscriber("abcd")
    assert not var.subscribers
