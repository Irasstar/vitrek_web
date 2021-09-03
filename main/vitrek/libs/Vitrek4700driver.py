from .connectors import *


class Vitrek4700:

    def __init__(self, connector):

        self.connector = connector

    def __del__(self):
        self.connector.disconnect()

    def get_hi_probe_id(self):
        self.connector.send('HIPROBE?')
        return self.connector.receive()

    def get_lo_probe_id(self):
        self.connector.send('LOPROBE?')
        return self.connector.receive()

    def get_mode(self):
        """MODE: prec, fast or ripple; Digits count; Band range; Average"""

        def mode():
            self.connector.send('MODE?')
            return self.connector.receive()

        def digits():
            self.connector.send('DIGITS?')
            return self.connector.receive()

        def band():
            self.connector.send('BAND?')
            return self.connector.receive()

        def average():
            self.connector.send('AVERAGE?')
            return self.connector.receive()

        current_mode = mode()
        # curmode = curmode.rstrip()
        if current_mode == 'PRECISE':
            return {'mode': current_mode, 'digits': digits(), 'band': band(), 'average': average()}
        elif current_mode == 'RIPPLE':
            return {'mode': current_mode, 'digits': None, 'band': None, 'average': average()}
        else:
            return {'mode': current_mode, 'digits': None, 'band': None, 'average': None}

    def set_mode(self, modes):
        pass

    def clear_screen(self):
        """useless. Will not use it"""
        self.connector.send('*CLS')

    def interface_rest(self):
        """turn off local control label without connection drop"""
        self.connector.send('*RST')

    def dc_zero(self):
        self.connector.send('DCZERO')

    def get_acv(self):
        self.connector.send('ACV?')
        return float(self.connector.receive())

    def get_dcv(self):
        self.connector.send('DCV?')
        return float(self.connector.receive())

    def get_freq(self):
        self.connector.send('FREQ?')
        return float(self.connector.receive())

    def get_peak_peak(self):
        self.connector.send('PKPK?')
        return float(self.connector.receive())

    def get_cr_factor(self):
        self.connector.send('CF?')
        return float(self.connector.receive())

    def get_measures(self):
        """The function returns 5 parameters: 1 - DCV; 2 - ACV; 3 - Frequency; 4 - PKPK; 5 - CF"""
        return {'DCV': self.get_dcv(),
                'ACV': self.get_acv(),
                'FR': self.get_freq(),
                'PKPK': self.get_peak_peak(),
                'CF': self.get_cr_factor()
                }

    def get_idn(self):
        self.connector.send('*IDN?')
        return self.connector.receive()


if __name__ == '__main__':
    pass
