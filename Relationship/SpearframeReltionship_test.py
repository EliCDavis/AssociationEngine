from .SpearframeRelationship import SpearframeRelationship
from.Variable import Variable


def test_should_initialize_empty_frames():
    rel = SpearframeRelationship(Variable(), Variable())
    assert len(rel.frames) == 0
