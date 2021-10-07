#!/usr/bin/env python

from datetime import datetime
import logging
import os.path
import re
import sys

import click

def add_signature(text):
    """Add a program signature line"""
    script_name = os.path.basename(sys.argv[0])
    fdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text += f"% Fixed by {script_name} on {fdate}"
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


def fix_article_only_sections(text):
    """Update sections that are declared article mode only
    
    Fix strings like:

        \mode<article>{%
        \section*{Objectives}
        }% end mode<article>

    To:

        \section<article>*{Objectives}
    """
    text = re.sub(r"^\\mode<article>\{%?\n\\section\*\{(.*?)\}.*\}.*$",
        r"\\section<article>*{\1}",
        text,
        flags=re.MULTILINE)
    return text


def fix_quotes(text):
    """Replace ASCII TeX quotes with UTF curly quotes"""
    open_quote = re.escape(r"``")
    close_quote = re.escape(r"''")
    text = re.sub(
        open_quote + r"(.*?)" + close_quote, 
        r"“\1”",
        text,
        flags=re.MULTILINE
    )
    return text


def fix_tabs(text):
    """Replace tabs with four spaces"""
    return text.replace('\t','    ')


# Command line helpers
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
    text = fix_date(text,date)
    text = fix_article_only_sections(text)
    text = fix_quotes(text)
    text = fix_tabs(text)
    text = add_signature(text)
    print(text)


if __name__ == '__main__':
    cli()