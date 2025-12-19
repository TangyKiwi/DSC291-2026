# Plan: Lightning Notebook for TAVG PC1 Geographic Distribution

## Objective
Create a lightning notebook that visualizes the geographic distribution of the top eigenvector (PC1) coefficients from TAVG PCA analysis using Folium. The map displays:
- **Color**: Average value of PC1 coefficient per station
- **Circle size**: Number of years (measurements) per station

## Notebook Structure

### Cell 1: Introduction (Markdown)
- Brief explanation of what the notebook does
- Describe PC1 coefficients and their geographic interpretation

### Cell 2: Imports and Setup (Code)
- Import: `folium`, `dask.dataframe as dd`, `pandas as pd`, `numpy as np`, `pickle`, `Path`
- Define paths:
  - PCA results: `weather/weather_info/pca_results/tavg_pca_results.pkl`
  - Weather data: `weather_data/stations_weather_with_dist2coast_optimized.parquet` (or appropriate TAVG data source)
- Print confirmation message

### Cell 3: Load PCA Results (Code)
- Load TAVG PCA results from pickle file
- Extract PC1 component (first eigenvector)
- Print PC1 explained variance ratio
- Note: This gives us the PC1 component vector to project data onto

### Cell 4: Load TAVG Data (Code)
- Load weather parquet file using Dask
- Filter for TAVG element
- Select columns: `ID` (station), `latitude`, `longitude`, `year`, and daily columns (`day_1` through `day_365`)
- Compute sample to verify structure
- Print number of stations and years

### Cell 5: Compute PC1 Coefficients (Code)
- Extract daily data columns
- For each station-year record:
  - Subtract PCA mean from daily data
  - Project onto PC1 component: `coeff = (data - mean) @ PC1.T`
- Add PC1 coefficient column to dataframe
- Compute to pandas for aggregation

### Cell 6: Aggregate by Station (Code)
- Group by station ID (`ID`)
- Aggregate:
  - Average PC1 coefficient: `mean(PC1)`
  - Number of years: `count()` or `nunique(year)`
  - Station location: `first(latitude)`, `first(longitude)`
- Create aggregated dataframe with columns: `station_id`, `lat`, `lon`, `avg_pc1`, `n_years`
- Print summary statistics (min/max PC1, min/max years, number of stations)

### Cell 7: Create Folium Map (Code)
- Initialize map centered on USA (or appropriate location based on data coverage)
- Create color scale function: map PC1 values to color (e.g., blue for negative, red for positive, or use colormap)
- Create size scale function: map number of years to circle radius (e.g., 5-50 pixels)
- For each station:
  - Calculate color from `avg_pc1`
  - Calculate radius from `n_years`
  - Create CircleMarker with color and radius
  - Add popup with station info (ID, avg PC1, n_years, coordinates)
- Add colorbar legend if possible
- Display map

### Cell 8: Optional - Enhanced Visualization (Code)
- Add title/description to map
- Add layer control
- Save map to HTML file
- Print map summary (filename, number of stations plotted)

## Key Considerations
- **Data aggregation**: Need to decide if computing PC1 coefficients on-the-fly or loading precomputed coefficients
- **Color mapping**: Use diverging colormap (blue-white-red) for PC1 coefficients (negative to positive)
- **Size mapping**: Scale circle sizes appropriately (use log scale if years vary widely)
- **Performance**: May need to sample stations or use Dask efficiently for large datasets
- **Missing data**: Handle stations with incomplete daily data

## Expected Output
Interactive Folium map showing:
- Circles at each station location
- Colors representing average PC1 coefficient (climate pattern)
- Sizes representing data richness (number of years of measurements)



