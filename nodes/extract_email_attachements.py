from models.state import State


def extract_email_attachements(state: State):
    # extract email attachments
    # read content of invoice
    # add invoice details to excel file
    # add invoice to google drve
    # move email to folder
    print(state["email"]["sentDateTime"])
