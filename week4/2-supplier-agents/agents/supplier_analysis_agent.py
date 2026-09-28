"""Supplier Analysis Agent.

Goal: compare the available suppliers and recommend one.
Tool: the Supplier Information Tool.
It does not talk to the user. It is called by the Buyer Agent.
"""

from common import ask, banner
from tools.supplier_tool import supplier_information

# ---------------------------------------------------------------------------
# TODO 2  —  Complete this prompt.
#
# As written, it only says "recommend one supplier". It does not tell the
# agent which attributes matter, how to weigh them, or that the factory's
# quantity and deadline are hard constraints rather than preferences.
#
# Run the system first and look at what it recommends. Then rewrite the
# instruction block so the agent explicitly compares price, delivery time,
# reliability and capacity, and rejects any supplier that cannot meet the
# requested quantity or deadline.
# ---------------------------------------------------------------------------
ANALYSIS_PROMPT = """You are the Supplier Analysis Agent for a factory.

Factory request:
{request}

Criteria identified by the Buyer Agent:
{criteria}

Supplier information:
{suppliers}

Recommend one supplier.
"""


def analyze(llm, request: str, criteria: str) -> str:
    """Reads the supplier catalogue through the tool, then recommends one."""
    banner("Supplier Analysis Agent  ->  Supplier Information Tool")
    suppliers = supplier_information.invoke({})
    print(suppliers)

    banner("Supplier Analysis Agent: recommending")
    recommendation = ask(
        llm,
        ANALYSIS_PROMPT.format(
            request=request, criteria=criteria, suppliers=suppliers
        ),
    )
    print(recommendation)
    return recommendation
