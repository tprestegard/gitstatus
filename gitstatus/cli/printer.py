import click


# Print levels
LEVELS = {
    "debug": 10,
    "info": 20,
    "warning": 30,
    "error": 40,
    "quiet": 100,
}


class Printer:
    """
    Helper class for printing output with varying verbosity options,
    indentations, color, and headers.
    """
    def __init__(self, level: str = "info"):
        self.level = LEVELS.get(level, LEVELS["info"])
        self._indent = '  '

    def echo(self, msg: str, level: str, header: str = '',
               indent: int = 0, **kwargs):
        """Generic print method using click.secho"""
        # Just return if nothing should be printed
        if (LEVELS[level] < self.level):
            return

        # Add a space to the end of the header to separate the message
        if header:
            header += ' '

        # Construct and print full message
        msg = f'{self._indent*indent}{header}{msg}'
        click.secho(msg, **kwargs)

    def ok(self, msg: str = "", level: str = "info"):
        msg = msg if msg else "OK"
        self.echo(msg, fg="green", bold=True)

    def not_ok(self, msg: str = "", level: str = "info"):
        msg = msg if msg else "NOT OK"
        self.echo(msg, fg="red", bold=True)

    def warning(self, msg: str, indent: int = 0):
        self.echo(msg, LEVELS["warning"],
                  header=click.style("[warning]", fg="yellow"),
                  indent=indent)

    def error(self, msg: str, indent: int = 0):
        self.echo(msg, LEVELS["error"],
                  header=click.style("[error]", fg="red"),
                  indent=indent)

