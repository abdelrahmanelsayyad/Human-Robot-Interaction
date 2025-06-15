import torch
import cv2
import pyttsx3
import time
import warnings

# 🔇 Suppress warnings
warnings.filterwarnings("ignore")

# 🧠 Load YOLOv5 Nano model (lightweight, fast)
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)

# 🎥 Connect to Razer Kiyo (usually /dev/video0 or video1)
cap = cv2.VideoCapture('/dev/video0')  # Change to '/dev/video1' if needed
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 🗣 Initialize text-to-speech engine
engine = pyttsx3.init(driverName='espeak')
engine.setProperty('rate', 150)

# 🧠 Track spoken labels
last_spoken = ""
last_time = time.time()

print("🟢 Razer Kiyo + YOLOv5 + Voice running... Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠ Could not read from Razer Kiyo.")
        continue

    # 🔍 Run detection
    results = model(frame)
    results.render()

    # 🖼 Show output window
    cv2.imshow("YOLOv5 - Razer Kiyo", results.ims[0])

    # 🎯 Get labels
    labels = results.xyxyn[0][:, -1].numpy()
    detected = list(set([results.names[int(l)] for l in labels]))

    # 🗣 Speak if label is new or time passed
    if detected:
        obj = detected[0]
        if obj != last_spoken or time.time() - last_time > 5:
            print(f"I see a {obj}")
            engine.say(f"I see a {obj}")
            engine.runAndWait()
            last_spoken = obj
            last_time = time.time()

    # ❌ Quit with Q key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
