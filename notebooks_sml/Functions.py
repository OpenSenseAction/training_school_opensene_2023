
import pickle
from ftplib import FTP
from tkinter import *
from tkinter import messagebox

import time
import datetime
from datetime import date, timedelta, time
import os
import numpy as np
# import dateparser
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#import plotly.graph_objs as go
from dateutil.rrule import HOURLY
import matplotlib.pyplot as plt
from matplotlib.dates import rrulewrapper, RRuleLocator, HourLocator, DateFormatter
from pandas.plotting import register_matplotlib_converters
#import torch
#from torch.utils.data import TensorDataset, DataLoader
from pathlib import Path
import scipy.signal
import matplotlib.dates as mdates



chilPath=os.path.dirname(os.path.abspath(__file__))
# Parameter Definition

Tm = 275
Tg = 50
Tc = 3
La = 0.3
Tr = 14
alpha = 28.14  # 17.910
beta = 0.798
teta = 31.58 * np.pi / 180
dh = 0.400
h0 = 2
DiffGapValue=0.4


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

#
# def timeRange(start, end):
#     for n in range(int((end - start).minutes)):
#         yield start_date + timedelta(n)
#


def Kalman_ST(observations,Q=10e-5,R_div=10):
    # intial parameters

    z=observations
    n_iter = len(z)
    sz = (n_iter,)  # size of array
    # x = -0.37727  # truth value (typo in example at top of p. 13 calls this z)
    # z = np.random.normal(x, 0.1, size=sz)  # observations (normal about x, sigma=0.1)


    # R = np.var(z)/R_div  #0.1 ** 0.2  # estimate of measurement variance, change to see effect
    # Q = 0.02 # 25e-5  # process variance

    # allocate space for arrays
    xhat = np.zeros(sz)  # a posteri estimate of x
    P = np.zeros(sz)  # a posteri error estimate
    xhatminus = np.zeros(sz)  # a priori estimate of x
    Pminus = np.zeros(sz)  # a priori error estimate
    K = np.zeros(sz)  # gain or blending factor

    R = np.var(z) *100 #0.1 ** 0.2  # estimate of measurement variance, change to see effect
    Q = np.var(z)/1000 # 25e-5  # process variance

    # intial guesses
    xhat[0] = np.median(z) # was 0
    P[0] = 1.0

    for k in range(1, n_iter):
        # time update
        xhatminus[k] = xhat[k - 1]
        Pminus[k] = P[k - 1] + Q

        # measurement update
        K[k] = Pminus[k] / (Pminus[k] + R)
        xhat[k] = xhatminus[k] + K[k] * (z[k] - xhatminus[k])
        P[k] = (1 - K[k]) * Pminus[k]
    return xhat
    # plt.figure()
    # plt.plot(z, 'k+', label='noisy measurements')
    # plt.plot(xhat, 'b-', label='a posteri estimate')
    # # plt.axhline(z, color='g', label='truth value')
    # plt.legend()
    # plt.title(' ST Estimate vs. iteration step', fontweight='bold')
    # plt.xlabel('Iteration')
    # plt.ylabel('Voltage')
    # plt.grid()
    # plt.show()


