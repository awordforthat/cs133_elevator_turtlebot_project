# Sad Robots Asking for Help in Elevators

# Install
## Windows
I have this running in WSL. It might be possible to run it natively in Windows but I haven't had time to investigate it yet. 

To install WSL:
1. Open a PowerShell window with admin privileges (Start > type PowerShell > right click on PowerShell result > select "run as admin")
2. Run `wsl --install Ubuntu-22.04`

Official documentation is [here](https://learn.microsoft.com/en-us/windows/wsl/install)

Once WSL is installed, enter the Linux environment from powershell by running `wsl -d Ubuntu-22.04`. 

Now you can pick up from the Linux install steps. 

## Mac OSX
I don't know much more than what's in the official docs [here](https://docs.ros.org/en/crystal/Installation/macOS-Install-Binary.html#system-requirements). Once you have ROS installed though, you can start with the project installation steps below. 

## Linux
The following steps (up until the project installation setup steps) are copied directly from the official ROS2 Humble documentation. You can find that here if you prefer to use the original: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html

1. Check that your locale supports UTF-8. If you have a computer that uses any major language, chances are good that you already have UTF-8 support. But you can check - from your Linux/UNIX command prompt, run: 
    - `locale` - check the output for anything that says "UTF-8". If you don't see that, continue with the sub-steps. If you do, continue to step 2.
    - `sudo apt update && sudo apt install locales`
    - `sudo locale-gen en_US en_US.UTF-8`
    - `sudo update-locale LC_ALL=en_US.UTF-8`
    - `LANG=en_US.UTF-8`
    - `export LANG=en_US.UTF-8`
    - rerun `locale`. Check the output to make sure 'UTF-8' appears.
2. Add the ROS2 apt repository:
    - `sudo apt install software-properties-common`
    - `sudo add-apt-repository universe`
3. Add the ros-apt-source packages:
    - Install curl if it's not already installed: `sudo apt update && sudo apt install curl -y`
    - `export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')`
    - `curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"`
    - `sudo dpkg -i /tmp/ros2-apt-source.deb`
4. Update your repo caches:
    - `sudo apt update`
    - `sudo apt upgrade`
5. Add the core ROS packages:
    - `sudo apt install ros-humble-desktop`
    - `sudo apt install ros-humble-ros-base`
    - `sudo apt install ros-dev-tools`
6. Set up your environment. You will have to do this every time you restart your computer/environment. 
    - `source /opt/ros/humble/setup.bash`

# Extra Dependencies
1. The audio code relies on ffmpeg. Install it with: `sudo apt update; sudo apt install ffmpeg`
2. Also install pydub into the system environment (sorry, I ran out of time to get this working in a venv): 
    - `sudo apt install python3-pip` (if you don't already have it installed)
    - `pip3 install pydub` 
3. You might need to install some pulseaudio utilities. Do this if you get errors on launch like "[ERROR] [1763922903.540994613] [audio_capture_node]: Unsupported media type."
    - `sudo apt install pulseaudio-utils`


# Forwarding joystick ports (Windows only)
1. In Windows Powershell, run `winget install usbipd`
2. Run `usbipd list`. Look for your joystick controller in the output list and note its BUSID. 
3. Attach the joysticks to WSL with `usbipd attach --wsl --busid <BUSID>`
    - you may need to expose the port first. If this errors, follow the prompts given to run expose the port as an admin (something like `usbipd bind --busid <BUSID>`)
4. In WSL, install the joystick packages: 
    - `sudo apt install joystick`
    - `sudo modprobe joydev`



# Installing the elevator project
Now that you have ROS installed, you can download and run this project.

1. Choose a folder to put this project in. I have it directly in the home directory (~). You can put it anywhere, but it might be good if we all have it in the same location for easy communication.
2. `cd` into that directory: `cd ~`. 
3. Clone this repo: `git clone https://github.com/awordforthat/cs133_elevator_turtlebot_project`
4. You should now have a folder at `~/cs133_elevator_turtlebot_project`. Inside that folder should be a `src` directory.
5. Change into the project directory: `cd cs133_elevator_turtlebot_project`
6. Install the project's dependencies: `rosdep install --from-paths src -y --ignore-src`
7. Build the project: `colcon build --symlink-install`. This first build will take a long time (30 minutes on my laptop). Subsequent builds will be much faster.
8. Every time you build, you'll need to source the install file. Do that now: `source install/setup.bash`
9. Now you're ready to run the project!
    - In this same shell, run the elevator project: `ros2 launch elevator_proj launch_elevator_proj.py`
    - Open a second terminal. In Windows, that means starting from PowerShell again and running `wsl -d Ubuntu-22.04`. On Mac, just open a new terminal in the install directory.
    - You should see some text that indicates which process ID (PID) is assigned to which node. 
    - In the second terminal, run `ros2 run elevator_proj test_node`. You should see a prompt that says "Enter a command:".
10. Interact with the nodes:
    - In the test node shell, type anything you want at the prompt and press Enter. You should see printouts in the other shell indicating that the control node has received the prompt and passed it on to the speech node. The speech node counts down 3 seconds, then passes the Done command to the feedback topic, where the control node picks it up. 


There's an existing bug that sends the test commands twice. I need to fix that. But until then, happy testing!


# Adding a new node
Luckily ROS makes this pretty easy. 
1. Create a new Python node file in `<root>/src/elevator_proj/elevator_proj`.
2. Add the following imports:
    - `import rclpy`
    - `from rclpy.node import Node`
    - `from std_msgs.msg import String` You can change what type of message you send if performance is important. For easy testing, choose String.
3. Create a new class that inherits from Node:
    - `class MyNode(Node):
        super().__init__("my_node")
    - Replace "MyNode" and "my_node" with whatever you want to call your node.
4. Add the entrypoint:
    - In the same file, write a main method and an entry point to run the main method (this is outside the class definition):
    ```
    def main(args=None):
        rclpy.init(args=args)
        my_node = MyNode()

        rclpy.spin(my_node)

        my_node.destroy_node()
        rclpy.shutdown()
        
    if __name__ == "__main__":
        main()
    ```
5. If you want to run your node manually, you're done! To run it, use `ros2 run elevator_proj <my_node>` where <my_node> is the name you gave it in the `super().__init__() call.
6. If you want to run the node at the same tiem as the existing ones, you'll have to edit the launch script:
    - Open `~/<root>/src/elevator_proj/elevator_proj/launch/launch_elevator_proj.py`
    - Add your new node to the list of Nodes. It should look something like:
    ```
    Node(
        package="elevator_proj",
        executable=<new_node_name>,
        name=<new_node_name>,
        output="screen"
    )
    ```
7. You will also need to add it to the build and install script. Open `~/<root>/src/elevator_proj/setup.py`.
    - In the section called `entry_points`, add your new node. It should look nearly the same as the existing ones: `"my_node = elevator_proj.test_node:main"`
8. Navigate to the source directory: `cd ~/cs133_elevator_proj`
9. Build the project: `colcon build --symlink-install --packages-select elevator_proj
10. Source the install script: `source install/setup.bash`
11. Now you can rerun the project using the launch script (`ros2 launch elevator_proj launch_elevator_proj.py`)

# Adding media
You will have to create the media directory and transfer image and audio files in manually because we don't want colcon to rebuild the project every time assets change. 

The robot assets are stored in this repo and you will have to put them in a specific location so the robot code can find them. 

1. From your shell terminal: `mv <repo_root>/robot_assets ~`

#TODOs
- Document running the telop/sim project
- fix the double publish bug in the control node
- add diagram showing relationships between nodes and topics



# Panic notes:
- Source these in order: `source /opt/ros/humble/setup.bash`
`source ~/ros2_kobuki_ws/install/setup.bash`




# Day of - how to run
1. Open WSL 
2. cd to ~/ros2_kobuki_ws/
3. Run `source /opt/ros/humble/setup.bash`
4. Run `source ~/ros2_kobuki_ws/install/setup.bash`
5. Attach the USB port to WSL, from Powershell as admin:
    - usbipd list
    - usbipd bind --busid 2-6
    - (admin) usbipd attach --busid 2-6 --wsl
6. Run the elevator project:  `ros2 launch elevator_proj launch_elevator_proj.py`
7. Run the test node: `ros2 run elevator_proj test_node`

Commands:
- hn = Happy Normal
- sn = Sad Normal
- hw = Happy Weird
- sw = Sad Weird