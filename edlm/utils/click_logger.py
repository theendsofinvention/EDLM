# coding=utf-8

import logging
import click

class ClickLoggingHandler(logging.Handler):
    """
    Transmits logging records to click
    """

    def emit(self, record: logging.LogRecord):
        """
        Emits a record

        Args:
            record: record to emit
        """
        msg = self.format(record)
        if record.levelno == logging.DEBUG:
            click.secho(msg)
        elif record.levelno == logging.INFO:
            click.secho(msg, fg='green')
        elif record.levelno == logging.WARNING:
            click.secho(msg, fg='magenta')
        else:
            click.secho(msg, fg='red', err=True)

    def __init__(self, level=logging.DEBUG):
        logging.Handler.__init__(self, level)


def install_click_logger(logger: logging.Logger, formatter: logging.Formatter = None, level=logging.DEBUG):
    """
    Installs a logging handler that'll emit logging records to the console

    Args:
        logger: logger to install the handler on
        formatter: special formatter (defaults to parent's)
        level: logging level (defaults to DEBUG)

    Returns:

    """
    handler = ClickLoggingHandler(level)
    if formatter:
        handler.setFormatter(formatter)
    logger.addHandler(handler)
