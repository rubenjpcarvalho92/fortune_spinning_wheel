import random
import pandas as pd

# Define the intervals and corresponding outputs stable

intervals_stable = [
    (1, 18750, "P1", 500),
    (18751, 65625, "P2", 200),
    (65626, 159375, "P3", 100),
    (159376, 346875, "P4", 50),
    (346876, 815625, "P5", 20),
    (815626, 1753125, "P6", 10),
    (1753126, 3628125, "P7", 5),
    (3628126, 8315625, "P8", 2)
]

# P8 metade P1 dobro

intervals_inicial = [
    (1, 9375, "P1", 500),
    (18751, 65625, "P2", 200),
    (65626, 159375, "P3", 100),
    (159376, 346875, "P4", 50),
    (346876, 815625, "P5", 20),
    (815626, 1753125, "P6", 10),
    (1753126, 3628125, "P7", 5),
    (3628126, 13003125, "P8", 2)
]



# Initialize variables
iteration = 0
total_sum = 0
data = []

# Generate 200,000 numbers
for _ in range(10000):
    iteration += 1
    number = random.randint(1, 100000000)
    output = "P0"
    value = 0

    if iteration <1000:
        intervals = intervals_inicial
        #while number < 18750:
            #number = random.randint(1, 100000000)
    else:
        intervals = intervals_inicial


    for start, end, out, val in intervals:
        if start <= number <= end:
            output = out
            value = val
            break

    total_sum += value

    # Append the data for this iteration
    data.append([iteration, number, output, value, total_sum])

# Create a DataFrame
columns = ["Iteration", "Random Number", "Output", "Value", "Cumulative Sum"]
df = pd.DataFrame(data, columns=columns)

# Save to an Excel file
df.to_excel("random_numbers_output_equilibrado_run1.xlsx", index=False)


print("Data generation complete. File saved as 'random_numbers_output_equilibrado_run1.xlsx'.")


# Initialize variables
iteration = 0
total_sum = 0
data = []

# Generate 200,000 numbers
for _ in range(10000):
    iteration += 1
    number = random.randint(1, 100000000)
    output = "P0"
    value = 0

    if iteration <1000:
        intervals = intervals_inicial
        #while number < 18750:
            #number = random.randint(1, 100000000)
    else:
        intervals = intervals_inicial


    for start, end, out, val in intervals:
        if start <= number <= end:
            output = out
            value = val
            break

    total_sum += value

    # Append the data for this iteration
    data.append([iteration, number, output, value, total_sum])

# Create a DataFrame
columns = ["Iteration", "Random Number", "Output", "Value", "Cumulative Sum"]
df = pd.DataFrame(data, columns=columns)

# Save to an Excel file
df.to_excel("random_numbers_output_equilibrado_run2.xlsx", index=False)


print("Data generation complete. File saved as 'random_numbers_output_equilibrado_run2.xlsx'.")

# Initialize variables
iteration = 0
total_sum = 0
data = []

# Generate 200,000 numbers
for _ in range(10000):
    iteration += 1
    number = random.randint(1, 100000000)
    output = "P0"
    value = 0

    if iteration <1000:
        intervals = intervals_inicial
        #while number < 18750:
            #number = random.randint(1, 100000000)
    else:
        intervals = intervals_inicial


    for start, end, out, val in intervals:
        if start <= number <= end:
            output = out
            value = val
            break

    total_sum += value

    # Append the data for this iteration
    data.append([iteration, number, output, value, total_sum])

# Create a DataFrame
columns = ["Iteration", "Random Number", "Output", "Value", "Cumulative Sum"]
df = pd.DataFrame(data, columns=columns)

# Save to an Excel file
df.to_excel("random_numbers_output_equilibrado_run3.xlsx", index=False)

print("Data generation complete. File saved as 'random_numbers_output_equilibrado_run3.xlsx'.")

# Initialize variables
iteration = 0
total_sum = 0
data = []

# Generate 200,000 numbers
for _ in range(10000):
    iteration += 1
    number = random.randint(1, 100000000)
    output = "P0"
    value = 0

    if iteration <1000:
        intervals = intervals_inicial
        #while number < 18750:
            #number = random.randint(1, 100000000)
    else:
        intervals = intervals_inicial


    for start, end, out, val in intervals:
        if start <= number <= end:
            output = out
            value = val
            break

    total_sum += value

    # Append the data for this iteration
    data.append([iteration, number, output, value, total_sum])

# Create a DataFrame
columns = ["Iteration", "Random Number", "Output", "Value", "Cumulative Sum"]
df = pd.DataFrame(data, columns=columns)

# Save to an Excel file
df.to_excel("random_numbers_output_equilibrado_run4.xlsx", index=False)


print("Data generation complete. File saved as 'random_numbers_output_equilibrado_run4.xlsx'.")

# Initialize variables
iteration = 0
total_sum = 0
data = []

# Generate 200,000 numbers
for _ in range(10000):
    iteration += 1
    number = random.randint(1, 100000000)
    output = "P0"
    value = 0

    if iteration <1000:
        intervals = intervals_inicial
        #while number < 18750:
            #number = random.randint(1, 100000000)
    else:
        intervals = intervals_inicial


    for start, end, out, val in intervals:
        if start <= number <= end:
            output = out
            value = val
            break

    total_sum += value

    # Append the data for this iteration
    data.append([iteration, number, output, value, total_sum])

