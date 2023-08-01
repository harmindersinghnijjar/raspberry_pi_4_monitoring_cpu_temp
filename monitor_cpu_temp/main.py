from cpu_temp_monitor import log_cpu_temperature, visualize_cpu_temperature

db_file = 'cpu_temp_data.db'
plot_file = 'cpu_temp_plot.png'
log_interval = 60  # Log every 60 seconds
max_temp_threshold = 80  # Maximum allowed CPU temperature

try:
    log_cpu_temperature(db_file, log_interval, max_temp_threshold)
except KeyboardInterrupt:
    print("Logging stopped by user.")

visualize_cpu_temperature(db_file, plot_file)
