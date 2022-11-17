import pytest
from math import sqrt, radians, degrees
from util_objects import *


def test_quadrant_zero():
    assert Velocity.quadrant_from_components(1, 1) == 0
    assert Velocity.quadrant_from_components(1, 10) == 0
    assert Velocity.quadrant_from_components(10, 1) == 0
    assert Velocity.quadrant_from_components(0, 0) == 0


def test_quadrant_one():
    assert Velocity.quadrant_from_components(-1, 1) == 1
    assert Velocity.quadrant_from_components(-1, 10) == 1
    assert Velocity.quadrant_from_components(-10, 1) == 1


def test_quadrant_two():
    assert Velocity.quadrant_from_components(-1, -1) == 2
    assert Velocity.quadrant_from_components(-1, -10) == 2
    assert Velocity.quadrant_from_components(-10, -1) == 2


def test_quadrant_three():
    assert Velocity.quadrant_from_components(1, -1) == 3
    assert Velocity.quadrant_from_components(1, -10) == 3
    assert Velocity.quadrant_from_components(10, -1) == 3


def test_angle_from_components_q0():
    cases = [ # (x, y), degrees, test #
        ((1, 0                 ), 0,  1),
        ((sqrt(3)/2, 1/2       ), 30, 2),
        ((sqrt(2)/2, sqrt(2)/2 ), 45, 3),
        ((1/2, sqrt(3)/2       ), 60, 4),
        ((0, 1                 ), 90, 5)
    ]
    for case, corr_answer, test_num in cases:
        answer = Velocity.angle_from_components(*case)
        assert answer == pytest.approx(radians(corr_answer)),\
            f"{test_num}:{case} != {corr_answer}, actually {degrees(answer)}"

def test_angle_from_components_q1():
    cases = [ # (x, y), degrees, test #
        ((-1/2, sqrt(3)/2       ), 120, 1),
        ((-sqrt(2)/2, sqrt(2)/2 ), 135, 2),
        ((-sqrt(3)/2, 1/2       ), 150, 3),
        ((-1, 0                 ), 180, 4)
    ]
    for case, corr_answer, test_num in cases:
        answer = Velocity.angle_from_components(*case)
        assert answer == pytest.approx(radians(corr_answer)),\
            f"{test_num}:{case} != {corr_answer}, actually {degrees(answer)}"

    # assert Velocity.angle_from_components(-1/2, sqrt(3)/2) == pytest.approx(radians(120))
    # assert Velocity.angle_from_components(-sqrt(2)/2, sqrt(2)/2) == pytest.approx(radians(135))
    # assert Velocity.angle_from_components(-sqrt(3)/2, 1/2) == pytest.approx(radians(150))
    # assert Velocity.angle_from_components(-1, 0) == pytest.approx(radians(180))


def test_angle_from_components_q2():
    cases = [ # (x, y), degrees, test #
        ((-sqrt(3)/2, -1/2       ), 210, 1),
        ((-sqrt(2)/2, -sqrt(2)/2 ), 225, 2),
        ((-1/2, -sqrt(3)/2       ), 240, 3),
        ((0, -1                  ), 270, 4)
    ]
    for case, corr_answer, test_num in cases:
        answer = Velocity.angle_from_components(*case)
        assert answer == pytest.approx(radians(corr_answer)),\
            f"{test_num}:{case} != {corr_answer}, actually {degrees(answer)}"

    # assert Velocity.angle_from_components(-sqrt(3)/2, -1/2) == pytest.approx(radians(210))
    # assert Velocity.angle_from_components(-sqrt(2)/2, -sqrt(2)/2) == pytest.approx(radians(225))
    # assert Velocity.angle_from_components(-1/2, -sqrt(3)/2) == pytest.approx(radians(240))
    # assert Velocity.angle_from_components(0, -1) == pytest.approx(radians(270))


def test_angle_from_components_q3():
    cases = [ # (x, y), degrees, test #
        ((1/2, -sqrt(3)/2       ), 300, 1),
        ((sqrt(2)/2, -sqrt(2)/2 ), 315, 2),
        ((sqrt(3)/2, -1/2       ), 330, 3)
    ]
    for case, corr_answer, test_num in cases:
        answer = Velocity.angle_from_components(*case)
        assert answer == pytest.approx(radians(corr_answer)),\
            f"{test_num}:{case} != {corr_answer}, actually {degrees(answer)}"

    # assert Velocity.angle_from_components(sqrt(3)/2, -1/2) == pytest.approx(radians(300))
    # assert Velocity.angle_from_components(sqrt(2)/2, -sqrt(2)/2) == pytest.approx(radians(315))
    # assert Velocity.angle_from_components(1/2, -sqrt(3)/2) == pytest.approx(radians(330))


def test_scalar_from_components():
    """Using Pythagorean Triples"""
    assert Velocity.scalar_from_components(sqrt(2) / 2, sqrt(2) / 2) == 1
    assert Velocity.scalar_from_components(3, 4) == 5
    assert Velocity.scalar_from_components(5, 12) == 13
    assert Velocity.scalar_from_components(8, 15) == 17


def test_velocity_flip_x_60():
    v = Velocity(scalar=1, degrees=60)
    assert v.x == pytest.approx(0.5)
    assert v.y == pytest.approx(sqrt(3)/2)
    assert v.degrees == pytest.approx(60)

    v.flip_x()

    assert v.x == pytest.approx(-0.5)
    assert v.y == pytest.approx(sqrt(3)/2)
    assert v.degrees == pytest.approx(120)


def test_velocity_flip_x_0():
    v = Velocity(scalar=1, degrees=0)
    assert v.x == pytest.approx(1)
    assert v.y == pytest.approx(0)
    assert v.degrees == pytest.approx(0)

    v.flip_x()

    assert v.x == pytest.approx(-1)
    assert v.y == pytest.approx(0)
    assert v.degrees == pytest.approx(180)


def test_velocity_flip_y_60():
    v = Velocity(scalar=1, degrees=60)
    assert v.x == pytest.approx(0.5)
    assert v.y == pytest.approx(sqrt(3)/2)
    assert v.degrees == pytest.approx(60)

    v.flip_y()

    assert v.x == pytest.approx(0.5)
    assert v.y == pytest.approx(-sqrt(3)/2)
    assert v.degrees == pytest.approx(300)


def test_velocity_flip_y_0():
    v = Velocity(scalar=1, degrees=90)
    assert v.x == pytest.approx(0)
    assert v.y == pytest.approx(1)
    assert v.degrees == pytest.approx(90)

    v.flip_y()

    assert v.x == pytest.approx(0)
    assert v.y == pytest.approx(-1)
    assert v.degrees == pytest.approx(270)


def test_subtract():
    one = Coord(3, 6)
    two = Coord(7, 9)
    res = one - two

    assert res.x == -4
    assert res.y == -3


def test_add():
    one = Coord(3, 6)
    two = Coord(7, 9)
    res = one + two

    assert res.x == 10
    assert res.y == 15


def test_abs():
    one = Coord(-3, -5)
    res = abs(one)

    assert res.x == 3
    assert res.y == 5


def test_dropping_stack():
    a = DroppingStack(3)
    assert a.arr == []

    a.put(3)
    assert a.arr == [3], a.arr

    a.put(2)
    a.put(1)
    assert a.arr == [3,2,1], a.arr

    a.put(0)
    assert a.arr == [2,1,0], a.arr

    a.put(-1)
    assert a.arr == [1,0,-1], a.arr

