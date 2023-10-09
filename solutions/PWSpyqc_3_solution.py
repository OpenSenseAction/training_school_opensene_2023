#----------------------------------------------------------------- Solution Exercise 3.1

df_pws_bias_corrected['ams1'].plot(color='blue', label='bias corrected')
df_pws_pcp_hourly['ams1'].plot(color='red', label='original')
plt.ylim(0,25)
plt.title('ams1')
plt.ylabel('[mm]')
plt.legend()
plt.show()
