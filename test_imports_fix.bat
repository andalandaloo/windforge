@echo off
echo 🔧 Testing Import Fixes for WindForge
echo.
echo 🐛 Previous Error:
echo "NameError: name 'SettingsDialog' is not defined"
echo.
echo ✅ Applied Fix:
echo • Added missing import: "from ui.settings_dialog import SettingsDialog"
echo • Organized UI component imports properly
echo • Verified all required imports are present
echo.

echo 🚀 Starting WindForge to test imports...
echo.
echo 📋 Test Steps:
echo 1. Application should start without import errors
echo 2. Navigate to Help menu
echo 3. Click "Settings" - should open without NameError
echo 4. Click "About" - should work properly
echo 5. Click "Icon Showcase" - should work properly
echo.

python main.py

echo.
echo 🔍 What to check:
echo • ✅ No "NameError" for SettingsDialog
echo • ✅ Settings dialog opens properly
echo • ✅ About dialog displays correctly
echo • ✅ Icon showcase launches successfully
echo • ✅ All menu items work without errors
echo.

echo 📊 Expected Console Messages:
echo • "✅ Theme 'apple_theme' loaded successfully"
echo • "✅ Gemini AI configured successfully!" (if API key is set)
echo • No Python import or NameError exceptions
echo.
pause
