# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest
from zeppelin.converters.markdown import LegacyConverter
from dateutil.parser import parse


@pytest.fixture
def zc():
    zc = LegacyConverter('in', 'out', '', 'anonymous', 'N/A', 'N/A')
    return zc


def test_header(zc):
    zc.user = 'tester'
    zc.build_header('title')
    assert zc.out == ['---',
                      'title: title',
                      'author(s): tester',
                      'created_at: ' + zc.date_created,
                      'updated_at: ' + zc.date_updated,
                      '---']


def test_build_markdown(zc):
    zc.build_markdown(None)
    assert zc.out == []
    zc.build_markdown('sample body')
    assert zc.out == ['sample body']


def test_build_code(zc):
    zc.build_code('scala', None)
    assert zc.out == ['```scala', '```']
    zc.build_code('scala', 'sample body')
    assert zc.out == ['```scala', '```',
                      '```scala', 'sample body', '```']


@pytest.mark.parametrize('test_input, expected_lang, expected_body', [
                         ('%md', 'md', None),
                         ('%md text', 'md', 'text'),
                         (' %md   text', 'md', 'text'),
                         (' sample text', 'scala', 'sample text'),
                         ('s%ample', 'scala', 's%ample')])
def test_parse_input_text(zc, test_input, expected_lang, expected_body):
    lang, body = zc.parse_input_text(test_input)
    assert (lang, body) == (expected_lang, expected_body)


def test_build_text(zc):
    zc.build_text('one ring to rule them all')
    zc.build_text('one ring to find them')
    assert zc.out == ['one ring to rule them all', 'one ring to find them']


def test_title(zc):
    assert zc.out == []
    zc.process_title('title')
    assert zc.out == ['#### title']


@pytest.mark.parametrize('test_input, expected', [
                         ('', []),
                         ('test', ['test']),
                         ('test\ttest2', ['|test|test2|']),
                         ('test\t\ttest2', ['|test||test2|'])
                         ])
def test_create_md_row(zc, test_input, expected):
    zc.create_md_row(test_input)
    assert zc.out == expected


def test_create_md_row_header(zc):
    zc.create_md_row('test\ttest2', True)
    assert zc.out == ['|test|test2|\n|-|-|']


def test_find_image(zc):
    data = 'nothing here'
    assert zc.find_image(data) is None
    data = ('\u003cdiv id\u003d\"inline1\" style\u003d\"height:400px\"\u003e'+
        '\u003csvg\u003e\u003c/svg\u003e\u003c/div\u003e\n')
    assert zc.find_image(data) is None # empty svg
    data = '<svg><text x="0" y="15">Test SVG</text></svg>'
    assert zc.find_image(data) == data # empty svg


def test_process_date_created(zc):
    zc.process_date_created('Feb 28, 2017 3:44:54 PM')
    zc.process_date_created('Feb 28, 2017 4:44:54 PM')
    assert zc.date_created == parse('Feb 28, 2017 3:44:54 PM')

    zc.date_created = 'N/A'
    zc.process_date_created('2015-07-03T01:43:40+0000')
    zc.process_date_created('2015-07-04T01:43:40+0000')
    assert zc.date_created == parse('2015-07-03T01:43:40+0000')


def test_process_date_updated(zc):
    zc.process_date_updated('Feb 28, 2017 3:44:54 PM')
    zc.process_date_updated('Feb 28, 2017 4:44:54 PM')
    assert zc.date_updated == parse('Feb 28, 2017 4:44:54 PM')

    zc.date_updated = 'N/A'
    zc.process_date_updated('2015-07-03T01:43:40+0000')
    zc.process_date_updated('2015-07-04T01:43:40+0000')
    assert zc.date_updated == parse('2015-07-04T01:43:40+0000')


def test_process_results(zc):
    paragraph = {}
    zc.process_results(paragraph)
    assert zc.out == []
    paragraph = {
        'result': {
            'code': 'SUCCESS',
            'msg': ''
        }
    }
    zc.process_results(paragraph)
    assert zc.out == []
    paragraph = {
        'result': {
            'code': 'SUCCESS',
            'msg': 'one ring to bring them all',
            'type': 'TEXT'
        }
    }
    zc.process_results(paragraph)
    assert zc.out == ['```python', '# Output:\n# -------\n# one ring to bring them all', '```']

