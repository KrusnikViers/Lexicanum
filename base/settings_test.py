import inspect
import re
import unittest

from base import settings


def _get_all_settings() -> list[settings.OptionDefinition]:
    return [
        value for name, value in inspect.getmembers(settings)
        if name.isupper() and isinstance(value, settings.OptionDefinition)
    ]


class TestSettings(unittest.TestCase):
    def test_settings_keys_format(self):
        keys_set = set()
        for option in _get_all_settings():
            stored_key = option.name
            self.assertEqual(stored_key, stored_key.strip(), "Stored key contains extra space characters.")
            self.assertGreater(len(stored_key), 0, f"Stored key for {stored_key} is empty.")
            self.assertTrue(re.match(r'^[\w/\-]*$', stored_key),
                            f'Stored settings key {stored_key} has characters that are not alphanumeric, /, - or _.')
            self.assertTrue(stored_key.islower(),
                            f'Stored key {stored_key} should be in lower register to avoid cross-system conflicts.')
            self.assertNotIn(stored_key, keys_set, f'Duplicate stored key: {stored_key}')
            keys_set.add(stored_key)

    def test_settings_default_value_types(self):
        for option in _get_all_settings():
            self.assertIsInstance(option.default, option.type,
                                  f'Default value for {option.name} should be {option.type}')

    def test_set_type_mismatch(self):
        test_option = settings.OptionDefinition('test_setting', int, 0)
        test_option.set(1)
        with self.assertRaises(TypeError):
            test_option.set("Not a string")