def Kalman_FT(observations):
    # intial parameters

    z = observations
    n_iter = len(z)
    sz = (n_iter,)  # size of array
    # x = -0.37727  # truth value (typo in example at top of p. 13 calls this z)
    # z = np.random.normal(x, 0.1, size=sz)  # observations (normal about x, sigma=0.1)

    Q = 1e-5   # process variance

    # allocate space for arrays
    xhat = np.zeros(sz)  # a posteri estimate of x
    P = np.zeros(sz)  # a posteri error estimate
    xhatminus = np.zeros(sz)  # a priori estimate of x
    Pminus = np.zeros(sz)  # a priori error estimate
    K = np.zeros(sz)  # gain or blending factor

    R = np.var(z) / 1000 # 0.1 ** 0.2  # estimate of measurement variance, change to see effect

    # intial guesses
    xhat[0] = np.median(z)
    P[0] = 1.0

    for k in range(1, n_iter):
        # time update
        xhatminus[k] = xhat[k - 1]
        Pminus[k] = P[k - 1] + Q

        # measurement update
        K[k] = Pminus[k] / (Pminus[k] + R)
        xhat[k] = xhatminus[k] + K[k] * (z[k] - xhatminus[k])
        P[k] = (1 - K[k]) * Pminus[k]
    return xhat
    # plt.figure()
    # plt.plot(z, 'k+', label='noisy measurements')
    # plt.plot(xhat, 'b-', label='a posteri estimate')
    # # plt.axhline(z, color='g', label='truth value')
    # plt.legend()
    # plt.title('FT Estimate vs. iteration step', fontweight='bold')
    # plt.xlabel('Iteration')
    # plt.ylabel('Voltage')
    # plt.grid()
    # plt.show()


def SatDataPreProcessing(DataIn):

    timedelta=0.5 #(30 seconds)
    interval=15 # min
    indexes=np.ceil(interval/timedelta)
    Din_r=np.zeros(len(DataIn))
    for  x in range(DataIn.shape[0]):
        if x>0:
            if x<=indexes :
                Din_r[x]=-1*(np.max(DataIn[0:x])-DataIn[x])
            else:
                Din_r[x]=-1*(np.max(DataIn[x-int(indexes):x])-DataIn[x])
        else:
            Din_r[x]=DataIn[x]
    Din_r=Din_r+np.median(DataIn)
    return (Din_r)



def LoadSatData(Date):
    try:
        AyeckaData = pd.read_pickle(os.path.join(chilPath, 'Sat_Data', 'ayekaData_' + Date.strftime("%Y_%m_%d") + '_df'))
        # Sat Data
        SR1 = AyeckaData[['esno', 'timestamp']][AyeckaData.name == 'sr1.1']
        SR1=SR1.iloc[10:, :]
        SR1.esno = SR1.esno / 10
        # SatDataDB=SR1.esno.to_numpy()
        return (SR1)

    except FileNotFoundError:
            # Handle the case where the file does not exist
            print("The file does not exist.")


def LoadSatDataCSV(SatDF,Date):
    try:
        # AyeckaData = pd.read_pickle(
        #     os.path.join(chilPath, 'Sat_Data', 'ayekaData_' + Date.strftime("%Y_%m_%d") + '_df'))
        SatDF['timestamp'] = pd.to_datetime(SatDF['timestamp'])
        SR1 = SatDF[SatDF['timestamp'].dt.date==Date]

        # # Sat Data
        # SR1 = AyeckaData[['esno', 'timestamp']]
        # SR1 = SR1.iloc[10:, :]
        # SR1.esno = SR1.esno / 10
        # SatDataDB=SR1.esno.to_numpy()
        return (SR1)

    except FileNotFoundError:
        # Handle the case where the file does not exist
        print("The file does not exist.")

def LoadRainData(Date) :

    try:
        IMS_HY_Gauge = pd.read_pickle(os.path.join(chilPath, 'Rain_Data', 'IMS_' + Date.strftime("%Y_%m_%d") + "_id" + str(275) + '_df'))
        IMS_dt = IMS_HY_Gauge.datetime.iloc[1] - IMS_HY_Gauge.datetime.iloc[0]
        # print(IMS_dt)
        # print(IMS_dt._m)
        IMS_dt=5 
        IMS_HY_Gauge.value = IMS_HY_Gauge.value * (60 / IMS_dt)  #  set rain value in mm/hr -> the relative part between the rain sample rate to the samples per hour  60/5=12)
        # IMS_HY_Gauge.datetime=IMS_HY_Gauge.datetime+ datetime.timedelta(minutes=10)
        return(IMS_HY_Gauge)
    except FileNotFoundError:
            # Handle the case where the file does not exist
            print("The file does not exist.")

