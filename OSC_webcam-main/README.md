# Webcam OSC Grid Analyzer

A Python application that captures webcam video, divides it into a grid, analyzes each cell's visual properties, and sends the data via OSC (Open Sound Control) protocol for real-time creative applications.

## Purpose

This project enables real-time video analysis and OSC communication for creative coding, interactive installations, audiovisual performances, and multimedia projects. It analyzes each grid cell for:

- Average RGB color values
- Brightness levels
- Contrast measurements
- Dominant colors

The analyzed data is transmitted via OSC protocol, making it compatible with software like Max/MSP, TouchDesigner, Processing, Pure Data, and other creative coding environments.

## How It Works

1. **Video Capture**: Captures frames from your webcam at a configurable frame rate
2. **Grid Division**: Divides each frame into a configurable grid (default: 4x4)
3. **Cell Analysis**: Analyzes each grid cell for color, brightness, contrast, and dominant color
4. **OSC Transmission**: Sends analyzed data to a specified host and port via OSC protocol
5. **Visual Feedback**: Displays the live webcam feed with grid overlay

## Project Structure

```
webcam_osc/
├── main.py         # Main application entry point
├── capture.py      # Webcam capture handling
├── analyzer.py     # Grid and cell analysis logic
├── osc_sender.py   # OSC protocol communication
├── config.py       # Configuration dataclasses
└── __init__.py     # Package initialization
```

## Setup

### Prerequisites

- Python 3.8 or higher
- A working webcam
- OSC-compatible receiving application (optional, for testing)

### Installation

1. **Clone or download this repository**

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   On Linux/macOS:
   ```bash
   source venv/bin/activate
   ```

   On Windows:
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Ensure your virtual environment is activated**

2. **Run the application**:
   ```bash
   python -m webcam_osc.main
   ```

3. **Configuration**: Edit `webcam_osc/main.py` to customize:
   - Grid size (rows and columns)
   - OSC host and port
   - Camera index (if you have multiple cameras)
   - Target FPS

4. **Exit**: Press `q` while the webcam window is focused to quit

## Configuration Options

In `webcam_osc/main.py`, modify the `AppConfig` initialization:

```python
config = AppConfig(
    grid=GridConfig(rows=4, cols=4),           # Grid dimensions
    osc=OSCConfig(host="127.0.0.1", port=5005), # OSC destination
    camera_index=0,                              # Camera to use
    target_fps=30                                # Frame rate
)
```

## OSC Message Format

### Overview

All data is sent as an OSC bundle per frame. Each grid cell generates 4 OSC messages with the following address pattern:

```
/cell/{row}/{col}/{metric}
```

Where:
- `{row}`: Grid row index (0-based)
- `{col}`: Grid column index (0-based)
- `{metric}`: The type of data being sent

### Message Structure

**Important**: All values are normalized to the range **0.0 - 1.0** for easy use in PureData.

| Address Pattern | Arguments | Data Type | Range | Description |
|----------------|-----------|-----------|-------|-------------|
| `/cell/{row}/{col}/rgb` | 3 floats | float, float, float | 0.0-1.0 each | Average red, green, blue values |
| `/cell/{row}/{col}/brightness` | 1 float | float | 0.0-1.0 | Cell brightness (grayscale average) |
| `/cell/{row}/{col}/contrast` | 1 float | float | 0.0-1.0 | Cell contrast (standard deviation) |
| `/cell/{row}/{col}/dominant` | 3 floats | float, float, float | 0.0-1.0 each | Dominant red, green, blue values |

### Example Messages (4x4 Grid)

For a 4x4 grid, each frame sends 64 messages (16 cells × 4 metrics). Here's what cell [0,0] sends:

```
/cell/0/0/rgb 0.234 0.567 0.891
/cell/0/0/brightness 0.564
/cell/0/0/contrast 0.123
/cell/0/0/dominant 0.200 0.600 0.900
```

### PureData Integration

To receive these messages in PureData, use the following pattern:

```
[udpreceive 5005]
|
[oscparse]
|
[route /cell]
|
[route 0 1 2 3]  <- routes by row
|
[route 0 1 2 3]  <- routes by column
|
[route rgb brightness contrast dominant]
|
[unpack f f f]   <- for rgb/dominant (3 floats)
[f]              <- for brightness/contrast (1 float)
```

**Example for specific cell (row 0, col 0)**:
```
[udpreceive 5005]
|
[oscparse]
|
[list trim]
|
[route /cell/0/0/rgb /cell/0/0/brightness /cell/0/0/contrast /cell/0/0/dominant]
|        |              |            |
[unpack f f f]  [f]     [f]    [unpack f f f]
   R  G  B    brightness contrast  R  G  B
```

### Complete Message List

For a 2×2 grid (simplified example), you'll receive these 16 messages per frame:

```
/cell/0/0/rgb {r} {g} {b}
/cell/0/0/brightness {value}
/cell/0/0/contrast {value}
/cell/0/0/dominant {r} {g} {b}

/cell/0/1/rgb {r} {g} {b}
/cell/0/1/brightness {value}
/cell/0/1/contrast {value}
/cell/0/1/dominant {r} {g} {b}

/cell/1/0/rgb {r} {g} {b}
/cell/1/0/brightness {value}
/cell/1/0/contrast {value}
/cell/1/0/dominant {r} {g} {b}

/cell/1/1/rgb {r} {g} {b}
/cell/1/1/brightness {value}
/cell/1/1/contrast {value}
/cell/1/1/dominant {r} {g} {b}
```

## Dependencies

- `opencv-python` (4.10.0.84): Video capture and image processing
- `python-osc` (1.9.0): OSC protocol communication
- `numpy` (1.26.4): Numerical computations

## Troubleshooting

- **Camera not found**: Try changing `camera_index` to 1, 2, etc.
- **Permission errors**: Ensure your system allows camera access
- **OSC not receiving**: Verify the host and port match your receiving application

## Use Cases

- Live video analysis for generative art
- Interactive installations responding to movement/color
- Audiovisual performances with video-to-sound mapping
- Educational demonstrations of computer vision
- Real-time data visualization projects
