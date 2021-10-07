#!/usr/bin/env python

from datetime import datetime
import logging
import re

import click

def add_signature(text):
    """Add a program signature line"""
    text += "%% Fixed by {} on {}".format(__name__,datetime.now().isoformat())
    return text


def fix_date(text,date):
    """Update the line that declares the date"""
    fdate = date.strftime("{%d}{%m}{%Y}")
    logging.debug(f"{fdate=}")
    text = re.sub(
        r'^\\newdate\{lessondate\}.*$',
        r'\\newdate{lessondate}' + fdate,
        text,
        flags=re.MULTILINE)
    return text

# cli helper
def set_log_level(ctx, param, value):
    """Set the logging level"""
    levels = {
        'verbose': logging.INFO,
        'debug' : logging.DEBUG
    }
    if value:
        logging.basicConfig(level=levels[param.name])

def process_option_date(ctx,param,value):
    """Convert the string date provided on the command line
    to a `datetime.datetime` object"""
    if value is None:
        result = datetime.now()
    else:
        result = datetime.fromisoformat(value)
    return result 

@click.command(
    help="""Update lesson docstrip files
    
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
@click.option('--date',
    help='date to stamp file (ISO 8601 format)',
    default=None,
    callback=process_option_date)
def cli(date,input):
    logging.info("Hello, world!")
    text = input.read().decode()
    text = fix_date(text,date)
    text = add_signature(text)
    print(text)


if __name__ == '__main__':
    cli()