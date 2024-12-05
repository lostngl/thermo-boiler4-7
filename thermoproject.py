#4) Performing a mass and energy balance to calculate the mass flow rate
#of water through the bypass pipe, in kg/min and lb/min, for each row in your data.

import pandas as pd
from CoolProp.CoolProp import PropsSI

# Load your dataset
data = pd.read_csv('data.csv')  # Replace with your file path

# Convert temperatures from Fahrenheit to Kelvin for CoolProp
data['PHWR Temp (K)'] = (data['PHWR Temp (°F)'] - 32) * 5/9 + 273.15
data['SHWS Temp (K)'] = (data['SHWS Temp (°F)'] - 32) * 5/9 + 273.15

# Calculate density of water using CoolProp at PHWR temperatures
data['Density (kg/m³)'] = data['PHWR Temp (K)'].apply(lambda T: PropsSI('D', 'T', T, 'P', 101325, 'Water'))

# Convert volumetric flow rates (gpm) to mass flow rates (kg/min)
data['Primary Mass Flow (kg/min)'] = data['Density (kg/m³)'] * data['SHWS Flow (gpm)'] * 0.00378541

# Calculate bypass mass flow using percentage (example assumption: 10% bypass)
bypass_percentage = 0.1  # Assume 10% of the primary flow bypasses the SHWS loop
data['Bypass Mass Flow (kg/min)'] = data['Primary Mass Flow (kg/min)'] * bypass_percentage

# Convert bypass mass flow rate from kg/min to lb/min
data['Bypass Mass Flow (lb/min)'] = data['Bypass Mass Flow (kg/min)'] * 2.20462

# Save the updated DataFrame back to the same file
data.to_csv('data.csv', index=False)

# Print a confirmation message
print("New headers and values added to data.csv successfully!")
#--------------------------------------------------------------------------------------------

#5) Calculate the mass flow rate of water through the primary loop (PHWR), in kg/min and
#  lb/min, for each row in your data.


import pandas as pd
from CoolProp.CoolProp import PropsSI

# Load your dataset
data = pd.read_csv('data.csv')

# Convert PHWR Temp from Fahrenheit to Kelvin for CoolProp
data['PHWR Temp (K)'] = (data['PHWR Temp (°F)'] - 32) * 5/9 + 273.15

# Calculate density of water at PHWR temperature using CoolProp
data['Density (kg/m³)'] = data['PHWR Temp (K)'].apply(lambda T: PropsSI('D', 'T', T, 'P', 101325, 'Water'))

# Calculate volumetric flow rate in m³/min
data['PHWR Volumetric Flow (m³/min)'] = data['SHWS Flow (gpm)'] * 0.00378541

# Calculate mass flow rate in kg/min
data['Primary Mass Flow (kg/min)'] = data['Density (kg/m³)'] * data['PHWR Volumetric Flow (m³/min)']

# Convert mass flow rate to lb/min
data['Primary Mass Flow (lb/min)'] = data['Primary Mass Flow (kg/min)'] * 2.20462

# Save the updated DataFrame back to the same file
data.to_csv('data.csv', index=False)

# Print a confirmation message
print("New titles and values have been successfully added to data.csv!")

#-----------------------------------------------------------------------------------------------

#6) Calculate the percentage of water flowing through the “common pipe (aka bypass)”, by
#obtaining the ratio of mass flowrate through the bypass divided by mass flowrate through
#the primary loop, in %. Plot this percentage vs date/time for each of the rows in the data
#assigned to you. Calculate the average value of the percentage of water flowing through
#the common pipe for the entire period of performance assigned to your group.

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('data.csv')

# Recalculate the percentage of water flowing through the common pipe
data['Bypass Percentage (%)'] = (data['Bypass Mass Flow (kg/min)'] / data['Primary Mass Flow (kg/min)']) * 100

# Check for any NaN or infinite values and handle them
data['Bypass Percentage (%)'].fillna(0, inplace=True)  # Replace NaN with 0
data['Bypass Percentage (%)'] = data['Bypass Percentage (%)'].replace([float('inf'), -float('inf')], 0)  # Replace infinities

# Calculate the average bypass percentage
average_bypass_percentage = data['Bypass Percentage (%)'].mean()

# Print the average bypass percentage
print(f"Average Percentage of Water Flowing Through Common Pipe: {average_bypass_percentage:.2f}%")

# Plot the percentage of water flowing through the common pipe vs. time
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Bypass Percentage (%)'], label='Bypass Percentage (%)', color='blue')

# Add a horizontal line for the average bypass percentage
plt.axhline(y=average_bypass_percentage, color='red', linestyle='--', label=f'Average: {average_bypass_percentage:.2f}%')

# Improve x-axis formatting
plt.title('Percentage of Water Flowing Through the Common Pipe Over Time')
plt.xlabel('Date')
plt.ylabel('Bypass Percentage (%)')
plt.xticks(ticks=range(0, len(data['Date']), max(1, len(data['Date']) // 10)), rotation=45)  # Show fewer x-axis labels
plt.legend()
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()

# Save the updated data with the Bypass Percentage column back to the file
data.to_csv('data.csv', index=False)
print("Bypass Percentage added to data.csv successfully!")

#------------------------------------------------------------------------------------------------------------------

# 7)Calculate the percentage of water being delivered to campus by calculating the ratio of
# mass flowrate through the campus divided by mass flowrate through the primary loop, in
# %. Plot this percentage vs date/time for each of the rows in the data assigned to you.
# Calculate the average value of the percentage of water flowing through the campus for
# the entire period of performance assigned to your group.

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('data.csv')

# Step 1: Calculate Campus Mass Flow (kg/min)
data['Campus Mass Flow (kg/min)'] = data['Primary Mass Flow (kg/min)'] - data['Bypass Mass Flow (kg/min)']

# Step 3: Calculate Campus Percentage (%)
data['Campus Percentage (%)'] = (data['Campus Mass Flow (kg/min)'] / data['Primary Mass Flow (kg/min)']) * 100

# Step 4: Handle any NaN or infinite values
data['Campus Percentage (%)'].fillna(0, inplace=True)  # Replace NaN with 0
data['Campus Percentage (%)'] = data['Campus Percentage (%)'].replace([float('inf'), -float('inf')], 0)  # Replace infinities

# Step 5: Calculate the average campus percentage
average_campus_percentage = data['Campus Percentage (%)'].mean()

# Print the average campus percentage
print(f"Average Percentage of Water Delivered to Campus: {average_campus_percentage:.2f}%")

# Step 6: Plot the campus percentage over time
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Campus Percentage (%)'], label='Campus Percentage (%)', color='blue')

# Add a horizontal line for the average campus percentage
plt.axhline(y=average_campus_percentage, color='red', linestyle='--', label=f'Average: {average_campus_percentage:.2f}%')

# Improve x-axis formatting
plt.title('Percentage of Water Delivered to Campus Over Time')
plt.xlabel('Date')
plt.ylabel('Campus Percentage (%)')
plt.xticks(ticks=range(0, len(data['Date']), max(1, len(data['Date']) // 10)), rotation=45)
plt.legend()
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()

# Step 7: Save the updated data with the Campus Percentage column back to the file
data.to_csv('data.csv', index=False)
print("Campus Percentage added to data.csv successfully!")








