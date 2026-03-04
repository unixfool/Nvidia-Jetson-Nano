#!/usr/bin/env python3.12
"""
Jetson IMX219 RAW capture — v4l2 + debayer pipeline
Usage: jcapture [output.jpg] [scale] [exposure]
  scale:    0.25/0.5/1.0 (default 0.5)
  exposure: 2495=auto / 50000=indoor / 200000=dark (default 2495)
Code by: y2k - URL: https://github.com/unixfool
"""
import sys
import subprocess
import numpy as np
import cv2
import os
import time

OUTPUT   = sys.argv[1] if len(sys.argv) > 1 else f"/tmp/capture_{int(time.time())}.jpg"
SCALE    = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
EXPOSURE = int(sys.argv[3]) if len(sys.argv) > 3 else 2495
RAW_TMP  = "/tmp/jetson_raw.bin"
WIDTH, HEIGHT = 3264, 2464

print(f"📷 Capturing IMX219 {WIDTH}x{HEIGHT} scale={SCALE} exposure={EXPOSURE}")

# Configurar exposición
subprocess.run(['v4l2-ctl', '--device=/dev/video0',
    f'--set-ctrl=exposure={EXPOSURE}'], capture_output=True)
time.sleep(0.3)

# Capturar RAW
subprocess.run([
    "v4l2-ctl", "--device=/dev/video0",
    f"--set-fmt-video=width={WIDTH},height={HEIGHT},pixelformat=RG10",
    "--stream-mmap", "--stream-count=1",
    f"--stream-to={RAW_TMP}"
], capture_output=True)

if not os.path.exists(RAW_TMP) or os.path.getsize(RAW_TMP) == 0:
    print("❌ Capture failed")
    sys.exit(1)

print(f"   RAW size: {os.path.getsize(RAW_TMP)/1024/1024:.1f} MB")

# Procesar RAW
raw = np.fromfile(RAW_TMP, dtype=np.uint16)
frame = raw[:WIDTH*HEIGHT].reshape(HEIGHT, WIDTH)
frame_norm = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
bgr = cv2.cvtColor(frame_norm, cv2.COLOR_BayerBG2BGR_EA)

# White balance
h, w = bgr.shape[:2]
zone = bgr[h//4:h//2, w//3:2*w//3]
ref = float(zone[:,:,1].mean())
b, g, r = cv2.split(bgr.astype(np.float32))
b = np.clip(b * (ref / (float(zone[:,:,0].mean()) + 1e-6)), 0, 255)
r = np.clip(r * (ref / (float(zone[:,:,2].mean()) + 1e-6)), 0, 255)
result_img = cv2.merge([b, g, r]).astype(np.uint8)

# CLAHE
lab = cv2.cvtColor(result_img, cv2.COLOR_BGR2LAB)
clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8,8))
lab[:,:,0] = clahe.apply(lab[:,:,0])
result_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

# Escalar
if SCALE != 1.0:
    nw, nh = int(WIDTH * SCALE), int(HEIGHT * SCALE)
    result_img = cv2.resize(result_img, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    print(f"   Resized: {nw}x{nh}")

cv2.imwrite(OUTPUT, result_img, [cv2.IMWRITE_JPEG_QUALITY, 95])
os.remove(RAW_TMP)
print(f"✅ Saved: {OUTPUT}")
