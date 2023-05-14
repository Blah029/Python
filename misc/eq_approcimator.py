import graphs #from https://github.com/Blah029/python/blob/main/modules/graphs.py 
import numpy as np
import matplotlib.pyplot as plt

# center frecencies of the preset
band_data_1 = np.array([31,62,125,250,500,1000,2000,4000,8000,16000]) #autoeq 10-band
band_data_2 = np.array([31,60,150,400,1000,3000,8000,16000]) #samsing 7-band + 31hz
band_data_3 = np.array([32,64,125,250,500,1000,2000,4000,8000,16000]) #hp 10-band

# center frequencies of the required bands
available_bands_1 = np.array([60,150,400,1000,3000,8000,16000]) #samsung 7-band
available_bands_2 = np.array([32,64,125,250,500,1000,2000,4000,8000,16000]) #hp 10-band

# gains corresponding to each band of the preset
gain_data_1 = np.array([6.5,1.8,-9.9,7.5,-13.0,-1.3,1.3,-0.7,-1.7,1.4]) #autoeq ath-ck1 parametric eq gains
gain_data_2 = np.array([6.5,2,-5.3,-6.4,-1.3,0.1,-1.7,1.4]) #autoeq ath-ck1 parametric eq gains converted to samsung 7-band
gain_data_3 = np.array([7.4,2.9,-3.7,-3.2,-1.7,0.6,1.6,2.3,-2.0,7.2]) #autoeg beoplay a1 10-band
gain_data_4 = np.array([6.6,-6.7,-6.1,-4.2,-1.9,3.0,-0.6,4.4,6.1,4.8]) #autoeq sony mdr zx110 10-band

# calculated gains
gain_approx_1 = np.zeros(len(available_bands_1))
gain_approx_2 = np.zeros(len(available_bands_2))
gain_approx_3 = np.zeros(len(available_bands_1))
gain_approx_4 = np.zeros(len(available_bands_1))

def get_approx(band_in,band_out,gain_in,gain_out, label_in=None, label_out=None, degree=9, colour_in="tab:blue", colour_out="tab:orange", plot_input=True, plot_output=True):
    print("   Band     Gain")
    
    for i in range(len(band_out)):
        f = np.polyfit(np.log(band_in),gain_in,degree)
        x_axis = np.linspace(band_in[0],band_in[-1],band_in[-1]-band_in[0]+1)
        y_fit = np.zeros(len(x_axis))
        
        for k in range(degree+1):
            y_fit += f[-k-1]*np.log(x_axis)**k
            gain_out += (f[-k-1]*np.log(band_out)**k)/len(band_out) #why tf does it need to be divided?

    for i in range(len(band_out)):
        print(i,"%5.0f"%band_out[i],"Hz","%5.1f"%gain_out[i],"dB") #why does this need a separate for loop?

    if plot_input:
        plt.plot(x_axis,y_fit, label="Calculated model", color=colour_in)
        plt.plot(band_in,gain_in,label=label_in, color=colour_in, alpha=0.5, linestyle="dashed")
        plt.plot(band_in,gain_in,"o", color=colour_in)

    if plot_output:
        plt.plot(band_out,gain_out,label=label_out, color=colour_out, alpha=0.5, linestyle="dashed")

    if plot_input:
        plt.plot(band_in,gain_in,"o", color=colour_in)

    if plot_output:
        plt.plot(band_out,gain_out,"o", color=colour_out)

# get_approx(band_data_3,available_bands_1,gain_data_1,gain_approx_1,"AutoEq 10-band preset","7-band approximation",9)
# get_approx(band_data_2,available_bands_2,gain_data_2,gain_approx_2,"7-band phone EQ","10-band mimic",7)
# get_approx(band_data_1,available_bands_1,gain_data_3,gain_approx_3,"AutoEq 10-band preset","7-band approximation",9)
get_approx(band_data_1,available_bands_1,gain_data_4,gain_approx_4,"AutoEq 10-band preset","7-band approximation",9)
plt.xscale("log")
graphs.set_grid("Frequency band / Hz","Gain / dB","EQ")
plt.show()