"""Buyer Agent.

Goal: receive the factory request, identify the decision criteria,
coordinate the workflow, and present the final answer to the user.
It is the only agent that talks to the user.
"""

from agents.supplier_analysis_agent import analyze
from common import ask, banner
from tools.supplier_tool import find_supplier

# ---------------------------------------------------------------------------
# TODO 1  —  Complete this prompt.
#
# As written it asks for a loose summary, so the Supplier Analysis Agent
# receives vague criteria and has to guess the quantity and the deadline.
#
# Rewrite it so the Buyer Agent states the required quantity, the deadline
# in days, and which attributes matter for the decision. A short, fixed
# output shape is easier for the next agent to use than free prose.
# ---------------------------------------------------------------------------
CRITERIA_PROMPT = """You are the Buyer Agent for a factory.

Read the factory request below and summarise what the factory wants.

Factory request:
{request}

Answer in two or three short lines.
"""


def extract_criteria(llm, request: str) -> str:
    banner("Buyer Agent: identifying the decision criteria")
    criteria = ask(llm, CRITERIA_PROMPT.format(request=request))
    print(criteria)
    return criteria


def check_risks(recommendation: str, request: str, criteria: str) -> list[str]:
    """Flags a recommendation that cannot actually be met.

    -----------------------------------------------------------------------
    TODO 3  —  Implement at least one rule.

    Right now this returns nothing, so an impossible recommendation reaches
    the user unchallenged.

    `find_supplier(recommendation)` gives you the structured record for the
    supplier the agent named, or None if it named one that does not exist.
    Each record has: name, price_per_unit, delivery_days,
    reliability_score, capacity_units.

    Rules worth adding:
      * the supplier does not exist in the catalogue at all
      * capacity_units is below the quantity the factory asked for
      * delivery_days is above the deadline the factory gave
      * reliability_score is below some threshold you choose

    You will need the quantity and the deadline as numbers. Getting them
    out of the request is part of the exercise -- TODO 1 is one way.
    -----------------------------------------------------------------------
    """
    warnings: list[str] = []
    return warnings


def format_response(recommendation: str, warnings: list[str]) -> str:
    """Builds the answer the user sees.

    -----------------------------------------------------------------------
    TODO 4  —  Improve this format.

    It currently passes the model's raw text straight through. Give the
    user a predictable structure instead: the selected supplier, the
    justification, the trade-offs against the rejected options, and any
    warnings from check_risks.
    -----------------------------------------------------------------------
    """
    parts = [recommendation]
    if warnings:
        parts.append("\nWarnings:")
        parts.extend(f"  - {w}" for w in warnings)
    return "\n".join(parts)


def handle_request(llm, request: str) -> str:
    """The coordination strategy: a sequential handoff, orchestrated here."""
    banner("Factory user  ->  Buyer Agent")
    print(request)

    criteria = extract_criteria(llm, request)
    recommendation = analyze(llm, request, criteria)
    warnings = check_risks(recommendation, request, criteria)

    banner("Buyer Agent  ->  Factory user")
    answer = format_response(recommendation, warnings)
    print(answer)
    return answer
