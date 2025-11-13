@echo off
echo ⚙️ WindForge Settings
echo.
echo 🔧 Opening configuration panel...
echo.
python -c "
import sys
from PyQt6.QtWidgets import QApplication
from core.config_manager import ConfigManager
from ui.settings_dialog import SettingsDialog

app = QApplication(sys.argv)
app.setApplicationName('WindForge Settings')
config_manager = ConfigManager()
dialog = SettingsDialog(config_manager)
dialog.exec()
"
pause
