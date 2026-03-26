# Nvidia-Jetson-Nano
Nvidia Jetson Nano Developer Kit from WaveShare (For JetBot)

# 🤖 AI/Robotics Environment

> Complete setup of NVIDIA Jetson Nano Developer Kit (JetBot) with Ubuntu 24.04 LTS, Docker, Python 3.12, ROS2 Humble, GPU, GPIO and full support for robotics and artificial intelligence.

---

## 📋 System Specifications

| Component | Detail |
|---|---|
| **Hardware** | NVIDIA Jetson Nano Developer Kit (JetBot) |
| **Module** | NVIDIA Jetson Nano module (16Gb eMMC) |
| **SoC** | Tegra210 (tegra210 / Porg) |
| **CUDA Arch BIN** | 5.3 |
| **BoardID** | p3448 |
| **OS** | Ubuntu 24.04 LTS (Noble Numbat) |
| **Kernel** | 4.9.337-tegra |
| **JetPack** | 4.6.4 [L4T 32.7.4] |
| **Hostname** | `jetson` |
| **Boot** | eMMC (bootloader + kernel) + microSD (OS + data) |
| **Storage** | 115GB microSD |
| **RAM** | 4GB LPDDR4 + 2GB ZRAM swap |
| **GPU** | Tegra iGPU — 76MHz idle / 921MHz max |

---

## 🌐 Network

| Interface | Type | IP | Status |
|---|---|---|---|
| `wlan0` | WiFi (Intel iwlwifi) | `192.168.1.138/24` | ✅ Active |
| `eth0` | Ethernet | `192.168.1.37/24` | Configured |
| `docker0` | Docker Bridge | `172.17.0.1/16` | Automatic |

**Gateway:** `192.168.1.1`

**WiFi SSID:** `JETSON` — configured via `wpa_supplicant`

### Network configuration (`/etc/network/interfaces`)

```
auto eth0
iface eth0 inet static
    address 192.168.1.37
    netmask 255.255.255.0
    gateway 192.168.1.1

auto wlan0
iface wlan0 inet static
    address 192.168.1.138
    netmask 255.255.255.0
    gateway 192.168.1.1
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```

