FROM ros:humble

# ===== Ustawienia środowiska =====
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble

# ===== Instalacja zależności systemowych =====
RUN apt update && apt install -y \
    python3-pip \
    python3-colcon-common-extensions \
    python3-opencv \
    ros-humble-cv-bridge \
    ros-humble-usb-cam \
    ros-humble-rqt-image-view \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-ur \
    ros-humble-ur-robot-driver \
    ros-humble-ur-simulation-gz \
    && rm -rf /var/lib/apt/lists/*

# ===== Workspace =====
WORKDIR /workspace

# ===== Kopiowanie projektu =====
COPY src ./src

# ===== Build ROS 2 =====
RUN . /opt/ros/humble/setup.sh && \
    colcon build

# ===== Source workspace przy starcie =====
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc && \
    echo "source /workspace/install/setup.bash" >> /root/.bashrc

CMD ["bash"]
