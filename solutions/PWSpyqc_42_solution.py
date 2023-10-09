#----------------------------------------------------------------- Solution for Excercise 1.1


# Interpolate all PWS (raw data)

# Set up the IDW interpolator
idw_interpolator = pycml.spatial.interpolator.IdwKdtreeInterpolator(
    nnear=15, 
    p=2, 
    exclude_nan=True, 
    max_distance=0.3)

#Create coordinates and data for interpolating values for a given timestamp/index
lon_pws=df_pws_coords.loc[:]
lat_pws=df_pws_coords.loc[:]
pcp_all=df_pws_pcp_hourly.iloc[18210, :].values

#Create indices for valid stations for the specific time step
idx=np.where(pcp_all>= 0)

R_grid_raw = idw_interpolator(
    x=lon_pws.lon.values[idx], 
    y=lat_pws.lat.values[idx], 
    z=pcp_all[idx], 
    resolution=0.01,)

# Plot the interpolated map and the locations of all PWS
bounds = np.arange(0, 8, 0.5)
norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=256, extend='both')
fig, ax = plt.subplots(figsize=(8, 6))
pc = plt.pcolormesh(
    idw_interpolator.xgrid, 
    idw_interpolator.ygrid, 
    R_grid_raw, 
    shading='nearest', 
    cmap='Blues',
    norm=norm,
)
plt.scatter(lon_pws.lon,lat_pws.lat, marker='o', color='r', alpha=.6)
fig.colorbar(pc, label='Rainfall sum in mm');
plt.title('Add a meaningful title here')
plt.show()
