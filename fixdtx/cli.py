from datetime import datetime
import logging

import click

from fixdtx.fix import fix_all

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
    help='date to stamp lesson (ISO 8601 format)',
    default=None,
    callback=process_option_date)
def cli(date,input):
    logging.info("Hello, world!")
    text = input.read().decode()
    text = fix_all(text,date)
    print(text)


if __name__ == '__main__':
    cli()