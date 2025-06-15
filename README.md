# 🎯 Real-Time Object Detection with Voice Feedback

A Python application that performs real-time object detection using YOLOv5 and provides audio feedback through text-to-speech. Specifically designed and optimized for **Raspberry Pi 5 (8GB)** with Razer Kiyo camera.

## ✨ Features

- **Real-time Object Detection**: Uses YOLOv5 Nano model optimized for Raspberry Pi performance
- **Voice Feedback**: Announces detected objects using text-to-speech via eSpeak
- **Live Video Feed**: Displays detection results with bounding boxes in real-time
- **Smart Announcement Logic**: Prevents repetitive announcements with time-based filtering
- **Raspberry Pi Optimized**: Lightweight YOLOv5n model for optimal Pi 5 performance
- **Camera Optimized**: Pre-configured for Razer Kiyo at 640x480 resolution

## 🔧 Requirements

### System Requirements
- **Raspberry Pi 5 (8GB RAM)** - Primary tested platform
- Python 3.9+ (Raspberry Pi OS default)
- Webcam or USB camera (Razer Kiyo recommended)
- MicroSD card (32GB+ recommended, Class 10)
- Stable power supply (official Pi 5 adapter recommended)

### Hardware Compatibility
- **Primary**: Razer Kiyo
- **Compatible**: Most USB webcams, built-in laptop cameras
- **Resolution**: 640x480 (configurable)

## 📦 Installation

### 1. Prepare Raspberry Pi 5

#### Flash Raspberry Pi OS
```bash
# Use Raspberry Pi Imager with Raspberry Pi OS (64-bit) recommended
# Enable SSH, configure WiFi, and set username/password during flashing
```

#### Initial Pi Setup
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Enable camera interface
sudo raspi-config
# Navigate to: Interface Options > Camera > Enable

# Reboot to apply changes
sudo reboot
```

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/realtime-object-detection-voice.git
cd realtime-object-detection-voice
```

### 3. Install System Dependencies
```bash
# Essential packages for Raspberry Pi
sudo apt update
sudo apt install -y python3-pip python3-venv git

# Audio and speech synthesis
sudo apt install -y espeak espeak-data libespeak1 libespeak-dev

# OpenCV and camera dependencies
sudo apt install -y python3-opencv
sudo apt install -y libcamera-apps

# Additional Pi 5 optimizations
sudo apt install -y python3-dev libatlas-base-dev
```

### 4. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Python Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install dependencies (this may take 10-15 minutes on Pi)
pip install -r requirements.txt
```

## 📋 Dependencies

Create a `requirements.txt` file with Raspberry Pi 5 optimized versions:

```txt
# PyTorch for ARM64 (Raspberry Pi 5)
torch>=2.0.0
torchvision>=0.15.0

# Computer Vision
opencv-python>=4.8.0

# Text-to-Speech
pyttsx3>=2.90

# YOLOv5 and related
ultralytics>=8.0.0
numpy>=1.21.0
Pillow>=9.0.0

# Performance optimizations for Pi
psutil>=5.9.0
```

### Raspberry Pi Specific Notes
- **PyTorch**: Uses ARM64 optimized builds for better Pi 5 performance
- **OpenCV**: System installation recommended over pip for Pi hardware acceleration
- **Memory Management**: psutil helps monitor system resources during detection

## 🚀 Usage

### Basic Usage
```bash
# Activate virtual environment
source venv/bin/activate

# Run the detection
python3 object_detection.py
```

### Auto-Start on Pi Boot (Optional)
Create a systemd service to run on startup:

```bash
# Create service file
sudo nano /etc/systemd/system/object-detection.service
```

Add this content:
```ini
[Unit]
Description=Real-time Object Detection
After=multi-user.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/realtime-object-detection-voice
Environment=DISPLAY=:0
ExecStart=/home/pi/realtime-object-detection-voice/venv/bin/python3 object_detection.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable object-detection.service
sudo systemctl start object-detection.service

# Check status
sudo systemctl status object-detection.service
```

### Camera Configuration

#### Raspberry Pi 5 Camera Detection
```bash
# List available cameras
ls /dev/video*

# Check USB devices (for Razer Kiyo)
lsusb | grep -i razer

# Test camera with v4l2
v4l2-ctl --list-devices
```

#### Code Configuration
If your Razer Kiyo is not at `/dev/video0`:
```python
# Try different video devices
cap = cv2.VideoCapture('/dev/video0')  # First try
cap = cv2.VideoCapture('/dev/video1')  # If Razer Kiyo is secondary

# For Pi Camera Module (if using instead of USB)
# cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
```

#### Raspberry Pi 5 USB Performance
```python
# Optimized settings for Pi 5 + Razer Kiyo
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)           # Stable 30fps on Pi 5
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)     # Reduce latency
```

### Controls
- **Q Key**: Quit the application
- **ESC**: Alternative quit method
- **Window Close**: Click X to close

## ⚙️ Configuration

### Camera Settings
Modify these parameters in the code:
```python
# Camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Camera device (change if needed)
cap = cv2.VideoCapture('/dev/video0')  # Linux/macOS
cap = cv2.VideoCapture(0)              # Windows (usually)
```

### Voice Settings
```python
# Speech rate (words per minute)
engine.setProperty('rate', 150)

