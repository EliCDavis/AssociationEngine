import pytest
import datetime

from AssociationEngine.Relationship.Frame import Frame


def test_should_not_allow_corr_greater_than_1():
    with pytest.raises(ValueError):
        frame = Frame(datetime.datetime.now())
        frame.add_correlation(1, 1.1)


def test_should_not_allow_corr_less_than_neg_1():
    with pytest.raises(ValueError):
        frame = Frame(datetime.datetime.now())
        frame.add_correlation(1, -1.1)


def test_should_not_allow_negative_durations():
    with pytest.raises(ValueError):
        frame = Frame(datetime.datetime.now())
        frame.add_correlation(-1, 1)


def test_should_avg_pos_when_duration_is_longer():
    frame = Frame(datetime.datetime.now())
    frame.add_correlation(4, 1)
    frame.add_correlation(1, -1)
    assert frame.get_final_correlation() == .6


def test_should_avg_to_0_when_equal_opposite_corr_are_added():
    frame = Frame(datetime.datetime.now())
    frame.add_correlation(1, 1)
    frame.add_correlation(1, -1)
    assert frame.get_final_correlation() == 0
