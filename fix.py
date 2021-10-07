#!/usr/bin/env python

import logging
import re

import click



# cli helper
def set_log_level(ctx, param, value):
    """Set the logging level"""
    levels = {
        'verbose': logging.INFO,
        'debug' : logging.DEBUG
    }
    if value:
        logging.basicConfig(level=levels[param.name])


@click.command(
    help="""Fix HTML issues created by the Sakai to Brightspace conversion.
    
    INPUT can be a file, or - or empty for stdin.
    """
)
@click.argument('input',type=click.File('rb'),default="-")
@click.option('--debug',
    help="Print lots of debugging statements",
    is_flag=True,
    expose_value=False,
    callback=set_log_level)
@click.option('--verbose',
    help="Be verbose",
    is_flag=True,
    expose_value=False,
    callback=set_log_level)
def cli(input):
    logging.info("Hello, world!")
    text = input.read().decode()
    print(text)


if __name__ == '__main__':
    cli()