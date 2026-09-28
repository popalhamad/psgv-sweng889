# The sample inputs, and what is planted in them

Every assignment option has a fixture set in `data/`, loaded by `app/fixtures.py`. You
should not have to go looking for data.

**The awkward cases are deliberate.** They are the ones an agent will guess at, and
therefore the ones your specification has to decide. `tests/test_fixtures.py` asserts
that each one is still there — if one of those tests fails, a fixture has drifted and an
option has quietly got easier than it was meant to be.

---

## `data/libraries.csv` — 200 records

The main table. Used by the app itself, and by **option E (merge the duplicates)**.

Records 1–10 are planted. The rest is generated filler with a fixed seed.

| ids | What is planted | The decision it forces |
|---|---|---|
| 1, 2 | `Eastport Public Library` / `Eastport Publ. Library` — same place, and they **disagree on `kind` and `annual_visits`** | When two records conflict on a field, which value survives, and where does the discarded one go? |
| 3, 4, 5 | **The transitivity chain.** 3 matches 4. 4 matches 5. 3 does **not** match 5 | There is no correct answer. Only a decided one. Merge all three? Refuse the chain? Ask a human? |
| 6, 7, 8 | Three genuinely *different* facilities in one city with similar names | Your threshold will want to merge some of these. Where do you set it, and what does a false merge cost? |
| 9 | `Cold Harbor Bookmobile` — founded 2025, **zero annual visits** | Legal but unusual. Does "zero visits" mean stale, new, or broken? A bulk delete of zero-visit records destroys it |
| 10 | `Grand Meridian` — 1,480,000 visits, far above everything else | Range filters and any averaging have an outlier to survive |

## `data/tickets.json` — 30 tickets

**Option B (support ticket triage).**

- Ten clear cases across billing, access, data and outage.
- Four **near-duplicates** of earlier tickets — same problem, different words. *Two
  tickets that are obviously the same problem: one ticket, or two?*
- Five **genuinely ambiguous** ones (`"Help"`, `"Follow up"`, `"Something is wrong with
  my account"`). The classifier returns low confidence on these. *Guess anyway, or route
  straight to a person?*
- One with **no subject**, one with **no body**. *Reject, or classify on what is there?*
- One all-caps escalation, one accessibility report, one data-retention question, one
  deletion request. *Does a draft reply ever go out without a human reading it?*

## `data/documents/` — 9 policy documents

**Option C (ask the documents).**

- `policy-loans.md` says loans run **21 days** and carry **no fine**.
- `faq-borrowing.md` says loans run **14 days** and fines are **10c per day**.
- `notice-2019-fines.md` abolishes fines and says it **supersedes earlier guidance**.

So a question about loan periods has two contradicting answers, and a question about
fines has three documents where the newest overrides one of the others. *Which wins?
Does the answer say they disagree? Is a document's date part of the answer?*

`guide-interlibrary.md` adds a fourth wrinkle: it says the *lending* library sets the
period, "which may be shorter than our own 21 days" — correct in context, wrong if
quoted alone.

## `data/diffs/` — 3 diffs

**Option D (pull request review assistant).**

| File | |
|---|---|
| `01-small-clean.diff` | 25 lines, adds a filter correctly. **Nothing to say about it.** Does your assistant stay quiet? |
| `02-has-a-real-bug.diff` | Contains a hardcoded API key, a `TODO`, an `== None`, and a bare `except: pass` — all of which the model finds. It **also** contains an off-by-one (`page * limit + 1`) that silently skips a record, and a `NameError` when the swallowed exception fires. **The model finds neither.** |
| `03-very-large.diff` | 496 lines of mechanical rename. *What happens on a very large diff — review it all, sample it, or refuse?* |

Diff 02 is the point of the option: the assistant produces four confident comments about
the shallow problems and misses both real bugs. *What is a comment worth, and what does
a clean review from this assistant actually license you to believe?*

## `data/operations.json` — 10 operations, 8 goals

**Option A (agentic task runner).**

Operations are tagged `reversible: true | false`. `records.apply_merge`,
`records.delete`, `records.bulk_import` and `notify.email_owner` cannot be undone.

The goals escalate on purpose:

| | |
|---|---|
| G1, G2 | Straightforward, all reversible |
| G3 | Needs an irreversible step — `apply_merge` |
| G4 | **Destructive**, and it matches record 9, a legitimately new facility |
| G5 | "Make the Ashfield records consistent" — **underspecified**. Consistent how? Which one wins? |
| G6 | **Invites a loop** — step two changes the input to step one |
| G7 | **Impossible** — there is no budget field and no operation creates one |
| G8 | Irreversible **and high-volume**. How many emails is too many to send without asking? |
