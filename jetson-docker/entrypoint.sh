#!/bin/bash
source /opt/ros/humble/setup.bash 2>/dev/null || true
if [ -f /workspace/ros2_ws/install/setup.bash ]; then
    source /workspace/ros2_ws/install/setup.bash
fi
exec "$@"
