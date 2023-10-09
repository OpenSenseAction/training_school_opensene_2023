#----------------------------------------------------------------- Solution for Excercise 4.1


# New DataFrame with all accepted PWS with and row-wise of occurences of precipitation > 0mm
all_pcp=(df_corrected[pws_ids_accepted] > 0).sum(axis =1)
# All time intervals with more than 60 PWS with  precipitation > 0mm
all_pcp.loc[all_pcp>60]

# Select an arbitrary time step and cahnge the line in the IDW interpolator as follows
# df_corrected_interp.loc['2017-02-23 04:00:00', stn_in].values
