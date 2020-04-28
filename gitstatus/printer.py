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

    def _print(self, msg: str, msg_level: int, header: str = '',
               indent: int = 0):
        """Generic print method using click.secho"""
        # Just return if nothing should be printed
        if (msg_level < self.level):
            return

        # Add a space to the end of the header to separate the message
        if header:
            header += ' '

        # Construct and print full message
        msg = f'{self._indent*indent}{header}{msg}'
        click.secho(msg)

    # Print methods
    def debug(self, msg: str, indent: int = 0):
        self._print(msg, LEVELS["debug"],
                    header=click.style("[debug]  ", fg="blue"),
                    indent=indent)

    def info(self, msg: str, indent: int = 0):
        self._print(msg, LEVELS["info"],
                    header=click.style("[info]   ", fg="cyan"),
                    indent=indent)

    def warning(self, msg: str, indent: int = 0):
        self._print(msg, LEVELS["warning"],
                    header=click.style("[warning]", fg="yellow"),
                    indent=indent)

    def error(self, msg: str, indent: int = 0):
        self._print(msg, LEVELS["error"],
                    header=click.style("[error]  ", fg="red"),
                    indent=indent)
