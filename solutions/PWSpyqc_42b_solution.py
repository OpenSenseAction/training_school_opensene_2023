#----------------------------------------------------------------- Solution for Excercise 1.1


# [1:,:] omits one row from the raw data grid to match correted PWS grid
diff=R_grid-R_grid_raw[1:,:]

lon_pws=df_pws_coords.loc[pws_ids_accepted]
lat_pws=df_pws_coords.loc[pws_ids_accepted]


lon_pws2=df_pws_coords.loc[:]
lat_pws2=df_pws_coords.loc[:]

bounds = np.arange(-5, 5, 0.5)
norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=256, extend='both')
fig, ax = plt.subplots(figsize=(8, 6))
pc=plt.pcolormesh(
    idw_interpolator.xgrid[1:,:], 
    idw_interpolator.ygrid[1:,:], 
    diff, 
    shading='nearest', 
    cmap='RdBu',
    norm=norm,
    )
plt.scatter(lon_pws2.lon,lat_pws2.lat, marker='x', color='r', alpha=.6)
plt.scatter(lon_pws.lon,lat_pws.lat, marker='o', color='k', alpha=.6)

fig.colorbar(pc, label='Rainfall difference in mm')
plt.title('Difference PWS-QC minus raw PWS')
plt.show()

