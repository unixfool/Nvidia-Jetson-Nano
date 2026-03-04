# ═══════════════════════════════════════════════════════════════
# Jetson Nano AI Environment
# Base: Ubuntu 22.04 (Jammy)
# Target: NVIDIA Jetson Nano — JetPack 4.6.4 / L4T 32.7.4 / CUDA 10.2
#
# Includes:
#   - Python 3.12.3 (compiled from source)
#   - ROS2 Humble
#   - OpenCV 4.x + NumPy + SciPy + Pandas + Scikit-learn
#   - Jetson.GPIO 2.1.12 + smbus2 (I2C)
#   - TensorRT 8.2.1 ctypes wrapper (libs mounted from host)
#   - v4l2-ctl 1.33.0 (compiled from source)
#   - Jupyter Lab
#
# Code by: y2k — https://github.com/unixfool
# ═══════════════════════════════════════════════════════════════

FROM ubuntu:22.04

LABEL description="Jetson Nano AI Environment — Python3.12 + ROS2 Humble + GPIO + TensorRT + IMX219"
LABEL maintainer="y2k <https://github.com/unixfool>"
LABEL version="2.0.0"

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV ROS_DISTRO=humble
ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages:$PYTHONPATH

# ── Sistema base ───────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget git vim nano htop build-essential cmake pkg-config \
    ca-certificates gnupg lsb-release software-properties-common \
    apt-transport-https sudo \
    libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
    libsqlite3-dev libffi-dev liblzma-dev \
    libncurses5-dev libncursesw5-dev \
    libhdf5-dev libatlas-base-dev \
    python3 python3-pip \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ── Python 3.12 desde fuente ───────────────────────────────────
RUN cd /tmp && \
    wget -q https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz && \
    tar -xf Python-3.12.3.tgz && \
    cd Python-3.12.3 && \
    ./configure --enable-optimizations --with-lto --prefix=/usr/local && \
    make -j$(nproc) && \
    make altinstall && \
    cd / && rm -rf /tmp/Python-3.12.3* && \
    ln -sf /usr/local/bin/python3.12 /usr/local/bin/python3 && \
    ln -sf /usr/local/bin/python3.12 /usr/local/bin/python && \
    ln -sf /usr/local/bin/pip3.12 /usr/local/bin/pip3 && \
    ln -sf /usr/local/bin/pip3.12 /usr/local/bin/pip && \
    pip3 install --upgrade pip setuptools wheel

# ── ROS2 Humble ───────────────────────────────────────────────
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) \
    signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
    http://packages.ros.org/ros2/ubuntu jammy main" | \
    tee /etc/apt/sources.list.d/ros2.list > /dev/null && \
    apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-ros-base \
    ros-dev-tools \
    python3-colcon-common-extensions \
    python3-rosdep \
    && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    rosdep init && rosdep update

# ── OpenCV ────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-opencv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ── v4l2-utils (compilado para GLIBC 2.35) ────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    meson ninja-build libudev-dev libjpeg-dev \
    && cd /tmp \
    && git clone --depth=1 https://git.linuxtv.org/v4l-utils.git \
    && cd v4l-utils \
    && meson setup builddir --prefix=/usr/local \
        -Dqv4l2=disabled \
        -Dqvidcap=disabled \
        -Dgconv=disabled \
    && ninja -C builddir \
    && ninja -C builddir install \
    && cd / && rm -rf /tmp/v4l-utils \
    && apt-get remove -y meson ninja-build \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ── Python packages ───────────────────────────────────────────
RUN pip3 install --no-cache-dir \
    jetson-stats \
    numpy \
    Pillow \
    matplotlib \
    scipy \
    scikit-learn \
    pandas \
    tqdm \
    opencv-python-headless \
    pyyaml \
    jupyter \
    jupyterlab \
    smbus2 \
    Jetson.GPIO

# ── Grupos GPIO/I2C ───────────────────────────────────────────
RUN groupadd -f gpio && \
    groupadd -f i2c && \
    groupadd -f dialout

# ── TensorRT 8.2.1 Python wrapper ─────────────────────────────
RUN mkdir -p /usr/local/lib/python3.12/site-packages/tensorrt && \
    printf '__version__ = "8.2.1"\nimport ctypes\n_RTLD_LAZY=0x1\n_RTLD_GLOBAL=0x100\n_libs_to_load=["libEGL.so.1.1.0","libEGL_nvidia.so.0","libnvidia-eglcore.so.32.7.6","libnvrm.so","libnvrm_gpu.so","libnvmedia.so","libnvinfer.so.8","libnvinfer_plugin.so.8","libnvonnxparsers.so.8","libnvparsers.so.8"]\n_loaded=[]\nfor _lib in _libs_to_load:\n    try:\n        _loaded.append(ctypes.CDLL(_lib,_RTLD_LAZY|_RTLD_GLOBAL))\n    except OSError:\n        pass\ndef is_available():\n    return len(_loaded)>=7\n' \
    > /usr/local/lib/python3.12/site-packages/tensorrt/__init__.py

# ── LD_LIBRARY_PATH para TensorRT ─────────────────────────────
RUN echo 'export LD_LIBRARY_PATH=/usr/lib/aarch64-linux-gnu/tegra-egl:/usr/lib/aarch64-linux-gnu/tegra:/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH' \
    >> /etc/bash.bashrc

# ── Usuario no-root ───────────────────────────────────────────
RUN useradd -m -u 1000 -s /bin/bash jetson && \
    echo "jetson ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/jetson && \
    usermod -aG gpio,i2c,dialout jetson && \
    mkdir -p /workspace && chown jetson:jetson /workspace

USER jetson
WORKDIR /workspace

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "export PYTHONPATH=/usr/local/lib/python3.12/site-packages:\$PYTHONPATH" >> ~/.bashrc && \
    echo "export JETSON_TESTING_MODEL_NAME=JETSON_NANO" >> ~/.bashrc && \
    echo "export LD_LIBRARY_PATH=/usr/lib/aarch64-linux-gnu/tegra-egl:/usr/lib/aarch64-linux-gnu/tegra:/usr/lib/aarch64-linux-gnu:\$LD_LIBRARY_PATH" >> ~/.bashrc && \
    echo "export GST_PLUGIN_PATH=/usr/lib/aarch64-linux-gnu/gstreamer-1.0" >> ~/.bashrc

COPY --chown=jetson:jetson entrypoint.sh /entrypoint.sh
RUN sudo chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]
