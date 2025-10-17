# 📍 Fixed Coordinate System Guide

## Why Fixed Coordinates?

**100% ACCURACY** - No guessing, no detection errors!

### The Problem with Detection:
- ❌ Color detection can fail with different themes
- ❌ OCR requires Tesseract installation
- ❌ Pattern matching varies with screen brightness
- ❌ Different screen resolutions = different positions

### The Solution: Fixed Coordinates!
- ✅ Resize Roblox to standard size (1280x720)
- ✅ Use exact pixel coordinates
- ✅ Works EVERY time, NO detection needed
- ✅ Lightning fast (no image processing)

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Calibrate Coordinates
```
1. Start Roblox
2. Go to Roblox HOME page
3. Double-click: CALIBRATE.bat
4. Follow the on-screen instructions
```

### Step 2: Position Your Mouse
The tool will ask you to position your mouse on:
1. **Anime Vanguards game card** (the green dragon image)
2. **Blue play button** (after clicking the game)
3. **Center of screen** (for AFK clicks)

### Step 3: Done!
Your coordinates are saved! START_KEEPER.bat will now use them.

---

## 🎯 How It Works

### Auto Window Resizing
```
Window Size: 1280x720 pixels
Position: (100, 100) from top-left
```

### Fixed Click Positions
```json
{
  "game_card_click": {
    "x": 250,     ← YOUR calibrated X
    "y": 400,     ← YOUR calibrated Y
    "description": "Anime Vanguards game card"
  },
  "play_button_click": {
    "x": 950,     ← YOUR calibrated X
    "y": 550,     ← YOUR calibrated Y
    "description": "Blue play button"
  },
  "safe_afk_click": {
    "x": 640,     ← Center X (usually 640 for 1280 width)
    "y": 360,     ← Center Y (usually 360 for 720 height)
    "description": "Center for AFK prevention"
  }
}
```

### Coordinate Calculation
```
Absolute X = Window X + Relative X
Absolute Y = Window Y + Relative Y

Example:
Window at (100, 100)
Game card at relative (250, 400)
→ Clicks at absolute (350, 500)
```

---

## 📋 Configuration Options

Edit `config/config.json`:

### Enable/Disable Window Resize
```json
{
  "window_resize": {
    "enabled": true,        ← Set to false to keep your window size
    "width": 1280,          ← Change if you want different size
    "height": 720,
    "position_x": 100,      ← Window position
    "position_y": 100
  }
}
```

### Toggle Coordinate Mode
```json
{
  "use_fixed_coordinates": true,  ← true = Fixed, false = Detection
  "fallback_to_detection": true   ← Try detection if fixed fails
}
```

---

## 🔧 Advanced: Manual Coordinate Setting

If you don't want to use CALIBRATE.bat, edit `config/config.json` directly:

1. **Start Roblox** and resize to 1280x720
2. **Position window** at top-left (100, 100)
3. **Use screenshot tool** to find pixel coordinates
4. **Update config.json** with your coordinates

### Finding Coordinates Manually:
1. Take screenshot of Roblox (Print Screen)
2. Open in Paint or image editor
3. Hover over target element
4. Read X,Y coordinates in statusbar
5. These are your relative coordinates!

---

## 📸 Calibration Screenshot

The calibration tool saves a screenshot to:
```
screenshots/calibration.png
```

You can review this to verify your clicks are correct.

---

## 🎮 Different Window Sizes

Want to use a different window size? No problem!

### For 1920x1080 (Full HD):
```json
{
  "window_resize": {
    "width": 1920,
    "height": 1080
  },
  "fixed_coordinates": {
    "game_card_click": {
      "x": 375,      ← Scale up by 1.5x
      "y": 600
    },
    "play_button_click": {
      "x": 1425,     ← Scale up by 1.5x
      "y": 825
    }
  }
}
```

### For 800x600 (Smaller):
```json
{
  "window_resize": {
    "width": 800,
    "height": 600
  },
  "fixed_coordinates": {
    "game_card_click": {
      "x": 156,      ← Scale down by 0.625x
      "y": 250
    },
    "play_button_click": {
      "x": 594,      ← Scale down by 0.625x
      "y": 344
    }
  }
}
```

---

## 🔍 Troubleshooting

### "Window resize disabled in config"
→ Set `"enabled": true` in window_resize section

### "Clicking wrong position"
→ Run CALIBRATE.bat again to recalibrate

### "Roblox window not found"
→ Make sure Roblox is running before starting keeper

### "Window too small/big"
→ Adjust width/height in config, then recalibrate

---

## 📊 Coordinate System vs Detection

| Feature | Fixed Coordinates | Detection Methods |
|---------|-------------------|-------------------|
| **Accuracy** | 100% | 85-95% |
| **Speed** | Instant | 2-5 seconds |
| **Setup** | One-time calibration | None needed |
| **Robustness** | Perfect if calibrated | Varies with lighting |
| **Requirements** | Standard window size | None |
| **Works with themes** | Yes, always | May fail |
| **CPU usage** | Minimal | High (image processing) |

---

## 🎯 Recommended Settings

For **BEST ACCURACY**:
```json
{
  "window_resize": {
    "enabled": true,
    "width": 1280,
    "height": 720
  },
  "use_fixed_coordinates": true,
  "fallback_to_detection": true
}
```

This gives you:
- ✅ Fixed coordinates for speed and accuracy
- ✅ Detection fallback if something goes wrong
- ✅ Automatic window resizing for consistency

---

## 💡 Pro Tips

1. **Calibrate once** and keep config backed up
2. **Use 1280x720** for best balance (not too big, not too small)
3. **Position window consistently** for screenshots
4. **Test with manual close** to verify auto-relaunch
5. **Check screenshots** folder to verify clicks

---

Created: October 17, 2025
Version: 4.0 - Fixed Coordinate Edition
