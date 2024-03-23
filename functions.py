#code by: Vasco Morais 100278

import matplotlib.pyplot as plt

def calculate_h_r(T, T_inf, eps, sigma):
    current_temperature = T
    h_r = eps * sigma * (current_temperature + T_inf) * (current_temperature ** 2 + T_inf ** 2)
    return h_r


def calculate_a(h, As_c, As_r, h_r, rho, vol, c):
    a = (h * As_c + As_r * h_r) / (rho * vol * c)
    return a


def read_constants(file_name):
    constants = {}
    with open(file_name, 'r') as file:
        lines = file.readlines()
        constants['T_i'] = float(lines[0].strip())
        constants['T_inf'] = float(lines[1].strip())
        constants['h'] = float(lines[2].strip())
        constants['rho'] = float(lines[3].strip())
        constants['c'] = float(lines[4].strip())
        constants['eps'] = float(lines[5].strip())
        constants['sigma'] = float(lines[6].strip())
    return constants


def export_data_to_txt(file_name, data_for_time_steps):
    for index, (time_values, temperature_values) in enumerate(data_for_time_steps):
        with open(f"{file_name}{index + 1}.txt", "w") as file:
            for i in range(len(time_values)):
                file.write(f"{time_values[i]}\t{temperature_values[i]}\n")

        print(f'Data exported to {file_name}{index + 1}')



def plot_temperature_data(data_for_time_steps, time_steps):
    colors = ['b', 'g', 'r', 'c', '0', 'orange']
    plt.figure(figsize=(8, 6))  # Adjust figure size if needed

    for i, (step, data) in enumerate(zip(time_steps, data_for_time_steps)):
        time_values, temperature_values = data
        plt.plot(time_values, temperature_values, label=f'Time Step = {step} s', color=colors[i])

    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature vs. Time')
    plt.axhline(y=80, color='red', linestyle='--', label='T = 80°C')  # Add the constant line
    plt.grid(True)
    plt.legend()
    plt.show()


def euler_explicit_iteration(T_inf, step, max_time, theta_initial,
                             eps, sigma, h, As_c, As_r, rho, vol, c):
    theta_values = [theta_initial]
    time_values = [0.0]  # Initialize time at t = 0
    time_reached_80 = None

    i = 0
    while i <= max_time:
        # Calculate the current temperature based on the current theta value
        current_temperature = theta_values[-1] + T_inf

        # Calculate h_r using the auxiliary function
        h_r = calculate_h_r(current_temperature, T_inf, eps, sigma)
        # print(f'h_r = {h_r}')

        # Calculate a using the auxiliary function
        a = calculate_a(h, As_c, As_r, h_r, rho, vol, c)

        # Calculate the next theta value
        next_theta = -a * theta_values[-1] * step + theta_values[-1]

        # Append the next theta value to the list
        theta_values.append(next_theta)

        # Increment time by delta_t (step)
        time_values.append(time_values[-1] + step)

        # Check if the temperature has reached 80
        if current_temperature > (80 + 273.15) and time_reached_80 is None:
            time_reached_80 = time_values[-1]

        i += step

    return time_values, theta_values, time_reached_80


def convert_theta_to_temperature(theta_values, T_inf):
    temperature_values = [theta + (T_inf - 273.15) for theta in theta_values]
    return temperature_values

def export_time_reached_80(file_name, time_steps, time_reached_80_values):
    with open(file_name, "w") as file:
        for step, time_reached_80 in zip(time_steps, time_reached_80_values):
            file.write(f"Time Step = {step} s: {time_reached_80} s\n")
    print(f'Data exported to {file_name}')
    print(f'Times when temperature reached 80°C exported to {file_name}')