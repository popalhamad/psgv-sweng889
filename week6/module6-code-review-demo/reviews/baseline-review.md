# Baseline Code Review

Agent: Claude Code - Opus 5.5 Medium
Condition: Code review skill unavailable
Prompt: Review @src/review_target.py. Do not modify the file. Report your findings.

## Agent Response

I reviewed [src/review_target.py](src/review_target.py) without changing it. Running the script confirmed the first bug: it crashes every time.

## High severity

**1. Every run crashes because the customer lookup finds nothing** ([review_target.py:35-36](src/review_target.py#L35-L36))
`create_invoice` looks up customer ID `999`, but the list only has `101` and `102`. `find_customer` returns `None`, and the next line reads `customer["name"]` without checking for that:
```
TypeError: 'NoneType' object is not subscriptable
```
So no invoice is ever made. There are two problems here: the hard-coded ID is wrong, and the code never handles a missing customer. It should either check for `None` and give a clear error, or have `find_customer` raise a specific exception such as `KeyError` or `CustomerNotFound`.

## Medium severity

**2. The code pauses for 0.05 seconds on every invoice line** ([review_target.py:17](src/review_target.py#L17))
`time.sleep(0.05)` runs inside the loop, so the wait grows with the number of lines: 1,000 lines take about 50 seconds. The pause does nothing for the calculation and should be removed. If it stands in for real I/O, such as a price lookup per line, that work should be batched, or run concurrently, outside the adding-up loop.

**3. Money is stored as ordinary floating-point numbers** ([review_target.py:15-20](src/review_target.py#L15-L20), [39](src/review_target.py#L39))
Prices, the subtotal and the 8% tax are all floats, which can't hold most cent amounts exactly. Totals can come out slightly off, for example `104.22000000000001`, and `round()` can round a borderline value the wrong way (`round(2.675, 2)` gives `2.67`). Currency should use `decimal.Decimal` with an explicit rounding mode such as `ROUND_HALF_UP`.

**4. Totals can print without the second decimal place** ([review_target.py:39](src/review_target.py#L39))
`str(round(total, 2))` drops trailing zeros. A total of 10.80 prints as `$10.8`, which I confirmed. Use `f"${total:.2f}"` instead.

## Low severity / maintainability

5. **The tax rate is a bare number in the code** ([review_target.py:19](src/review_target.py#L19)): `0.08` should be a named constant or a parameter, since rates depend on location and change over time.
6. **Line items aren't checked** ([review_target.py:14-16](src/review_target.py#L14-L16)): a negative quantity, a negative price or a missing key is either accepted without complaint or fails with an unclear `KeyError`.
7. **Calculation and output are mixed together** ([review_target.py:23-39](src/review_target.py#L23-L39)): `create_invoice` hard-codes its data and prints its results instead of taking inputs and returning an invoice, which makes it hard to test or reuse.
8. **Minor:** `find_customer` checks every customer in turn. That's fine for two records, but a dictionary keyed by ID would be better at scale. There are also no type hints or docstrings, and the output is built with `+` instead of f-strings.

## Suggested priority
Fix #1 first, because it stops the script entirely. Then #2 for performance, and #3 and #4 for correct amounts.