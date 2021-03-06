from datetime import datetime
import pytest

from fixdtx import fix


@pytest.mark.parametrize("test_input,expected",[
    ("``foo''","“foo”"),
    ("`foo'","‘foo’")
])
def test_fix_quotes(test_input,expected):
    assert fix.fix_quotes(test_input) == expected


@pytest.mark.parametrize("test_input,expected",[
    ('\n'.join([
        r'\title[',
        r'%	short title=,',
        r'	lesson number=15,',
        r'	textbook section=11.6',
        r'	]{Directional Derivatives and the Gradient Vector Field}',
        r'\input{../course.def}'
    ]),
    '\n'.join([
        r'\title[',
        r'%    short title=,',
        r'    lesson number=15,',
        r'    textbook section=11.6',
        r'    ]{Directional Derivatives and the Gradient Vector Field}',
        r'\input{../course.def}'
    ]))
])
def test_fix_tabs(test_input,expected):
    assert fix.fix_tabs(test_input) == expected


@pytest.mark.parametrize("test_input,expected",[
    (
        '\n'.join([r'\mode<article>{',r'\section*{Do Now}}']),
        '\n'.join([r'\section<article>*{Do Now}',''])
    ),
    (
        '\n'.join([r'\mode<article>{%',r'\section*{Anticipatory Set}}']),
        '\n'.join([r'\section<article>*{Anticipatory Set}',''])
    ),
    (
        '\n'.join([
            r'\mode<article>{%',
            r'\section*{Objectives}',
            r'}% end mode<article>'
        ]),
        '\n'.join([r'\section<article>*{Objectives}',''])
    ),
    # make sure the matching isn't too greedy
    (
        '\n'.join([
            r'\mode<article>{%',
            r'\section*{Objectives}',
            r'}% end mode<article>',
            r'\foo{bar}'
        ]),
        '\n'.join([
            r'\section<article>*{Objectives}',
            '',
            r'\foo{bar}'
        ])
    )
])
def test_fix_article_only_sections(test_input,expected):
    assert fix.fix_article_only_sections(test_input) == expected


def test_fix_date():
    dt = datetime(2021,10,7)
    test_input = r'\newdate{lessondate}{8}{3}{2016}'
    expected = r'\newdate{lessondate}{07}{10}{2021}'
    assert fix.fix_date(test_input,dt) == expected