# Voice volume (0.0 to 1.0)
engine.setProperty('volume', 1.0)

# Voice selection (system dependent)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change index for different voices
```

### Detection Settings
```python
# Time between repeated announcements (seconds)
announcement_cooldown = 5

# Confidence threshold (0.0 to 1.0)
model.conf = 0.25  # Add this line after model loading

# NMS threshold
model.iou = 0.45   # Add this line after model loading
```

## 📁 Project Structure

```
realtime-object-detection-voice/
├── README.md
├── requirements.txt
├── object_detection.py
├── .gitignore
├── LICENSE
└── docs/
    ├── installation.md
    ├── troubleshooting.md
    └── configuration.md
```

## 🐛 Troubleshooting

### Common Issues

#### Camera Not Found
```bash
# List available cameras (Linux)
ls /dev/video*

# Test camera access
v4l2-ctl --list-devices
```

#### No Audio Output
```bash
# Test TTS system
python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('Test'); engine.runAndWait()"
```

#### Poor Detection Performance
- Ensure good lighting conditions
- Check camera focus and cleanliness
- Verify camera resolution settings
- Consider upgrading to YOLOv5s for better accuracy:
```python
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
```

### Raspberry Pi 5 Specific Issues

#### Camera Not Detected
```bash
# Check if camera is recognized
lsusb | grep -i camera
dmesg | grep -i video

# Ensure sufficient power
vcgencmd measure_volts core
# Should show ~1.1V, lower values indicate power issues
```

#### Performance Issues
```bash
# Check CPU temperature
vcgencmd measure_temp
# Should be below 70°C for optimal performance

# Monitor system resources
htop
# Look for high CPU/memory usage

# Check power throttling
vcgencmd get_throttled
# 0x0 = no throttling, other values indicate power/thermal issues
```

#### Audio/TTS Issues on Pi
```bash
# Test audio output
aplay /usr/share/sounds/alsa/Front_Left.wav

# Check audio devices
aplay -l

# Set default audio output (if using HDMI/headphones)
sudo raspi-config
# System Options > Audio > select output device
```

#### Memory Optimization for Pi 5
```python
# Add these optimizations to your code
import gc
import psutil

# Monitor memory usage
def check_memory():
    memory = psutil.virtual_memory()
    print(f"Memory usage: {memory.percent}%")
    if memory.percent > 80:
        gc.collect()  # Force garbage collection

# Call periodically in your main loop
if frame_count % 100 == 0:  # Every 100 frames
    check_memory()
```

## 🎛️ Advanced Features

### Model Switching
```python
# For better accuracy (slower)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# For maximum accuracy (slowest)
model = torch.hub.load('ultralytics/yolov5', 'yolov5m', pretrained=True)
```

### Custom Object Classes
```python
# Filter specific objects
target_classes = ['person', 'car', 'dog', 'cat']
detected = [obj for obj in detected if obj in target_classes]
```

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log detections
logger.info(f"Detected: {detected}")
```

## 🔒 Privacy & Security

- **Local Processing**: All detection happens locally on your device
- **No Data Upload**: No video or audio data is sent to external servers
- **Camera Access**: Only accesses camera when application is running
- **Open Source**: Full source code available for review

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black object_detection.py
flake8 object_detection.py
```

## 📊 Performance (Raspberry Pi 5 - 8GB)

| Model | Speed (FPS) | Accuracy | Memory Usage | Pi 5 Recommendation |
|-------|-------------|----------|--------------|---------------------|
| YOLOv5n | 15-25 | Good | ~400MB | ✅ **Recommended** |
| YOLOv5s | 8-15 | Better | ~800MB | ⚠️ Usable but slower |
| YOLOv5m | 4-8 | Best | ~1.2GB | ❌ Too slow for real-time |

*Performance tested on Raspberry Pi 5 (8GB) with 640x480 camera resolution*

### Performance Tips for Pi 5
- **Cooling**: Use active cooling for sustained performance
- **Power**: Ensure stable 5V/5A power supply
- **SD Card**: Use high-speed Class 10 or better microSD
- **GPU Memory Split**: Increase GPU memory if using Pi camera
```bash
# Increase GPU memory (optional)
sudo raspi-config
# Advanced Options > Memory Split > 128 or 256
```

## 🔄 Version History

- **v1.0.0**: Initial release with basic object detection and TTS
- **v1.1.0**: Added Razer Kiyo optimization
- **v1.2.0**: Improved announcement logic and error handling

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5) for the object detection model
- [Raspberry Pi Foundation](https://www.raspberrypi.org/) for the excellent Pi 5 hardware
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) for text-to-speech functionality
- [OpenCV](https://opencv.org/) for computer vision capabilities
- Razer for the excellent Kiyo camera that works great with Pi 5

---

**Made with ❤️ for the Raspberry Pi and computer vision community**
