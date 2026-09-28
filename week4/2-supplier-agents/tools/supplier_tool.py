"""The Supplier Information Tool.

This is the agents' only window onto the environment. Everything the
Supplier Analysis Agent knows about suppliers comes through this tool.

If an agent mentions a supplier that this tool never returned, the agent
invented it. Watch for that when you run the system.
"""

import json
import os

from langchain_core.tools import tool

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "suppliers.json")


def load_catalogue() -> dict:
    """Reads the raw supplier data. Used by the tool and by the risk check."""
    with open(DATA_FILE, "r", encoding="utf-8") as handle:
        return json.load(handle)


@tool("supplier_information")
def supplier_information() -> str:
    """Returns every available supplier with price per unit, delivery time in
    days, a reliability score between 0 and 1, and maximum capacity in units.
    Call this before recommending any supplier. Never recommend a supplier
    that this tool did not return."""
    catalogue = load_catalogue()
    lines = [f"Component: {catalogue['component']}  (prices in {catalogue['currency']})"]
    for supplier in catalogue["suppliers"]:
        lines.append(
            f"- {supplier['name']} "
            f"| price per unit: ${supplier['price_per_unit']:.2f} "
            f"| delivery: {supplier['delivery_days']} days "
            f"| reliability: {supplier['reliability_score']:.2f} "
            f"| capacity: {supplier['capacity_units']} units"
        )
    return "\n".join(lines)


def find_supplier(text: str) -> dict | None:
    """Returns the supplier record whose name appears in `text`, or None.

    Useful for the risk check in agents/buyer_agent.py: pass the agent's
    recommendation and get back the structured record it refers to.
    """
    lowered = text.lower()
    for supplier in load_catalogue()["suppliers"]:
        if supplier["name"].lower() in lowered:
            return supplier
    return None
