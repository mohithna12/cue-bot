# Eye Tracking Camera Switcher
//testcomment
A Python application that tracks your eyes in real-time using MediaPipe and automatically switches between cameras based on your gaze direction.

## Features

- **Real-time eye tracking** using MediaPipe face mesh
- **Automatic camera switching** based on gaze direction
- **Stable switching** with debouncing to prevent flickering
- **Debug display** showing gaze direction and camera status
- **Simple setup** - no OBS or complex configuration needed

## How It Works

- **Eye Tracking**: Uses front camera (Camera 0) to detect your gaze direction
- **Left Gaze**: Switches to webcam (Camera 1) when you look left
- **Center/Right Gaze**: Switches to front camera (Camera 0) when you look center or right
- **Stable Switching**: Waits for stable gaze direction before switching to prevent rapid changes

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Make sure you have at least 2 cameras:**
   - Camera 0: Front camera (for eye tracking)
   - Camera 1: Webcam (for display when looking left)

## Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Position yourself** in front of the front camera

3. **Look in different directions:**
   - Look **left** → switches to webcam view
   - Look **center/right** → switches to front camera view

4. **Press 'q'** to quit

## Controls

- `q` - Quit application

## Debug Information

The application displays:
- **Gaze Direction**: LEFT or CENTER/RIGHT
- **Current Camera**: Which camera is currently showing
- **Target Camera**: Which camera it wants to switch to
- **Ratio**: Gaze detection ratio (lower = more left)
- **Active Camera**: Which camera is currently active

## Requirements

- **2 Cameras**: Front camera and webcam
- **Good Lighting**: Ensure your face is well-lit
- **Python 3.7+**
- **MediaPipe** and **OpenCV**

## Troubleshooting

### "Need at least 2 cameras"
- Make sure both cameras are connected and working
- Check camera permissions in Windows settings

### "NO FACE DETECTED"
- Ensure good lighting on your face
- Position yourself directly in front of the front camera
- Make sure the front camera is not blocked

### Rapid switching between cameras
- The app has built-in debouncing (2-second delay + 10-frame stability)
- This prevents rapid switching and ensures stable operation

## File Structure

```
├── main.py              # Main application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Dependencies

- `mediapipe==0.10.7` - Face mesh and landmark detection
- `opencv-python==4.8.1.78` - Video capture and display

## License

This project is open source. Feel free to modify and distribute as needed.
