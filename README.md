Projekt wykorzystuje ROS 2 Humble do detekcji markerów ArUco i w zależności 
od ich położenia powyżej lub poniżej środka obrazu z kamery odbywa się sterowanie
jednym ze stawów robota UR5 w Gazebo/Rviz (ruch pion-poziom 0-90 stopni)


## Wymagania
Projekt wymaga zainstalowanego ROS 2 Humble oraz pobocznych bibliotek. Użyj skryptu:

```bash
sudo apt update 
sudo apt install ros-humble-desktop ros-humble-ur-simulation-gz ros-humble-usb-cam ros-humble-cv-bridge python3-opencv -y
```

## Utworzenie folderu roboczego, wykonaj:

```bash
mkdir -p ~/projekt/src
cd ~/projekt/src
```

## Pobierz projekt:

```bash
git clone https://github.com/Kacperrro134/projekt-aruco.git
```

## Zbuduj projekt:

```bash
cd ~/projekt
source /opt/ros/humble/setup.bash
colcon build --packages-select aruco_control
source install/setup.bash
```

## Uruchomienie

```bash
ros2 launch aruco_control projekt_launch.py
```

## Autorzy
Kacper K
Artem K
