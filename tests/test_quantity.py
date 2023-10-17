import math

import pytest

import ansys.units as ansunits

DELTA = 1.0e-5


def test_properties_1():
    v = ansunits.Quantity(10.6, "m")
    assert v.value == 10.6
    assert v.units == "m"
    assert v.si_value == 10.6
    assert v.si_units == "m"


def test_properties_2():
    v = ansunits.Quantity(1, "ft s^-1")
    assert v.value == 1
    assert v.units == "ft s^-1"
    assert v.si_value == pytest.approx(0.30479999, DELTA)
    assert v.si_units == "m s^-1"


def test_properties_3():
    v = ansunits.Quantity(1.0, "farad")
    assert v.value == 1.0
    assert v.units == "farad"
    assert v.si_value == 1.0
    assert v.si_units == "kg^-1 m^-2 s^4 A^2"


def test_value():
    v = ansunits.Quantity(1, "m")
    v.value = 20
    assert v.value == 20
    assert v.units == "m"


def test_dimensions_1():
    dims = ansunits.BaseDimensions
    v = ansunits.Quantity(1.0, "ft")
    assert v.dimensions == ansunits.Dimensions({dims.LENGTH: 1.0})


def test_dimensions_2():
    dims = ansunits.BaseDimensions
    v = ansunits.Quantity(1.0, "kPa")
    assert v.dimensions == ansunits.Dimensions(
        {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0}
    )


def test_dimensions_3():
    dims = ansunits.BaseDimensions
    v = ansunits.Quantity(1.0, "slug ft s R delta_K radian slugmol cd A sr")
    assert v.dimensions == ansunits.Dimensions(
        {
            dims.MASS: 1.0,
            dims.LENGTH: 1.0,
            dims.TIME: 1.0,
            dims.TEMPERATURE: 1.0,
            dims.TEMPERATURE_DIFFERENCE: 1.0,
            dims.ANGLE: 1.0,
            dims.CHEMICAL_AMOUNT: 1.0,
            dims.LIGHT: 1.0,
            dims.CURRENT: 1.0,
            dims.SOLID_ANGLE: 1.0,
        }
    )


def test_to_1():
    v = ansunits.Quantity(1.0, "m")
    to = v.to("ft")
    assert to.value == pytest.approx(3.2808398, DELTA)
    assert to.units == "ft"


def test_to_2():
    v = ansunits.Quantity(1.0, "m")
    to = v.to("mm")
    assert to.value == 1000
    assert to.units == "mm"


def test_to_3():
    v = ansunits.Quantity(100000.0, "Pa")
    to = v.to("kPa")
    assert to.value == 100.0
    assert to.units == "kPa"


def test_to_4():
    v = ansunits.Quantity(1.0, "dm^3")
    to = v.to("m^3")
    assert to.value == pytest.approx(0.001, DELTA)
    assert to.units == "m^3"


def test_to_5():
    v = ansunits.Quantity(1.0, "radian")
    to = v.to("degree")
    assert to.value == pytest.approx(57.295779, DELTA)
    assert to.units == "degree"


def test_to_6():
    v = ansunits.Quantity(1.0, "degree")
    to = v.to("radian")
    assert to.value == pytest.approx(0.01745329251, DELTA)
    assert to.units == "radian"


def test_to_7():
    v = ansunits.Quantity(1.0, "Pa s")
    to = v.to("dyne cm^-2 s")
    assert to.value == pytest.approx(10.0, DELTA)
    assert to.units == "dyne cm^-2 s"


def test_to_8():
    v = ansunits.Quantity(1.0, "kg m^-1 s^-1")
    to = v.to("dyne cm^-2 s")
    assert to.value == pytest.approx(10.0, DELTA)
    assert to.units == "dyne cm^-2 s"


def test_to_9():
    v = ansunits.Quantity(1.0, "Pa s")
    to = v.to("slug in^-1 s^-1")
    assert to.value == pytest.approx(0.00174045320, DELTA)
    assert to.units == "slug in^-1 s^-1"


def test_to_10():
    v = ansunits.Quantity(1.0, "kg m^-1 s^-1")
    to = v.to("slug in^-1 s^-1")
    assert to.value == pytest.approx(0.00174045320, DELTA)
    assert to.units == "slug in^-1 s^-1"


