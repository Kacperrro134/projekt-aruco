from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    ur_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ur_simulation_gz'), 'launch', 'ur_sim_control.launch.py')
        ]),
        launch_arguments={'ur_type': 'ur5e'}.items(),
    )

    # wezel kamery
    camera_node = Node(
        package='usb_cam',
        executable='usb_cam_node_exe',
        name='usb_cam',
        parameters=[{'video_device': '/dev/video0', 'image_width': 640, 'image_height': 480}]
    )

    # sterowanie aruco
    aruco_node = Node(
        package='aruco_control',
        executable='aruco_node',
        name='aruco_control_node',
        output='screen'
    )

    # podgląd kamery
    rqt_node = Node(
        package='rqt_image_view',
        executable='rqt_image_view',
        name='rqt_image_view',
        arguments=['/aruco_preview']
    )

    return LaunchDescription([
        ur_sim_launch,
        camera_node,
        aruco_node,
        rqt_node
    ])
