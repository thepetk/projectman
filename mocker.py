from github.Repository import Repository
from github.Requester import Requester


class GithubMocker:
    REPO = Repository(
        requester=Requester(
            auth=None,
            base_url="https://test.com",
            timeout=0,
            user_agent="",
            per_page=1,
            retry=1,
            pool_size=1,
            verify=False,
        ),
        headers={},
        attributes={},
        completed=True,
    )
    FILEPATH = "filepath"
    SIMPLE_CONTENT = '[{"name": "test", "labels": ["bug"],"assignees": ["thepetk"],"reviewers": ["thepetk"],"milestones": ["12/12/2023"],"created_on": "dmdmd","last_updated_on": "fefde","closed_on": "rfcrsd","type": "None"}]'  # noqa: E501
    NO_LIST_CONTENT = '{"name": "test", "labels": ["bug"],"assignees": ["thepetk"],"reviewers": ["thepetk"],"milestones": ["12/12/2023"],"created_on": "dmdmd","last_updated_on": "fefde","closed_on": "rfcrsd","type": "None"}'  # noqa: E501
