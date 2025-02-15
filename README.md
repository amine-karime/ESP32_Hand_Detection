# ESP32_Hand_Detection
This project streams video from an ESP32-CAM and uses a Python script with MediaPipe to detect hands and toggle an LED via HTTP endpoints, showcasing a simple IoT and computer vision integration.

### The frame_size options for the ESP32-CAM, from lowest to highest resolution, are:

Frame Size	Resolution (WxH)	FPS Performance
FRAMESIZE_QQVGA	160x120	🔥 Fastest (Highest FPS)
FRAMESIZE_QVGA	320x240	⚡ Fast
FRAMESIZE_VGA	640x480	🏎️ Moderate
FRAMESIZE_SVGA	800x600	🚶‍♂️ Slower
FRAMESIZE_XGA	1024x768	🐌 Much Slower
FRAMESIZE_SXGA	1280x1024	🐢 Very Slow
FRAMESIZE_UXGA	1600x1200	💤 Slowest (Lowest FPS)
