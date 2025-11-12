from setuptools import setup
import os
from glob import glob

package_name = 'kobuki_launch'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    data_files=[
        (os.path.join('share', package_name, 'launch'), glob('kobuki_launch/launch/*.py')),
        (os.path.join('share', package_name), ['package.xml']),
    ],
)