def test_to_11():
    v = ansunits.Quantity(1.0, "lb ft^-1 s^-1")
    to = v.to("Pa s")
    assert to.value == pytest.approx(1.488164, DELTA)
    assert to.units == "Pa s"


def test_to_12():
    v = ansunits.Quantity(1.0, "lb ft^-1 s^-1")
    to = v.to("kg m^-1 s^-1")
    assert to.value == pytest.approx(1.488164, DELTA)
    assert to.units == "kg m^-1 s^-1"


def test_to_13():
    v = ansunits.Quantity(1.0, "Hz")
    with pytest.raises(ansunits.QuantityError) as e:
        to = v.to("radian s^-1")


def test_to_14():
    v = ansunits.Quantity(1.0, "radian s^-1")
    with pytest.raises(ansunits.QuantityError) as e:
        to = v.to("Hz")


def test_to_15():
    v = ansunits.Quantity(1.0, "lbf ft^-2")
    to = v.to("N m^-2")
    assert to.value == pytest.approx(47.88024159, DELTA)
    assert to.units == "N m^-2"


def test_to_16():
    v = ansunits.Quantity(1.0, "ft^-3 s^-1")
    to = v.to("m^-3 s^-1")
    assert to.value == pytest.approx(35.3146667, DELTA)
    assert to.units == "m^-3 s^-1"


def test_to_17():
    v = ansunits.Quantity(1.0, "m^-2")
    to = v.to("cm^-2")
    assert to.value == pytest.approx(0.0001, DELTA)
    assert to.units == "cm^-2"


def test_to_18():
    v = ansunits.Quantity(1.0, "m^2")
    to = v.to("in^2")
    assert to.value == pytest.approx(1550.0031, DELTA)
    assert to.units == "in^2"


def test_to_19():
    v = ansunits.Quantity(1.0, "radian s^-1")
    to = v.to("degree s^-1")
    assert to.value == pytest.approx(57.295779, DELTA)
    assert to.units == "degree s^-1"


def test_to_20():
    v = ansunits.Quantity(1.0, "degree s^-1")
    to = v.to("radian s^-1")
    assert to.value == pytest.approx(0.01745329251, DELTA)
    assert to.units == "radian s^-1"


def test_to_21():
    v = ansunits.Quantity(1.0, "dyne cm^-2")
    to = v.to("N m^-2")
    assert to.value == pytest.approx(0.1, DELTA)
    assert to.units == "N m^-2"


def test_to_22():
    v = ansunits.Quantity(1.0, "psi")
    to = v.to("Pa")
    assert to.value == pytest.approx(6894.76, DELTA)
    assert to.units == "Pa"


def test_to_23():
    v = ansunits.Quantity(1.0, "pdl")
    to = v.to("N")
    assert to.value == pytest.approx(0.138254999, DELTA)
    assert to.units == "N"


def test_to_24():
    v = ansunits.Quantity(1.0, "ohm cm")
    to = v.to("ohm m")
    assert to.value == pytest.approx(0.01, DELTA)
    assert to.units == "ohm m"


def test_to_25():
    v = ansunits.Quantity(1.0, "erg")
    to = v.to("J")
    assert to.value == pytest.approx(1.0e-7, DELTA)
    assert to.units == "J"


def test_to_26():
    v = ansunits.Quantity(1.0, "BTU")
    to = v.to("J")
    assert to.value == pytest.approx(1055.056, DELTA)
    assert to.units == "J"


def test_to_27():
    v = ansunits.Quantity(1.0, "gal")
    to = v.to("m^3")
    assert to.value == pytest.approx(0.00378541, DELTA)
    assert to.units == "m^3"


def test_to_28():
    v = ansunits.Quantity(1.0, "l")
    to = v.to("m^3")
    assert to.value == pytest.approx(0.001, DELTA)
    assert to.units == "m^3"


def test_to_29():
    v = ansunits.Quantity(1.0, "BTU lb^-1 R^-1")
    to = v.to("J kg^-1 K^-1")
    assert to.value == pytest.approx(4186.8161854, DELTA)
    assert to.units == "J kg^-1 K^-1"


def test_to_30():
    v = ansunits.Quantity(1.0, "BTU lb^-1 F^-1")
    to = v.to("J kg^-1 K^-1")
    assert to.value == pytest.approx(4186.8161854, DELTA)
    assert to.units == "J kg^-1 K^-1"


