import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
import json

# Adjust path to import Model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import model as Model

class TestStartup(unittest.TestCase):

    @patch('utils.model.winreg')
    @patch('shutil.copy2')
    @patch('utils.model.os')
    @patch('builtins.open', new_callable=mock_open, read_data='{"Startup": false}')
    def test_toggle_startup_enable(self, mock_file, mock_os, mock_copy2, mock_winreg):
        # Setup mocks
        mock_os.path.join.side_effect = os.path.join
        mock_os.path.abspath.side_effect = os.path.abspath
        mock_os.path.dirname.side_effect = os.path.dirname
        mock_os.getenv.return_value = r"C:\Users\Test\AppData\Local"
        
        mock_os.path.exists.return_value = False # Folder doesn't exist initially
        
        # Call function
        Model.toggle_startup(True)
        
        # Verifications
        # 1. Check directory creation
        expected_dir = os.path.join(r"C:\Users\Test\AppData\Local", "FileORZ")
        mock_os.makedirs.assert_called_with(expected_dir)
        
        # 2. Check file copy
        self.assertTrue(mock_copy2.called, "File copy should be called")
        # self.assertEqual(mock_copy2.call_count, 2)
        
        # 3. Check registry
        mock_winreg.OpenKey.assert_called()
        mock_winreg.SetValueEx.assert_called()
        
        # Check if set value points to the new location
        args, _ = mock_winreg.SetValueEx.call_args
        key, name, reserved, type_, value = args
        self.assertEqual(name, "FileORZ")
        self.assertTrue(value.startswith(expected_dir))

    @patch('utils.model.winreg')
    def test_toggle_startup_disable(self, mock_winreg):
        # Call function
        Model.toggle_startup(False)
        
        # Verify delete
        mock_winreg.DeleteValue.assert_called()

if __name__ == '__main__':
    unittest.main()
