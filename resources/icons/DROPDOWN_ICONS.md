# 🔽 Dropdown Icons for WindForge

## 📋 Available Icons

### 🎯 **Standard Size (24x24)**

#### 🔽 **Dropdown Down**
- **File**: `dropdown-down.svg`
- **Size**: 24x24px
- **Style**: Outlined with gradient
- **Color**: Gray (#86868b)
- **Usage**: Standard dropdown menus

#### 🔼 **Dropdown Up**
- **File**: `dropdown-up.svg`
- **Size**: 24x24px
- **Style**: Outlined with gradient
- **Color**: Gray (#86868b)
- **Usage**: Collapse menus, accordions

---

### 🍎 **Apple Blue Variants**

#### 🔽 **Blue Dropdown Down**
- **File**: `dropdown-down-blue.svg`
- **Size**: 24x24px
- **Style**: Outlined with blue gradient
- **Color**: Apple Blue (#007aff)
- **Usage**: Active/selected states

#### 🔼 **Blue Dropdown Up**
- **File**: `dropdown-up-blue.svg`
- **Size**: 24x24px
- **Style**: Outlined with blue gradient
- **Color**: Apple Blue (#007aff)
- **Usage**: Active/selected collapse states

---

### 📏 **Small Size (16x16)**

#### 🔽 **Small Dropdown Down**
- **File**: `dropdown-down-small.svg`
- **Size**: 16x16px
- **Style**: Compact outlined
- **Color**: Gray (#86868b)
- **Usage**: ComboBox, SpinBox, compact UI

#### 🔼 **Small Dropdown Up**
- **File**: `dropdown-up-small.svg`
- **Size**: 16x16px
- **Style**: Compact outlined
- **Color**: Gray (#86868b)
- **Usage**: SpinBox up button, compact collapse

---

### 🔶 **Filled Variants**

#### 🔽 **Filled Dropdown Down**
- **File**: `dropdown-down-filled.svg`
- **Size**: 24x24px
- **Style**: Solid filled triangle
- **Color**: Gray gradient
- **Usage**: Strong visual emphasis

#### 🔼 **Filled Dropdown Up**
- **File**: `dropdown-up-filled.svg`
- **Size**: 24x24px
- **Style**: Solid filled triangle
- **Color**: Gray gradient
- **Usage**: Strong collapse indication

---

## 🎨 Design Specifications

### 📐 **Dimensions**
```
Standard: 24x24px
Small:    16x16px
Stroke:   2px (standard), 1.5px (small)
```

### 🎨 **Colors**
```css
/* Gray Gradient */
Primary:   #86868b
Secondary: #6d6d70

/* Apple Blue Gradient */
Primary:   #007aff
Secondary: #0056b3
```

### 🔧 **Technical Details**
- **Format**: SVG (Scalable Vector Graphics)
- **Encoding**: UTF-8
- **Optimization**: Clean paths, minimal nodes
- **Compatibility**: All modern browsers and Qt

---

## 🔧 Usage in Qt StyleSheets

### 📦 **ComboBox Integration**
```qss
QComboBox::down-arrow {
    image: url(resources/icons/dropdown-down-small.svg);
    width: 12px;
    height: 12px;
    margin-right: 5px;
}
```

### 🔢 **SpinBox Integration**
```qss
QSpinBox::up-arrow {
    image: url(resources/icons/dropdown-up-small.svg);
    width: 10px;
    height: 10px;
}

QSpinBox::down-arrow {
    image: url(resources/icons/dropdown-down-small.svg);
    width: 10px;
    height: 10px;
}
```

### 🎛️ **Custom Widgets**
```python
# Python usage
icon_down = QIcon("resources/icons/dropdown-down.svg")
icon_up = QIcon("resources/icons/dropdown-up.svg")

button.setIcon(icon_down)
```

---

## 🎯 Use Cases

### 📋 **Dropdown Menus**
- ComboBox selection indicators
- Context menu arrows
- Navigation dropdowns
- Filter selectors

### 🔢 **Numeric Controls**
- SpinBox increment/decrement
- Slider controls
- Value adjusters
- Range selectors

### 📁 **Collapsible Content**
- Accordion panels
- Tree view expanders
- Section toggles
- Detail disclosure

### 🎨 **Visual States**
- **Default**: Gray outline icons
- **Hover**: Blue outline icons
- **Active**: Filled icons
- **Disabled**: Light gray icons

---

## 🎨 Apple Design Compliance

### ✅ **Design Principles**
- **Clarity**: Clean, recognizable shapes
- **Deference**: Subtle, non-intrusive
- **Depth**: Gradient effects for dimension
- **Consistency**: Uniform stroke width and style

### 🍎 **Apple Guidelines**
- Rounded line caps and joins
- Consistent visual weight
- Appropriate sizing for context
- Accessible color contrast

### 🎯 **Visual Hierarchy**
- Primary actions: Blue variants
- Secondary actions: Gray variants
- Emphasis: Filled variants
- Compact spaces: Small variants

---

## 📊 Icon Matrix

| Icon | Size | Style | Color | Usage |
|------|------|-------|-------|-------|
| `dropdown-down.svg` | 24x24 | Outline | Gray | Standard dropdown |
| `dropdown-up.svg` | 24x24 | Outline | Gray | Standard collapse |
| `dropdown-down-blue.svg` | 24x24 | Outline | Blue | Active dropdown |
| `dropdown-up-blue.svg` | 24x24 | Outline | Blue | Active collapse |
| `dropdown-down-small.svg` | 16x16 | Outline | Gray | Compact dropdown |
| `dropdown-up-small.svg` | 16x16 | Outline | Gray | Compact collapse |
| `dropdown-down-filled.svg` | 24x24 | Filled | Gray | Emphasis dropdown |
| `dropdown-up-filled.svg` | 24x24 | Filled | Gray | Emphasis collapse |

---

## 🚀 Integration Status

### ✅ **Implemented**
- [x] Created all 8 dropdown icon variants
- [x] Integrated into QSS theme file
- [x] Applied to ComboBox controls
- [x] Applied to SpinBox controls
- [x] Documented usage patterns

### 🔄 **In Progress**
- [ ] Testing across different screen densities
- [ ] Performance optimization
- [ ] Additional color variants

### 📋 **Planned**
- [ ] Dark mode variants
- [ ] Animation support
- [ ] Custom hover states
- [ ] Accessibility enhancements

---

<div align="center">

## 🎨 **Professional Dropdown Icons**

**Clean • Consistent • Apple-Inspired**

[![SVG](https://img.shields.io/badge/Format-SVG-green?style=for-the-badge)](.)
[![Apple Design](https://img.shields.io/badge/Design-Apple%20Style-blue?style=for-the-badge)](.)
[![Qt Compatible](https://img.shields.io/badge/Qt-Compatible-orange?style=for-the-badge)](.)

</div>