def test_to_31():
    v = ansunits.Quantity(1.0, "gal^-1")
    to = v.to("m^-3")
    assert to.value == pytest.approx(264.172, DELTA)
    assert to.units == "m^-3"


def test_to_32():
    v = ansunits.Quantity(1.0, "BTU ft^-2")
    to = v.to("J m^-2")
    assert to.value == pytest.approx(11356.5713242, DELTA)
    assert to.units == "J m^-2"


def test_to_33():
    v = ansunits.Quantity(2.0, "radian")
    with pytest.raises(ansunits.QuantityError) as e:
        convert = v.to(0)


def test_temperature_to():
    dims = ansunits.BaseDimensions
    t1 = ansunits.Quantity(273.15, "K")
    t1C = t1.to("C")
    assert t1C.dimensions == ansunits.Dimensions({dims.TEMPERATURE: 1.0})
    assert t1C.value == 0.0
    assert t1C.units == "C"


def test_temperature_difference_to_with_explicit_delta():
    dims = ansunits.BaseDimensions
    t1 = ansunits.Quantity(1.0, "K")
    t2 = ansunits.Quantity(2.0, "K")
    td1 = t2 - t1
    td1C = td1.to("delta_C")
    assert td1C.dimensions == ansunits.Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})
    assert td1C.value == 1.0
    assert td1C.units == "delta_C"
    td2 = t1 - t2
    td2C = td2.to("delta_C")
    assert td2C.dimensions == ansunits.Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})
    assert td2C.value == -1.0
    assert td2C.units == "delta_C"


def test_temperature_difference_to_with_implicit_delta():
    dims = ansunits.BaseDimensions
    t1 = ansunits.Quantity(1.0, "K")
    t2 = ansunits.Quantity(2.0, "K")
    td1 = t2 - t1
    td1C = td1.to("delta_C")
    assert td1C.dimensions == ansunits.Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})
    assert td1C.value == 1.0
    assert td1C.units == "delta_C"
    td2 = t1 - t2
    td2C = td2.to("delta_C")
    assert td2C.dimensions == ansunits.Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})
    assert td2C.value == -1.0
    assert td2C.units == "delta_C"


def test_complex_temperature_difference_to():
    t1 = ansunits.Quantity(1.0, "K")
    t2 = ansunits.Quantity(2.0, "K")
    m = ansunits.Quantity(1.0, "kg")
    result = m * (t2 - t1)
    resultC1 = result.to("kg C")
    assert resultC1.value == 1.0
    assert resultC1.units == "kg C"
    resultC2 = result.to("kg delta_C")
    assert resultC2.value == 1.0
    assert resultC2.units == "kg delta_C"


def test_repr():
    v = ansunits.Quantity(1.0, "m")
    assert v.__repr__() == 'Quantity (1.0, "m")'


def test_math():
    deg = ansunits.Quantity(90, "degree")
    assert math.sin(deg) == 1.0

    rad = ansunits.Quantity(math.pi / 2, "radian")
    assert math.sin(rad) == 1.0

    root = ansunits.Quantity(100.0, "")
    assert math.sqrt(root) == 10.0


def test_subtraction():
    q1 = ansunits.Quantity(10.0, "m s^-1")
    q2 = ansunits.Quantity(5.0, "m s^-1")

    assert float(q1 - q2) == 5.0
    assert float(q2 - q1) == -5.0
    assert float(q1) - 2.0 == 8.0
    assert 2.0 - float(q1) == -8.0
    assert float(q1) - 3 == 7.0
    assert 3 - float(q1) == -7.0


def test_pow():
    q1 = ansunits.Quantity(10.0, "m s^-1")
    q2 = ansunits.Quantity(5.0, "ft")

    q1_sq = q1**2
    assert q1_sq.units == "m^2 s^-2"
    assert q1_sq.value == 100
    q2_sq = q2**2
    assert q2_sq.units == "m^2"
    assert q2_sq.value == pytest.approx(2.3225759999999993, DELTA)

    assert float(q1) ** 2 == 100.0
    assert float(q2) ** 2 == pytest.approx(2.3225759999999993, DELTA)


def test_neg():
    q0 = ansunits.Quantity(10.0, "m s^-1")
    q1 = -q0
    assert q1.value == -10.0


def test_neq():
    x = ansunits.Quantity(10.5, "cm")
    y = ansunits.Quantity(10.5, "m")
    z = ansunits.Quantity(10.5, "g")
    r = ansunits.Quantity(10.5, "")

    assert y != x
    assert x != y

    assert r != 0.5
    assert 0.5 != r


