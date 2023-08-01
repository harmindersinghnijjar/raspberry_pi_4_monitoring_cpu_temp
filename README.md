# Raspberry Pi CPU Monitoring

This project is a Python-based script designed for Raspberry Pi owners to effectively monitor their device's CPU usage in real-time. It provides real-time visuals, user-defined parameters, efficiency, and logging/alert functionality to help you keep track of your Raspberry Pi's performance.

## Motivation

Raspberry Pi's are powerful and versatile devices, but they can get hot under the collar when pushed to their limits. As users, we often require insights about our device's performance and system health. This project was born out of the need to effectively track, visualize, and log CPU usage and temperature over time.

## Features

- **Real-time visuals:** This script offers a convenient way to visualize your Raspberry Pi's performance. It provides graphs of the device's CPU usage frequency/time and bar/temperature visualizations in real-time.

- **User-defined parameters:** You can adjust the sampling frequency according to your needs, as well as the size of the window used to calculate the CPU's average usage.

- **Efficient:** The script stops monitoring automatically when the device is inactive (zero CPU usage) and can also be manually stopped or customized at any time.

- **Logging and alerts:** The script logs the CPU temperature into a SQLite database and also sends email alerts if the temperature exceeds a threshold.

## Installation

1. Install Python 3 if you haven't already.
2. Install the required packages using pip:
```
pip install gpiozero matplotlib
```

3. Download the script files from the [GitHub repository](https://github.com/harmindersinghnijjar/raspberry_pi_cpu_monitoring)
4. Execute the script in your preferred Python environment.

## Usage

1. Run the main script in your terminal:
```
python main.py
```

2. The script will start logging the CPU temperature data and display it in the console.
3. If the CPU temperature exceeds the threshold, an email alert will be sent.
4. Once the logging is complete, the script will generate a plot of the CPU temperature data.

## Code Organization

The code is organized into several modules:

- `main.py`: The entry point of the script that handles the logging and visualization of CPU temperature data.
- `cpu_temp_monitor.py`: Contains functions for logging CPU temperature data, creating tables in the SQLite database, and sending email alerts.
- `email_sender.py`: Handles the sending of initial and follow-up email alerts, along with necessary configurations.
- `show_plot.py`: Contains a function to visualize CPU temperature data from the database and generate a plot.

## Documentation

Additional information and instructions are available in the script files as comments.

## Code of Conduct

We welcome contributing and discussions, but please follow the guidelines listed in the [CODE_OF_CONDUCT.md](https://github.com/your-repository/blob/main/CODE_OF_CONDUCT.md) file to ensure a friendly and respectful environment.

## License

The script files are licensed under the MIT license. You are free to use, modify, and distribute the code, given that you abide by the terms presented in the [LICENSE](https://github.com/harmindersinghnijjar/raspberry_pi_cpu_monitoring/blob/main/LICENSE) file.

## Future Improvements

We're always open to suggestions and contributions. Some of the future improvements we're considering include:

- Expansion of the alert system to other communication channels such as SMS or push notifications.
- Addition of more detailed metrics, such as memory and disk usage.
- Creation of a web interface for remote monitoring and control.

## Who can use this

This script is aimed at Raspberry Pi enthusiasts, developers, system administrators, and any tech-savvy individuals interested in keeping an eye on their Pi's system health. Whether you are running a server, a home automation system, or a weather station, this tool can be useful to monitor and manage the performance of your Raspberry Pi.

## Maintainers

This project is currently maintained by [Harminder Singh Nijjar](https://www.linkedin.com/in/harmindersinghnijjar/). Feel free to reach out if you have any questions or suggestions.

## Acknowledgments

We'd like to express our gratitude to the open-source community for making projects like this possible. Your efforts inspire us to create and contribute back to the community.


