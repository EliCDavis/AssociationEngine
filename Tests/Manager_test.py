from Snapper.Manager import Manager


def test_should_initialize_object():
    manager = Manager()
    assert isinstance(manager, Manager)
