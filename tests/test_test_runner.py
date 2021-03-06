from unittest import TestCase

from mock import patch
from pyselenium.test_metadata import Test
from pyselenium.test_steps import Step
from pyselenium.test_steps import StepResult

from pyselenium.test_runner import TestResult
from pyselenium.test_runner import TestRunner
from tests.test_data import any_click
from tests.test_data import any_navigate
from tests.testables import DriverTestable
from tests.testables import TestRunnerTestable


class TestTestResult(TestCase):
    """"Has unit tests for the TestResult class"""

    def test_add_step_result(self):
        test_result = TestResult(Test())

        test_result.add_step_result(StepResult(any_click()))
        test_result.add_step_result(StepResult(any_click()))
        test_result.add_step_result(StepResult(any_click()))

        self.assertEqual(3, len(test_result.step_results))


class TestTestRunner(TestCase):
    """"Has unit tests for the TestRunner class"""

    def test_run_test_exception(self):
        test_runner = TestRunner(Test())

        self.assertRaises(ValueError, test_runner.run_test)

    def test_run_test(self):
        with patch.object(Step, 'run') as run_mock:
            test = Test()

            test.add_step(any_click())
            test.add_step(any_navigate())

            test_runner_testable = TestRunnerTestable(test)

            driver_testable = DriverTestable()

            test_runner_testable.inject_driver_testable(driver_testable)

            run_mock.run.return_value(StepResult(any_click()))

            test_result = test_runner_testable.run_test()

            self.assertEqual(len(test.steps), len(test_result.step_results))