def test_eq_1():
    q1 = ansunits.Quantity(10.0, "m s^-1")
    q2 = ansunits.Quantity(5.0, "m s^-1")
    q3 = ansunits.Quantity(10.0, "m s^-1")
    q4 = ansunits.Quantity(10.0, "")

    assert q1 != q2
    assert q1 == q3
    assert float(q1) == 10.0
    assert q4 == 10.0


def test_eq_2():
    x = ansunits.Quantity(10.5, "cm")
    y = ansunits.Quantity(10.5, "m")
    z = ansunits.Quantity(10.5, "g")
    r = ansunits.Quantity(10.5, "")

    l = ansunits.Quantity(10.5, "cm")
    m = ansunits.Quantity(10.5, "m")
    n = ansunits.Quantity(10.5, "")

    assert x == l
    assert y == m
    assert r == n

    with pytest.raises(ansunits.QuantityError) as e_info:
        assert z == x
        assert y == x
        assert r == 0.5
        assert 5.0 == x


def test_rdiv():
    q1 = ansunits.Quantity(10.0, "m s^-1")
    q2 = ansunits.Quantity(5.0, "m s^-1")

    assert float(q1) / float(q2) == 2.0
    assert float(q2) / float(q1) == 0.5
    assert float(q1) / 2 == 5.0
    assert 2.0 / float(q1) == 0.2


def test_power():
    qt = ansunits.Quantity(5.0, "m^0")
    qtm = qt * 2

    assert qtm.value == 10.0
    assert qtm.dimensions == ansunits.Dimensions()
    assert qtm.units == ""


def test_ge():
    x = ansunits.Quantity(10.5, "cm")
    y = ansunits.Quantity(10.5, "m")
    z = ansunits.Quantity(10.5, "g")
    r = ansunits.Quantity(10.5, "")

    assert y >= x
    assert 15.7 >= r
    assert r >= 7.8

    with pytest.raises(ansunits.QuantityError) as e_info:
        assert x >= z
        assert x >= y
        assert 5.0 >= r
        assert x >= 5.0


def test_gt():
    x = ansunits.Quantity(10.5, "cm")
    y = ansunits.Quantity(10.5, "m")
    z = ansunits.Quantity(10.5, "g")
    r = ansunits.Quantity(10.5, "")

    assert y > x
    assert 15.7 > r
    assert r > 7.8

    with pytest.raises(ansunits.QuantityError) as e_info:
        assert x > z
        assert x > y
        assert 5.0 > r
        assert x > 5.0


def test_lt():
    x = ansunits.Quantity(10.5, "cm")
    y = ansunits.Quantity(10.5, "m")
    z = ansunits.Quantity(10.5, "g")
    r = ansunits.Quantity(10.5, "")

    assert x < y
    assert r < 15.7
    assert 7.8 < r

    with pytest.raises(ansunits.QuantityError) as e_info:
        assert z < x
        assert y < x
        assert r < 0.5
        assert 5.0 < x


def test_le():
    x = ansunits.Quantity(10.5, "cm")
    y = ansunits.Quantity(10.5, "m")
    z = ansunits.Quantity(10.5, "g")
    r = ansunits.Quantity(10.5, "")

    assert x <= y
    assert r <= 15.7
    assert 7.8 <= r

    with pytest.raises(ansunits.QuantityError) as e_info:
        assert z <= x
        assert y <= x
        assert r <= 0.5
        assert 5.0 <= x


def test_temp_1():
    k = ansunits.Quantity(-40, "K")

    kc = k.to("C")
    assert kc.value == -313.15
    assert kc.units == "delta_C"

    kc = k.to("R")
    assert kc.value == pytest.approx(-72.0, DELTA)
    assert kc.units == "delta_R"

    kc = k.to("F")
    assert kc.value == pytest.approx(-531.67, DELTA)
    assert kc.units == "delta_F"


def test_temp_2():
    mk = ansunits.Quantity(-40000.0, "mK")
    uc = mk.to("uC^1")
    assert uc.value == -40000000.0


def test_temp_3():
    k = ansunits.Quantity(1.0, "K")

    f = k.to("F")
    r = k.to("R")
    c = k.to("C")

    assert f.value == pytest.approx(-457.87, DELTA)
    assert r.value == pytest.approx(1.8, DELTA)
    assert c.value == pytest.approx(-272.15, DELTA)