### WiFi configuration (`/etc/wpa_supplicant/wpa_supplicant.conf`)

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="JETSON"
    psk="YOUR_WIFI_PASSWORD"
}
```

### SSH Access

```bash
ssh jetbot@192.168.1.138    # via WiFi
ssh jetbot@192.168.1.37     # via Ethernet
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────┐
│             NVIDIA Jetson Nano                  │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │           Ubuntu 24.04 LTS                │  │
│  │           kernel 4.9.337-tegra            │  │
│  │                                           │  │
│  │  Python 3.12  │  jtop 4.3.2  │  GPIO      │  │
│  │  tegrastats   │  ZRAM 2GB    │  I2C       │  │
│  │  CUDA 10.2    │  cuDNN 8.2   │  UART      │  │
│  │                                           │  │
│  │  ┌────────────────────────────────────┐   │  │
│  │  │       Docker (overlay2)            │   │  │
│  │  │                                    │   │  │
│  │  │  jetson-ai:latest                  │   │  │
│  │  │  ├── Python 3.12.3                 │   │  │
│  │  │  ├── OpenCV 4.13.0                 │   │  │
│  │  │  ├── NumPy 2.4.2                   │   │  │
│  │  │  ├── ROS2 Humble                   │   │  │
│  │  │  ├── Jupyter Lab :8888             │   │  │
│  │  │  └── jetson-stats                  │   │  │
│  │  └────────────────────────────────────┘   │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  eMMC: bootloader + kernel                      │
│  microSD: operating system + data               │
└─────────────────────────────────────────────────┘
```

---

## ⚙️ Installed Components

### Host (Ubuntu 24.04)

| Component | Version | Notes |
|---|---|---|
| Python | 3.12.3 | System |
| Docker | 20.10.24 | Storage: overlay2 |
| runc | 1.2.5 | overlay2 compatible |
| jtop | 4.3.2 | GPU/CPU/RAM monitor |
| CUDA | 10.2.300 | Detected via `/usr/local/cuda/version.txt` |
| cuDNN | 8.2.1 | Registered in dpkg (L4T 32.7.4) |
| TensorRT | 8.2.1.8 | Registered in dpkg (L4T 32.7.4) |
| VPI | 2.0.0 | Registered in dpkg (L4T 32.7.4) |
| OpenCV | 4.13.0 | Detected via `/usr/local/bin/opencv_version` |
| tegrastats | L4T 32.7.4 | Extracted from nvidia-l4t-tools |
| jetson_clocks | L4T 32.7.4 | Frequency control |
| nvpmodel | L4T 32.7.4 | Power mode control |
| Jetson.GPIO | 2.1.12 | GPIO control |
| smbus2 | 0.6.0 | I2C communication |
| adafruit-blinka | 8.69.0 | CircuitPython on Jetson |
| adafruit-circuitpython-ssd1306 | 2.12.22 | SSD1306 OLED display |
| adafruit-circuitpython-ina219 | 3.5.0 | INA219 power monitor |
| adafruit-servokit | 1.3.22 | PCA9685 servo control |
| adafruit-circuitpython-pca9685 | 3.4.20 | PWM controller (motors) |
| adafruit-circuitpython-motor | 3.4.18 | DC motor control |
| psutil | 7.2.2 | System metrics |
| Pillow | 12.1.1 | Image processing for OLED |
| pyserial | 3.5 | UART communication |
| ZRAM swap | 2GB | lzo compression, priority 100 |

### Docker Container (`jetson-ai:latest`)

| Component | Version |
|---|---|
| Base | ubuntu:22.04 |
| Python | 3.12.3 (compiled from source) |
| OpenCV | 4.13.0 |
| NumPy | 2.4.2 |
| ROS2 | Humble |
| Jupyter Lab | Latest |
| jetson-stats | Latest |
| scikit-learn | Latest |
| pandas | Latest |
| matplotlib | Latest |
| Jetson.GPIO | 2.1.12 |
| smbus2 | 0.6.0 |
| adafruit-servokit | 1.3.22 |
| pyserial | 3.5 |

---

## 🔧 Critical Configurations

### ⚠️ cgroups v1 (required for Docker with kernel 4.9)

File: `/mnt/emmc/boot/extlinux/extlinux.conf`

Parameter added to the `APPEND` line:
```
systemd.unified_cgroup_hierarchy=0
```

Without this parameter Docker does not work with kernel 4.9-tegra.

### ⚠️ iptables legacy

```bash
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
```

Required because Ubuntu 24 uses nftables by default and kernel 4.9 requires iptables.

### Docker daemon (`/etc/docker/daemon.json`)

```json
{
    "storage-driver": "overlay2",
    "iptables": true,
    "ip-forward": true,
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "10m",
        "max-file": "3"
    },
    "exec-opts": ["native.cgroupdriver=cgroupfs"]
}
```

### GPU initialization service (`/etc/systemd/system/jetson-gpu-init.service`)

Required to initialize the GPU before jtop starts on boot. Without this service the GPU is not detected after reboot.

```ini
[Unit]
Description=Jetson GPU Initialization
After=local-fs.target
Before=jtop.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/bash -c 'modprobe nvgpu && sleep 2 && echo 0 > /sys/devices/57000000.gpu/railgate_enable && echo gpu-init-ok'

[Install]
WantedBy=multi-user.target
```

jtop dependency override (`/etc/systemd/system/jtop.service.d/gpu-init.conf`):

```ini
[Unit]
After=jetson-gpu-init.service
Requires=jetson-gpu-init.service
```

### jtop library detection

jtop reads libraries from the host system. These files make all libraries visible in the INFO tab:

```bash
# CUDA — version file
sudo mkdir -p /usr/local/cuda
echo "CUDA Version 10.2.300" | sudo tee /usr/local/cuda/version.txt

