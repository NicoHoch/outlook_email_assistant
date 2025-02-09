from typing import TypedDict, List
from api.azure_graph_api import AzureGraphApiClient


class State(TypedDict):
    email: dict
    category: str
    attachments: list
    azureGraphClient: AzureGraphApiClient
