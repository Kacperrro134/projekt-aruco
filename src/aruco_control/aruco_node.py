import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from cv_bridge import CvBridge
import cv2

class ArucoUR5ControlNode(Node):
    def __init__(self):
        super().__init__('aruco_ur5_control_node')
        self.subscription = self.create_subscription(Image, '/image_raw', self.image_callback, 10)
        self.image_publisher = self.create_publisher(Image, '/aruco_preview', 10)
        self.publisher = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        self.bridge = CvBridge()
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters_create()
        
        # Zapamiętujemy ostatnią pozycję, żeby robot wiedział gdzie się zatrzymać
        self.current_pos = -1.57 

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        height, width, _ = frame.shape
        center_y = height // 2
        cv2.line(frame, (0, center_y), (width, center_y), (255, 0, 0), 2)
        corners, ids, _ = cv2.aruco.detectMarkers(frame, self.aruco_dict, parameters=self.aruco_params)

        if ids is not None:
            c = corners[0][0]
            m_y = int(c[:, 1].mean())
            cv2.circle(frame, (int(c[:, 0].mean()), m_y), 7, (0, 255, 0), -1)
            
            if m_y < (center_y - 40):
                self.get_logger().info('GÓRA (PION)')
                self.current_pos = -1.57 # Wartość dla pionu
                self.send_command(self.current_pos)
            elif m_y > (center_y + 40):
                self.get_logger().info('DÓŁ (POZIOM)')
                self.current_pos = 0.0   # Wartość dla poziomu
                self.send_command(self.current_pos)
        
        # Jeśli ids jest None (brak znacznika), po prostu nie wywołujemy send_command
        # Dzięki temu robot zostaje w ostatniej wysłanej pozycji self.current_pos

        preview_msg = self.bridge.cv2_to_imgmsg(frame, "bgr8")
        self.image_publisher.publish(preview_msg)

    def send_command(self, target_angle):
        traj_msg = JointTrajectory()
        traj_msg.joint_names = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 
                                'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
        point = JointTrajectoryPoint()
        
        # Wszystkie stawy na 0, oprócz shoulder_lift_joint
        # Ustawiamy pozycję: [obrót_podstawy, bark, łokieć, nadgarstek1, nadgarstek2, nadgarstek3]
        point.positions = [0.0, target_angle, 0.0, 0.0, 0.0, 0.0]
        
        # Bardzo krótki czas wykonania, żeby robot reagował natychmiastowo
        point.time_from_start.nanosec = 200000000 # 0.2 sekundy
        traj_msg.points.append(point)
        self.publisher.publish(traj_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ArucoUR5ControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.init.shutdown()

if __name__ == '__main__':
    main()