# OpenCV — wrapper script
sudo tee /usr/local/bin/opencv_version << 'EOF'
#!/bin/bash
echo "4.13.0"
EOF
sudo chmod +x /usr/local/bin/opencv_version

# cuDNN, TensorRT, VPI — registered in /var/lib/dpkg/status
# Package: libcudnn8  Version: 8.2.1
# Package: tensorrt   Version: 8.2.1.8
# Package: libvpi2    Version: 2.0.0
```

### Manually installed L4T libraries

The `nvidia-l4t-*` packages cannot be installed via apt on Ubuntu 24. They are extracted manually:

```bash
cd /tmp
apt-get download nvidia-l4t-tools nvidia-l4t-camera nvidia-l4t-cuda \
    nvidia-l4t-multimedia nvidia-l4t-multimedia-utils nvidia-l4t-3d-core

for deb in nvidia-l4t-*.deb; do
    dpkg-deb -x $deb extracted_$(basename $deb .deb)
done

# Copy binaries
sudo cp extracted_nvidia-l4t-tools_*/usr/bin/tegrastats /usr/bin/
sudo cp extracted_nvidia-l4t-tools_*/usr/bin/jetson_clocks /usr/bin/
sudo cp extracted_nvidia-l4t-tools_*/usr/sbin/nvpmodel /usr/sbin/
sudo cp extracted_nvidia-l4t-tools_*/etc/nvpmodel/nvpmodel_t210_jetson-nano.conf /etc/nvpmodel.conf

# Copy tegra libraries
sudo cp extracted_nvidia-l4t-camera_*/usr/lib/aarch64-linux-gnu/tegra/* /usr/lib/aarch64-linux-gnu/tegra/
sudo cp extracted_nvidia-l4t-cuda_*/usr/lib/aarch64-linux-gnu/tegra/libcuda.so.1.1 /usr/lib/aarch64-linux-gnu/tegra/

# Add paths to ldconfig
echo "/usr/lib/aarch64-linux-gnu/tegra" | sudo tee /etc/ld.so.conf.d/nvidia-tegra.conf
echo "/usr/lib/aarch64-linux-gnu/tegra-egl" | sudo tee -a /etc/ld.so.conf.d/nvidia-tegra.conf
sudo ldconfig
```

### L4T metadata files (created manually)

```bash
# /etc/nv_tegra_release
echo "# R32 (release), REVISION: 7.4, GCID: 33916208, BOARD: t210ref, EABI: aarch64, DATE: Tue Jan 17 01:31:27 UTC 2023" \
    | sudo tee /etc/nv_tegra_release

# /etc/nv_boot_control.conf
sudo tee /etc/nv_boot_control.conf << 'EOF'
TNSPEC 3448-0002-300-A.0-1-0-jetson-nano-
COMPATIBLE_SPEC 3448-0002-300-A.0-1-0-jetson-nano-
TEGRA_CHIPID 0x21
TEGRA_OTA_BOOT_DEVICE /dev/mmcblk0boot0
TEGRA_OTA_GPT_DEVICE /dev/mmcblk0boot1
EOF
```

---

## 🔌 I2C Bus — Connected Devices

The WaveShare JetBot expansion board exposes the following devices on I2C bus 1:

| Address | Device | Function |
|---|---|---|
| `0x3C` | SSD1306 | OLED display 128x32 |
| `0x41` | INA219 | Battery voltage/current/power monitor |
| `0x60` | PCA9685 | PWM controller — DC motor driver |
| `0x70` | PCA9685 | PCA9685 broadcast address (group) |

Bus 2 (`0x50`, `0x57`) contains EEPROM chips — system use only.

### Scan I2C devices

```bash
python3 << 'EOF'
import smbus2
for bus_num in range(9):
    try:
        bus = smbus2.SMBus(bus_num)
        found = []
        for addr in range(0x03, 0x78):
            try:
                bus.read_byte(addr)
                found.append(hex(addr))
            except:
                pass
        bus.close()
        if found:
            print(f"Bus {bus_num}: {found}")
    except:
        pass
