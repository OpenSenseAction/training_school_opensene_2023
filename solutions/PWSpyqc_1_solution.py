#----------------------------------------------------------------- Solution for Excercise 1.1


# Plot data of ams105 from september 2016 onwards
df_pws_pcp_hourly[['2016-09-01':].plot(ylabel='mm', title='PWS ams105')

# set values before October 2016 to NaN
df_pws_pcp_hourly['ams105'][df_pws_pcp_hourly.index < '2016-09-01T00:00:00'] = np.nan