def test_temp_4():
    c = ansunits.Quantity(1.0, "C")

    f = c.to("F")
    r = c.to("R")
    k = c.to("K")

    assert f.value == pytest.approx(33.80, DELTA)
    assert r.value == pytest.approx(493.469, DELTA)
    assert k.value == 274.15


def test_temp_5():
    r = ansunits.Quantity(1.0, "R")

    f = r.to("F")
    c = r.to("C")
    k = r.to("K")

    assert f.value == pytest.approx(-458.6699, DELTA)
    assert c.value == pytest.approx(-272.5944, DELTA)
    assert k.value == pytest.approx(0.555556, DELTA)


def test_temp_6():
    f = ansunits.Quantity(1.0, "F")

    c = f.to("C")
    r = f.to("R")
    k = f.to("K")

    assert c.value == pytest.approx(-17.2222, DELTA)
    assert r.value == pytest.approx(460.670, DELTA)
    assert k.value == pytest.approx(255.927, DELTA)


def test_temp_7():
    hc = ansunits.Quantity(1.0, "J g^-1 K^-1")

    hcto1 = hc.to("kJ kg^-1 K^-1")

    assert hcto1.value == pytest.approx(1.0, DELTA)
    assert hcto1.units == "kJ kg^-1 K^-1"

    hcto2 = hc.to("J kg^-1 C^-1")

    assert hcto2.value == pytest.approx(1000.0, DELTA)
    assert hcto2.units == "J kg^-1 C^-1"

    hcto3 = hc.to("kJ kg^-1 C^-1")

    assert hcto3.value == pytest.approx(1.0, DELTA)
    assert hcto3.units == "kJ kg^-1 C^-1"

    hcto4 = hc.to("cal g^-1 C^-1")

    assert hcto4.value == pytest.approx(0.2390057, DELTA)
    assert hcto4.units == "cal g^-1 C^-1"

    hcto5 = hc.to("cal kg^-1 C^-1")

    assert hcto5.value == pytest.approx(239.0057, DELTA)
    assert hcto5.units == "cal kg^-1 C^-1"

    hcto6 = hc.to("kcal kg^-1 C^-1")

    assert hcto6.value == pytest.approx(0.2390057, DELTA)
    assert hcto6.units == "kcal kg^-1 C^-1"

    hcto7 = hc.to("BTU lb^-1 F^-1")

    assert hcto7.value == pytest.approx(0.238845, DELTA)
    assert hcto7.units == "BTU lb^-1 F^-1"


def test_temp_8():
    temp_var = ansunits.Quantity(1.0, "kg m^-3 s^-1 K^2")

    temp_varto1 = temp_var.to("g cm^-3 s^-1 K^2")

    assert temp_varto1.value == pytest.approx(0.001, DELTA)
    assert temp_varto1.units == "g cm^-3 s^-1 K^2"

    temp_varto2 = temp_var.to("kg mm^-3 s^-1 K^2")

    assert temp_varto2.value == pytest.approx(1e-09, DELTA)
    assert temp_varto2.units == "kg mm^-3 s^-1 K^2"

    temp_varto3 = temp_var.to("kg um^-3 s^-1 K^2")

    assert temp_varto3.value == pytest.approx(9.999999999999999e-19, DELTA)
    assert temp_varto3.units == "kg um^-3 s^-1 K^2"

    temp_varto4 = temp_var.to("mg mm^-3 ms^-1 K^2")

    assert temp_varto4.value == pytest.approx(1.0000000000000002e-06, DELTA)
    assert temp_varto4.units == "mg mm^-3 ms^-1 K^2"

    temp_varto5 = temp_var.to("g cm^-3 us^-1 K^2")

    assert temp_varto5.value == pytest.approx(1e-09, DELTA)
    assert temp_varto5.units == "g cm^-3 us^-1 K^2"

    temp_varto6 = temp_var.to("pg um^-3 ms^-1 K^2")

    assert temp_varto6.value == pytest.approx(9.999999999999997e-07, DELTA)
    assert temp_varto6.units == "pg um^-3 ms^-1 K^2"


def test_temp_inverse_1():
    c = ansunits.Quantity(2.0, "C")
    assert float(c) == 275.15

    c_inverse = ansunits.Quantity(2.0, "C^-1")
    assert float(c_inverse) == 2.0