EOF
```

---

## 📟 OLED Display (SSD1306 128x32)

The WaveShare JetBot expansion board includes a 128x32 pixel OLED display (SSD1306 at I2C address `0x3C`).

### Display content

The OLED shows 3 lines updated every 5 seconds:

```
JETSON DASHBOARD
IP 192.168.1.138
CPU 12%  48C
```

- **Line 1** — Dashboard title (bold)
- **Line 2** — Active WiFi IP address
- **Line 3** — CPU usage % and CPU temperature °C

### Required libraries (installed globally with sudo)

```bash
sudo pip3 install adafruit-circuitpython-ssd1306 --break-system-packages
sudo pip3 install adafruit-blinka --break-system-packages
sudo pip3 install Jetson.GPIO --break-system-packages
sudo pip3 install psutil --break-system-packages
sudo pip3 install Pillow --break-system-packages
```

### OLED service script (`/usr/local/bin/jetbot-oled.py`)

```python
#!/usr/bin/env python3
"""
JetBot OLED Display Service
Updates every 5 seconds with IP, CPU and temperature
"""
import time, socket, psutil, board, busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

FONT_BIG   = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_SMALL = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
OLED_ADDR  = 0x3C
UPDATE_SEC = 5

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "no network"

def get_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return int(f.read().strip()) / 1000.0
    except:
        return 0.0

def main():
    i2c  = busio.I2C(board.SCL, board.SDA)
    oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=OLED_ADDR)
    font_big   = ImageFont.truetype(FONT_BIG,   10)
    font_small = ImageFont.truetype(FONT_SMALL,  8)

    while True:
        try:
            ip   = get_ip()
            cpu  = psutil.cpu_percent(interval=1)
            temp = get_temp()

            img  = Image.new("1", (128, 32))
            draw = ImageDraw.Draw(img)
            draw.text((0,  0), "JETSON DASHBOARD",             font=font_big,   fill=255)
            draw.text((0, 13), f"IP {ip}",                     font=font_small, fill=255)
            draw.text((0, 23), f"CPU {cpu:.0f}%  {temp:.0f}C", font=font_small, fill=255)

            oled.image(img)
            oled.show()
        except Exception as e:
            print(f"OLED error: {e}")

        time.sleep(UPDATE_SEC)

if __name__ == "__main__":
    main()
```

### Systemd service (`/etc/systemd/system/jetbot-oled.service`)

```ini
[Unit]
Description=JetBot OLED Display Service
After=network.target
Wants=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /usr/local/bin/jetbot-oled.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Enable and start

```bash
sudo systemctl daemon-reload
sudo systemctl enable jetbot-oled
sudo systemctl start jetbot-oled

# Check status
sudo systemctl status jetbot-oled

# View logs
sudo journalctl -u jetbot-oled -f
```

---

## 🔋 Battery Monitor (INA219)

The INA219 current/voltage sensor at I2C address `0x41` monitors the JetBot battery pack (3x 18650, ~12.6V fully charged).

### Readings

| Measurement | Description |
|---|---|
| Bus voltage | Battery pack voltage (V) |
| Shunt voltage | Voltage drop across shunt resistor (mV) |
| Current | Current draw (mA) |
| Power | Power consumption (mW) |

### Battery state reference

| Voltage | State |
|---|---|
| 12.4 – 12.6V | Full |
| 11.5 – 12.4V | Good |
| 10.5 – 11.5V | Low |
| < 10.5V | Critical — charge immediately |

### Quick read

