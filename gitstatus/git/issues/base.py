

class Issue:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

    def __repr__(self):
        return self.name
