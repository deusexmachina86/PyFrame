import h5py as h5
import numpy as np
from scipy.interpolate import interp1d

class Utilities():
    @staticmethod
    def get_signals(f_path):
        cur_measurement = h5.File(f_path, 'r')
        return list(cur_measurement['sys']['INCA']['data'].keys())
   
    @staticmethod
    def execute(f_paths, signals=['EngN', 'TrsmVehSpd', 'HiWay', 'Data_DB61'], interp_strat = ['linear', 'zero', 'zero', 'zero'], delta_t=1.0):
        #input data here:
        filepaths = f_paths

        signal_names = signals
        interp_strategy = interp_strat

        out_tables = [] #output is a list of tables
        gl_missing_signals = [] # gLOBAl list of missing signals for all files/cars in the f_paths variable 
        for cur_src in filepaths:

            cur_measurement = h5.File(cur_src, 'r')

            missing_signals = [] # for current file/car
            
            tstarts = []
            tends = []
            # Time resolution is currently set through the parameter "delta_t" of the method "execute"
            # for 10 ms: dt = 0.01
            # ideally should be moved to the "__init" method
            dt = delta_t# 1 second by default

            # Get time window
            for cur_sig in signal_names:
                try:
                    tstarts.append(np.min(cur_measurement['sys']['INCA']['data'][cur_sig]['data']['!ADAF_Basis!'].value))
                    tends.append(np.max(cur_measurement['sys']['INCA']['data'][cur_sig]['data']['!ADAF_Basis!'].value))
                except KeyError as e:
                    missing_signals.append(cur_sig)

            tnew = np.array([])
            try:
                tnew = np.arange(max(tstarts), min(tends), dt)
                tnew = tnew[tnew < min(tends)]
            except ValueError as e:
                pass

#            tnew = np.arange(max(tstarts), min(tends), dt)
#            tnew = tnew[tnew < min(tends)]

            out_table = {} #the table is a simple dict with numpy arrays
            out_table['Time'] = tnew
#------------------------------------------------------------------------------
            #    Resample of all signals with time vector tnew
#------------------------------------------------------------------------------   
            
##                  UPDATED VERSION, a product of collaboration btw
## 					Daniel Karlsson (daniel.karlsson.2@volvocars.com) and
##					Kiryl Bletsko	(kiryl.bletsko@volvocars.com)					             
            for (cursig, curmethod) in zip(signal_names, interp_strategy):
                #for debug print(cursig, curmethod)
                ynew = None
                if cursig in missing_signals:
                    print(cursig + ' missing in measurement')
                else:
                    try:
                        f_i = interp1d(
                            cur_measurement['sys']['INCA']['data'][cursig]['data']['!ADAF_Basis!'].value,
                            cur_measurement['sys']['INCA']['data'][cursig]['data'][cursig].value,
                            kind=curmethod, bounds_error=True)
                        ynew = f_i(tnew)
                    except ValueError as e:
                        print(cursig + 'fails: due to too few samples')
                       
                # for debug print(ynew)
                if ynew is not None:
                    out_table[cursig] = ynew
            out_tables.append(out_table)
            gl_missing_signals.append(missing_signals)
## END OF                  UPDATED VERSION                                
#------------------------------------------------------------------------------
        return out_tables, gl_missing_signals
