#----------------------------------------------------------------- Solution Exercise 1.1
cml = (xr.open_dataset(data_path + '/example_cml_data.nc') #<----- see 1.1
       .isel(cml_id = 0, channel_id = 0) #<----------------------- see 1.2
       .sel(time=slice('2018-05-11','2018-05-18')).load()) #<----- see 1.3 and 1.4
cml['tsl'] = cml.tsl.where(cml.tsl != 255.0) #<------------------- see 2.2
cml['rsl'] = cml.rsl.where(cml.rsl != -99.9) #<------------------- see 2.2
cml['trsl'] = cml.tsl - cml.rsl #<-------------------------------- see 2.3
cml['rstd'] = cml.trsl.rolling(time=60, center=True).std() #<----- see 3.1
cml['wet'] = cml.rstd > 0.8 #<------------------------------------ see 3.2
#----------------------------------------------------------------- Plot the result
fig, axs = plt.subplots(2,1, figsize=(16,4), sharex=True)
cml['trsl'].plot.line(x='time', ax=axs[0])
cml['wet'].plot.line(x='time', ax=axs[1])
axs[1].set_title('')
plt.show()