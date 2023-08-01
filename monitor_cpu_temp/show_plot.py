import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

def visualize_cpu_temperature(db_file, plot_file):
    """Visualize CPU temperature data from the database and generate a plot."""
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
    plt.show()

if __name__ == "__main__":
    db_file = 'cpu_temp_data.db'
    plot_file = 'cpu_temp_plot.png'
    visualize_cpu_temperature(db_file, plot_file)

