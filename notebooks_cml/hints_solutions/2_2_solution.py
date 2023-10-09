# possible solution exercise 2.2

for r in [2, 5, 10, 15, 25]:
    ds_dist["within_r"] = (
        (ds_dist.a_to_all_a < r)
        & (ds_dist.a_to_all_b < r)
        & (ds_dist.b_to_all_a < r)
        & (ds_dist.b_to_all_b < r)
    )
    ds_dist.within_r.sum(dim="cml_id2").plot.hist(
        bins=int(ds_dist.within_r.sum(dim="cml_id2").max())
    )
    plt.vlines(4, ymin=0, ymax=50, color="red")
    plt.xlabel("CMLs within radius r")
    plt.ylabel("count")
    plt.title("Radius r = " + str(r) + " km")
    plt.show()

# before you continure, do not forget to set r to the default value of 15 km again