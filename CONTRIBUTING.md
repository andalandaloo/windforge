# 🤝 Contributing to WindForge

<div align="center">

**Thank you for your interest in contributing to WindForge!**

[![Contributors](https://img.shields.io/github/contributors/windforge/windforge?style=for-the-badge)](https://github.com/windforge/windforge/graphs/contributors)
[![Pull Requests](https://img.shields.io/github/issues-pr/windforge/windforge?style=for-the-badge)](https://github.com/windforge/windforge/pulls)
[![Issues](https://img.shields.io/github/issues/windforge/windforge?style=for-the-badge)](https://github.com/windforge/windforge/issues)

</div>

---

## 🌟 Ways to Contribute

<table>
<tr>
<td width="33%">

### 💻 **Code Contributions**
- 🐛 Fix bugs and issues
- ✨ Add new features
- 🧪 Write and improve tests
- ⚡ Optimize performance
- 🔧 Refactor code

</td>
<td width="33%">

### 🎨 **Design & UI**
- 🎭 Create new icons
- 🎨 Improve UI/UX
- 📱 Enhance responsiveness
- 🌙 Develop dark mode
- 🎯 Design improvements

</td>
<td width="33%">

### 📚 **Documentation**
- 📖 Write tutorials
- 🔧 Improve API docs
- 🌍 Translate content
- 📝 Fix typos
- 💡 Add examples

</td>
</tr>
</table>

---

## 🚀 Getting Started

### 1️⃣ **Fork the Repository**
```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/your-username/windforge.git
cd windforge
```

### 2️⃣ **Set Up Development Environment**
```bash
# Create virtual environment
python -m venv windforge-env
source windforge-env/bin/activate  # Linux/Mac
windforge-env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### 3️⃣ **Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number
```

### 4️⃣ **Make Your Changes**
- Follow our coding standards (see below)
- Add tests for new functionality
- Update documentation as needed
- Test your changes thoroughly

### 5️⃣ **Commit and Push**
```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

### 6️⃣ **Create Pull Request**
- Go to GitHub and create a pull request
- Fill out the PR template
- Wait for review and feedback

---

## 📋 Development Guidelines

### 🎯 **Code Standards**

#### Python Code Style
- ✅ Follow **PEP 8** guidelines
- ✅ Use **type hints** for all functions
- ✅ Add **docstrings** for all public methods
- ✅ Maximum line length: **88 characters** (Black formatter)
- ✅ Use **meaningful variable names**

#### Example:
```python
def generate_rule_md(
    title: str, 
    category: str, 
    activation: str, 
    description: str
) -> tuple[str, str]:
    """
    Generate Markdown content for a rule file.
    
    Args:
        title: Rule title
        category: Rule category
        activation: Activation mode
        description: Rule description
    
    Returns:
        tuple: (filename, markdown_content)
    """
    # Implementation here
    pass
```

### 🧪 **Testing Requirements**
- ✅ Write tests for all new features
- ✅ Maintain **>80% test coverage**
- ✅ Use **pytest** for testing
- ✅ Test both success and error cases

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=core tests/
```

### 📚 **Documentation Standards**
- ✅ Update README.md for new features
- ✅ Add docstrings to all functions
- ✅ Include usage examples
- ✅ Update API documentation

---

## 🎨 **UI/UX Guidelines**

### Icon Design
- 🎭 Follow **macOS design principles**
- 🌈 Use **gradient colors** for depth
- ☁️ Add **subtle shadows**
- 🔘 Use **rounded corners**
- 📏 Standard sizes: **64x64px** for UI icons

### Color Palette
```css
Primary:   #667eea → #764ba2
Secondary: #f093fb → #f5576c
Success:   #4CAF50
Warning:   #FF9800
Error:     #F44336
Text:      #2C3E50
```

---

## 🐛 **Bug Reports**

### Before Reporting
- 🔍 Search existing issues
- 🧪 Test with latest version
- 📋 Gather system information

### Bug Report Template
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Screenshots**
If applicable

**Environment**
- OS: [e.g., Windows 11]
- Python: [e.g., 3.9.0]
- WindForge: [e.g., 2.0.0]
```

---

## 💡 **Feature Requests**

### Feature Request Template
```markdown
**Feature Description**
Clear description of the feature

**Problem it Solves**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other solutions you considered

**Additional Context**
Screenshots, mockups, etc.
```

---

## 📝 **Commit Message Guidelines**

### Format
```
type(scope): description

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples
```bash
feat(ai): add Gemini Flash 2.5 integration
fix(ui): resolve icon display issue on Windows
docs(readme): update installation instructions
style(core): format code with Black
```

---

## 🏆 **Recognition**

### Contributors Hall of Fame
All contributors are recognized in:
- 📋 **README.md** contributors section
- 🎉 **Release notes** for their contributions
- 🏅 **GitHub contributors** page
- 💝 **Special thanks** in documentation

### Contribution Levels
- 🥉 **Bronze**: 1-5 contributions
- 🥈 **Silver**: 6-15 contributions  
- 🥇 **Gold**: 16+ contributions
- 💎 **Diamond**: Core maintainer

---

## 📞 **Getting Help**

### Communication Channels
- 💬 **GitHub Discussions**: General questions
- 🐛 **GitHub Issues**: Bug reports and features
- 📧 **Email**: windforge.team@example.com
- 💬 **Discord**: [Join our server](https://discord.gg/windforge)

### Response Times
- 🐛 **Critical bugs**: 24 hours
- ✨ **Feature requests**: 1 week
- 💬 **General questions**: 2-3 days
- 🔍 **PR reviews**: 3-5 days

---

## 📄 **Code of Conduct**

### Our Pledge
We pledge to make participation in WindForge a harassment-free experience for everyone, regardless of:
- Age, body size, disability
- Ethnicity, gender identity
- Experience level, nationality
- Personal appearance, race
- Religion, sexual orientation

### Our Standards
**Positive behavior includes:**
- ✅ Using welcoming language
- ✅ Being respectful of differing viewpoints
- ✅ Gracefully accepting constructive criticism
- ✅ Focusing on what's best for the community

**Unacceptable behavior includes:**
- ❌ Trolling, insulting, or derogatory comments
- ❌ Public or private harassment
- ❌ Publishing others' private information
- ❌ Other conduct inappropriate in a professional setting

---

<div align="center">

## 🙏 **Thank You!**

**Your contributions make WindForge better for everyone.**

[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)](https://github.com/windforge/windforge)

</div>
