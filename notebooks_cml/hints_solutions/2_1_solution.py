# possible solution exercise 2.1
fig, ax = plt.subplots(3, 1, figsize=(12, 6), sharex=True)
# plotting rsl and tsl
cmls.tsl.isel(cml_id=0, channel_id=0).plot(ax=ax[0], label="tsl")
cmls.rsl.isel(cml_id=0, channel_id=0).plot(ax=ax[0], label="rsl")
(cmls.tsl - cmls.rsl).isel(cml_id=0, channel_id=0).plot(ax=ax[0], label="TL")
ax[0].legend()
# pmin, the 15 minuten minimum of rsl
pmin.isel(cml_id=0, channel_id=0).plot(ax=ax[1], label="pmin")
# max_pmin, maximum value of pmin over the previous number of hours including the present time interval
max_pmin.isel(cml_id=0, channel_id=0).plot(ax=ax[1], label="max_pmin")
ax[1].legend()
ax[1].set_title("min max values: pmin&max_pmin")
# deltaP, differnce between pmin and max_pmin, regarded as attenuation
deltaP.isel(cml_id=0, channel_id=0).plot(ax=ax[2], label="deltaP")
# deltaPL, deltaP divided by the CMLs length, regarded as specific attenuation
deltaPL.isel(cml_id=0, channel_id=0).plot(ax=ax[2], label="deltaPL")
ax[2].legend()
ax[2].set_title("min max values: deltaP&deltaPL")
plt.tight_layout()
plt.xlim(pd.to_datetime("2018-05-13 20:00"), pd.to_datetime("2018-05-14 3:00"))
