from setuptools import find_packages, setup

package_name = 'elevator_proj'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', [
            'elevator_proj/launch/launch_elevator_proj.py'
        ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ewachtel',
    maintainer_email='emily.w.charles@gmail.com',
    description='Code for running CS133 elevator HRI project',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'control_node = elevator_proj.control_node:main',
            'speech_node = elevator_proj.speech_node:main',
            'screen_node = elevator_proj.screen_node:main',
            'test_node = elevator_proj.test_node:main'
        ],
    },
)