def LoadRainDataCSV(RainDF,Date):

    try:
        RainDF['datetime'] = pd.to_datetime(RainDF['datetime'])
        IMS_HY_Gauge = RainDF[RainDF['datetime'].dt.date==Date]
        # IMS_dt = IMS_HY_Gauge.datetime.iloc[1] - IMS_HY_Gauge.datetime.iloc[0]
        # print(IMS_dt)
        # print(IMS_dt._m)
        # IMS_dt = IMS_dt._m
        # IMS_HY_Gauge.value = IMS_HY_Gauge.value * (
        #             60 / IMS_dt)  # set rain value in mm/hr -> the relative part between the rain sample rate to the samples per hour  60/5=12)
        # IMS_HY_Gauge.datetime=IMS_HY_Gauge.datetime+ datetime.timedelta(minutes=10)
        return (IMS_HY_Gauge)
    except FileNotFoundError:
        # Handle the case where the file does not exist
        print("The file does not exist.")


def PlotRainVsSatData(RainDF,SatDF):

    fig, ax = plt.subplots(1, figsize=(10,8))
    # Plots of rain estimation from Sat signal
    ax1 = ax.twinx()

    # ax.plot_date(SR1.timestamp, FinalData, '-', color='b', label='Processed Data ')
    # ax.plot_date(SLNBData.timestamp[SLNBData.esno>0], SLNBData.esno[SLNBData.esno>0] ,'-', color='purple', label='SLNB 4 ESNO Data')
    ax.plot_date(SatDF.timestamp, SatDF.esno, '-', color='purple', label='Esno Data ')
    ax1.plot_date(RainDF.datetime, RainDF.value, '-', label="Rain Gauge [HaKfar HaYarok]")

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    # ax1.set_ylim([0, 10])
    ax.set_ylim([-15, 12])
    ax.set_ylabel('Satellite  Signal Es/No [dB]')

    ax1.set_ylim([0, 80])
    ax1.set_ylabel('Rain[mm/h]')

    ax.legend(loc='upper left')
    ax1.legend(loc='upper right')
    ax.grid()

    # ax[1].plot_date(IMS_HY_Gauge.datetime, IMS_HY_Gauge.value, '-', label="Rain Gauge [HaKfar HaYarok]")
    #
    # # ax[4].xaxis.set_minor_locator(dates.HourLocator(interval=1))   # every 4 hours
    # # ax[4].xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    # ax[1].xaxis.set_major_locator(hours)  # every 4 hours
    # ax[1].xaxis.set_major_formatter(formatter2)  # hours and minutes
    # ax[1].set_ylim([0, 60])
    # ax[1].grid()
    # ax[1].legend()
    # ax[1].set_ylabel('Rain[mm/h]')
    fig.suptitle(' Rain Gauge Vs Sat Data at Kfar Saba ' + str(RainDF.datetime.iloc[100].date()))
    fig.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def PlotRainEstimationVsGaugeData(RainEst,RainDF,SatDF,ST,FT):
    
    fig, ax = plt.subplots(1, figsize=(15,10))
    # Plots of rain estimation from Sat signal
    ax1 = ax.twinx()

    # ax.plot_date(SR1.timestamp, FinalData, '-', color='b', label='Processed Data ')
    # ax.plot_date(SLNBData.timestamp[SLNBData.esno>0], SLNBData.esno[SLNBData.esno>0] ,'-', color='purple', label='SLNB 4 ESNO Data')
    ax.plot_date(SatDF.timestamp, SatDF.esno, '-', color='purple', label='Esno Data ')
    ax.plot_date(SatDF.timestamp, ST, '-', color='c', label='SlowTracker')
    ax.plot_date(SatDF.timestamp, FT, '-', color='b', label='FastTracker')
    ax1.plot_date(SatDF.timestamp, RainEst, '-', color='r', label='Rain Rate')
    ax1.plot_date(SatDF.timestamp, np.cumsum(RainEst/120), '-', color='k', label='Cumulative Sum Rain Rate')



    ax1.plot_date(RainDF.datetime, RainDF.value, '-',color='g', label="Rain Gauge [HaKfar HaYarok]")
    ax1.plot_date(RainDF.datetime, np.cumsum(RainDF.value/12), '-',color='y', label="Cumulative Rain Gauge [HaKfar HaYarok]")
    RainGaugSum=np.sum(RainDF.value/12)
    EstRainSum=np.sum(RainEst/120)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    # ax1.set_ylim([0, 10])
    ax.set_ylim([-15, 12])
    ax.set_ylabel('Satellite  Signal Es/No [dB]')

    ax1.set_ylim([0, 80])
    ax1.set_ylabel('Rain[mm/h]')

    ax.legend(loc='upper left')
    ax1.legend(loc='upper right')
    ax.grid()

    # ax[1].plot_date(IMS_HY_Gauge.datetime, IMS_HY_Gauge.value, '-', label="Rain Gauge [HaKfar HaYarok]")
    #
    # # ax[4].xaxis.set_minor_locator(dates.HourLocator(interval=1))   # every 4 hours
    # # ax[4].xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    # ax[1].xaxis.set_major_locator(hours)  # every 4 hours
    # ax[1].xaxis.set_major_formatter(formatter2)  # hours and minutes
    # ax[1].set_ylim([0, 60])
    # ax[1].grid()
    # ax[1].legend()
    # ax[1].set_ylabel('Rain[mm/h]')

    fig.suptitle('satellite link measurements at ' + str(RainDF.datetime.iloc[100].date()) + "\n \n" + "Sum HAKFAR HAYAROK   " + str(RainGaugSum) + "   [mm]" +

                         "      |        Sum Algorithm   " + str(EstRainSum) + "   [mm]" + " \n" )
    # fig.suptitle(' Rain Gauge Vs Sat Data at Kfar Saba ' + str(RainDF.datetime.iloc[100].date()))
    fig.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def  Calc_L(FT,ST):

    L = (np.multiply(np.divide(FT, ST), (Tc / La + Tm * (1 - 1 / La) + Tg + Tr)) + (Tm - Tc) / La) / (Tm + Tg + Tr)
    return (L)

