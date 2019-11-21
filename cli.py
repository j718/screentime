# -*- coding: utf-8 -*-

"""Console script for screentime."""
import sys
import click
from screentime.app import Screentime


@click.command()
def main(args=None):
    """Console script for screentime."""
    app = Screentime()
    app.apply_limits()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
