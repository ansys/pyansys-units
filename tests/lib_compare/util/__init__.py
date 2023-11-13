import math

one_degree_in_radians = (2.0 * math.pi) / 360.0


def assert_rightly_but_fail(cond, test):
    assert not cond, f"{test} didn't fail as expected!"


def assert_wrongly(cond, test):
    assert cond, f"{test}, which is wrong, was expected to pass but failed"
