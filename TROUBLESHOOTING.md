# 🔧 WindForge Troubleshooting Guide

## 🚨 Common Installation Issues

### ❌ **Error: "Metaclasses with custom tp_new are not supported"**

This error typically occurs with Python 3.14+ and Google AI libraries. Here are the solutions:

#### 🔧 **Solution 1: Use Fix Installation Script**
```bash
# Run the automated fix
fix_installation.bat
```

#### 🔧 **Solution 2: Manual Fix**
```bash
# Step 1: Clean installation
pip uninstall -y google-generativeai google-api-core protobuf grpcio

# Step 2: Install minimal requirements first
pip install -r requirements-minimal.txt

# Step 3: Install compatible versions
pip install protobuf==4.25.1
pip install google-generativeai==0.3.2
```

#### 🔧 **Solution 3: Use Python 3.11 or 3.12**
```bash
# Install Python 3.12 (recommended)
# Then create virtual environment
python -m venv windforge-env
windforge-env\Scripts\activate
pip install -r requirements.txt
```

---

### ❌ **Error: "Could not find platform independent libraries"**

#### 🔧 **Solution: Virtual Environment**
```bash
# Create clean virtual environment
python -m venv windforge-env
windforge-env\Scripts\activate

# Install requirements
pip install --upgrade pip
pip install -r requirements-minimal.txt

# Test basic functionality
python main.py
```

---

### ❌ **Error: "ImportError: No module named 'google.generativeai'"**

#### 🔧 **Solution: Optional AI Features**
WindForge now works without AI features! The application will automatically detect if AI libraries are available.

```bash
# Option 1: Run without AI (basic functionality)
python main.py

# Option 2: Install AI features
setup_ai.bat
```

---

## 🐛 Runtime Issues

### ❌ **AI Tab Not Showing**

This is normal if AI libraries aren't installed.

#### 🔧 **Solutions:**
1. **Install AI features**: Run `setup_ai.bat`
2. **Check installation**: 
   ```bash
   python -c "import google.generativeai; print('AI available')"
   ```
3. **Use basic features**: Rules and Workflows generators work without AI

---

### ❌ **Icons Not Displaying**

#### 🔧 **Solutions:**
1. **Check icon files**:
   ```bash
   # Verify icons exist
   dir resources\icons\*.svg
   ```

2. **Run icon showcase**:
   ```bash
   python icon_showcase.py
   ```

3. **Reinstall if needed**:
   - Download fresh copy of the project
   - Ensure `resources/icons/` folder is complete

---

### ❌ **Settings Not Saving**

#### 🔧 **Solutions:**
1. **Check permissions**:
   - Ensure write access to `config/` folder
   - Run as administrator if needed

2. **Reset settings**:
   ```bash
   # Delete settings file to reset
   del config\settings.json
   ```

---

## 🖥️ Platform-Specific Issues

### 🪟 **Windows Issues**

#### **Python Path Issues**
```bash
# Add Python to PATH
# Or use full path
C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe main.py
```

#### **Permission Denied**
```bash
# Run as administrator
# Or change folder permissions
```

### 🐧 **Linux Issues**

#### **Missing Dependencies**
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt6 python3-pip

# Install requirements
pip3 install -r requirements.txt
```

### 🍎 **macOS Issues**

#### **PyQt6 Installation**
```bash
# Use Homebrew
brew install python-tk
pip3 install -r requirements.txt
```

---

## 🧪 Testing Your Installation

### ✅ **Basic Test**
```bash
# Test PyQt6
python -c "import PyQt6; print('✅ PyQt6 working')"

# Test core functionality
python -c "from core.generators import generate_rule_md; print('✅ Core working')"

# Test AI (optional)
python -c "try: import google.generativeai; print('✅ AI available'); except: print('ℹ️ AI not available')"
```

### ✅ **Full Application Test**
```bash
# Launch application
python main.py

# Should show:
# - Rules Generator tab ✅
# - Workflow Generator tab ✅  
# - AI Generator tab (if AI installed) ✅
```

---

## 📞 **Getting Help**

### 🔍 **Before Asking for Help**
1. ✅ Try the automated fix: `fix_installation.bat`
2. ✅ Check this troubleshooting guide
3. ✅ Test with minimal installation: `requirements-minimal.txt`
4. ✅ Gather system information:
   ```bash
   python --version
   pip list | findstr -i "pyqt6 google protobuf"
   ```

### 💬 **Support Channels**
- 🐛 **GitHub Issues**: [Report bugs](https://github.com/windforge/windforge/issues)
- 💡 **Discussions**: [Ask questions](https://github.com/windforge/windforge/discussions)
- 📧 **Email**: windforge.support@example.com

### 📋 **Issue Template**
When reporting issues, please include:

```
**Environment:**
- OS: Windows 11 / Ubuntu 22.04 / macOS 13
- Python: 3.12.0
- WindForge: 2.0.0

**Error Message:**
[Paste full error message here]

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Error occurs

**Expected Behavior:**
What should happen

**Additional Info:**
Any other relevant information
```

---

## 🎯 **Quick Fixes Summary**

| Problem | Quick Fix |
|---------|-----------|
| 🚨 Metaclass error | Run `fix_installation.bat` |
| 🤖 No AI tab | Install with `setup_ai.bat` or ignore |
| 🎨 No icons | Check `resources/icons/` folder |
| ⚙️ Settings not saving | Check folder permissions |
| 🐍 Import errors | Use virtual environment |
| 📦 Missing modules | Run `pip install -r requirements.txt` |

---

<div align="center">

**Still having issues? We're here to help!**

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-red?style=for-the-badge&logo=github)](https://github.com/windforge/windforge/issues)
[![Discord](https://img.shields.io/badge/Discord-Support-blue?style=for-the-badge&logo=discord)](https://discord.gg/windforge)

</div>
