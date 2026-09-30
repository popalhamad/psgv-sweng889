"""Tests for invoice processing.

Each test maps to a test ID in specs/invoice/test-plan.md and to an
acceptance criterion in specs/invoice/requirements.md. Assertions follow
the requirements, not the current implementation.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from invoice import calculate_invoice_total, create_invoice


@pytest.fixture
def customers():
    return [
        {"id": 101, "name": "Avery"},
        {"id": 102, "name": "Morgan"},
    ]


@pytest.fixture
def valid_lines():
    return [
        {"unit_price": 24.00, "quantity": 2},
        {"unit_price": 15.50, "quantity": 1},
        {"unit_price": 8.25, "quantity": 4},
    ]


# AC1: Create Invoice for Existing Customer


def test_ac1_existing_customer_creates_invoice(customers, valid_lines):
    """T1.1"""
    invoice = create_invoice(customers, 101, valid_lines)

    assert invoice is not None
    assert invoice["customer"] == "Avery"


def test_ac1_invoice_is_for_the_selected_customer(customers, valid_lines):
    """T1.2"""
    invoice = create_invoice(customers, 102, valid_lines)

    assert invoice["customer"] == "Morgan"


# AC2: Reject Missing Customer


def test_ac2_missing_customer_is_rejected_with_clear_error(customers, valid_lines):
    """T2.1"""
    with pytest.raises(ValueError, match="999"):
        create_invoice(customers, 999, valid_lines)


def test_ac2_empty_customer_list_is_rejected_with_clear_error(valid_lines):
    """T2.2"""
    with pytest.raises(ValueError, match="101"):
        create_invoice([], 101, valid_lines)


# AC3: Reject Invalid Quantity


@pytest.mark.parametrize("quantity", [0, -1], ids=["zero", "negative"])
def test_ac3_non_positive_quantity_is_rejected_with_clear_error(customers, quantity):
    """T3.1, T3.2"""
    lines = [{"unit_price": 10.00, "quantity": quantity}]

    with pytest.raises(ValueError, match="(?i)quantity"):
        create_invoice(customers, 101, lines)


def test_ac3_one_invalid_quantity_rejects_whole_invoice(customers, valid_lines):
    """T3.3"""
    lines = valid_lines[:2] + [{"unit_price": 10.00, "quantity": 0}]

    with pytest.raises(ValueError, match="(?i)quantity"):
        create_invoice(customers, 101, lines)


def test_ac3_quantity_of_one_is_accepted(customers):
    """T3.4"""
    lines = [{"unit_price": 10.00, "quantity": 1}]

    invoice = create_invoice(customers, 101, lines)

    assert invoice["customer"] == "Avery"


# AC4: Reject Invalid Unit Price


def test_ac4_negative_unit_price_is_rejected_with_clear_error(customers):
    """T4.1"""
    lines = [{"unit_price": -0.01, "quantity": 1}]

    with pytest.raises(ValueError, match="(?i)price"):
        create_invoice(customers, 101, lines)


def test_ac4_one_negative_unit_price_rejects_whole_invoice(customers, valid_lines):
    """T4.2"""
    lines = valid_lines[:2] + [{"unit_price": -5.00, "quantity": 1}]

    with pytest.raises(ValueError, match="(?i)price"):
        create_invoice(customers, 101, lines)


def test_ac4_zero_unit_price_is_accepted(customers):
    """T4.3"""
    lines = [{"unit_price": 0.00, "quantity": 1}]

    invoice = create_invoice(customers, 101, lines)

    assert invoice["total"] == pytest.approx(0.00, abs=0.005)


# AC5: Calculate Invoice Total


def test_ac5_single_line_total_includes_8_percent_tax():
    """T5.1"""
    lines = [{"unit_price": 10.00, "quantity": 2}]

    assert calculate_invoice_total(lines) == pytest.approx(21.60, abs=0.005)


def test_ac5_multi_line_total_is_subtotal_plus_8_percent_tax(valid_lines):
    """T5.2: subtotal 96.50 + tax 7.72 = 104.22"""
    assert calculate_invoice_total(valid_lines) == pytest.approx(104.22, abs=0.005)


def test_ac5_zero_price_lines_total_zero():
    """T5.3"""
    lines = [
        {"unit_price": 0.00, "quantity": 3},
        {"unit_price": 0.00, "quantity": 3},
    ]

    assert calculate_invoice_total(lines) == pytest.approx(0.00, abs=0.005)


def test_ac5_created_invoice_has_correct_total(customers, valid_lines):
    """T5.4"""
    invoice = create_invoice(customers, 101, valid_lines)

    assert invoice["total"] == pytest.approx(104.22, abs=0.005)