```bash
python3 << 'EOF'
import board, busio, adafruit_ina219

i2c = busio.I2C(board.SCL, board.SDA)
ina = adafruit_ina219.INA219(i2c, addr=0x41)
print(f"Voltage: {ina.bus_voltage:.2f} V")
print(f"Current: {ina.current:.0f} mA")
print(f"Power:   {ina.power:.0f} mW")
EOF
```

---

## 🔄 Persistent Services

| Service | Function | Status |
|---|---|---|
| `jetson-gpu-init` | GPU initialization on boot | ✅ enabled |
| `jtop` | System monitor daemon | ✅ enabled |
| `zram-swap` | 2GB compressed swap | ✅ enabled |
| `wpa_supplicant` | WiFi connection | ✅ enabled |
| `jetson-stats-fix` | Symlink fix for jetson_stats | ✅ enabled |
| `jetbot-oled` | OLED display — IP/CPU/Temp | ✅ enabled |

---

## 🐳 Docker — Usage

### Interactive container with GPU

```bash
docker run -it --rm \
    --device=/dev/nvhost-ctrl \
    --device=/dev/nvhost-ctrl-gpu \
    --device=/dev/nvhost-gpu \
    --device=/dev/nvhost-as-gpu \
    --device=/dev/nvmap \
    -v ~/jetson-workspace:/workspace \
    jetson-ai:latest bash
```

### Jupyter Lab

```bash
docker run -d \
    --name jetson-jupyter \
    --network=host \
    --device=/dev/nvhost-ctrl \
    --device=/dev/nvhost-ctrl-gpu \
    --device=/dev/nvhost-gpu \
    --device=/dev/nvhost-as-gpu \
    --device=/dev/nvmap \
    -v ~/jetson-workspace:/workspace \
    jetson-ai:latest \
    jupyter lab --ip=0.0.0.0 --port=8888 --no-browser \
    --NotebookApp.token="" --NotebookApp.password="" --allow-root
```

Access from browser: `http://192.168.1.138:8888`

### Rebuild image

```bash
cd ~/jetson-docker
docker build --progress=plain -t jetson-ai:latest . 2>&1 | tee build.log
```

### Install packages without rebuild

```bash
docker run --name temp-install -u root jetson-ai:latest \
    pip3 install --no-cache-dir <package>
docker commit temp-install jetson-ai:latest
docker rm temp-install
```

---

## 🎮 GPU — Devices

| Device | Function |
|---|---|
| `/dev/nvhost-ctrl` | Main GPU control |
| `/dev/nvhost-ctrl-gpu` | GPU-specific control |
| `/dev/nvhost-gpu` | GPU device |
| `/dev/nvhost-as-gpu` | GPU address space |
| `/dev/nvhost-vic` | Video Image Compositor |
| `/dev/nvmap` | NVIDIA memory manager |

### GPU test from container

```bash
docker run --rm \
    --device=/dev/nvhost-ctrl --device=/dev/nvhost-ctrl-gpu \
    --device=/dev/nvhost-gpu --device=/dev/nvhost-as-gpu \
    --device=/dev/nvmap \
    -v ~/jetson-workspace:/workspace \
    jetson-ai:latest python3 -c "
import cv2, numpy, sys
print('✅ Python:', sys.version.split()[0])
print('✅ OpenCV:', cv2.__version__)
print('✅ NumPy:', numpy.__version__)
"
```

---

## 🔌 GPIO / I2C / UART

### Available interfaces

| Interface | Devices | Status |
|---|---|---|
| I2C | `/dev/i2c-0` to `/dev/i2c-8` | ✅ Available |
| UART | `/dev/ttyTHS1`, `/dev/ttyTHS2` | ✅ Available |
| GPIO | `/dev/gpiochip0`, `/dev/gpiochip1` | ✅ Available |
| SPI | Not enabled by default | ⚠️ Requires device tree config |

### Permissions (`/etc/udev/rules.d/99-gpio.rules`)

