# Skill Assisted Code Review

Agent: Claude Code
Condition: Code review skill available
Prompt: Review @src/review_target.py. Do not modify the file. Report your findings.

## Agent Response

I reviewed [src/review_target.py](src/review_target.py) against the project's code-review checklist. I didn't change the file. I ran it once, and it crashes before it prints anything useful.

## Correctness

**1. The script crashes every time it runs** ([review_target.py:35-36](src/review_target.py#L35-L36))
`create_invoice()` looks up customer `999`, which isn't in the list. `find_customer` returns `None`, so `customer["name"]` fails:
```
TypeError: 'NoneType' object is not subscriptable
```
- **Why it matters:** the main path of the script never works, and nothing checks for a missing customer.
- **Fix:** handle the missing customer before using it. Either check `if customer is None:` and log or raise a clear error, or have `find_customer` raise a `KeyError`/custom `CustomerNotFound`. If `999` was a typo for `101` or `102`, fix the ID too. Either way, the `None` case still needs handling.

**2. Floating-point math for money** ([review_target.py:15-20](src/review_target.py#L15-L20), [line 39](src/review_target.py#L39))
Prices and tax are `float`s, and the result is rounded only when printed. Python's `round()` uses banker's rounding on binary floats, so totals can be off by a cent.
- **Fix:** use `decimal.Decimal` with `quantize(Decimal("0.01"), ROUND_HALF_UP)`, or store amounts in integer cents.

## Edge cases

**3. Bad input isn't checked** ([review_target.py:14-16](src/review_target.py#L14-L16))
- A missing `unit_price` or `quantity` key raises an unhelpful `KeyError`.
- Negative quantities or prices are accepted without complaint.
- An empty `lines` list returns `0`. That's probably fine, but it's an assumption worth stating or testing.

## Performance

**4. A `time.sleep(0.05)` runs for every line** ([review_target.py:17](src/review_target.py#L17))
A pure calculation blocks for 50 ms per line, so a 1,000-line invoice takes about 50 seconds. The comment says it "simulates a blocking operation", but nothing here needs it.
- **Fix:** remove it. If a real I/O call belongs here, do it outside the calculation, in bulk or asynchronously.

**5. Customer lookup is a linear scan** ([review_target.py:4-8](src/review_target.py#L4-L8))
This is fine for two customers. For large lists or repeated lookups, a dict keyed by `id` is O(1). This is minor.

## Maintainability and style

**6. The tax rate is hard-coded** ([review_target.py:19](src/review_target.py#L19))
- **Fix:** make `0.08` a named constant (`TAX_RATE`) or a parameter, since rates change by location.

**7. `create_invoice()` does too much**
It creates its own sample data, does the lookup and calculation, and prints the output. Because it takes no inputs and returns nothing, it can't be reused or tested.
- **Fix:** take `customers`, `customer_id` and `lines` as parameters, return the invoice data, and do the printing in `__main__`.

**8. Smaller style points**
- There are no type hints or docstrings.
- Use f-strings, such as `f"Invoice total: ${total:.2f}"`, instead of joining strings with `+` and `str()`.
- Use `logging` instead of `print` if this becomes more than a demo.

## Testability

There are no tests. Automated tests should cover:
- `find_customer`: the ID is found, the ID is missing, and the list is empty.
- `calculate_invoice_total`: a known total (the sample data gives 81.00 subtotal, 6.48 tax, 87.48 total), an empty list, and rounding at the cent boundary.
- `create_invoice`: the unknown-customer path gives a clear error instead of a `TypeError`.
- Removing the `sleep` (finding 4) is needed for these tests to run fast.

## Assumptions

- I assumed the 8% tax applies to the whole subtotal and that nothing is exempt.
- I assumed the `sleep` isn't there on purpose to rate-limit something outside this file.

**Priority:** fix finding 1 first, since it's a guaranteed crash. Finding 4 (the sleep) and finding 2 (money as floats) come next. The rest are cleanups.