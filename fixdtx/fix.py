#!/usr/bin/env python

from datetime import datetime
import logging
import os.path
import re
import sys


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

        
        \\mode<article>{%
        \\section*{Objectives}
        }% end mode<article>

    To:

        \\section<article>*{Objectives}
    """
    text = re.sub(
        # r"^\\mode<article>\{%?\n\\section\*\{(.*?)\}.*?\}.*$",
        r"\\mode<article>\{\%?\n\\section\*\{(.*?)\}\n?\}.*$",
        r"\\section<article>*{\1}\n",
        text,
        flags=re.MULTILINE)
    return text


def fix_quotes(text):
    """Replace ASCII TeX quotes with UTF curly quotes"""
    text = re.sub(r"``(.*?)''",r"“\1”",text,flags=re.MULTILINE)
    text = re.sub(r"`(.*?)'",r"‘\1’",text,flags=re.MULTILINE)
    return text


def fix_tabs(text):
    """Replace tabs with four spaces"""
    return text.replace('\t','    ')


def fix_driver_block(text):
    """Update the DocStrip “driver“ block at the head of the file"""
    driver_block = r"""%<*dtx>
%%!TEX TS-program = dtxmake
%</dtx>
%<*driver>
\\input docstrip.tex
\\declarepreamble\\xelatexmkpreamble
\\space
!TEX TS-program = xelatexmk
\\endpreamble
\\askforoverwritefalse
\\generate{
    \\file{\\jobname.ws.tex}{\\from{\\jobname.dtx}{worksheet}}
    \\file{\\jobname.ws-sol.tex}{\\from{\\jobname.dtx}{worksheet,solutions}}
    \\usepreamble\\xelatexmkpreamble
    \\file{\\jobname.slides.tex}{\\from{\\jobname.dtx}{slides,lesson}}
    \\file{\\jobname.handout.tex}{\\from{\\jobname.dtx}{handout,lesson}}    
    \\file{\\jobname.lp.tex}{\\from{\\jobname.dtx}{lesson,plan}}
}
\\endbatchfile
%</driver>"""
    text = re.sub(
        r'.*</driver>',
        driver_block,
        text,
        flags=re.DOTALL)
    return text


def fix_documentclass_declaration(text):
    """Update the `\\documentclass` declaration block"""
    text = re.sub(
        r'\\documentclass.*\\title',
        r"""\\documentclass
%<slides|handout>[ignorenonframetext,aspectratio=169]
%<slides>{ngelessonslides}
%<handout>{ngelessonhandout}
%<plan>{ngelessonplan}
%<worksheet&solutions>[solutions]
%<worksheet>{ngelessonworksheet}
\\title""",
        text,
        flags=re.DOTALL
    )
    return text


def fix_all(text,date=None):
    """Do all the fixes"""
    if date is None:
        date = datetime.now()
    text = fix_driver_block(text)
    text = fix_date(text,date)
    text = fix_article_only_sections(text)
    text = fix_documentclass_declaration(text)
    text = fix_quotes(text)
    text = fix_tabs(text)
    text = add_signature(text)
    return text
    