def test_temp_inverse_2():
    f = ansunits.Quantity(2.0, "F")
    assert float(f) == pytest.approx(256.483311, DELTA)

    f_inverse = ansunits.Quantity(2.0, "F^-1")
    assert float(f_inverse) == pytest.approx(3.5999999999999996, DELTA)


def test_temp_difference():
    dims = ansunits.BaseDimensions
    td1 = ansunits.Quantity(150.0, "delta_C")
    assert td1.dimensions == ansunits.Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})

    td2 = ansunits.Quantity(100.0, "delta_C")
    assert td2.dimensions == ansunits.Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})

    td = td1 - td2
    assert td.dimensions == ansunits.Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})

    td_m = td * 2
    assert td_m.units == "delta_K"
    assert td_m.dimensions == ansunits.Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})

    t1 = ansunits.Quantity(150.0, "C")
    assert t1.dimensions == ansunits.Dimensions({dims.TEMPERATURE: 1.0})

    t2 = ansunits.Quantity(100.0, "C")
    assert t2.dimensions == ansunits.Dimensions({dims.TEMPERATURE: 1.0})

    td = t1 - t2
    assert td.dimensions == ansunits.Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})

    td2 = t2 - t1
    assert td2.dimensions == ansunits.Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})

    tc1 = ansunits.Quantity(100.0, "C")
    td1 = ansunits.Quantity(50.0, "C^-1")

    with pytest.raises(ValueError) as e:
        t = tc1 + td1


def test_temp_diff_combined_multiply():
    k = ansunits.Quantity(1.38e-23, "J K^-1")
    t = ansunits.Quantity(4.0, "K")
    e = k * t
    assert e.value == 5.52e-23
    assert e.units == "kg m^2 s^-2"


def test_temp_diff_combined_multiply_2():
    q1 = ansunits.Quantity(2.0, "J K^-2")
    q2 = ansunits.Quantity(4.0, "K")
    res = q1 * q2
    assert res.value == 8.0
    assert res.units == "kg m^2 s^-2 K^-1"


def test_temp_diff_combined_inverse():
    t = ansunits.Quantity(4.0, "K")
    inv_t = 2.0 / t
    assert inv_t.value == 0.5
    assert inv_t.units == "K^-1"


def test_temp_diff_combined_divide():
    t = ansunits.Quantity(4.0, "K")
    t_div = t / 2.0
    assert t_div.value == 2.0
    assert t_div.units == "K"


def test_core_temp():
    dims = ansunits.BaseDimensions
    t1 = ansunits.Quantity(1.0, "K")
    assert float(t1) == 1.0

    t2 = ansunits.Quantity(2.0, "K")
    assert float(t2) == 2.0

    dt1 = t2 - t1
    assert float(dt1) == 1.0

    t3 = ansunits.Quantity(1.0, "C")
    assert float(t3) == 274.15

    t4 = ansunits.Quantity(2.0, "C")
    assert float(t4) == 275.15

    dt2 = t4 - t3
    assert float(dt2) == 1.0
    assert dt2.dimensions == ansunits.Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})

    invt1 = ansunits.Quantity(1.0, "K^-1")
    assert float(invt1) == 1.0

    dt3 = 1.0 / invt1
    assert float(dt3) == 1.0

    invt2 = ansunits.Quantity(1.0, "C^-1")
    assert float(invt2) == 1.0

    dt4 = 1.0 / invt2
    assert float(dt4) == 1.0


def test_temp_addition():
    t1 = ansunits.Quantity(150.0, "C")
    t2 = ansunits.Quantity(50.0, "C")

    td = t1 - t2
    assert td.units == "delta_C"
    assert float(td) == 100.0

    kd = ansunits.Quantity(50.0, "delta_C")
    k = ansunits.Quantity(50.0, "K")

    t = k + kd
    assert float(t) == 100.0
    assert t.units == "K"


def test_unit_from_dimensions_1():
    dims = ansunits.BaseDimensions
    p = ansunits.Quantity(
        10.5,
        dimensions=ansunits.Dimensions(
            {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0}
        ),
    )
    assert p.units == "kg m^-1 s^-2"


def test_unit_from_dimensions_2():
    dims = ansunits.BaseDimensions
    l = ansunits.Quantity(10.5, dimensions=ansunits.Dimensions({dims.LENGTH: 1.0}))
    assert l.units == "m"


