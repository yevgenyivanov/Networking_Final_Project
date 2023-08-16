from scapy.all import rdpcap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# delete folder contents
def delete_folder_contents(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            delete_folder_contents(item_path)
            os.rmdir(item_path)


# IMD
def imd(_csv_list, _namelist):
    # calculate IMD
    _timestamps = []
    _lengths = []
    packets = []
    for csv in _csv_list:
        _timestamps.append(csv['Time'])
        _lengths.append(csv['Length'])
    for i in range(len(_timestamps)):
        # save the current series of timestamps and lengths
        _currTimeStamp = _timestamps[i]
        _currLengths = _lengths[i] 
        _floatTime = []
        _floatLen = []
        # convert current timestamps and lengths series to float
        for time in _currTimeStamp:
            _floatTime.append(float(time))
        for lenght in _currLengths:
            _floatLen.append(float(lenght))
        # generate a plot per each converted float list
        plt.figure(figsize=(10, 6))
        plt.bar(_floatTime, _floatLen, width=0.1, edgecolor='black', alpha=0.7)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Packet Length (bytes)')
        plt.title(f'Packet Length Bar Plot over Time Intervals {_namelist[i]}')
        plt.grid()
        _currName = _namelist[i]
        _currName = _currName[0:len(_currName)-4]
        plt.savefig(os.path.abspath(f'./results/IMD_{_currName}_.png'))
        plt.clf()
        # plt.show()
    # print(_csv_list[0])
    return

# PDF
def pdf(_csv_list, _namelist):
    # do it all in one go
    for csv in _csv_list:
        csv['Delay_Time']=csv['Time'].diff() #create additional collumn
        csv.at[0, 'Delay_Time'] = 0.0 #fix NaN issue
    # 
    for i in range(len(_csv_list)):
        # arrange bins
        csv = _csv_list[i]
        bin_step = np.arange(0,csv['Delay_Time'].max())
        print(bin_step)
        # create histogram
        histogram, histogram_bins = np.histogram(csv['Delay_Time'], bins=bin_step, density=True)

        exp_dist_scalar = 1/np.mean(csv['Delay_Time']) #arithmetic mean 
        if histogram.size != 0:
            max_value = max(histogram)
            if max_value != 0:
                scale = max(histogram)/ exp_dist_scalar* np.exp(- exp_dist_scalar * histogram_bins[np.argmax(histogram)])
            else:
                scale = 0
        else:
            max_value = 0
            scale = 0
        x= np.linspace(0,csv['Delay_Time'].max(),1000)
        y = scale * exp_dist_scalar * np.exp(-exp_dist_scalar * x)
        plt.figure(figsize=(10, 6))
        plt.step(histogram_bins, np.append(histogram,0), label='PDF')
        plt.plot(x,y, label='Exponential Distribution')
        plt.title(f"{_namelist[i]}")
        plt.xlabel('Inter-Message Delays (seconds)')
        plt.ylabel('Probability Density')
        plt.legend()
        plt.grid(True)
        _currName = _namelist[i]
        _currName = _currName[0:len(_currName)-4]
        plt.savefig(os.path.abspath(f'./results/PDF_{_currName}_.png'))
        plt.clf()
        # plt.show()

# CCDF
def ccdf(_csv_list,_namelist):
    _maxList = [] #np.int64
    _lengthList = [] #series
    for csv in _csv_list:
        _lengthList.append(csv['Length'])
        currLen = csv['Length'].max()
        _maxList.append(currLen)
    # print(_lengthList)

    # normalise
    for i in range(len(_lengthList)):
        _lengthList[i] = _lengthList[i]/_maxList[i]
    # sort values
    for i in range(len(_lengthList)):
        _lengthList[i] = _lengthList[i].sort_values()
    # _lengthList is now normalised
    _ccdfList = []
    for i in range(len(_lengthList)):
        y_vals = (np.arange(1,len(_lengthList[i]) + 1)) / len(_lengthList[i])
        # print(f"y_vals: {y_vals}")
        _ccdfList.append( 1 - y_vals)
        # print(_ccdfList[i])
    # print(_ccdfList[0])
    for i in range(len(_ccdfList)):
        plt.semilogy(_lengthList[i], _ccdfList[i], label=f"{_namelist[i]}")

    plt.xlabel("Normalized Message Size")
    plt.ylabel("Complementary CCDF")
    plt.legend()
    plt.title("Complementary CCDF of Message Sizes (logaritmic Scale)")
    plt.grid()
    plt.savefig(os.path.abspath(f'./results/CCDF.png'))
    plt.clf()
    # plt.show()

def main():
    # create csv and names list from resources folder
    _csv_list = []
    _namelist = []
    csv_folder = os.path.abspath('./resources/csvs')
    if os.path.exists(csv_folder):
        for filename in os.listdir(csv_folder):
            # if csv folder isn't empty, for each element in folder append to list, and the name of the file to namelist.
            if filename.endswith(".csv"):
                # Append to csv_list and namelist
                _csv_list.append(pd.read_csv(os.path.join(csv_folder, filename), encoding='unicode_escape'))
                _namelist.append(filename)
    results_folder = os.path.abspath('./results')
    delete_folder_contents(results_folder)
    # send _csv_list to IMD
    imd(_csv_list, _namelist) # oved
    pdf(_csv_list,_namelist)
    ccdf(_csv_list,_namelist)
    

if __name__ == '__main__':
    main()
