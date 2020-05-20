import click


class StyledStr2(str):
    def __new__(cls, value: str, *args, **kwargs):
        return super().__new__(cls, value)

    def __init__(self, value: str, raw: str = None):
        self.raw = raw if raw else click.unstyle(value)

    def split(self, *args, **kwargs):
        return [self.__class__(s) for s in self.raw.split(*args, **kwargs)]


class BoldGreenStr2(StyledStr2):
    def __new__(cls, value, *args, **kwargs):
        return super().__new__(cls, click.style(value, fg="green", bold=True))


class BoldRedStr2(StyledStr2):
    def __new__(cls, value, *args, **kwargs):
        return super().__new__(cls, click.style(value, fg="red", bold=True))


class StyledStr(str):
    def __new__(cls, value: str, *args, **kwargs):
        return super().__new__(cls, value)

    def __init__(self, value: str):
        self.styled = self.style(value)

    @classmethod
    def style(cls, s: str):
        return s

    #def split(self, *args, **kwargs):
    #    return [self.__class__(s) for s in self.raw.split(*args, **kwargs)]


class BoldGreenStr(StyledStr):
    @classmethod
    def style(cls, s: str):
        return click.style(s, fg="green", bold=True)


class BoldRedStr(StyledStr):
    @classmethod
    def style(cls, s: str):
        return click.style(s, fg="red", bold=True)
