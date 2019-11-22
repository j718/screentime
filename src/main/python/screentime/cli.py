# -*- coding: utf-8 -*-

"""Console script for screentime."""
import sys
import click
from .app import runner


@click.command()
def main(args=None):
    """Console script for screentime."""
    runner()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
