import os
import platform
import time
import sqlite3
from gpiozero import CPUTemperature
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
from email_sender import send_initial_email
from matplotlib import pyplot as plt

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('cpu_temp_monitoring.log', mode='a')
log_format = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] [%(pathname)s:%(lineno)d] - %(message)s - '
                                '[%(process)d:%(thread)d]')
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

def clear_console():
    """Clear the console screen based on the platform (Windows/Linux)."""
    command = 'cls' if platform.system().lower() == 'windows' else 'clear'
    os.system(command)

def create_table(conn, table_name):
    """Create a new table in the database if it doesn't exist."""
    with conn:
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                            Timestamp TEXT PRIMARY KEY,
                            Temperature REAL
                        )''')

def log_cpu_temperature(db_file, log_interval, max_temp_threshold):
    """Log CPU temperature data into an SQLite3 database and send an email if it exceeds the threshold."""
    logger.info("Logging CPU temperature data.")

    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_file)

    while True:
        cpu = CPUTemperature()
        current_time = datetime.now().isoformat()

        # Get the current year and week number
        current_year = datetime.now().strftime('%Y')
        current_week = datetime.now().strftime('%U')

        # Ensure the table for the current year and week exists
        table_name = f'temps_{current_year}_W{current_week}'
        create_table(conn, table_name)

        # Insert data into the current week's table
        with conn:
            cursor = conn.cursor()
            cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?)', (current_time, cpu.temperature))

        # Remove old tables (older than one year)
        one_year_ago = datetime.now() - relativedelta(years=1)
        with conn:
            cursor = conn.cursor()
            tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            old_tables = [table[0] for table in tables if table[0].startswith('temps_') and
                          datetime.strptime(table[0].split('_')[1], '%Y') < one_year_ago]
            for old_table in old_tables:
                cursor.execute(f'DROP TABLE {old_table}')

        # Print temperature information and log if it exceeds the threshold
        print(f"Timestamp: {current_time}, Temperature: {cpu.temperature} °C")
        logger.info(f"Timestamp: {current_time}, Temperature: {cpu.temperature} °C")

        if cpu.temperature > max_temp_threshold:
            print("High CPU Temperature Alert!")
            logger.warning("High CPU Temperature Alert!")
            send_email_alert(current_time, cpu.temperature)

        print(f"Next temperature check in {log_interval} seconds.")
        time.sleep(log_interval)



def visualize_cpu_temperature(db_file, plot_file):
    """Visualize CPU temperature data from the database and generate a plot."""
    logger.info("Visualizing CPU temperature data.")

    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_file)

    timestamps = []
    temperatures = []

    # Fetch data from the current week's table
    current_week = datetime.now().strftime('%Y_W%U')
    table_name = f'temps_{current_week}'

    with conn:
        cursor = conn.cursor()
        data = cursor.execute(f'SELECT * FROM {table_name}').fetchall()

    for row in data:
        timestamp, cpu_temp = row
        timestamps.append(timestamp)
        temperatures.append(float(cpu_temp))

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, temperatures, label='CPU Temperature (°C)', color='b')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°C)')
    plt.title('Raspberry Pi CPU Temperature')

    # Adjust tick_spacing based on the number of data points.
    tick_spacing = max(1, len(timestamps) // 50)  # At most 50 ticks
    plt.xticks(timestamps[::tick_spacing], rotation=45)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.close()

def send_email_alert(timestamp, temperature):
    """Send an email alert if the CPU temperature exceeds the threshold."""
    subject = "CPU Temperature Alert"
    text = f"High CPU Temperature Alert!\n\nTimestamp: {timestamp}\nTemperature: {temperature} °C"
    to = ['your_email@example.com']  # Replace with recipient's email address
    files = ['cpu_temp_plot.png']
    send_initial_email(subject, text, to, files)  # Using send_initial_email instead of send_email