```
SUBSYSTEM=="gpio", GROUP="gpio", MODE="0660"
KERNEL=="gpiochip*", GROUP="gpio", MODE="0660"
KERNEL=="i2c-[0-9]*", GROUP="i2c", MODE="0660"
KERNEL=="ttyTHS*", GROUP="dialout", MODE="0660"
```

User groups: `gpio`, `i2c`, `dialout`

### GPIO usage in Python

```python
import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)
GPIO.cleanup()
```

### I2C usage in Python

```python
import smbus2

bus = smbus2.SMBus(1)
for addr in range(0x03, 0x78):
    try:
        bus.read_byte(addr)
        print(f"Device found at: {hex(addr)}")
    except:
        pass
bus.close()
```

### Servo control via PCA9685

```python
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
kit.servo[0].angle = 90
kit.servo[1].angle = 0
```

### DC motor control via PCA9685

```python
from adafruit_motorkit import MotorKit

kit = MotorKit()
kit.motor1.throttle = 0.5    # 50% forward
kit.motor1.throttle = -0.5   # 50% backward
kit.motor1.throttle = 0      # Stop
```

---

## 🤖 ROS2 Humble

ROS2 is installed inside the `jetson-ai:latest` Docker container.

```bash
# ROS2 interactive shell
jros

# Inside the container
source /opt/ros/humble/setup.bash
ros2 topic list
ros2 node list
colcon build --symlink-install
source install/setup.bash
```

**Workspace:** `~/jetson-workspace/ros2_ws/`

### IMX219 Camera Node

ROS2 package that captures RAW frames from the IMX219 sensor and publishes them as `sensor_msgs/Image`.

**Package:** `~/jetson-workspace/ros2_ws/src/imx219_camera/`

**Published topics:**

| Topic | Type | Description |
|---|---|---|
| `/camera/image_raw` | `sensor_msgs/Image` | Debayered BGR image |
| `/camera/camera_info` | `sensor_msgs/CameraInfo` | Camera metadata |

**Parameters:**

| Parameter | Default | Description |
|---|---|---|
| `fps` | 1 | Capture rate |
| `scale` | 0.25 | Output scale (0.25=816x616) |
| `exposure` | 2495 | Sensor exposure value |
| `device` | /dev/video0 | V4L2 device |

**Usage:**

```bash
jcam_node    # Start camera node (background)
jcam_logs    # View logs
jcam_stop    # Stop node
```

---

## 📈 jtop — System Monitor

```bash
jtop    # Open monitor
# 1=ALL  2=GPU  3=CPU  4=MEM  5=ENG  6=CTRL  7=INFO  Q=Quit
```

### jtop INFO tab (7) — verified output

| Library | Version | Status |
|---|---|---|
| CUDA | 10.2.300 | ✅ |
| cuDNN | 8.2.1 | ✅ |
| TensorRT | 8.2.1.8 | ✅ |
| VPI | 2.0.0 | ✅ |
| OpenCV | 4.13.0 | ✅ |

---

## 💾 ZRAM Swap

2GB compressed swap in RAM — persistent via systemd.

```bash
swapon --show
sudo systemctl status zram-swap
free -h
```

---

## 📁 Directory Structure

