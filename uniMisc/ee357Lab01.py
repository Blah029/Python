import sys
sys.path.append("D:\\User Files\\Documents\\Python\\modules")
import numpy as np
from scipy import signal
import graphs


def main():
    # Section 1 - Multplier Modulator/Demodulator
    # 1. Generate m(t)
    fm1 = 15000
    fc = 250000
    fs = 750000*10
    duration = 1/fm1*4
    t = np.linspace(0,duration,int(fs*duration+1))
    m1_t = 0.5*np.cos(2*np.pi*fm1*t)
    # 2. Multiply with carrier
    c_t = np.cos(2*np.pi*fc*t)
    mod1_t = m1_t*c_t
    # 3. Demodulator
    fCutoff = 2*15*1000
    lpfB, lpfA = signal.butter(5,fCutoff/(fs/2))
    e_t = mod1_t*c_t
    demod1_t = signal.filtfilt(lpfB,lpfA,e_t)
    # 4. Adjust oscillator amplitude
    oscAmp = 2

    #5. Plot spectrum
    def section1Plots():
        # Time domain
        graphs.plotLine(t,m1_t, label="m(t)")
        graphs.plotLine(t,mod1_t, label="Modulated")
        graphs.plotLine(t,oscAmp*demod1_t, label="Demodulated")
        graphs.setGrid("t /s","Amplitude","Time Domain")
        graphs.plt.xlim([0.00005,0.0002])
        graphs.plt.ylim([-1.1,1.1])
        graphs.plt.show()
        # Frequency domain
        fig1, ax1 = graphs.plt.subplots(3)
        ax1[0].magnitude_spectrum(m1_t, Fs=fs)
        ax1[0].set_title("m(t) Frequency Spectrum")
        ax1[1].magnitude_spectrum(mod1_t, Fs=fs)
        ax1[1].set_title("Modulator Output Frequency Spectrum")
        ax1[2].magnitude_spectrum(demod1_t, Fs=fs)
        ax1[2].set_title("Demodulator Output Frequency Spectrum")
        for axis in ax1:
            graphs.setSubGrid(axis,"f /kHz","Magnitude","log")
            axis.set_xticks([1e4,1e5,1e6])
            axis.set_xticklabels([10,100,100])
        fig1.tight_layout()
        graphs.plt.show()

    # Section 2 - Nonlinear Modulator/Demodulator
    # 1. Use same m(t)
    # 2. Modulator
    bpfB, bpfA = signal.butter(3,[(fc-fCutoff)/(fs/2),(fc+fCutoff)/(fs/2)],"bandpass")
    x1_t = c_t + m1_t
    x2_t = c_t - m1_t
    y1_t = 2*x1_t + x1_t**2
    y2_t = 2*x2_t + x2_t**2
    z_t = y1_t - y2_t
    mod2_t = signal.filtfilt(bpfB,bpfA,z_t)
    # 3. Demodulator
    x1Demod_t = c_t + mod2_t
    x2Demod_t = c_t - mod2_t
    y1Demod_t = 2*x1Demod_t + x1Demod_t**2
    y2Demod_t = 2*x2Demod_t + x2Demod_t**2
    zDemod_t = y1Demod_t - y2Demod_t
    demod2_t = signal.filtfilt(lpfB,lpfA,zDemod_t)

    # 4. Plot spectrum
    def section2Plots():
        # Time domain
        graphs.plotLine(t,m1_t, label="m(t)")
        graphs.plotLine(t,mod2_t, label="Modulated")
        graphs.plotLine(t,demod2_t, label="Demodulated")
        graphs.setGrid("t","Amplitude","Time Domain")
        graphs.plt.xlim([0.00005,0.0002])
        graphs.plt.ylim([-5,5])
        graphs.plt.show()
        # Frequency domain
        fig2, ax2 = graphs.plt.subplots(3)
        ax2[0].magnitude_spectrum(m1_t, Fs=fs)
        ax2[0].set_title("m(t) Frequency Spectrum")
        ax2[1].magnitude_spectrum(mod2_t, Fs=fs)
        ax2[1].set_title("Modulator Output Frequency Spectrum")
        ax2[2].magnitude_spectrum(demod2_t, Fs=fs)
        ax2[2].set_title("Demodulator Output Frequency Spectrum")
        for axis in ax2:
            graphs.setSubGrid(axis,"f /kHz","Magnitude","log")
            axis.set_xticks([1e4,1e5,1e6])
            axis.set_xticklabels([10,100,100])
        fig2.tight_layout()
        graphs.plt.show()
    
    # Section 3 - Effect of Phase Offset
    # 1. Use system in section 1
    fm3 = 3000
    duration = 1/fm3*4
    t3 = np.linspace(0,duration,int(fs*duration+1))
    m3_t = 0.5*np.cos(2*np.pi*fm3*t3)
    c3_t = np.cos(2*np.pi*fc*t3)
    mod3_t = m3_t*c3_t
    fCutoff3 = 2*15*1000
    lpfB3, lpfA3 = signal.butter(5,fCutoff3/(fs/2))
    attenuation = np.array([0])
    offset = np.array([0])
    
    # 2. Adjust oscillator phase offset
    def section3Plots():
        for i in range(51):
            cReceiver3_t = np.cos(2*np.pi*fc*t3 + i*np.pi/50)
            e3_t = mod3_t*cReceiver3_t
            demod3_t = signal.filtfilt(lpfB3,lpfA3,e3_t)
            nonlocal attenuation
            nonlocal offset
            attenuation = np.append(attenuation,np.max(demod3_t[500:750]))
            offset = np.append(offset,i)
            graphs.plotLine(t3,demod3_t, label="{0}π/50 offset".format(i))
            graphs.setGrid("t /s","Amplitude","Time Domain")
            graphs.plt.xlim([0.00025,0.001])
            graphs.plt.ylim([-0.3,0.3])
        # 3. Observe time domain and attenutation vs. offset
        # Time domain
        graphs.plt.show()
        # Attenuation vs. offset
        graphs.plotLine(offset[1:],attenuation[1:]-0.5,)
        graphs.setGrid("Phase offset /(π/50)","Attenuation","Time Domain")
        graphs.plt.show()

    section1Plots()
    section2Plots()
    section3Plots()


if __name__ == "__main__":
    main()