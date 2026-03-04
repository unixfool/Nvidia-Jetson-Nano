from setuptools import setup

package_name = 'imx219_camera'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='y2k',
    maintainer_email='y2k@desarrollaria.com',
    description='IMX219 Camera Node for Jetson Nano — ROS2 Humble',
    license='MIT',
    entry_points={
        'console_scripts': [
            'camera_node = imx219_camera.camera_node:main',
        ],
    },
)
