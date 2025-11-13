@echo off
echo 🔑 Testing API Key Settings Integration
echo.
echo 🎯 New Features:
echo • API Key configuration moved to Settings dialog
echo • Automatic saving and loading of API keys
echo • Persistent API key storage across app restarts
echo • Clean UI with settings link in AI tab
echo.

echo ✅ Changes Made:
echo • Added AI Settings tab to Settings dialog
echo • API key input with show/hide toggle
echo • Test API key functionality
echo • AI model configuration options
echo • Temperature and token limit settings
echo • AI feature toggles
echo • Automatic loading of saved API key on startup
echo • Settings synchronization with AI tab
echo.

echo 🚀 Starting WindForge to test API key settings...
echo.

echo 📋 Test Steps:
echo 1. Open application (should load any saved API key)
echo 2. Go to AI Generator tab
echo 3. Click "Open Settings" button
echo 4. Navigate to "AI Settings" tab
echo 5. Enter your Google API key
echo 6. Click "Test" to verify the key
echo 7. Click "OK" to save settings
echo 8. Close and restart the application
echo 9. Verify API key is still configured
echo.

python main.py

echo.
echo 🔍 What to check:
echo • ✅ API key persists after app restart
echo • ✅ Settings dialog opens from AI tab
echo • ✅ API key test function works
echo • ✅ AI status updates correctly
echo • ✅ No more API key input in AI tab
echo • ✅ Clean UI with settings link
echo.

echo 📊 Expected Console Messages:
echo • "✅ Theme 'apple_theme' loaded successfully"
echo • "✅ Loaded saved API key successfully" (if key exists)
echo • "✅ Updated API key from settings" (when changed)
echo.

echo 💾 Configuration File:
echo • API key saved in: config.json
echo • Section: ai_settings.api_key
echo • Encrypted storage: No (consider for future)
echo.
pause
