import pytest

import fix


@pytest.mark.parametrize("test_input,expected",[
    ("``foo''","“foo”"),
    ("`foo'","‘foo’")
])
def test_fix_quotes(test_input,expected):
    assert fix.fix_quotes(test_input) == expected


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