```
~/jetson-docker/
├── Dockerfile          # jetson-ai image definition
├── entrypoint.sh       # Entrypoint with ROS2 source
└── build.log           # Last build log

~/jetson-workspace/
├── projects/           # AI/robotics projects
├── datasets/           # Training datasets
├── models/             # Trained models
├── ros2_ws/            # ROS2 workspace
└── configs/            # Configurations

/etc/
├── network/interfaces              # Static network config (eth0 + wlan0)
├── wpa_supplicant/                 # WiFi config (SSID + PSK)
├── docker/daemon.json              # Docker config (overlay2, cgroupfs)
├── nv_tegra_release                # L4T version (created manually)
├── nv_boot_control.conf            # Bootloader config (created manually)
├── nvpmodel.conf                   # Power model config
├── ld.so.conf.d/nvidia-tegra.conf  # Tegra library paths
├── udev/rules.d/99-gpio.rules      # GPIO/I2C/UART permissions
└── systemd/system/
    ├── jetson-gpu-init.service     # GPU init on boot
    ├── jtop.service.d/             # jtop dependency override
    ├── zram-swap.service           # ZRAM swap
    └── jetbot-oled.service         # OLED display service

/usr/local/
├── cuda/version.txt                # CUDA version (for jtop detection)
├── bin/opencv_version              # OpenCV version wrapper (for jtop detection)
└── bin/jetbot-oled.py              # OLED display script

/usr/bin/
├── tegrastats                      # GPU monitor (extracted from L4T)
└── jetson_clocks                   # Frequency control (extracted from L4T)

/usr/sbin/
└── nvpmodel                        # Power model (extracted from L4T)
```

---

## 🐳 Docker — GPIO / I2C / Camera

| Variable | Value | Purpose |
|---|---|---|
| `JDEV` | nvhost devices | GPU access |
| `JGPIO` | gpiochip0/1 + i2c-0/1/2 + ttyTHS1 | GPIO/I2C/UART |
| `JCAM` | /dev/video0 | CSI camera |
| `JSYS` | sys/class/gpio + sys/devices + sys/firmware | GPIO detection |
| `JENV` | JETSON_TESTING_MODEL_NAME=JETSON_NANO | Model detection |

```bash
JIMG="jetson-ai:latest"
JWS="$HOME/jetson-workspace"
JDEV="--device=/dev/nvhost-ctrl --device=/dev/nvhost-ctrl-gpu --device=/dev/nvmap --device=/dev/nvhost-gpu"
JGPIO="--device=/dev/gpiochip0 --device=/dev/gpiochip1 --device=/dev/i2c-0 --device=/dev/i2c-1 --device=/dev/i2c-2 --device=/dev/ttyTHS1"
JCAM="--device=/dev/video0"
JSYS="-v /sys/class/gpio:/sys/class/gpio -v /sys/devices:/sys/devices -v /sys/firmware:/sys/firmware:ro -v /etc/nv_tegra_release:/etc/nv_tegra_release:ro"
JENV="-e JETSON_TESTING_MODEL_NAME=JETSON_NANO"
```

---

## 🔑 Aliases (`~/.bashrc`)

| Alias | Function |
|---|---|
| `jsh` | Interactive shell — GPU + GPIO + I2C + Camera |
| `jmon` | jtop monitor |
| `jlab` | Jupyter Lab on port 8888 |
| `jpy` | Python 3.12 REPL |
| `jros` | ROS2 shell |
| `jstatus` | System status summary |
| `jfull` | Privileged shell with all devices |
| `jcapture` | Capture image from IMX219 (host) |
| `jcam_node` | Start IMX219 ROS2 camera node |
| `jcam_stop` | Stop IMX219 ROS2 camera node |
| `jcam_logs` | Follow camera node logs |
| `jtemp` | CPU/GPU temperature |
| `jgpu` | Current GPU frequency |
| `jrestart` | Restart NVIDIA services |
| `jdocker` | Docker stats and images |

---

## 📷 CSI Camera IMX219

| Property | Value |
|---|---|
| Driver | tegra-video |
| Sensor | IMX219 (i2c 7-0010) |
| Format | RG10 — 10-bit Bayer RGRG/GBGB |
| Bayer pattern | BG (COLOR_BayerBG2BGR) |

### Available resolutions

| Resolution | FPS |
|---|---|
| 3264x2464 | 21 fps |
| 3264x1848 | 28 fps |
| 1920x1080 | 30 fps |
| 1640x1232 | 30 fps |
| 1280x720 | 60 fps |

### RAW capture

