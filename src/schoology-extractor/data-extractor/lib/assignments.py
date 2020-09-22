from .request_client import RequestClient


class Assignments:
    """
    The Assignments class contains methods to get assignments' information from Schoology API

    Args:
        SCHOOLOGY_KEY (str): The consumer key given by Schoology
        SCHOOLOGY_SECRET (str): The consumer secret given by Schoology

    Attributes:
        request_client (RequestClient): The client used for authenticate and send requests to Schoology

    """

    def __init__(self, SCHOOLOGY_KEY, SCHOOLOGY_SECRET):
        self.request_client = RequestClient(SCHOOLOGY_KEY, SCHOOLOGY_SECRET)

    def get_by_section_id_array(self, section_id_array):
        assignments = []
        for section_id in section_id_array:
            url = f"sections/{section_id}/assignments"
            response = self.request_client.get(url)

            assignments = assignments + response["assignment"]

        return assignments
