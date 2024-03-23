#code by: Vasco Morais 100278

import numpy as np

from functions import read_constants, export_data_to_txt, plot_temperature_data, \
    euler_explicit_iteration, convert_theta_to_temperature, export_time_reached_80


# IF YOU WANT TO TEST THE THEORETICAL CASE JUST PUT As_r = 0;

def main():
    # Define constants
    constants = read_constants("constants.txt")
    T_i, T_inf, h, rho, c, eps, sigma = (constants[key] for key in ['T_i', 'T_inf', 'h', 'rho', 'c', 'eps', 'sigma'])

    r0 = 0.05  # radius of the potato - change according to the potato
    As_c = 4 * np.pi * r0 ** 2  # Surface area exposed to conv [m^2]
    As_r = 4 * np.pi * r0 ** 2  # Surface area exposed to rad [m^2]; To try analytical solution just put As_r = 0;
    vol = (4 / 3) * np.pi * r0 ** 3  # Sphere volume [m^3]

    # Calculate theta0 using the initial condition
    theta_initial = (T_i - T_inf)

    # Create lists to store theta and time values
    theta_values = [theta_initial]
    time_values = [0.0]  # Initialize time at t = 0

    # Perform the Euler explicit method iteration using a while loop
    max_time = 3600
    time_steps = [600, 100, 10, 1, 0.1, 0.01]

    data_for_time_steps = []
    time_reached_80_values = []  # Store time values when temperature reaches 80°C

    for step in time_steps:
        # Perform the Euler explicit method iteration for each time step

        time_values, theta_values, time_reached_80 = euler_explicit_iteration(
            T_inf, step, max_time, theta_initial, eps, sigma, h, As_c, As_r, rho, vol, c)

        # Convert theta values to temperature values
        temperature_values = convert_theta_to_temperature(theta_values, T_inf)

        # Append the time and temperature data for this time step to the list
        data_for_time_steps.append((time_values, temperature_values))
        # Store the time when temperature reaches 80°C
        time_reached_80_values.append(time_reached_80)

    # Export each pair of data to a separate text file
    for index, (time_values, temperature_values) in enumerate(data_for_time_steps):
        file_name = f"temperature_data{index + 1}.txt"
        export_data_to_txt(file_name, [(time_values, temperature_values)])

    # Export times when temperature reached 80°C to a separate text file
    reached_80_file_name = "time_reached_80.txt"
    export_time_reached_80(reached_80_file_name, time_steps, time_reached_80_values)

    # Plot temperature data
    plot_temperature_data(data_for_time_steps, time_steps)


if __name__ == "__main__":
    main()
