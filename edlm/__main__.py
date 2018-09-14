# coding=utf-8
"""
Main entry point
"""

# noinspection SpellCheckingInspection
if __name__ == '__main__':
    from edlm.cli import cli

    cli(obj={})  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    exit(0)