# Create a DataFrame
columns = ["Iteration", "Random Number", "Output", "Value", "Cumulative Sum"]
df = pd.DataFrame(data, columns=columns)

# Save to an Excel file
df.to_excel("random_numbers_output_equilibrado_run5.xlsx", index=False)


print("Data generation complete. File saved as 'random_numbers_output_equilibrado_run5.xlsx'.")

# Initialize variables
iteration = 0
total_sum = 0
data = []

# Generate 200,000 numbers
for _ in range(10000):
    iteration += 1
    number = random.randint(1, 100000000)
    output = "P0"
    value = 0

    if iteration <1000:
        intervals = intervals_inicial
        #while number < 18750:
            #number = random.randint(1, 100000000)
    else:
        intervals = intervals_inicial


    for start, end, out, val in intervals:
        if start <= number <= end:
            output = out
            value = val
            break

    total_sum += value

    # Append the data for this iteration
    data.append([iteration, number, output, value, total_sum])

# Create a DataFrame
columns = ["Iteration", "Random Number", "Output", "Value", "Cumulative Sum"]
df = pd.DataFrame(data, columns=columns)

# Save to an Excel file
df.to_excel("random_numbers_output_equilibrado_run6.xlsx", index=False)


print("Data generation complete. File saved as 'random_numbers_output_equilibrado_run6.xlsx'.")

# Initialize variables
iteration = 0
total_sum = 0
data = []

# Generate 200,000 numbers
for _ in range(10000):
    iteration += 1
    number = random.randint(1, 100000000)
    output = "P0"
    value = 0

    if iteration <1000:
        intervals = intervals_inicial
        #while number < 18750:
            #number = random.randint(1, 100000000)
    else:
        intervals = intervals_inicial


    for start, end, out, val in intervals:
        if start <= number <= end:
            output = out
            value = val
            break

    total_sum += value

    # Append the data for this iteration
    data.append([iteration, number, output, value, total_sum])

# Create a DataFrame
columns = ["Iteration", "Random Number", "Output", "Value", "Cumulative Sum"]
df = pd.DataFrame(data, columns=columns)

# Save to an Excel file
df.to_excel("random_numbers_output_equilibrado_run7.xlsx", index=False)


print("Data generation complete. File saved as 'random_numbers_output_equilibrado_run7.xlsx'.")

# Initialize variables
iteration = 0
total_sum = 0
data = []

# Generate 200,000 numbers
for _ in range(10000):
    iteration += 1
    number = random.randint(1, 100000000)
    output = "P0"
    value = 0

    if iteration <1000:
        intervals = intervals_inicial
        #while number < 18750:
            #number = random.randint(1, 100000000)
    else:
        intervals = intervals_inicial


    for start, end, out, val in intervals:
        if start <= number <= end:
            output = out
            value = val
            break

    total_sum += value

    # Append the data for this iteration
    data.append([iteration, number, output, value, total_sum])

# Create a DataFrame
columns = ["Iteration", "Random Number", "Output", "Value", "Cumulative Sum"]
df = pd.DataFrame(data, columns=columns)

# Save to an Excel file
df.to_excel("random_numbers_output_equilibrado_run8.xlsx", index=False)


print("Data generation complete. File saved as 'random_numbers_output_equilibrado_run8.xlsx'.")

# Initialize variables
iteration = 0
total_sum = 0
data = []

# Generate 200,000 numbers
for _ in range(10000):
    iteration += 1
    number = random.randint(1, 100000000)
    output = "P0"
    value = 0

    if iteration <1000:
        intervals = intervals_inicial
        #while number < 18750:
            #number = random.randint(1, 100000000)
    else:
        intervals = intervals_inicial


    for start, end, out, val in intervals:
        if start <= number <= end:
            output = out
            value = val
            break

    total_sum += value

    # Append the data for this iteration
    data.append([iteration, number, output, value, total_sum])

# Create a DataFrame
columns = ["Iteration", "Random Number", "Output", "Value", "Cumulative Sum"]
df = pd.DataFrame(data, columns=columns)

# Save to an Excel file
df.to_excel("random_numbers_output_equilibrado_run9.xlsx", index=False)


print("Data generation complete. File saved as 'random_numbers_output_equilibrado_run9.xlsx'.")
# Initialize variables
iteration = 0
total_sum = 0
data = []

# Generate 200,000 numbers
for _ in range(10000):
    iteration += 1
    number = random.randint(1, 100000000)
    output = "P0"
    value = 0

    if iteration <1000:
        intervals = intervals_inicial
        #while number < 18750:
            #number = random.randint(1, 100000000)
    else:
        intervals = intervals_inicial


    for start, end, out, val in intervals:
        if start <= number <= end:
            output = out
            value = val
            break

    total_sum += value

    # Append the data for this iteration
    data.append([iteration, number, output, value, total_sum])

# Create a DataFrame
columns = ["Iteration", "Random Number", "Output", "Value", "Cumulative Sum"]
df = pd.DataFrame(data, columns=columns)

# Save to an Excel file
df.to_excel("random_numbers_output_equilibrado_run10.xlsx", index=False)


print("Data generation complete. File saved as 'random_numbers_output_equilibrado_run10.xlsx'.")
