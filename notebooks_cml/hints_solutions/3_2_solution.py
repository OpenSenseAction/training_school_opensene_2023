# possible solution
cmls_5min.sel(time=da_radar_along_cmls.time).mean(dim='cml_id').plot(label='CML')
da_radar_along_cmls.mean(dim="cml_id").plot(label='radar')
plt.legend();