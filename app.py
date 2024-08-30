import platform
import os
import socket
import psutil
import subprocess

# Finding the OS information
def os_info():
    os_name = platform.system()
    os_version = platform.version()

    print(f"OS Name: {os_name}")
    print(f"OS Version: {os_version}")

# Finding computer information using socket and subprocess libraries
def computer_info():
    hostname = socket.gethostname()
    private_ip = socket.gethostbyname(hostname)

    try:
        public_ip = subprocess.getoutput("curl -s ifconfig.me")
        if platform.system() == 'Windows':
            gateway = subprocess.getoutput("ipconfig | findstr /i \"Gateway\"")
        else:
            gateway = subprocess.getoutput("ip route | grep default | awk '{print $3}'")
    except Exception as e:
        public_ip = f"Error occurred during fetching public IP: {e}"
        gateway = f"Error occurred during fetching gateway: {e}"

    print(f"\nHostname: {hostname}")
    print(f"Private IP: {private_ip}")
    print(f"Public IP: {public_ip}")
    print(f"Default Gateway: {gateway}")

#cpu temperature function
# import platform

def cpu_temperature():
    system = platform.system()
    
    if system == 'Linux':
        try:
            temp_file = '/sys/class/thermal/thermal_zone0/temp'
            with open(temp_file, 'r') as f:
                temp = int(f.read().strip()) / 1000
                print(f"CPU Temperature: {temp:.2f} C")
        except FileNotFoundError:
            print("Temperature information not available.")
        except Exception as e:
            print(f"Error retrieving CPU temperature: {e}")
    
    elif system == 'Windows':
        try:
            import wmi
            c = wmi.WMI()
            temperature_found = False
            for sensor in c.Win32_TemperatureProbe():
                if sensor.CurrentReading is not None:
                    print(f"CPU Temperature: {sensor.CurrentReading / 10.0} C")
                    temperature_found = True
            if not temperature_found:
                print("Temperature information not available or unsupported.")
        except ImportError:
            print("wmi module not found. Please install it using 'pip install WMI'.")
        except Exception as e:
            print(f"Error retrieving CPU temperature: {e}")
    
    elif system == 'Darwin':  # macOS
        try:
            import subprocess
            result = subprocess.run(['system_profiler', 'SPHardwareDataType'], capture_output=True, text=True)
            output = result.stdout
            temperature_found = False
            for line in output.splitlines():
                if 'Temperature' in line:
                    print(line)
                    temperature_found = True
            if not temperature_found:
                print("\nTemperature information not available.")
        except Exception as e:
            print(f"Error retrieving CPU temperature: {e}")
    
    else:
        print("Unsupported platform for temperature retrieval.")


#function to display current user
def user_info():
    user = os.getlogin()
    print(f"Current User: {user}")
    print(f"System: {platform.node()}\n")


# Finding disk information using psutil library
def disk_info():
    disk_usage = psutil.disk_usage('/')
    total_space = disk_usage.total / (1024**3)  # Total disk space
    free_space = disk_usage.free / (1024**3)    # Free disk space
    used_space = disk_usage.used / (1024**3)    # Used disk space

    print(f"\nTotal Disk Size: {total_space:.2f} GB")
    print(f"Used Disk Space: {used_space:.2f} GB")
    print(f"Free Disk Space: {free_space:.2f} GB")

# Finding the largest directories in the specified path


# ! WARNING! MY WINDOWS CONTAINS MANY FOLDERS AND FILES (also node modules for my projects), THAT'S WHY I COMMENTED SCANNING DIRECTORY PRINT FUNCTION
def largest_directories(path, n=5):
    directories = []
    for dirpath, dirnames, files in os.walk(path):
        total_size = 0
        for f in files:
            fp = os.path.join(dirpath, f)
            try:
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
            except (FileNotFoundError, PermissionError) as e:
                print(f"Skipping file {fp}: {e}")  # Debug line
                continue
        directories.append((dirpath, total_size))
    
    # Sort directories by total size in descending order
    directories.sort(key=lambda x: x[1], reverse=True)
    
    # Get the top n largest directories
    largest_dirs = directories[:n]
    
    print(f"\n{n} Largest Directories by Size:")
    for dirpath, size in largest_dirs:
        print(f"{dirpath}: {size / (1024**3):.2f} GB")

# Function to parse the auth.log file for command usage
def auth_log_info(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if 'COMMAND=' in line:
                    parts = line.split()
                    timestamp = ' '.join(parts[0:3])
                    user_part = parts[9] if len(parts) > 9 else "USER=unknown"
                    user = user_part.split('=')[1]
                    command_index = line.find('COMMAND=') + len('COMMAND=')
                    command = line[command_index:].strip()
                    print(f"Timestamp: {timestamp}, User: {user}, Command: {command}")
    except FileNotFoundError:
        print(f"Log file not found: {file_path}")

# Monitoring and printing the CPU usage every ten seconds until interrupted
def cpu_usage_info(interval=10):
    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=interval)
            print(f"CPU Usage: {cpu_usage} %")
    except KeyboardInterrupt:
        print("CPU checkment Disabled")

log_file_path = '/var/log/auth.log'
# Main function to call all functions
def main():
    cpu_temperature()
    os_info()
    computer_info()
    disk_info()
    user_info()


    auth_log_info(log_file_path)
    
    # Define the root path based on OS
    print(f"\nFinding Largest Directories. Please Wait!🔎")  # Debug line
    if platform.system() == 'Windows':
        path = os.path.abspath('C:\\')  # you can put the path to the directory you want
    else:
        path = os.path.abspath('/')  # Root for Unix-like systems
    
    largest_directories(path, 5)
    print("\n CPU Statistics:")
    cpu_usage_info()

if __name__ == "__main__":
    main()
