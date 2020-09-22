from .request_client import RequestClient


class Sections:
    """
    The Sections class contains methods to get sections' information from Schoology API

    Args:
        SCHOOLOGY_KEY (str): The consumer key given by Schoology
        SCHOOLOGY_SECRET (str): The consumer secret given by Schoology

    Attributes:
        request_client (RequestClient): The client used for authenticate and send requests to Schoology

    """

    def __init__(self, SCHOOLOGY_KEY, SCHOOLOGY_SECRET):
        self.request_client = RequestClient(SCHOOLOGY_KEY, SCHOOLOGY_SECRET)

    def get_by_id(self, section_id):
        response = self.request_client.get(f"sections/{section_id}")
        return response