def ApplySTMask(FT,ST):

    Diff = ST - FT

    # plt.figure(1)
    # plt.plot(ST,color='r', label='ST')
    # plt.plot(FT,color='b', label='FT')
    # plt.plot(Diff,color='g', label='Diff')
    # # plt.plot(DataIn,color='y', label='DataIn')
    #
    # plt.legend()
    # plt.grid()
    # plt.show()
    Diff_Rain_Flag = np.zeros((len(Diff)))
    Diff_Rain_Flag[Diff >= DiffGapValue] = 1
    z2one_ind = np.where(np.roll(Diff_Rain_Flag, 1) != Diff_Rain_Flag)[0]
    # print(z2one_ind)
    # plt.figure(2)
    # plt.plot(Diff_Rain_Flag)
    z2one_ind = z2one_ind[1:len(z2one_ind) - 1]
    z2onemat = np.reshape(z2one_ind, (-1, 2))

    for ind in z2onemat:
        # print (ind)
        ST[ind[0]:ind[1]] = ST[ind[0] + 1]

    return (FT,ST,Diff_Rain_Flag)

def ApplyDiffMask(RainRate_org,Diff_Rain_Flag):

    RainRate = np.multiply(RainRate_org, Diff_Rain_Flag)
    # RainRate=np.nan_to_num(RainRate,0)
    RainEstimated = RainRate[~np.isnan(np.nan_to_num(RainRate, 0))]  # 120 - normelize rain rate to mm/h ( we have 120 samples of 30 second in one hour  )
    RainEstimated_mmhr=RainEstimated/120;

    return(RainEstimated,RainEstimated_mmhr)

