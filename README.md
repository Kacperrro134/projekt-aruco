# Projekt ArUco – Docker + ROS 2 Humble

Projekt wykorzystuje ROS 2 Humble do detekcji markerów ArUco.  
Na podstawie położenia markera powyżej lub poniżej środka obrazu z kamery
realizowane jest sterowanie jednym ze stawów robota UR5 w środowisku Gazebo / RViz
(ruch pion–poziom w zakresie 0–90 stopni).

Projekt jest uruchamiany **wyłącznie z wykorzystaniem Dockera** – nie wymaga
lokalnej instalacji ROS 2 ani dodatkowych bibliotek.

---

## Wymagania
- Linux z serwerem X11
- Zainstalowany Docker
- Kamera USB (V4L2)

---

## Pobranie projektu

```bash
git clone https://github.com/Kacperrro134/projekt-aruco.git
cd projekt-aruco
```
---

## Budowanie obrazu 

```bash
docker build -t aruco_project .
```
---

## Zezwolenie Dockerowi na dostęp do GUI (jednorazowo)

```bash
xhost +local:docker
```
---


## Konfigurcja projektu

```bash
docker run --rm -it \
  --net=host \
  --device=/dev/video0:/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  aruco_project
```
Jeśli kamera znajduje się pod innym urządzeniem (np. /dev/video1),
należy odpowiednio zmienić parametr --device.

---

## Urochomienie projektu
Po uruchomieniu kontenera Docker i uzyskaniu dostępu do jego terminala, należy wykonać:

```bash
ros2 launch aruco_control projekt_launch.py
```
---

## Autorzy
Kacper K
Artem K
