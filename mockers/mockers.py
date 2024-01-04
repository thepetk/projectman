import json

from github.Repository import Repository
from github.Requester import Requester

from configuration import ConfigurationItem
from utils import ISSUES


class ConfigurationMocker:
    def __init__(
        self,
        filepath: str = "filepath",
        name: str = "test",
        description: str = "",
        public: bool = True,
        item_type: str = ISSUES,
        labels: list[str] = [],
        assignees: list[str] = [],
        reviewers: list[str] = [],
        milestones: list[str] = [],
        created_on: str = "2023-11-11T01:59:59",
        last_updated_on: str = "2023-11-11T01:59:59",
        closed_on: str = "2023-11-11T01:59:59",
    ) -> None:
        self.filepath = filepath
        self.configuration_item = ConfigurationItem(
            item_type=item_type,
            labels=labels,
            assignees=assignees,
            milestones=milestones,
            last_updated_on=last_updated_on,
            created_on=created_on,
            closed_on=closed_on,
        )
        self.config_dict = {
            "name": name,
            "description": description,
            "public": public,
            "type": item_type,
            "labels": labels,
            "assignees": assignees,
            "reviewers": reviewers,
            "milestones": milestones,
            "created_on": created_on,
            "last_updated_on": last_updated_on,
            "closed_on": closed_on,
        }

    @property
    def no_list_json_content(self) -> str:
        return json.dumps(self.config_dict)

    @property
    def list_json_content(self) -> str:
        return json.dumps([self.config_dict])


class GithubMocker(ConfigurationMocker):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.repo = Repository(
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
        self.file_contents = self.list_json_content
