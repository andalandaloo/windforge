@echo off
echo 🔧 Testing API Key Fix for WindForge
echo.
echo 🐛 Previous Error:
echo "setEnabled(self, a0: bool): argument 1 has unexpected type 'str'"
echo.
echo ✅ Applied Fixes:
echo • Added explicit bool() conversion for setEnabled calls
echo • Added error handling in check_ai_status function
echo • Added error handling in set_api_key function
echo • Added error handling in browse_project_folder function
echo • Added fallback status messages for error cases
echo.

echo 🚀 Starting WindForge to test API key functionality...
echo.
echo 📋 Test Steps:
echo 1. Application should start without errors
echo 2. Navigate to AI Generator tab
echo 3. Enter a Google API key
echo 4. Click "Set API Key" button
echo 5. Check that no setEnabled errors occur
echo.

python main.py

echo.
echo 🔍 What to check:
echo • ✅ No "setEnabled" type errors in console
echo • ✅ API key setting works smoothly
echo • ✅ Status messages display correctly
echo • ✅ Generate button enables/disables properly
echo • ✅ Error dialogs show helpful messages
echo.

echo 📊 Expected Console Messages:
echo • "✅ Theme 'apple_theme' loaded successfully"
echo • "✅ Gemini AI configured successfully!" (if API key is valid)
echo • No Python traceback errors
echo.
pause
