import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize
import sys
sys.path.append("D:\\User Files\\Documents\\Python\\modules")
import graphs

def fit_sin(xx, yy):
    '''Fit sin to the input time sequence, and return fixxing parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    xx = np.array(xx)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(xx), (xx[1]-xx[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * np.sin(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, xx, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c
    return {"amp": A, "ome,ga": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}

distance = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250])
vNoLoad = np.array([1.117, 1.185, 1.1, 0.903, 0.608, 0.174, 0.247, 0.628, 0.746, 0.765, 0.71, 0.918, 1.096, 1.24, 1.228, 0.999, 0.839, 0.063, 0.426, 0.568, 0.678, 0.776, 0.856, 0.994, 1.052, 1.234])
vShortCircuit = np.array([0.222, 0.902, 1.024, 0.857, 0.796, 0.944, 0.963, 0.914, 0.818, 0.949, 1.03, 1.125, 0.537, 0.707, 0.996, 0.985, 0.967, 0.933, 0.895, 0.834, 0.823, 0.664, 0.935, 1.097, 1.042, 0.224])
vInductive = np.array([1.07, 1.067, 0.963, 0.848, 0.653, 0.65, 0.586, 0.057, 0.309, 0.456, 0.623, 0.808, 0.983, 1.106, 1.067, 0.984, 0.781, 0.682, 0.632, 0.493, 0.338, 0.345, 0.302, 0.639, 0.907, 1.125])
vCapacitive = np.array([0.448, 1.156, 0.848, 0.496, 0.355, 0.567, 0.723, 0.743, 0.744, 0.812, 0.939, 0.992, 1.07, 0.85, 0.96, 0.651, 0.612, 0.599, 0.574, 0.721, 0.175, 0.722, 0.696, 0.936, 1.117, 1.198])
vMatched = np.array([1.023, 1.047, 0.909, 0.705, 0.684, 0.653, 0.701, 0.79, 0.69, 0.701, 0.814, 0.84, 0.931, 1.092, 1.009, 0.744, 0.713, 0.76, 0.716, 0.72, 0.967, 0.651, 0.168, 0.827, 0.994, 1.144])

distanceFit = np.linspace(0,250,500)
fitNoLoad = fit_sin(distance,vNoLoad)
fitShortCircuit = fit_sin(distance, vShortCircuit)
fitInductive = fit_sin(distance,vInductive)
fitCapacitive = fit_sin(distance,vCapacitive)
fitMatched = fit_sin(distance,vMatched)

readings = np.array([vNoLoad,vShortCircuit,vInductive,vCapacitive,vMatched])
readingsFit = np.array([fitNoLoad,fitShortCircuit,fitInductive,fitCapacitive,fitMatched])

for i in range(len(readingsFit)):
    plt.figure(i+1)
    plt.plot(distanceFit,readingsFit[i]["fitfunc"](distanceFit))
    graphs.setGrid("Distance /cm","No Load Voltage /V")
    graphs.plotPoints(distance,readings[i],"tab:blue")
    plt.show()