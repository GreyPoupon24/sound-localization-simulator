import matplotlib.pyplot as plt
from scipy.signal import correlate
import numpy as np
from simulator_main import sim_config as cfg
import logging
from sim_utils.output_utils import initialize_logger

# create logger object for this module
logger = initialize_logger(__name__)

class CrossCorrelation:
    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

    def apply(self, sim_signal):
        # compute cross correlation
        h0_sig, h_sig = sim_signal
        cross_correlation = correlate(h0_sig, h_sig, mode='same')
        
        # find discrete signal frequency
        f = cfg.signal_frequency / cfg.sampling_frequency
        # find number of samples per signal period
        N = int(np.ceil(1/f))
        # constrain region of interest based on signal periodicity
        # note that the correlation distribution is centered at n=0
        center_idx = int(len(cross_correlation)/2)
        halfrange = int(N/2)
        roi = cross_correlation[center_idx-halfrange:center_idx+halfrange]

        # plot cross correlation result if log level in debug mode
        level = logger.getEffectiveLevel()
        if level <= logging.DEBUG:
            self.plot_cross_correlation(cross_correlation, center_idx, halfrange, roi)

        maxima_idx = np.argmax(roi) - halfrange

        return maxima_idx / cfg.sampling_frequency

    def write_frame(self, frame):
        return {}

    def plot_cross_correlation(self, cross_correlation, center_idx, halfrange, roi):
        N = len(cross_correlation)
        n = np.linspace(-N/2, N/2, N)
        plt.figure()
        plt.plot(n, cross_correlation)
        plt.plot(n[center_idx-halfrange:center_idx+halfrange] ,roi)
        plt.title(self.id)