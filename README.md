# Radian Watchface Generator

Tool for easily creating radial elements for watchfaces.

## Overview
Radian is a tool that enables design, preview and export high quality radial elements for watchfaces with vector graphics rendering.

## Project Structure
```
Radian/
├── project/
│   ├── main.py              # Application entry point
│   ├── requirements.txt     # Python dependencies
│   ├── core/                # Core engine and rendering logic
│   ├── elements/            # Watchface visual components (Radial elements)
│   ├── export/              # Export functionality
│   ├── fonts/               # Font manager
│   ├── output/              # Exported images directory
│   └── ui/                  # Graphical user interface
├── .gitignore
└── README.md
```

## Features
**1. Rendering modes**
- Marks (ticks) – Marks around a circle with two styles: Line (radial segments) and Circle (dots).
- Rings – Filled concentric rings with configurable outer radius and ring thickness.
- Typography – Text laid out along a circle with adjustable font, size, rotation, and letter spacing.
- Multi-element composition
- Layered elements – Add several elements (Marks, Rings, Typography) that stack in order.
- Element list – View and manage all elements; select one to edit its parameters.
- Delete selected – Remove the currently selected element from the composition.

**2. Per-element controls**
- Marks: number of marks, length, width, size (radius), mark type (Line / Circle), color.
- Rings: size (radius), ring thickness (length), color.
- Typography: text, font family, font variant, font size, letter spacing, rotation, flip 180°, color.
- Per-element masking
- Enable masking – Toggle masking per element.
- Angle – Opening angle of the masked sector (0–360°).
- Rotation – Orientation of the sector (0–360°).
- Mask is a sector from the center; masked area is transparent (or white when background is not transparent).
- Each element has its own mask; masks do not affect other elements.
Export
- Transparent background – Option to export with or without transparency.
- Outputs folder – Files saved under an outputs/ directory with descriptive filenames based on date.

**3. UI & Preview**
- Simple interface – Real-time preview and controls (sliders, inputs, color picker).
- Live preview – Updates as parameters or selections change.
- Font selection – Choose from system fonts and project fonts (e.g., Roboto); ¿
- High-quality vector rendering engine.
- Layered compositing – Each element (including masked ones) is rendered to a transparent - layer and composited, so stacking and transparency behave correctly.

## Requirements
- Python 3.10+
- Dependencies listed in `requirements.txt`

## Installation
1. Clone this repository
2. Create virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate virtual environment:
   ```bash
   # Windows
   .venv\Scripts\activate.bat
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
```bash
python main.py
```

## Output
Generated watchfaces will be exported to `/output/` directory.

## Tech Stack
- **UI Framework**: PySide6 (Qt 6)
- **Graphics Engine**: Skia-python
- **Math/Calculations**: Numpy

## How to Cite
If you use Radian for your commercial projects or derivative works, please provide attribution by linking back to this repository or citing it as:

“Designed with Radian - [Koi]”.
