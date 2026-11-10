# Copyright (C) 2023 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Tests for the product-agnostic expression core.

These tests use a small, made-up dialect and must not import anything product-specific.
"""

from enum import Enum
from typing import final

import pytest
from typing_extensions import override

from ansys.expressions import (
    DEFAULT_DIALECT,
    BinOp,
    Call,
    DescriptorNameStrategy,
    Dialect,
    Discovery,
    ExpressionBuilder,
    ExpressionBuildError,
    FunctionRegistry,
    Kind,
    Literal,
    Param,
    Quantity,
    RawName,
    ScalarSlot,
    Signature,
    StaticDiscovery,
    Variable,
    make_call,
    parse,
)
from ansys.variable_descriptor import (
    ConversionStrategy,
    MappingConversionStrategy,
    VariableCatalog,
    VariableDescriptor,
)

V = VariableCatalog


@final
class _ToyNaming(MappingConversionStrategy):
    _mapping = {
        V.ABSOLUTE_PRESSURE: "P",
        V.TEMPERATURE: "T",
        V.VELOCITY: "U",
        V.VELOCITY_X: "U.x",
    }


class _Mode(Enum):
    FAST = "Fast"
    SLOW = "Slow"


def _toy_functions() -> FunctionRegistry:
    functions = FunctionRegistry()
    functions.register(
        "reductions",
        Signature(
            "Avg",
            "avg",
            (
                Param("expression", Kind.SCALAR),
                Param("locations", Kind.LOCATION_LIST),
                Param(
                    "mode",
                    Kind.SCALAR,
                    optional=True,
                    keyword="Mode",
                    allowed_literals=_Mode,
                ),
            ),
        ),
    )
    functions.register(
        "vector",
        Signature("Vec", "vec", (Param("x", Kind.SCALAR),), returns=Kind.VECTOR),
    )
    functions.register(
        "misc",
        Signature(
            "Pick", "pick", (Param("which", Kind.SCALAR, allowed_literals=("a", "b")),)
        ),
    )
    return functions


@pytest.fixture
def toy() -> Dialect:
    return Dialect("toy", naming=_ToyNaming(), functions=_toy_functions())


@pytest.fixture
def b(toy: Dialect) -> ExpressionBuilder:
    return ExpressionBuilder(toy)


# --------------------------------------------------------------------------- #
# Dialect-driven rendering                                                    #
# --------------------------------------------------------------------------- #


def test_builder_renders_with_its_dialect(b: ExpressionBuilder):
    node = b.reductions.avg(V.ABSOLUTE_PRESSURE, ["in"]) / 2
    assert str(node) == "(Avg(P,['in']) / 2)"


def test_bare_descriptor_operand_takes_tree_dialect(b: ExpressionBuilder):
    # The descriptor on the right has no dialect of its own; the tree's applies.
    node = b.literal(1) + V.TEMPERATURE
    assert str(node) == "(1 + T)"


def test_tree_without_dialect_uses_default():
    node = Literal(1) + V.ABSOLUTE_PRESSURE
    assert node.find_dialect() is None
    assert str(node) == "(1 + absolute_pressure)"


def test_explicit_dialect_overrides_tree_dialect(b: ExpressionBuilder):
    node = b.variable(V.TEMPERATURE)
    assert node.render() == "T"
    assert node.render(DEFAULT_DIALECT) == "temperature"
    assert b.render(Literal(2) * Variable(V.TEMPERATURE)) == "(2 * T)"


def test_mixing_dialects_is_rejected(b: ExpressionBuilder):
    other = ExpressionBuilder(Dialect("other"))
    with pytest.raises(ExpressionBuildError, match="'toy' and 'other'"):
        _ = b.variable(V.TEMPERATURE) + other.variable(V.TEMPERATURE)
    with pytest.raises(ExpressionBuildError, match="dialects"):
        _ = b.literal(1) < other.literal(2)


def test_unsupported_variable_rejected_at_build_time(b: ExpressionBuilder):
    with pytest.raises(ExpressionBuildError, match="'toy' dialect"):
        b.variable(V.DENSITY)


def test_unsupported_variable_rejected_at_render_time(b: ExpressionBuilder):
    node = b.literal(1) + V.DENSITY
    with pytest.raises(ExpressionBuildError, match="no variable name"):
        node.render()
    # repr never needs a dialect.
    assert repr(node).startswith("BinOp(op='+'")


def test_non_descriptor_variable_rejected():
    with pytest.raises(ExpressionBuildError, match="not a VariableDescriptor"):
        Variable("pressure")  # pyright: ignore[reportArgumentType]


def test_naming_strategy_returning_none_is_rejected():
    @final
    class _NoneNaming(DescriptorNameStrategy):
        @override
        def to_string(self, variable: VariableDescriptor | str | None) -> str | None:
            return None

    dialect = Dialect("none", naming=_NoneNaming())
    with pytest.raises(ExpressionBuildError):
        dialect.variable_name(V.TEMPERATURE)


def test_unary_and_comparison_keep_dialect(b: ExpressionBuilder, toy: Dialect):
    v = b.variable(V.ABSOLUTE_PRESSURE)
    assert (-v).dialect is toy
    assert str(-v) == "(-P)"
    cond = v >= 0
    assert cond.dialect is toy and str(cond) == "(P >= 0)"


# --------------------------------------------------------------------------- #
# Functions                                                                   #
# --------------------------------------------------------------------------- #


def test_registry_groups_and_lookup(toy: Dialect):
    assert toy.functions.groups() == ("reductions", "vector", "misc")
    assert toy.find_function("Avg") is toy.functions.group("reductions")["avg"]
    assert toy.find_function("Nope") is None


def test_enum_literal_keyword(b: ExpressionBuilder):
    node = b.reductions.avg(V.TEMPERATURE, ["in"], mode=_Mode.SLOW)
    assert str(node) == "Avg(T,['in'],Mode=Slow)"
    assert str(b.reductions.avg(V.TEMPERATURE, ["in"], mode="FAST")) == (
        "Avg(T,['in'],Mode=Fast)"
    )


def test_iterable_allowed_literals(b: ExpressionBuilder):
    assert str(b.misc.pick("a")) == "Pick(a)"
    with pytest.raises(ExpressionBuildError, match="must be one of"):
        b.misc.pick("c")


def test_signature_build_without_dialect():
    sig = Signature("F", "f", (Param("x", Kind.SCALAR),))
    node = sig.build(V.TEMPERATURE)
    assert node.dialect is None
    assert str(node) == "F(temperature)"


def test_signature_binding_errors(b: ExpressionBuilder):
    with pytest.raises(ExpressionBuildError, match="positional"):
        b.vector.vec(1, 2)
    with pytest.raises(ExpressionBuildError, match="unexpected keyword"):
        b.vector.vec(y=1)
    with pytest.raises(ExpressionBuildError, match="multiple values"):
        b.vector.vec(1, x=2)


def test_make_call_with_dialect(toy: Dialect):
    node = make_call("Grad", V.TEMPERATURE, returns=Kind.VECTOR, dialect=toy)
    assert str(node) == "Grad(T)" and node.kind is Kind.VECTOR


def test_builder_unknown_group_raises(b: ExpressionBuilder):
    with pytest.raises(AttributeError, match="Function groups"):
        b.nothing
    assert "reductions" in dir(b)
    assert "avg" in dir(b.reductions)


# --------------------------------------------------------------------------- #
# Parsing                                                                     #
# --------------------------------------------------------------------------- #


def test_parse_with_dialect_round_trips(toy: Dialect):
    text = "(Avg(P,['in'],Mode=Fast) - Vec(T))"
    node = parse(text, toy)
    assert node.find_dialect() is toy
    assert str(node) == text
    assert isinstance(node, BinOp) and isinstance(node.right, Call)
    assert node.right.kind is Kind.VECTOR


def test_parse_with_default_dialect_uses_catalog_names():
    node = parse("absolute_pressure * 2")
    assert isinstance(node, BinOp) and isinstance(node.left, Variable)
    assert node.left.descriptor is V.ABSOLUTE_PRESSURE
    assert str(node) == "(absolute_pressure * 2)"
    assert isinstance(parse("not_a_variable"), RawName)


def test_builder_parse_and_render(b: ExpressionBuilder):
    node = b.parse("P + 1")
    assert b.render(node) == "(P + 1)"


# --------------------------------------------------------------------------- #
# Dialect helpers and default naming strategy                                 #
# --------------------------------------------------------------------------- #


def test_descriptor_name_strategy():
    naming = DescriptorNameStrategy()
    assert naming.to_string(V.TEMPERATURE) == "temperature"
    assert naming.to_string("raw") == "raw"
    assert naming.to_string(None) is None
    assert naming.to_variable_descriptor("temperature") is V.TEMPERATURE
    assert naming.to_variable_descriptor(V.TEMPERATURE) is V.TEMPERATURE
    assert naming.to_variable_descriptor("bogus") is None
    assert naming.supports(V.TEMPERATURE) is True


def test_supported_variables(toy: Dialect):
    assert set(toy.supported_variables()) == {
        V.ABSOLUTE_PRESSURE,
        V.TEMPERATURE,
        V.VELOCITY,
        V.VELOCITY_X,
    }
    assert V.TEMPERATURE in DEFAULT_DIALECT.supported_variables()

    @final
    class _Opaque(ConversionStrategy):
        @override
        def to_string(self, variable: VariableDescriptor | str | None) -> str | None:
            return None

        @override
        def to_variable_descriptor(
            self, variable: VariableDescriptor | str
        ) -> VariableDescriptor | None:
            raise KeyError(variable)

        @override
        def supports(self, variable: VariableDescriptor) -> bool:
            raise TypeError

    opaque = Dialect("opaque", naming=_Opaque())
    assert opaque.supported_variables() == []
    assert opaque.variable_descriptor("x") is None
    assert opaque.supports_variable(V.TEMPERATURE) is False


# --------------------------------------------------------------------------- #
# Discovery                                                                   #
# --------------------------------------------------------------------------- #


def test_static_discovery(toy: Dialect):
    discovery = StaticDiscovery(toy, locations=["a", "b"], named_expressions=["dp"])
    assert isinstance(discovery, Discovery)
    builder = ExpressionBuilder(toy, discovery)
    assert builder.discovery is discovery
    assert builder.dialect is toy
    assert builder.location_names() == ["a", "b"]
    assert builder.named_expression_names() == ["dp"]
    assert set(builder.variables()) == set(toy.supported_variables())

    avg = builder.reductions.avg
    assert avg.locations.allowed_values() == ["a", "b"]
    assert avg.locations.is_allowed(["a", "b"]) is True
    assert avg.locations.is_allowed("c") is False
    assert avg.expression.is_allowed(V.TEMPERATURE) is True
    assert avg.expression.is_allowed(V.DENSITY) is False
    assert isinstance(avg.expression, ScalarSlot)
    assert avg.expression.named.is_allowed("dp") is True


def test_default_builder_has_no_functions():
    builder = ExpressionBuilder()
    assert builder.dialect is DEFAULT_DIALECT
    assert str(builder.quantity(5, "m/s")) == "5 [m/s]"
    assert str(builder.raw("my_expr") + 1) == "(my_expr + 1)"
    with pytest.raises(AttributeError):
        builder.reductions


def test_quantity_dimensions_are_unit_aware():
    assert Quantity(1.0, "Pa").__settings_dimensions__() == {
        "MASS": 1.0,
        "LENGTH": -1.0,
        "TIME": -2.0,
    }
    assert Quantity(1.0, "not-a-unit").__settings_dimensions__() is None


# --------------------------------------------------------------------------- #
# Tree structure, operators, and settings protocol                            #
# --------------------------------------------------------------------------- #


def test_find_dialect_searches_children(toy: Dialect):
    from ansys.expressions import (
        Compare,
        KeywordArg,
        UnaryOp,
    )

    leaf = Variable(V.TEMPERATURE, dialect=toy)
    assert UnaryOp("-", leaf).find_dialect() is toy
    assert Compare("<", Literal(1), leaf).find_dialect() is toy
    assert KeywordArg("K", leaf).find_dialect() is toy
    assert BinOp("+", Literal(1), Literal(2)).find_dialect() is None


def test_reflected_operators_and_comparisons(b: ExpressionBuilder):
    v = b.variable(V.TEMPERATURE)
    assert str(1 + v) == "(1 + T)"
    assert str(1 - v) == "(1 - T)"
    assert str(1 / v) == "(1 / T)"
    assert str(v**2) == "(T ** 2)"
    assert str(v <= 1) == "(T <= 1)"
    assert str(v > 1) == "(T > 1)"
    assert str(v != 1) == "(T != 1)"


def test_invalid_operands_and_locations(b: ExpressionBuilder):
    from ansys.expressions import LocationList

    with pytest.raises(ExpressionBuildError, match="as an expression"):
        _ = b.literal(1) + "x"  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(ExpressionBuildError, match="non-empty strings"):
        LocationList(("",))
    with pytest.raises(ExpressionBuildError, match="as a LocationList"):
        b.locations(5)  # pyright: ignore[reportArgumentType]
    locations = b.locations(["a"])
    assert b.locations(locations) is locations


def test_variable_settings_protocol():
    assert Variable(V.VELOCITY).__settings_kind__() == "vector"
    assert Variable(V.TEMPERATURE).__settings_kind__() == "scalar"
    assert Variable(V.TEMPERATURE).__settings_dimensions__() == {"TEMPERATURE": 1.0}
    assert Variable(V.CELL_REYNOLDS_NUMBER).__settings_dimensions__() is None


def test_arithmetic_requires_scalar_operands(b: ExpressionBuilder):
    with pytest.raises(ExpressionBuildError, match="left operand is a vector"):
        _ = b.vector.vec(1) + 1


def test_param_coerce_missing_value():
    assert Param("x", Kind.SCALAR, optional=True).coerce(None) is None
    with pytest.raises(ExpressionBuildError, match="Missing required"):
        Param("x", Kind.SCALAR).coerce(None)


def test_invoker_introspection(b: ExpressionBuilder):
    avg = b.reductions.avg
    assert avg.signature.name == "Avg"
    assert repr(avg) == (
        "<avg(expression: scalar, locations: location_list, mode: scalar) "
        "-> scalar | toy='Avg'>"
    )


def test_generic_slot_accessors(b: ExpressionBuilder):
    vec_slot = b.vector.vec.x
    assert (vec_slot.name, vec_slot.kind) == ("x", Kind.SCALAR)
    assert repr(vec_slot) == "<slot 'x': scalar>"

    from ansys.expressions import SlotAccessor

    @final
    class _Fixed(SlotAccessor):
        @override
        def allowed_values(self) -> list[object]:
            return [1, 2]

    slot = _Fixed(Param("n", Kind.VECTOR), StaticDiscovery(DEFAULT_DIALECT))
    assert slot.is_allowed(1) is True and slot.is_allowed(3) is False

    offline = b.reductions.avg.locations
    assert offline.is_allowed(["a", "b"]) is True
    assert offline.is_allowed(5) is False
    online = ExpressionBuilder(
        b.dialect, StaticDiscovery(b.dialect, locations=["a"])
    ).reductions.avg.locations
    assert online.is_allowed(5) is False


@pytest.mark.parametrize(
    "text, match",
    [
        ("1@", "Unexpected character"),
        ("1 +", "end of input"),
        (",", "Unexpected token"),
        ("5 [m", "Unterminated"),
    ],
)
def test_parse_errors(text: str, match: str):
    with pytest.raises(ExpressionBuildError, match=match):
        parse(text)


def test_parse_misc_atoms():
    assert str(parse("+5")) == "5"
    node = parse("'quoted'")
    assert isinstance(node, RawName) and node.name == "'quoted'"
    quantity = parse("5 [m [x]]")
    assert isinstance(quantity, Quantity) and quantity.units == "m [x]"


# --------------------------------------------------------------------------- #
# Parser: atoms, operators, calls                                             #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "text, value", [("42", 42), ("3.14", 3.14), ("1.5e-3", 1.5e-3)]
)
def test_parse_numeric_literals(text: str, value: float):
    node = parse(text)
    assert isinstance(node, Literal) and node.value == value


def test_parse_quantity():
    node = parse("5 [m/s]")
    assert isinstance(node, Quantity)
    assert (node.value, node.units) == (5.0, "m/s")


def test_parse_variables_and_raw_names(toy: Dialect):
    pressure = parse("P", toy)
    assert isinstance(pressure, Variable) and pressure.descriptor is V.ABSOLUTE_PRESSURE
    dotted = parse("U.x", toy)
    assert isinstance(dotted, Variable) and dotted.descriptor is V.VELOCITY_X
    raw = parse("MyNamedExpression", toy)
    assert isinstance(raw, RawName) and raw.name == "MyNamedExpression"


def test_parse_location_lists():
    from ansys.expressions import LocationList

    node = parse("['inlet1', 'inlet2']")
    assert isinstance(node, LocationList) and node.names == ("inlet1", "inlet2")
    empty = parse("[]")
    assert isinstance(empty, LocationList) and empty.names == ()


def test_parse_operator_precedence():
    from ansys.expressions import Compare, UnaryOp

    node = parse("1 + 2 * 3")
    assert isinstance(node, BinOp) and node.op == "+"
    assert isinstance(node.right, BinOp) and node.right.op == "*"
    grouped = parse("(1 + 2) * 3")
    assert isinstance(grouped, BinOp) and grouped.op == "*"
    assert isinstance(grouped.left, BinOp) and grouped.left.op == "+"
    negated = parse("-5")
    assert isinstance(negated, UnaryOp) and isinstance(negated.operand, Literal)
    power = parse("2 ** 3 ** 2")
    assert isinstance(power, BinOp) and isinstance(power.right, BinOp)
    assert power.right.op == "**"
    assert isinstance(parse("T > 10"), Compare)


def test_parse_calls(toy: Dialect):
    from ansys.expressions import KeywordArg

    node = parse("Avg(P,['in'],Mode=Fast)", toy)
    assert isinstance(node, Call) and node.name == "Avg"
    assert isinstance(node.args[0], Variable)
    assert isinstance(node.args[2], KeywordArg) and node.args[2].keyword == "Mode"
    nested = parse("Avg(Vec(1),[])", toy)
    assert isinstance(nested, Call) and isinstance(nested.args[0], Call)
    assert parse("Unknown(1,2)", toy).kind is Kind.SCALAR
    assert parse("Empty()").render() == "Empty()"


@pytest.mark.parametrize(
    "canonical",
    [
        "P",
        "U.x",
        "42",
        "5.0 [m/s]",
        "['in', 'out']",
        "Avg(P,['in'],Mode=Fast)",
        "Vec(T)",
        "(Avg(P,['in']) - Avg(P,['out']))",
        "((2 * T) + 1)",
        "(-T)",
        "(T ** 2)",
        "(T >= 0)",
    ],
)
def test_round_trip_canonical(toy: Dialect, canonical: str):
    assert str(parse(canonical, toy)) == canonical


def test_round_trip_of_builder_output(b: ExpressionBuilder):
    dp = b.reductions.avg(V.ABSOLUTE_PRESSURE, ["in"]) - b.reductions.avg(
        V.ABSOLUTE_PRESSURE, ["out"]
    )
    text = str(dp)
    assert str(b.parse(text)) == text


def test_edit_parsed_tree(b: ExpressionBuilder):
    edited = b.parse("Avg(P,['in'])") - b.reductions.avg(V.ABSOLUTE_PRESSURE, ["out"])
    assert str(edited) == "(Avg(P,['in']) - Avg(P,['out']))"


@pytest.mark.parametrize(
    "text, match",
    [
        ("", "empty"),
        ("Avg(P,['in']", "Expected"),
        ("42 garbage", "Unexpected token"),
        ("1 @ 2", "Unexpected character"),
    ],
)
def test_more_parse_errors(text: str, match: str):
    with pytest.raises(ExpressionBuildError, match=match):
        parse(text)


def test_parse_rejects_non_string():
    with pytest.raises(ExpressionBuildError, match="expects a string"):
        parse(123)  # pyright: ignore[reportArgumentType]


# --------------------------------------------------------------------------- #
# Builder: leaves, composition, and introspection                             #
# --------------------------------------------------------------------------- #


def test_builder_leaves(b: ExpressionBuilder):
    assert str(b.literal(1.5)) == "1.5"
    assert str(b.quantity(5, "m/s")) == "5 [m/s]"
    assert str(b.variable(V.ABSOLUTE_PRESSURE)) == "P"
    assert str(b.locations(["a", "b"])) == "['a', 'b']"
    with pytest.raises(ExpressionBuildError):
        b.locations("a")


def test_builder_composition(b: ExpressionBuilder):
    v = b.variable(V.TEMPERATURE)
    assert str(2 * v + 1) == "((2 * T) + 1)"
    assert str(v - 1) == "(T - 1)"
    assert str(-v) == "(-T)"
    cond = v == b.variable(V.ABSOLUTE_PRESSURE)
    assert str(cond) == "(T == P)" and cond.kind is Kind.BOOLEAN
    assert v in {v}
    assert cond.__settings_str__() == "(T == P)"
    assert cond.__settings_kind__() == "boolean"
    assert cond.__settings_dimensions__() is None


def test_function_group_introspection(b: ExpressionBuilder):
    assert b.reductions.available() == ["avg"]
    with pytest.raises(AttributeError, match="Available"):
        _ = b.reductions.not_a_thing
    avg = b.reductions.avg
    assert avg.params() == ["expression", "locations", "mode"]
    assert {"expression", "locations"} <= set(dir(avg))
    with pytest.raises(AttributeError, match="has no parameter"):
        _ = avg.nonexistent


def test_signature_argument_validation(b: ExpressionBuilder):
    with pytest.raises(ExpressionBuildError, match="missing required argument"):
        b.reductions.avg(expression=V.ABSOLUTE_PRESSURE)
    with pytest.raises(ExpressionBuildError, match="expects scalar, got vector"):
        b.vector.vec(b.vector.vec(1))
    with pytest.raises(ExpressionBuildError, match="must be one of"):
        b.reductions.avg(V.ABSOLUTE_PRESSURE, ["in"], mode="Bogus")
    with pytest.raises(ExpressionBuildError):
        b.reductions.avg(V.ABSOLUTE_PRESSURE, V.TEMPERATURE)


def test_scalar_slot_sub_slots(b: ExpressionBuilder):
    slot = b.reductions.avg.expression
    assert isinstance(slot, ScalarSlot)
    assert V.ABSOLUTE_PRESSURE in slot.allowed_values()
    assert slot.variables.is_allowed("P") is False
    assert slot.named.allowed_values() == []
    assert slot.named.is_allowed("anything") is True
    assert slot.named.is_allowed(1) is False
    assert slot.is_allowed("anything") is True
