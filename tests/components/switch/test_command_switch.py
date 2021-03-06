"""
tests.components.switch.test_command_switch
~~~~~~~~~~~~~~~~~~~~~~~~

Tests command switch.
"""
import json
import os
import tempfile
import unittest

from homeassistant import core
from homeassistant.const import STATE_ON, STATE_OFF
import homeassistant.components.switch as switch


class TestCommandSwitch(unittest.TestCase):
    """ Test the command switch. """

    def setUp(self):  # pylint: disable=invalid-name
        self.hass = core.HomeAssistant()

    def tearDown(self):  # pylint: disable=invalid-name
        """ Stop down stuff we started. """
        self.hass.stop()

    def test_state_none(self):
        with tempfile.TemporaryDirectory() as tempdirname:
            path = os.path.join(tempdirname, 'switch_status')
            test_switch = {
                'oncmd': 'echo 1 > {}'.format(path),
                'offcmd': 'echo 0 > {}'.format(path),
            }
            self.assertTrue(switch.setup(self.hass, {
                'switch': {
                    'platform': 'command_switch',
                    'switches': {
                        'test': test_switch
                    }
                }
            }))

            state = self.hass.states.get('switch.test')
            self.assertEqual(STATE_OFF, state.state)

            switch.turn_on(self.hass, 'switch.test')
            self.hass.pool.block_till_done()

            state = self.hass.states.get('switch.test')
            self.assertEqual(STATE_ON, state.state)

            switch.turn_off(self.hass, 'switch.test')
            self.hass.pool.block_till_done()

            state = self.hass.states.get('switch.test')
            self.assertEqual(STATE_OFF, state.state)


    def test_state_value(self):
        with tempfile.TemporaryDirectory() as tempdirname:
            path = os.path.join(tempdirname, 'switch_status')
            test_switch = {
                'statecmd': 'cat {}'.format(path),
                'oncmd': 'echo 1 > {}'.format(path),
                'offcmd': 'echo 0 > {}'.format(path),
                'value_template': '{{ value=="1" }}'
            }
            self.assertTrue(switch.setup(self.hass, {
                'switch': {
                    'platform': 'command_switch',
                    'switches': {
                        'test': test_switch
                    }
                }
            }))

            state = self.hass.states.get('switch.test')
            self.assertEqual(STATE_OFF, state.state)

            switch.turn_on(self.hass, 'switch.test')
            self.hass.pool.block_till_done()
        
            state = self.hass.states.get('switch.test')
            self.assertEqual(STATE_ON, state.state)

            switch.turn_off(self.hass, 'switch.test')
            self.hass.pool.block_till_done()

            state = self.hass.states.get('switch.test')
            self.assertEqual(STATE_OFF, state.state)


    def test_state_json_value(self):
        with tempfile.TemporaryDirectory() as tempdirname:
            path = os.path.join(tempdirname, 'switch_status')
            oncmd = json.dumps({'status': 'ok'})
            offcmd = json.dumps({'status': 'nope'})
            test_switch = {
                'statecmd': 'cat {}'.format(path),
                'oncmd': 'echo \'{}\' > {}'.format(oncmd, path),
                'offcmd': 'echo \'{}\' > {}'.format(offcmd, path),
                'value_template': '{{ value_json.status=="ok" }}'
            }
            self.assertTrue(switch.setup(self.hass, {
                'switch': {
                    'platform': 'command_switch',
                    'switches': {
                        'test': test_switch
                    }
                }
            }))

            state = self.hass.states.get('switch.test')
            self.assertEqual(STATE_OFF, state.state)

            switch.turn_on(self.hass, 'switch.test')
            self.hass.pool.block_till_done()

            state = self.hass.states.get('switch.test')
            self.assertEqual(STATE_ON, state.state)

            switch.turn_off(self.hass, 'switch.test')
            self.hass.pool.block_till_done()

            state = self.hass.states.get('switch.test')
            self.assertEqual(STATE_OFF, state.state)

    def test_state_code(self):
        with tempfile.TemporaryDirectory() as tempdirname:
            path = os.path.join(tempdirname, 'switch_status')
            test_switch = {
                'statecmd': 'cat {}'.format(path),
                'oncmd': 'echo 1 > {}'.format(path),
                'offcmd': 'echo 0 > {}'.format(path),
            }
            self.assertTrue(switch.setup(self.hass, {
                'switch': {
                    'platform': 'command_switch',
                    'switches': {
                        'test': test_switch
                    }
                }
            }))

            state = self.hass.states.get('switch.test')
            self.assertEqual(STATE_OFF, state.state)

            switch.turn_on(self.hass, 'switch.test')
            self.hass.pool.block_till_done()

            state = self.hass.states.get('switch.test')
            self.assertEqual(STATE_ON, state.state)

            switch.turn_off(self.hass, 'switch.test')
            self.hass.pool.block_till_done()

            state = self.hass.states.get('switch.test')
            self.assertEqual(STATE_ON, state.state)
