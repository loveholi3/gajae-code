import unittest
import importlib.util
from pathlib import Path
import sys

# Import the cursor-log.py script as a module
script_path = Path(__file__).parent / "cursor-log.py"
spec = importlib.util.spec_from_file_location("cursor_log", script_path)
if spec and spec.loader:
    cursor_log = importlib.util.module_from_spec(spec)
    sys.modules["cursor_log"] = cursor_log
    spec.loader.exec_module(cursor_log)
    extract_text_delta = cursor_log.extract_text_delta
else:
    raise ImportError(f"Could not load module from {script_path}")


class TestExtractTextDelta(unittest.TestCase):
    def test_direct_text(self):
        """Test happy path: direct text in data."""
        entry = {"data": {"text": "hello direct"}}
        self.assertEqual(extract_text_delta(entry), "hello direct")

    def test_nested_text(self):
        """Test happy path: nested text inside data.message.value."""
        entry = {
            "data": {
                "message": {
                    "value": {
                        "text": "hello nested"
                    }
                }
            }
        }
        self.assertEqual(extract_text_delta(entry), "hello nested")

    def test_empty_entry(self):
        """Test edge case: empty entry."""
        entry = {}
        self.assertIsNone(extract_text_delta(entry))

    def test_data_missing(self):
        """Test edge case: data is missing (not explicitly needed since empty entry covers it, but good to be explicit)."""
        entry = {"other": "value"}
        self.assertIsNone(extract_text_delta(entry))

    def test_data_not_dict(self):
        """Test error condition: data is not a dict."""
        entry = {"data": "not a dict"}
        self.assertIsNone(extract_text_delta(entry))

        entry_list = {"data": ["list", "of", "strings"]}
        self.assertIsNone(extract_text_delta(entry_list))

    def test_message_not_dict(self):
        """Test error condition: data.message is not a dict."""
        entry = {
            "data": {
                "message": "not a dict"
            }
        }
        self.assertIsNone(extract_text_delta(entry))

    def test_value_not_dict(self):
        """Test error condition: data.message.value is not a dict."""
        entry = {
            "data": {
                "message": {
                    "value": "not a dict"
                }
            }
        }
        self.assertIsNone(extract_text_delta(entry))

    def test_value_missing_text(self):
        """Test error condition: data.message.value missing text."""
        entry = {
            "data": {
                "message": {
                    "value": {
                        "other_key": "other_value"
                    }
                }
            }
        }
        self.assertIsNone(extract_text_delta(entry))

    def test_none_inputs(self):
        """Test with None values where dicts are expected."""
        entry_data_none = {"data": None}
        self.assertIsNone(extract_text_delta(entry_data_none))

        entry_msg_none = {"data": {"message": None}}
        self.assertIsNone(extract_text_delta(entry_msg_none))

        entry_val_none = {"data": {"message": {"value": None}}}
        self.assertIsNone(extract_text_delta(entry_val_none))


if __name__ == '__main__':
    unittest.main()
