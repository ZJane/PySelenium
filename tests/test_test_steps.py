from unittest import TestCase
from tests.testables import DriverTestable
from test_steps import Click
from test_steps import Navigate
from test_steps import StepResult
from mock import patch


class TestStepResult(TestCase):
    """"Has unit tests for the StepResult class"""

    def test_initializer(self):
        click = Click()

        step_result = StepResult(click)

        self.assertIsNone(step_result.exception)
        self.assertTrue(step_result.success)
        self.assertEqual(click, step_result.step)

    def test_add_exception(self):
        exception = TypeError()

        step_result = StepResult(Click())
        step_result.exception = exception

        self.assertEqual(step_result.exception, exception)
        self.assertFalse(step_result.success)


class TestClick(TestCase):
    """"Has unit tests for the Click class"""

    def test_run_click_exception(self):
        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'click') as click_mock:
            exception = Exception()
            click_mock.side_effect = exception
            click = Click()
            click.css_path = 'any css path'
            click.hint = 'any hint'

            step_result = click.run(driver_testable)

            click_mock.assert_called_with(click.css_path, click.hint)
            self.assertFalse(step_result.success)
            self.assertEqual(step_result.step, click)
            self.assertEqual(step_result.exception, exception)


class TestNavigate(TestCase):
    """"Has unit tests for the Navigate class"""

    def test_run_navigate(self):
        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'navigate') as navigate_mock:
            navigate = Navigate()
            navigate.url = 'http://anyurl.com'

            step_result = navigate.run(driver_testable)

            navigate_mock.assert_called_with(navigate.url)
            self.assertTrue(step_result.success)
            self.assertEqual(step_result.step, navigate)

    def test_run_navigate_exception(self):
        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'navigate') as navigate_mock:
            exception = Exception()
            navigate_mock.side_effect = exception
            navigate = Navigate()
            navigate.url = 'http://anyurl.com'

            step_result = navigate.run(driver_testable)

            navigate_mock.assert_called_with(navigate.url)
            self.assertFalse(step_result.success)
            self.assertEqual(step_result.step, navigate)
            self.assertEqual(step_result.exception, exception)