def ApplyPowerLaw(L):
    L_dB = 10 * np.log10(L)
    hr = h0 - dh
    L1_dB = L_dB * np.sin(teta) / hr
    RainRate_org = alpha * (np.power(L1_dB, beta, dtype=complex))
    RainRate_org = abs(RainRate_org)
    return(RainRate_org)

def RainEstimator(Date,SatData):

    # print(Date.strftime("%Y_%m_%d"))
    #
    # pathSat = Path(os.path.join(chilPath, 'Data_pickle', 'ayekaData_' + Date.strftime("%Y_%m_%d") + '_df'))
    # if not pathSat.is_file():
    #     continue
    #
    # pathRain = Path(os.path.join(chilPath, 'Data_IMS', 'IMS_' + Date.strftime("%Y_%m_%d") + '_df'))
    # if not pathRain.is_file():
    #     continue
    # dates.append(Date)
    # SatData = pd.read_pickle(os.path.join(chilPath, 'Data_pickle', 'ayekaData_' + Date.strftime("%Y_%m_%d") + '_df'))
    # RainData = pd.read_pickle(os.path.join(chilPath, 'Data_IMS', 'IMS_' + Date.strftime("%Y_%m_%d") + '_df'))

    # sr1 = (SatData[SatData.name == ['sr1.1'].esno[SatData[SatData.name == 'sr1.1'].esno > 0] / 10).to_numpy()
    # # min max on sat data every 10 minutes
    # sr1 = SatData[['esno', 'timestamp']][SatData.name == 'sr1.1']
    # sr1_startTime = sr1.timestamp.iloc[0]
    # sr1_EndTime = sr1.timestamp.iloc[-1]
    # dt = timedelta(minutes=5)
    # # plt.plot(sr1.esno / 10)
    # Raw_Data = sr1.esno
    # Raw_Data = Raw_Data.to_numpy()
    # Raw_Data = Raw_Data[10:] / 10
    # sr1.esno=np.convolve(sr1.esno, np.ones(10)/10, mode='same') # apply moving avarage to the signal
    # sr1.timestamp=sr1.timestamp+ timedelta(hours=2)

    # plt.plot(sr1.esno/10)
    # sr1.esno = (np.abs(sr1.esno - np.median(sr1.esno)))/10 # remove base line
    # plt.plot(sr1.esno )
    # plt.grid()
    # plt.show()
    # sr1 = sr1.iloc[10:, :]
    # DataIn = sr1.esno / 10
    #
    # DataIn = DataIn.to_numpy()
    # if i>0 :
    #     WetAntFlag=True
    # else :
    #     WetAntFlag=False

    # if WetAntFlag:
    #     Din_r = WetAntennaElimination(DataIn)
    #     Raw_Data = WetAntennaElimination(Raw_Data)
    # else:
    #     Din_r = DataIn

    print(Date.strftime("%Y_%m_%d"))

    Din_r=SatData.esno.to_numpy()
    # Kalman filter estimation
    ST = Kalman_ST(Din_r)
    FT = Kalman_FT(Din_r)
    # ST=ST[2:] ; FT=FT[2:]

    # Diff=np.abs(FT-ST)

    ###############################################covered in applydiffmask ########################################################
    # Diff = ST - FT
    #
    # # plt.figure(1)
    # # plt.plot(ST,color='r', label='ST')
    # # plt.plot(FT,color='b', label='FT')
    # # plt.plot(Diff,color='g', label='Diff')
    # # # plt.plot(DataIn,color='y', label='DataIn')
    # #
    # # plt.legend()
    # # plt.grid()
    # # plt.show()
    # Diff_Rain_Flag = np.zeros((len(Diff)))
    # Diff_Rain_Flag[Diff >= 0.4] = 1
    # z2one_ind = np.where(np.roll(Diff_Rain_Flag, 1) != Diff_Rain_Flag)[0]
    # # print(z2one_ind)
    # # plt.figure(2)
    # # plt.plot(Diff_Rain_Flag)
    # z2one_ind = z2one_ind[1:len(z2one_ind) - 1]
    # z2onemat = np.reshape(z2one_ind, (-1, 2))
    #
    # for ind in z2onemat:
    #     # print (ind)
    #     ST[ind[0]:ind[1]] = ST[ind[0] + 1]

    #################################################################  Rain Rate Calculator ##########################

    # # Parameter Definition ############################# moved to top #############################################
    #
    # Tm = 275
    # Tg = 50
    # Tc = 3
    # La = 0.3
    # Tr = 14
    # alpha = 28.14  # 17.910
    # beta = 0.798
    # teta = 31.58 * np.pi / 180
    # dh = 0.400
    # h0 = 2

    # SR1 polarization : Vertical

    # Freq : 12.130 Ghz oman
    #  https://www.lyngsat.com/Nilesat-201-and-Eutelsat-7-West-A.html    -  SR1 \ TC1 -- > 33.58

    # https: // www.lyngsat.com / Eutelsat - 33E.html   -   -  SLNB

    # https: // www.lyngsat.com / Nilesat - 201 - and -Eutelsat - 7 - West - A.html

    # teta=32

    # Algorithem Math
    # L = (np.multiply(np.divide(FT, ST), (Tc / La + Tm * (1 - 1 / La) + Tg + Tr)) + (Tm - Tc) / La) / (Tm + Tg + Tr)

    [FT,ST,Diff_Rain_Flag]=ApplySTMask(FT, ST)
    L=Calc_L(FT, ST)
    ####################  Apply power Law  ##############################################
    # L_dB = 10 * np.log10(L)
    # hr = h0 - dh
    # L1_dB = L_dB * np.sin(teta) / hr
    # RainRate_org = alpha * (np.power(L1_dB, beta, dtype=complex))
    # RainRate_org = abs(RainRate_org)
    RainRate_org=ApplyPowerLaw(L)
    [RainEstimated,RainEstimated_mmhr]=ApplyDiffMask(RainRate_org,Diff_Rain_Flag)

    return(RainEstimated,ST,FT)

    # #########################################################################   Rain From HMS #########################################################
    # # rain data to mm /hr
    # HK = RainData.value.to_numpy()
    # time_rain = RainData.datetime
    # # dt = timedelta(hours=1)
    # # ReainTimeRes = 5  # sampled by 5 min
    # # HK_mm_hr = HK * 12  # ( the signal is in mm / 5 min to get it in an hour its must be multiplied by 12
    #
    # RainGaugCumSum = np.cumsum(HK)
    # RainGaugSum = np.sum(HK)





    # sr1.timestamp = sr1.timestamp + timedelta(hours=2)




    # rule = rrulewrapper(HOURLY, byeaster=1, interval=5)
    # loc = RRuleLocator(rule)
    # hours = HourLocator(interval=2)
    # formatter = DateFormatter('%m-%d %H:%M ')

    # if plot:
    #
    #     # Plot
    #     fig, ax = plt.subplots(2, 1)
    #
    #     # ax[0].plot_date(sr1.timestamp,DataIn,'-',color='y', label='DataIn')
    #
    #     # ax[0].plot_date(sr1.timestamp,Diff,'-',color='g', label='Diff')
    #     # ax[0].plot_date(sr1.timestamp,Diff_Rain_Flag,'-',color='m', label='Flag')
    #     # ax[0].plot_date(sr1.timestamp,RainRate_org,'-',color='k', label='RainRate_org')
    #     ax1 = ax[0].twinx()
    #     ax1.plot_date(sr1.timestamp,Raw_Data,'-',color='y', label='Raw Data')
    #
    #     ax1.plot_date(sr1.timestamp, ST, '-', color='c', label='SlowTracker')
    #     ax1.plot_date(sr1.timestamp, FT, '-', color='b', label='FastTracker')
    #     ax[0].plot_date(sr1.timestamp, Rain, '-', color='r', label='Rain Rate')
    #     ax[0].plot_date(sr1.timestamp, RainCumSumEst, '-', color='k', label='Cumulative Sum Rain Rate')
    #
    #     ax[0].set_ylabel('Rain[mm/h]')
    #     ax[0].xaxis.set_major_locator(hours)  # every 4 hours
    #     ax[0].xaxis.set_major_formatter(formatter)  # hours and minutes
    #     ax[0].legend(loc=6)
    #     ax1.set_ylim([0, 10])
    #     ax[0].set_ylim([0, 40])
    #     ax1.set_ylabel('Satellite  Signal Es/No [dB]')
    #     ax1.legend(loc=7)
    #     ax[0].grid()
    #
    #     ax[1].plot_date(time_rain, HK_mm_hr, '-', label="HAKFAR HAYAROK")
    #     ax[1].plot_date(time_rain, RainGaugCumSum, '-', color='k', label="Cumulative Sum HAKFAR HAYAROK")
    #
    #     # ax[4].xaxis.set_minor_locator(dates.HourLocator(interval=1))   # every 4 hours
    #     # ax[4].xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
    #     ax[1].xaxis.set_major_locator(hours)  # every 4 hours
    #     ax[1].xaxis.set_major_formatter(formatter)  # hours and minutes
    #     ax[1].set_ylim([0, 40])
    #     ax[1].grid()
    #     ax[1].legend()
    #     ax[1].set_ylabel('Rain[mm/h]')
    #     #
    #     # plt.grid()
    #
    #     # if WetAntFlag:
    #     #     fig.suptitle('satellite link measurements at ' + Date.strftime("%Y_%m_%d") + "\n \n" + "Sum HAKFAR HAYAROK   " + str(RainGaugSum) + "   [mm]" +
    #     #
    #     #                  "      |        Sum Algorithm   " + str(RainSum) + "   [mm]" + " \n   Wet antenna correction On")
    #     # else:
    #     #     fig.suptitle('satellite link measurements at ' + Date.strftime("%Y_%m_%d") + "\n \n" + "Sum HAKFAR HAYAROK   " + str(RainGaugSum) + "   [mm]" +
    #     #
    #     #                  "      |        Sum Algorithm   " + str(RainSum) + "   [mm]" + " \n   Wet antenna correction Off")
    #
    #     fig.tight_layout()
    #     # fig.autofmt_xdate()
    #     # plt.ylim([100, 50])
    #
    #     plt.draw()




# Date= date(2021, 12, 20)
# Rain=LoadRainData(Date)
# Sat=LoadSatData(Date)
# PlotRainVsSatData(Rain,Sat)
# [RainEstimated,ST,FT]=RainEstimator(Date,Sat)
# PlotRainEstimationVsGaugeData(RainEstimated,Rain,Sat,ST,FT)
# Sat.esno=WetAntennaElimination(Sat.esno.to_numpy())
# [RainEstimated,ST,FT]=RainEstimator(Date,Sat)
# PlotRainEstimationVsGaugeData(RainEstimated,Rain,Sat,ST,FT)









# Rain=LoadRainData(Date)
# Sat=LoadSatData(Date)
# PlotRainVsSatData(Rain,Sat)
# [RainEstimated,ST,FT]=RainEstimator(Date,Sat)
# PlotRainEstimationVsGaugeData(RainEstimated,Rain,Sat,ST,FT)
# Sat.esno=WetAntennaElimination(Sat.esno.to_numpy())
# [RainEstimated,ST,FT]=RainEstimator(Date,Sat)
# PlotRainEstimationVsGaugeData(RainEstimated,Rain,Sat,ST,FT)