```bash
v4l2-ctl --device=/dev/video0 \
    --set-fmt-video=width=3264,height=2464,pixelformat=RG10 \
    --stream-mmap --stream-count=1 --stream-to=/tmp/frame_raw.bin
```

---

## ⚠️ Known Limitations

| Limitation | Cause | Solution |
|---|---|---|
| CSI IMX219 — no color | nvargus EGL display + device-tree incomplete | RAW capture works — use USB camera for full color |
| nvargus full pipeline blocked | Shader compile requires EGL display | Not solvable without JetPack native install |
| SPI not available | Not enabled in device tree | Requires device tree modification |
| TensorRT not functional | Registered for jtop display only | Install natively per project needs |
| OpenCV with CUDA: NO on host | OpenCV installed via pip without CUDA | Use Docker container |

---

## 🚀 System Verification

After each reboot verify in order:

```bash
# 1. Docker
docker run --rm hello-world

# 2. GPU + libraries in container
docker run --rm \
    --device=/dev/nvhost-ctrl --device=/dev/nvhost-ctrl-gpu \
    --device=/dev/nvhost-gpu --device=/dev/nvhost-as-gpu \
    --device=/dev/nvmap \
    jetson-ai:latest python3 -c "
import cv2, numpy, sys
print('✅ Python:', sys.version.split()[0])
print('✅ OpenCV:', cv2.__version__)
print('✅ NumPy:', numpy.__version__)
"

# 3. ZRAM active
swapon --show

# 4. GPIO
python3 -c "import Jetson.GPIO as GPIO; print('✅ GPIO:', GPIO.VERSION)"

# 5. Services
sudo systemctl is-active jetson-gpu-init jtop zram-swap jetbot-oled

# 6. OLED display
sudo systemctl status jetbot-oled

# 7. Battery monitor
python3 -c "
import board, busio, adafruit_ina219
i2c = busio.I2C(board.SCL, board.SDA)
ina = adafruit_ina219.INA219(i2c, addr=0x41)
print(f'✅ Battery: {ina.bus_voltage:.2f}V  {ina.current:.0f}mA')
"

# 8. CSI Camera
v4l2-ctl --device=/dev/video0 --info 2>/dev/null | grep "Card type" && echo "✅ Camera detected"

# 9. System monitor
jtop
```

---

## 📝 Important Notes

> This system runs **Ubuntu 24.04 LTS with kernel 4.9-tegra**, NOT a standard JetPack installation. Multiple compatibility patches have been applied to make Docker and NVIDIA tools work correctly on this non-standard configuration.

**For projects requiring the CSI IMX219 camera:**
1. **Option A:** Use a USB camera — works instantly with OpenCV/V4L2
2. **Option B:** Flash a new SD card with official JetPack 4.6 (Ubuntu 18.04), keeping the current SD as backup

---

## 🧠 TensorRT 8.2.1

TensorRT C++ libraries natively installed on host. Python 3.12 bindings available inside Docker via ctypes wrapper.

```bash
sudo apt install -y libnvinfer8 libnvinfer-plugin8 libnvparsers8 \
    libnvonnxparsers8 libnvinfer-dev libnvinfer-bin libnvinfer-samples
```

```bash
JTRT="-v /usr/lib/aarch64-linux-gnu:/usr/lib/aarch64-linux-gnu \
    -v /usr/lib/aarch64-linux-gnu/tegra:/usr/lib/aarch64-linux-gnu/tegra \
    -v /usr/lib/aarch64-linux-gnu/tegra-egl:/usr/lib/aarch64-linux-gnu/tegra-egl \
    -e LD_LIBRARY_PATH=/usr/lib/aarch64-linux-gnu/tegra-egl:/usr/lib/aarch64-linux-gnu/tegra:/usr/lib/aarch64-linux-gnu"
```

```bash
/usr/src/tensorrt/bin/trtexec --onnx=model.onnx --saveEngine=model.trt
/usr/src/tensorrt/bin/trtexec --loadEngine=model.trt --batch=1
```
