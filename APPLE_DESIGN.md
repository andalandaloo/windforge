# 🍎 WindForge Apple-Style Design Guide

## 🎨 Design Philosophy

WindForge has been redesigned to follow **Apple's Human Interface Guidelines**, bringing a clean, modern, and intuitive user experience that feels familiar to Apple users while maintaining cross-platform compatibility.

---

## 🎯 Key Design Elements

### 🎨 **Color Palette**
- **Primary Blue**: `#007aff` - Apple's signature system blue
- **Background**: `#f8f9fa` - Clean, light background similar to macOS
- **Text**: `#1d1d1f` - High contrast dark text
- **Secondary Text**: `#86868b` - Subtle gray for secondary information
- **Success**: `#30d158` - Apple's system green
- **Warning**: `#ff9500` - Apple's system orange
- **Error**: `#ff3b30` - Apple's system red

### 📝 **Typography**
- **Font Stack**: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Weights**: 
  - Regular (400) for body text
  - Medium (500) for tabs and labels
  - Semibold (600) for headings and buttons
  - Bold (700) for titles

### 🔘 **Border Radius**
- **Small elements**: `8px` (buttons, inputs)
- **Cards**: `12px` (group boxes, panels)
- **Large containers**: `16px` (main content areas)

### 📏 **Spacing System**
- **Micro**: `4px` - Internal padding for small elements
- **Small**: `8px` - Standard padding
- **Medium**: `12px` - Section spacing
- **Large**: `16px` - Card padding
- **XL**: `20px` - Major section spacing
- **XXL**: `24px` - Page margins

---

## 🧩 Component Design

### 📑 **Tabs**
```
┌─────────────┬─────────────┬─────────────┐
│ Rules Gen   │ Workflows   │ AI Gen      │ ← Selected: Blue background
├─────────────┴─────────────┴─────────────┤
│                                         │
│           Tab Content Area              │
│                                         │
└─────────────────────────────────────────┘
```

**Features:**
- Clean, pill-shaped tabs
- Blue accent for active tab
- Subtle hover effects
- Proper spacing and typography

### 🔘 **Buttons**
```
┌─────────────────┐  ┌─────────────────┐
│   Primary       │  │   Secondary     │
│   #007aff       │  │   #f2f2f7       │
└─────────────────┘  └─────────────────┘
```

**States:**
- **Normal**: Blue background, white text
- **Hover**: Darker blue (`#0056b3`)
- **Pressed**: Even darker (`#004494`)
- **Disabled**: Gray background (`#f2f2f7`)

### 📝 **Input Fields**
```
┌─────────────────────────────────────┐
│ Placeholder text...                 │ ← Normal state
└─────────────────────────────────────┘

┌═════════════════════════════════════┐
│ Focused input with blue border      │ ← Focus state
└═════════════════════════════════════┘
```

**Features:**
- Rounded corners (8px)
- Blue focus border
- Subtle hover effects
- Proper padding and typography

### 📦 **Cards (Group Boxes)**
```
┌─ Card Title ─────────────────────────┐
│                                     │
│  Card content with proper spacing   │
│  and clean typography               │
│                                     │
└─────────────────────────────────────┘
```

**Features:**
- White background
- Subtle border (`#e5e5e7`)
- 12px border radius
- Proper title positioning
- Consistent internal spacing

---

## 🎭 Status Indicators

### ✅ **Success State**
```
┌─────────────────────────────────────┐
│ ✅ Operation completed successfully │ ← Green background
└─────────────────────────────────────┘
```

### ⚠️ **Warning State**
```
┌─────────────────────────────────────┐
│ ⚠️ Please check configuration      │ ← Orange background
└─────────────────────────────────────┘
```

### ❌ **Error State**
```
┌─────────────────────────────────────┐
│ ❌ Connection failed, retry needed  │ ← Red background
└─────────────────────────────────────┘
```

### ℹ️ **Info State**
```
┌─────────────────────────────────────┐
│ ℹ️ Additional information available │ ← Gray background
└─────────────────────────────────────┘
```

---

## 🖥️ Window Layout

```
┌─ WindForge ─────────────────────────────────────────┐
│ File  Help                                          │ ← Menu bar
├─────────────────────────────────────────────────────┤
│ ┌─────────┬─────────┬─────────┐                     │
│ │ Rules   │Workflow │ AI Gen  │                     │ ← Tabs
│ └─────────┴─────────┴─────────┘                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │                                                 │ │
│ │              Tab Content                        │ │ ← Content area
│ │                                                 │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 🎨 Visual Hierarchy

### 1️⃣ **Primary Level**
- App title and main navigation
- Primary action buttons
- Key status indicators

### 2️⃣ **Secondary Level**
- Section headings
- Secondary buttons
- Form labels

### 3️⃣ **Tertiary Level**
- Helper text
- File names
- Timestamps

---

## 🔧 Implementation Details

### CSS Classes Used
```css
/* Main application styling */
QMainWindow { background-color: #f8f9fa; }

/* Apple-style tabs */
QTabBar::tab:selected { 
    background-color: #007aff; 
    color: #ffffff; 
}

/* Input focus states */
QLineEdit:focus { 
    border: 2px solid #007aff; 
}

/* Status indicators */
.status-success { 
    background-color: #f0fff4; 
    color: #30d158; 
}
```

### Font Loading
The application automatically loads Apple's system font stack:
1. **macOS**: `-apple-system` (San Francisco)
2. **Windows**: `Segoe UI`
3. **Linux**: `Roboto`
4. **Fallback**: `sans-serif`

---

## 🎯 User Experience Improvements

### ✨ **Micro-interactions**
- Smooth hover transitions
- Focus state feedback
- Button press animations
- Tab switching effects

### 🎨 **Visual Feedback**
- Color-coded status messages
- Clear visual hierarchy
- Consistent spacing
- Proper contrast ratios

### 🧭 **Navigation**
- Intuitive tab structure
- Clear button labeling
- Logical information flow
- Accessible design patterns

---

## 🚀 Testing the Design

Run the application and test these elements:

### 🔍 **Visual Elements**
- [ ] Clean, modern appearance
- [ ] Consistent color usage
- [ ] Proper typography rendering
- [ ] Rounded corners on all elements

### 🖱️ **Interactions**
- [ ] Tab switching smoothness
- [ ] Button hover effects
- [ ] Input field focus states
- [ ] Status indicator colors

### 📱 **Responsiveness**
- [ ] Proper spacing on different screen sizes
- [ ] Text readability
- [ ] Button accessibility
- [ ] Icon clarity

---

## 🎨 Customization

The design can be customized by modifying the CSS variables in `main.py`:

```python
# Primary colors
APPLE_BLUE = "#007aff"
BACKGROUND = "#f8f9fa"
TEXT_PRIMARY = "#1d1d1f"
TEXT_SECONDARY = "#86868b"

# Border radius
RADIUS_SMALL = "8px"
RADIUS_MEDIUM = "12px"
RADIUS_LARGE = "16px"
```

---

<div align="center">

## 🍎 **Apple-Inspired. Cross-Platform Compatible.**

*WindForge brings the best of Apple's design language to your development workflow*

</div>
