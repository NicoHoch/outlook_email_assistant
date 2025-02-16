from pydantic import BaseModel, Field
from models.state import State
from typing_extensions import Literal
from langchain_core.messages import HumanMessage, SystemMessage
import os
from langchain_anthropic import ChatAnthropic


anthropicApiKey = os.getenv("ANTHROPIC_API_KEY")

llm = ChatAnthropic(model="claude-3-5-sonnet-latest", api_key=anthropicApiKey)


# Schema for structured output to use as routing logic
class Route(BaseModel):
    step: Literal["invoice", "advertisement", "other"] = Field(
        None, description="The next step in the routing process"
    )


# Augment the LLM with schema for structured output
router = llm.with_structured_output(Route)


def classify_email(state: State):
    """Route the input to the appropriate node"""

    result = "other"

    if state["email"]["subject"].startswith("Neuer Download"):
        result = "download"
    elif state["email"]["subject"].startswith("Neues Ereignis"):
        result = "meeting"
    else:

        sysMessage = SystemMessage(
            content="""Be my personal E-Mail Routing assistant. Your job is to look at the email subject, the sender and the has_attachment flag to classify the mail as invoice, spam, or other.
                        invoice - the email subject indicates the email to contain an invoice and the email has an attachment.
                        advertisement - the email indicates a newsletter or advertisement email from a company. It's always this class if the email contains emojis or a strong advertisment language promising discounts or offers. Example subjects: No Custom Email Domain? Let's Change That! ✏️, Make your Menti presentation even better 💪
                        other - the email is neither an invoice nor advertisement. It may be a personal email or a notification.
                    """,
        )
        humanMessage = HumanMessage(
            content=f"subject: {state['email']['subject']}; sender: {state['email']['sender']['emailAddress']['address']}; has_attachment: {state['email']['hasAttachments']}"
        )
        # Run the augmented LLM with structured output to serve as routing logic
        decision = router.invoke(
            [
                sysMessage,
                humanMessage,
            ]
        )

        result = decision.step

    return {"decision": result}
