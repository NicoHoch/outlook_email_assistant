from api.azure_graph_api import AzureGraphApiClient


class State(dict):
    email: dict
    category: str
    attachments: list
    azureGraphClient: AzureGraphApiClient