def test_unit_from_dimensions_3():
    x = ansunits.Quantity(10.5, dimensions=ansunits.Dimensions())
    assert x.units == ""


def test_unit_from_dimensions_4():
    dims = ansunits.BaseDimensions
    test = ansunits.Quantity(
        10.5, dimensions=ansunits.Dimensions({dims.LENGTH: 1.0, dims.TIME: -1})
    )
    assert test.units == "m s^-1"
    assert test.dimensions == ansunits.Dimensions({dims.LENGTH: 1.0, dims.TIME: -1})


def test_unit_from_dimensions_5():
    dims = ansunits.BaseDimensions
    test = ansunits.Quantity(
        10.5, dimensions=ansunits.Dimensions({dims.LENGTH: 1.0, dims.TIME: -2})
    )
    assert test.units == "m s^-2"
    assert test.dimensions == ansunits.Dimensions({dims.LENGTH: 1.0, dims.TIME: -2})


def test_quantity_map_1():
    quantity_map_from_settings_API = {
        "Mass": 1,
        "Velocity": 2.5,
        "Current": 3,
        "Light": 1,
        "Epsilon Flux Coefficient": 2,
    }

    api_test = ansunits.Quantity(10.5, quantity_map=quantity_map_from_settings_API)
    assert api_test.value == 10.5
    assert api_test.units == "kg^3 m^-1.5 s^-6.5 A^3 cd"


def test_quantity_map_2():
    quantity_map_from_settings_API = {
        "Mass": 1,
        "Velocity": 2.5,
        "Current": 3,
        "Light": 2,
        "Epsilon Flux Coefficient": 2,
    }

    with pytest.raises(ValueError):
        api_test = ansunits.Quantity(
            10.5, units="kg m s^-1", quantity_map=quantity_map_from_settings_API
        )


def test_quantity_map_3():
    quantity_map_from_settings_API = {
        "Temperature": 1,
        "Pressure": 1,
        "Volume": 1,
    }

    api_test = ansunits.Quantity(10.5, quantity_map=quantity_map_from_settings_API)
    assert api_test.value == 10.5
    assert api_test.units == "K kg m^2 s^-2"


