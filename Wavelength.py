#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
import matplotlib.pyplot as plt

file_path = r"Z:\DATA\Soil Moisture.csv"  
df = pd.read_csv(file_path, index_col=0)

numeric_df = df.select_dtypes(include=["number"])

numeric_columns = [col for col in numeric_df.columns if col.isdigit()] 

numeric_df = numeric_df[numeric_columns]

ranges = {
    'Red': (626, 740),    # Red: 626-740 nm
    'Orange': (591, 625), # Orange: 591-625 nm
    'Yellow': (566, 590), # Yellow: 566-590 nm
    'Green': (501, 565),  # Green: 501-565 nm
    'Blue': (450, 500)    # Blue: 450-500 nm
}

color_map = {
    'Red': 'red',
    'Orange': 'orange',
    'Yellow': 'yellow',
    'Green': 'green',
    'Blue': 'blue'
}

mean_std = {}

for label, (min_wavelength, max_wavelength) in ranges.items():
    # Filter the columns that fall within the wavelength range
    band_columns = [col for col in numeric_df.columns if min_wavelength <= int(col) <= max_wavelength]
    
    # Check if there are columns in the range
    if not band_columns:
        print(f"No bands found in the {label} range ({min_wavelength}-{max_wavelength} nm).")
        mean_std[label] = {'Mean': None, 'Standard Deviation': None}
    else:
        # Calculate mean and standard deviation for the selected columns
        mean_std[label] = {
            'Mean': numeric_df[band_columns].mean().mean(),  # Mean of all selected bands
            'Standard Deviation': numeric_df[band_columns].std().mean()  # Std of all selected bands
        }

results = pd.DataFrame(mean_std).T  # Transpose to get the labels as rows

results = results.fillna(value=float('nan'))

plt.figure(figsize=(12, 6))  

bars = plt.bar(results.index, results["Mean"], yerr=results["Standard Deviation"], capsize=5, 
               color=[color_map[label] for label in results.index], edgecolor='black')

results_cleaned = results.dropna()

plt.xticks(rotation=0)  # Rotate x-axis labels for better visibility
plt.xlabel("Wavelength Range (nm)", fontsize=12)
plt.ylabel("Mean ± Standard Deviation", fontsize=12)
plt.title("Descriptive Statistics: Mean with Standard Deviation Error Bars (Hyperspectral Ranges)", fontsize=14)
plt.tight_layout()  # Adjust layout to prevent clipping

plt.show()

print(results_cleaned)

