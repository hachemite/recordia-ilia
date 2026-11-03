"""Unit and integration tests for AutoStepper module."""

import time
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from core.auto_stepper import AutoStepper, TriggerMode


class TestAutoStepper(unittest.TestCase):
    def test_init_and_state(self):
        stepper = AutoStepper(step_trigger_callback=lambda desc, meta: None)
        self.assertFalse(stepper.is_running)
        self.assertEqual(stepper.mode, TriggerMode.MANUAL)

    def test_periodic_timer_trigger(self):
        triggers = []
        def on_step(desc, meta):
            triggers.append((desc, meta))

        stepper = AutoStepper(step_trigger_callback=on_step)
        # Use very short interval for fast test
        stepper.start(TriggerMode.PERIODIC, interval_seconds=0.5)
        self.assertTrue(stepper.is_running)

        time.sleep(1.2)
        stepper.stop()
        self.assertFalse(stepper.is_running)

        self.assertGreaterEqual(len(triggers), 1)
        first_desc, first_meta = triggers[0]
        self.assertIn("Periodic capture", first_desc)
        self.assertEqual(first_meta["trigger_type"], "periodic_timer")

    def test_stop_when_idle(self):
        stepper = AutoStepper(step_trigger_callback=lambda desc, meta: None)
        stepper.stop()
        self.assertFalse(stepper.is_running)


if __name__ == "__main__":
    unittest.main()
