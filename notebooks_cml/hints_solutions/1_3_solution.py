#----------------------------------------------------------------- Solution Exercise 1.1
cml = (xr.open_dataset(data_path + '/example_cml_data.nc') #<----- see 1.1
       .isel(channel_id = 0).sel(cml_id = '67')#<----------------- see 1.2 
       .sel(time=slice('2018-05-11','2018-05-18')).load()) # #<--- see 1.3 
cml['tsl'] = cml.tsl.where(cml.tsl != 255.0) #<------------------- see 2.2 
cml['rsl'] = cml.rsl.where(cml.rsl != -99.9) #<------------------- see 2.2 
cml['trsl'] = cml.tsl - cml.rsl #<-------------------------------- see 2.3
cml['rstd'] = cml.trsl.rolling(time=60, center=True).std() #<----- see 3.1
cml['wet'] = cml.rstd > 0.1 #<------------------------------------ see 3.2 (changed 0.8 to 0.1, notice that we now predict more rain events)
#----------------------------------------------------------------- Plot the result
fig, axs = plt.subplots(2,1, figsize=(16,4), sharex=True)
cml['trsl'].plot.line(x='time', ax=axs[0])
cml['wet'].plot.line(x='time', ax=axs[1])
axs[1].set_title('')
plt.show()