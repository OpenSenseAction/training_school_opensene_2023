# possible solution exercise 2.3

t_start, t_end = "2018-05-13", "2018-05-15"
for cmlid in ["5", "66", "78", "100"]:
    (cmls.sel(cml_id=cmlid).tsl - cmls.sel(cml_id=cmlid).rsl).isel(channel_id=0).sel(
        time=slice(t_start, t_end)
    ).plot(figsize=(10, 4), label="TL")
    pmin.sel(cml_id=cmlid, time=slice(t_start, t_end)).isel(
        channel_id=0
    ).plot(label="pmin = 15-minute minimum of rsl - tsl")
    max_pmin.sel(cml_id=cmlid, time=slice(t_start, t_end)).isel(
        channel_id=0
    ).plot(label="max_pmin = rolling 24h maximum of pmin")
    deltaP.sel(cml_id=cmlid, time=slice(t_start, t_end)).isel(
        channel_id=0
    ).plot(label="deltaP = Pmin − max_pmin")
    deltaPL.sel(cml_id=cmlid, time=slice(t_start, t_end)).isel(
        channel_id=0
    ).plot(label="deltaPL = deltaP/length")

    (
        (
            wet.isel(channel_id=0)
            .sel(cml_id=cmlid, time=slice(t_start, t_end))
            * 200
        )
        - 100
    ).plot(label="classified wet", alpha=0.5)

    plt.legend()
