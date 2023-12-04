from secret_santa import *

def test_pair_lengts():
    c = 100
    participants = list(range(c))
    assert len(create_pairs(participants)) == c


def test_pair_equivalence():
    participants = list(range(100))
    out = create_pairs(participants)
    gifters, receivers = zip(*out)
    assert set(gifters) == set(receivers)


def test_pair_uniqueness():
    participants = list(range(100))
    out = create_pairs(participants)
    gifters, receivers = zip(*out)
    assert set(participants) == set(gifters)
    assert set(participants) == set(receivers)


def test_proper_assignment():
    participants = list(range(100))
    assert all(santa != receiver for santa, receiver in create_pairs(participants))

