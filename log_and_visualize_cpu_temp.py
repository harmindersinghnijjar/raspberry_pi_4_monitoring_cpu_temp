import time
import csv
from gpiozero import CPUTemperature
from datetime import datetime
import matplotlib.pyplot as plt

# Start logging process
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a handler that writes log messages to a file
file_handler = logging.FileHandler('cpu_temp_monitoring.log', mode='a')
log_format = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] [%(pathname)s:%(lineno)d] - %(message)s - '
                               '[%(process)d:%(thread)d]')
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

# Create a handler that writes log messages to the console
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

# Function to clear the console
def clear_console():
    # Identify the OS and clear the console accordingly
    command = 'cls' if platform.system().lower() == 'windows' else 'clear'
    os.system(command)

# Function to log CPU temperature
def log_cpu_temperature(logfile, interval):
    """
    Continuously logs the CPU temperature to a CSV file.

    Args:
        logfile (str): The name of the file to store the log.
        interval (int): Time interval in seconds between temperature logs.
    """
    logger.info("Starting CPU temperature logging.")
    with open(logfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Temperature (°C)"])

        try:
            while True:
                cpu = CPUTemperature()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cpu_temp = cpu.temperature
                writer.writerow([timestamp, cpu_temp])
                f.flush()
                logger.info(f"Logged CPU temperature: {timestamp}, {cpu_temp:.2f} °C")

                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("CPU temperature logging stopped.")

# Function to visualize CPU temperature
def visualize_cpu_temperature(logfile):
    """
    Visualizes the CPU temperature data from the CSV log file.

    Args:
        logfile (str): The name of the file containing CPU temperature data.
    """
    logger.info("Visualizing CPU temperature data.")
    timestamps = []
    temperatures = []

    with open(logfile, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            timestamp, cpu_temp = row
            timestamps.append(timestamp)
            temperatures.append(float(cpu_temp))

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, temperatures, label='CPU Temperature (°C)', color='b')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°C)')
    plt.title('Raspberry Pi CPU Temperature')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('cpu_temp_plot.png')
    plt.show()

if __name__ == "__main__":
    log_file = "cpu_temp_log.csv"
    log_interval = 5  # Log temperature every 5 seconds (you can adjust this interval)

    try:
        log_cpu_temperature(log_file, log_interval)
    except KeyboardInterrupt:
        pass  # Exit gracefully on Ctrl+C

    visualize_cpu_temperature(log_file)
