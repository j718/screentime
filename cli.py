# -*- coding: utf-8 -*-

"""Console script for linux_screentime."""
import sys
import click
from linux_screentime import linux_screentime


@click.command()
def main(args=None):
    """Console script for linux_screentime."""
    linux_screentime.main()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
