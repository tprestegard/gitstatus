import enum


class Issue:
    def __init__(self, name: str, type_: str, desc: str = ""):
        self.name = name
        self.type_ = type_
        if not desc:
            desc = " ".join(
                [word.lower() for word in name.split("_")]).capitalize()]
            )

    def __repr__(self):
        return self.name


class IssueType(enum.Enum):
    BRANCH = "branch"
    REPO = "repo"
