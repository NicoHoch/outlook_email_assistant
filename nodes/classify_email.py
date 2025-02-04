from pydantic import BaseModel, Field
from models.state import State
from typing_extensions import Literal
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()


anthropicApiKey = os.getenv("ANTHROPIC_API_KEY")

llm = ChatAnthropic(model="claude-3-5-sonnet-latest", api_key=anthropicApiKey)


# Schema for structured output to use as routing logic
class Route(BaseModel):
    step: Literal["invoice", "spam", "meeting"] = Field(
        None, description="The next step in the routing process"
    )


# Augment the LLM with schema for structured output
router = llm.with_structured_output(Route)


def classify_email(state: State):
    """Route the input to the appropriate node"""

    # Run the augmented LLM with structured output to serve as routing logic
    decision = router.invoke(
        [
            SystemMessage(
                content="Route the input to invoice, spam, or meeting based on the user's request."
            ),
            HumanMessage(content=state["email"]["subject"]),
        ]
    )

    print("decision", decision)

    return {"decision": decision.step}
