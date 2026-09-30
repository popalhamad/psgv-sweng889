# Invoice Processing Test Plan

This plan maps each acceptance criterion in [requirements.md](requirements.md) to one or more automated tests. Expected results come from the requirements, not from the current implementation in `src/invoice.py`.

## Assumptions

The requirements leave these points open. The tests use the following interpretations:

- **Clear error:** `create_invoice` raises a specific exception (for example `ValueError`) whose message names the problem: the customer ID, the quantity, or the unit price. No invoice is returned. An incidental `TypeError` or `KeyError` from inside the code does not count as a clear error.
- **Money comparisons:** totals are compared to the cent (for example with `pytest.approx` or `round(x, 2)`), because the requirements don't define rounding.

## AC1: Create Invoice for Existing Customer

| ID | Condition | Expected result |
|---|---|---|
| T1.1 | Customers include ID 101 ("Avery"); call `create_invoice` with ID 101 and valid lines | An invoice is returned and its customer is "Avery" |
| T1.2 | Customers 101 ("Avery") and 102 ("Morgan"); call with ID 102 | The invoice is for "Morgan", not the first customer in the list |

## AC2: Reject Missing Customer

| ID | Condition | Expected result |
|---|---|---|
| T2.1 | Customers 101 and 102; call with ID 999 and valid lines | Creation is rejected with a clear error that mentions customer 999; no invoice is returned |
| T2.2 | Empty customer list; call with any ID | Creation is rejected with the same clear "customer not found" error |

## AC3: Reject Invalid Quantity

| ID | Condition | Expected result |
|---|---|---|
| T3.1 | Existing customer; one line with `quantity = 0` | Rejected with a clear error about the quantity |
| T3.2 | Existing customer; one line with `quantity = -1` | Rejected with a clear error about the quantity |
| T3.3 | Two valid lines plus one line with `quantity = 0` | The whole invoice is rejected, not just that line |
| T3.4 | Boundary: one line with `quantity = 1` | Accepted; an invoice is created |

## AC4: Reject Invalid Unit Price

| ID | Condition | Expected result |
|---|---|---|
| T4.1 | Existing customer; one line with `unit_price = -0.01` | Rejected with a clear error about the unit price |
| T4.2 | Two valid lines plus one line with `unit_price = -5.00` | The whole invoice is rejected |
| T4.3 | Boundary: one line with `unit_price = 0.00`, `quantity = 1` | Accepted, because only prices below zero are invalid; the total is 0.00 |

## AC5: Calculate Invoice Total

| ID | Condition | Expected result |
|---|---|---|
| T5.1 | One line: 10.00 × 2 | Subtotal is 20.00; total is 21.60 |
| T5.2 | Three lines: 24.00 × 2, 15.50 × 1, 8.25 × 4 | Subtotal is 96.50, tax is 7.72, total is 104.22 |
| T5.3 | Two lines with price 0.00, quantity 3 each | Total is 0.00 |
| T5.4 | End to end: call `create_invoice` for customer 101 with the T5.2 lines | The invoice's `total` is 104.22 |

## Traceability Summary

| Acceptance criterion | Tests |
|---|---|
| AC1: Create invoice for existing customer | T1.1, T1.2, T5.4 |
| AC2: Reject missing customer | T2.1, T2.2 |
| AC3: Reject invalid quantity | T3.1, T3.2, T3.3, T3.4 |
| AC4: Reject invalid unit price | T4.1, T4.2, T4.3 |
| AC5: Calculate invoice total | T5.1, T5.2, T5.3, T5.4 |

## Expected Failures Against the Current Implementation

Based on reading `src/invoice.py`; these tests have not been run yet.

- **T2.1, T2.2:** `find_customer` returns `None` for a missing ID, so `customer["name"]` raises a `TypeError` instead of a clear error.
- **T3.1–T3.3, T4.1–T4.2:** no validation is done on quantity or unit price, so these invoices are created with incorrect totals.
- **Test speed:** `calculate_invoice_total` sleeps 0.05 s per line. This doesn't affect results, but it slows the suite.

## Open Questions

These need a decision before the related tests are finalized:

1. **Empty invoice:** should an invoice with no lines be rejected, or created with a total of 0.00?
2. **Error precedence:** if the customer is missing and a line is also invalid, which error is reported?
3. **Rounding:** should the stored total be rounded to cents, or only rounded when compared?
4. **Quantity type:** is a fractional quantity (for example 1.5) valid?
5. **Error type:** should rejections use one exception type (such as `ValueError`) or a separate one for each case?