def testing_dimensions():
    print(f"{'*' * 25} {testing_dimensions.__name__} {'*' * 25}")
    dims = ansunits.BaseDimensions

    def dim_test(units, dim_dict):
        qt = ansunits.Quantity(10, units)
        print(f"{units} : {qt.dimensions}")
        assert qt.dimensions == ansunits.Dimensions(dim_dict)

    dim_test("m", {dims.LENGTH: 1.0})
    dim_test("m s^-1", {dims.LENGTH: 1.0, dims.TIME: -1.0})
    dim_test("kg m s^-2 m^-2", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("Pa", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("kPa", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("Pa^2", {dims.MASS: 2.0, dims.LENGTH: -2.0, dims.TIME: -4.0})
    dim_test("daPa", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("MPa", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("kPa^2", {dims.MASS: 2.0, dims.LENGTH: -2.0, dims.TIME: -4.0})
    dim_test("slug in^-1 s^-1", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -1.0})
    dim_test("radian", {dims.ANGLE: 1.0})
    dim_test(
        "ohm", {dims.MASS: 1.0, dims.LENGTH: 2.0, dims.TIME: -3.0, dims.CURRENT: -2.0}
    )
    dim_test("lb cm s^-2", {dims.MASS: 1.0, dims.LENGTH: 1.0, dims.TIME: -2.0})
    print("-" * 75)


def testing_multipliers():
    print(f"{'*' * 25} {testing_multipliers.__name__} {'*' * 25}")

    def from_to(from_str, to_str):
        qt = ansunits.Quantity(1, from_str)
        to = qt.to(to_str)
        print(f"from {qt} -> to {to}")

    from_to("mm", "cm")
    from_to("m", "ft")
    from_to("dm^3", "m^3")
    from_to("m s^-1", "cm s^-1")
    from_to("N", "dyne")
    from_to("m^2", "in^2")
    from_to("degree s^-1", "radian s^-1")
    from_to("radian s^-1", "degree s^-1")
    from_to("Pa", "lb m s^-2 ft^-2")
    from_to("lb m s^-2 ft^-2", "Pa")

    from_to("J kg^-1 K^-1", "J kg^-1 C^-1")
    from_to("J kg^-1 K^-1", "J kg^-1 R^-1")
    from_to("J kg^-1 K^-1", "J kg^-1 F^-1")

    from_to("K", "C")
    from_to("K", "R")
    from_to("K", "F")

    print("-" * 75)


def testing_arithmetic_operators():
    print(f"{'*' * 25} {testing_arithmetic_operators.__name__} {'*' * 25}")

    qt1 = ansunits.Quantity(10, "m s^-1")
    qt2 = ansunits.Quantity(5, "m s^-1")

    qt3 = qt1 * qt2

    print(f"{qt1} * {qt2} =  {qt3}")
    assert qt3.value == 50
    assert qt3.units == "m^2 s^-2"

    result = qt1 * 2
    print(f"{qt1} * {2} =  {result}")
    assert result.value == 20
    assert result.units == "m s^-1"

    result1 = 2 * qt1
    print(f"{2} * {qt1} =  {result1}")
    assert result1.value == 20
    assert result1.units == "m s^-1"

    q3 = qt1 / qt2

    print(f"{qt1} / {qt2} =  {q3}")
    assert q3.value == 2
    assert q3.units == ""

    result3 = qt1 / 2
    print(f"{qt1} / {2} =  {qt1 / 2}")
    assert result3.value == 5
    assert result3.units == "m s^-1"

    qa3 = qt1 + qt2

    print(f"{qt1} + {qt2} =  {qa3}")
    assert qa3.value == 15
    assert qa3.units == "m s^-1"

    with pytest.raises(ansunits.QuantityError) as e:
        result5 = qt1 + 2
        print(f"{qt1} + {2} =  {result5}")

    with pytest.raises(ansunits.QuantityError) as e:
        result6 = 2 + qt1
        print(f"{2} + {qt1} =  {result6}")

    qs3 = qt1 - qt2

    print(f"{qt1} - {qt2} =  {qs3}")
    assert qs3.value == 5
    assert qs3.units == "m s^-1"

    with pytest.raises(ansunits.QuantityError) as e:
        result7 = qt1 - 2
        print(f"{qt1} - {2} =  {result7}")

    with pytest.raises(ansunits.QuantityError) as e:
        result8 = 2 - qt1
        print(f"{2} - {qt1} =  {result8}")


def test_errors():
    dims = ansunits.BaseDimensions
    with pytest.raises(ansunits.QuantityError):
        e1 = ansunits.Quantity(
            value=10,
            units="farad",
            dimensions=ansunits.Dimensions({dims.MASS: 1}),
            quantity_map={"Velocity": 3},
        )


def test_error_messages():
    e1 = ansunits.QuantityError.EXCESSIVE_PARAMETERS()
    assert (
        str(e1)
        == "Quantity only accepts one of the following parameters: \
            (units) or (quantity_map) or (dimensions)."
    )

    e2 = ansunits.QuantityError.INCOMPATIBLE_DIMENSIONS("mm", "K")
    assert str(e2) == "`mm` and `K` have incompatible dimensions."

    e3 = ansunits.QuantityError.INCOMPATIBLE_VALUE("radian")
    assert str(e3) == "`radian` is incompatible with the current quantity object."


def test_instantiate_quantity_with_unrecognized_units_causes_exception():
    with pytest.raises(ansunits.UnitError):
        ansunits.Quantity(value=10, units="piggies")
    with pytest.raises(ansunits.UnitError):
        ansunits.Quantity(value=10, units="piggies s^-1")
    with pytest.raises(ansunits.UnitError):
        ansunits.Quantity(value=10, units="piggies^2 m^-3")


def test_compute_temp_unit():
    dims = ansunits.BaseDimensions
    kb = ansunits.Quantity(1.382e-23, "J K^-1")
    t = ansunits.Quantity(2.0, "K")
    e = kb * t
    assert e.dimensions == ansunits.Dimensions(
        {dims.MASS: 1.0, dims.LENGTH: 2.0, dims.TIME: -2.0}
    )
    assert e.units == "kg m^2 s^-2"


def test_unit_multiply_quantity():
    dims = ansunits.BaseDimensions
    ur = ansunits.UnitRegistry()
    mass = ansunits.Quantity(10.0, ur.kg)
    mass_flow_rate = mass / ur.s
    assert mass_flow_rate.units == "kg s^-1"
    assert mass_flow_rate.value == 10
    assert mass_flow_rate.dimensions == ansunits.Dimensions(
        {dims.MASS: 1.0, dims.TIME: -1.0}
    )
