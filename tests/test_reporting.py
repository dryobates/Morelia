# -*- coding: utf-8 -*-
import json
import os
from unittest import TestCase
from unittest.mock import patch, mock_open

from six.moves import StringIO

from morelia import run
from morelia.decorators import tags
from morelia.reporters import JSONReporter

pwd = os.path.dirname(os.path.realpath(__file__))


@tags(['acceptance'])
class ReportingTest(TestCase):

    class TestCaseStub(TestCase):

        def step_this_step_passes(self):
            r'this step passes'
            pass

    def test_reporting(self):
        filename = os.path.join(pwd, 'features/reporting.feature')
        run(filename, self)

    def step_a_feature_file_with(self, filename, _text=None):
        r'a feature file "([^"]+)" with'
        self.__filename = filename
        self.__file_contents = _text.encode('utf-8')

    def step_JSON_reporter_is_configured(self):
        r'JSON reporter is configured'
        self.__output_file = StringIO()
        self.__reporter = JSONReporter(self.__output_file)

    def step_Morelia_evaluates_the_file(self):
        r'Morelia evaluates the file'
        file_mock = mock_open(read_data=self.__file_contents)
        with patch('morelia.parser.open', file_mock):
            test_case = self.TestCaseStub()
            run(self.__filename, test_case, reporter=self.__reporter)

    def step_it_writes_json_file(self, _text=None):
        r'it writes json file'

        expected_json = json.loads(_text)
        written_file_contents = self.__output_file.getvalue()
        written_json = json.loads(written_file_contents)
        self.assertEqual(expected_json, written_json)
