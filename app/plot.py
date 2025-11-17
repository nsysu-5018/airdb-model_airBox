import matplotlib.pyplot  as plt
import matplotlib.dates as mdates
from datetime import datetime
from constants import record_time_key

def plot_simple_metric(ax, data, value_key, title, fill_color):
    """
    Plot a simple time-series metric with filled area and line.
    
    Args:
        ax: matplotlib axis object
        data: list of dictionaries containing the data
        value_key: key for the value field in data dictionaries
        title: title for the plot
        fill_color: color for the filled area
    """
    times = []
    values = []

    for record in data:
        try:
            time = datetime.strptime(record[record_time_key], '%Y-%m-%d %H:%M')
            value = float(record[value_key])
            times.append(time)
            values.append(value)
        except (TypeError, ValueError) as e:
            print(f"Error processing record: {record}")

    # Sort by time
    sorted_data = sorted(zip(times, values), key=lambda x: x[0])
    times, values = zip(*sorted_data)

    # Plot the filled area
    ax.fill_between(times, values, alpha=0.7, color=fill_color, 
                     edgecolor=fill_color, linewidth=2)

    # Add line on top
    ax.plot(times, values, color='#2183b3', linewidth=2)

    ax.set_title(title, fontsize=14, loc='left')

    # Format x-axis to show dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_ha('center')

def plot_total(pollution_data, temperature_data, humidity_data):
    fig = plt.figure(figsize=(18, 6))
        # --- AXES LAYOUT ---
    ax1 = fig.add_subplot(2, 1, 1)       # full-width top row
    ax2 = fig.add_subplot(2, 2, 3)       # bottom-left
    ax3 = fig.add_subplot(2, 2, 4)

    ###    pm2.5
    # Parse the data
    times = []
    pm25_values = []

    for record in pollution_data:
        try:
            time = datetime.strptime(record[record_time_key], '%Y-%m-%d %H:%M')
            pm25 = float(record['pm2.5'])
            times.append(time)
            pm25_values.append(pm25)
        except (TypeError, ValueError) as e:
            print(record)

    # Sort by time
    sorted_data = sorted(zip(times, pm25_values))
    times, pm25_values = zip(*sorted_data)

    # Fill areas based on PM2.5 levels (Taiwan AQI standards)
    # Good: 0-15.4 (green)
    # Moderate: 15.5-35.4 (yellow)
    # Unhealthy for Sensitive: 35.5-54.4 (orange)
    # Unhealthy: 54.5+ (red)

    ax1.fill_between(times, 0, pm25_values, 
                    color='#00ff01', alpha=0.8, interpolate=True)

    ax1.fill_between(times, 15, pm25_values,
                    where=[v > 15 for v in pm25_values],
                    color='#fed700', alpha=1, interpolate=True)

    ax1.fill_between(times, 35, pm25_values,
                    where=[v > 35 for v in pm25_values],
                    color='#ff9835', alpha=1, interpolate=True)

    ax1.fill_between(times, 55, pm25_values,
                    where=[v > 55 for v in pm25_values],
                    color='#ca0034', alpha=1, interpolate=True)

    # Plot the line
    ax1.plot(times, pm25_values, color='darkblue', linewidth=1.5)

    # Add reference lines
    ax1.axhline(y=15, color='black', linestyle='--', linewidth=1)
    ax1.axhline(y=35, color='black', linestyle='--', linewidth=1)

    # Format x-axis
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=0)

    # Labels and title
    ax1.set_title('PM2.5', fontsize=12, loc='left')
    ax1.set_ylim(0, max(pm25_values) * 1.1)

    ## Temperature
    plot_simple_metric(ax2, temperature_data, 'temperature', 'Temperature', '#ffc866')

    ### Humidity
    plot_simple_metric(ax3, humidity_data, 'humidity', 'Humidity', '#7acfce')

    plt.tight_layout()
    plt.savefig('fig_one.jpg', bbox_inches='tight', dpi=300)
    plt.close()