import numpy as np
from numba import njit
import numba
import math


@njit
def clockLock(
    _channels,
    _timetags,
    clockChan,
    dataChan,
    pulses_per_clock,
    phase,
    window=0.5,
    deriv=1800,
    prop=2e-12,
    guardPeriod=0,
):
    """
    This clock locking function takes in clock timetags on the clockChan variable, and data on the dataChan variable.
    It distributes an accurate virtual clock to muliple times bewteen each clock using a PLL.
    :param _channels:
    :param _timetags:
    :param clockChan:
    :param dataChan:
    :param pulses_per_clock: number of snspd/data tags per raw clock tag.
    :param phase:
    :param window: an area of time around each distributed clock time (pulse time) that
    is seached for timetags. Tags outside that range are discarded (this is useful
    for scanning for the phase offset of clock and snspd tags)
    :param deriv: the derivative parameter for the PLL
    :param prop: the proportional parameter for the PLL
    :param guardPeriod: number of actual clock tags that are used to let the PLL stabilize, but are not used for
    outputting data because the locked clock can oscillate a little before it stabilizes.
    :return:
    """
    j = 0
    k = 0
    phi0 = 0
    phiold = 0
    filterr = 0
    clock0 = -1
    cd = 0
    holdup = False  # a flag that is usually off, used for printing certain errors
    Clocks = np.zeros(len(_channels))
    dataTags = np.zeros(len(_channels))
    ClockPortion = np.zeros(1000)

    for i in range(1000):
        if _channels[i] == clockChan:
            ClockPortion[j] = _timetags[i]
            j = j + 1
    j = 0

    # Initial Estimates
    ClockPortion = ClockPortion[ClockPortion > 0]  # cut off extra zeros
    period = (ClockPortion[-1] - ClockPortion[0]) / (len(ClockPortion) - 1)
    freq = 1 / period

    RecoveredClocks = np.zeros(len(_channels))
    Periods = np.zeros(len(_channels))
    nearestPulseTimes = np.zeros(len(_channels))
    Cycles = np.zeros(len(_channels))

    for i in range(len(_channels)):
        if _channels[i] == clockChan:
            currentClock = _timetags[i]
            if clock0 == -1:
                clock0 = currentClock - period

            arg = ((currentClock - (clock0 + period)) / period) * 2 * math.pi
            phi0 = math.sin(arg)
            filterr = phi0 + (phi0 - phiold) * deriv
            freq = freq - filterr * prop
            clock0 = clock0 + (1 / freq)  # add one period
            period = 1 / freq
            phiold = phi0
            j = j + 1
            if j >= guardPeriod:
                RecoveredClocks[j - guardPeriod] = clock0
                Periods[j - guardPeriod] = period
                Clocks[j - guardPeriod] = _timetags[i]

        if _channels[i] == dataChan:
            if clock0 != -1 and j >= guardPeriod:
                tag = _timetags[i]
                hist_tag = _timetags[i] - clock0
                binTime = period / pulses_per_clock  # about 2000ps for now
                # dist = period/binTime # 64 for this awg run
                cycles = (
                    hist_tag + phase
                ) / binTime  # cycles ranges from a to a + 64 in this case
                if abs(cycles - round(cycles)) <= window:

                    # only add the data if its near a laser pulse
                    Cycles[k] = cycles
                    cycles = round(cycles)
                    nearestPulseTimes[k] = cycles * binTime + clock0
                    dataTags[k] = tag
                    k = k + 1
            else:
                # no usable recovered clock available yet. Throw out that data
                continue

    Clocks = Clocks[Clocks != 0]
    RecoveredClocks = RecoveredClocks[RecoveredClocks != 0]
    dataTags = dataTags[dataTags != 0]
    Periods = Periods[Periods != 0]
    nearestPulseTimes = nearestPulseTimes[nearestPulseTimes != 0]
    return Clocks, RecoveredClocks, dataTags, nearestPulseTimes, Cycles


@njit
def agnostic_clock_lock(
    _channels,
    _timetags,
    clockChan,
    dataChan,
    pulses_per_clock,
    phase,
    window=0.5,
    deriv=1800,
    prop=2e-12,
    guardPeriod=0,
    clock_mult=200,
):
    j = 0
    k = 0
    phi0 = 0
    phiold = 0
    filterr = 0
    clock0 = -1
    cd = 0
    holdup = False  # a flag that is usually off, used for printing certain errors
    Clocks = np.zeros(len(_channels))
    dataTags = np.zeros(len(_channels))
    ClockPortion = np.zeros(1000)

    for i in range(1000):
        if _channels[i] == clockChan:
            ClockPortion[j] = _timetags[i]
            j = j + 1
    j = 0

    # Initial Estimates
    ClockPortion = ClockPortion[ClockPortion > 0]  # cut off extra zeros
    period = (ClockPortion[-1] - ClockPortion[0]) / (len(ClockPortion) - 1)
    freq = 1 / period

    RecoveredClocks = np.zeros(len(_channels))
    Periods = np.zeros(len(_channels))
    nearestPulseTimes = np.zeros(len(_channels))
    Cycles = np.zeros(len(_channels))
    rel_clocks = np.zeros(len(_channels))

    for i in range(len(_channels)):
        if _channels[i] == clockChan:
            currentClock = _timetags[i]
            if clock0 == -1:
                clock0 = currentClock - period

            arg = ((currentClock - (clock0 + period)) / period) * 2 * math.pi
            phi0 = math.sin(arg)
            filterr = phi0 + (phi0 - phiold) * deriv
            freq = freq - filterr * prop
            clock0 = clock0 + (1 / freq)  # add one period
            period = 1 / freq
            phiold = phi0
            j = j + 1
            if j >= guardPeriod:
                RecoveredClocks[j - guardPeriod] = clock0
                Periods[j - guardPeriod] = period
                Clocks[j - guardPeriod] = _timetags[i]

        if _channels[i] == dataChan:
            if clock0 != -1 and j >= guardPeriod:
                tag = _timetags[i]
                hist_tag = _timetags[i] - clock0

                sub_period = (
                    period / clock_mult
                )  # this is dumb. It's exactly the same as period/pulses_per_clock, right?
                sub_addition = hist_tag // sub_period

                binTime = period / pulses_per_clock  # about 2000ps for now
                # dist = period/binTime # 64 for this awg run
                cycles = (
                    hist_tag + phase
                ) / binTime  # cycles ranges from a to a + 64 in this case

                # only add the data if its near a laser pulse
                Cycles[k] = cycles
                cycles = round(cycles)
                nearestPulseTimes[k] = cycles * binTime + clock0
                dataTags[k] = tag
                rel_clocks[k] = clock0 + sub_addition * sub_period
                k = k + 1
            else:
                # no usable recovered clock available yet. Throw out that data
                continue

    Clocks = Clocks[Clocks != 0]
    RecoveredClocks = RecoveredClocks[RecoveredClocks != 0]
    dataTags = dataTags[dataTags != 0]
    Periods = Periods[Periods != 0]
    nearestPulseTimes = nearestPulseTimes[nearestPulseTimes != 0]
    rel_clocks = rel_clocks[rel_clocks != 0]
    return Clocks, RecoveredClocks, dataTags, nearestPulseTimes, Cycles, rel_clocks


# used for phase locked loop in real time Swabian software. Layout based on an example for a CustomMeasurment
# from the Swabian documentation.
class RepeatedPll:
    def __init__(
        self,
        tags_per_cycle,
        channels,
        timetags,
        clock_chan,
        data_chan,
        mult,  # if set to pulses_per_clock, then a virtual clock is aligned with each pulse time
        phase,
        window=0.5,
        deriv=1800,
        prop=2e-12,
        guard_period=0,
    ):

        self.tags_per_cycle = tags_per_cycle
        self.channels = channels
        self.timetags = timetags
        self.clock_chan = clock_chan
        self.data_chan = data_chan
        self.mult = mult
        self.phase = phase
        self.window = window
        self.deriv = deriv
        self.prop = prop
        self.guard_period = guard_period
        self.clock0 = 0
        self.period = 1
        self.phi_old = 0
        self.init = (
            1  # used during 1st run of jit-function to get a rough clock estimate
        )
        # NOTE this won't work if clocks might be missing.

        # print("length of channels: ", len(channels))
        self.hist_tags = np.zeros(len(channels))
        self.clocks = np.zeros(len(channels))
        self.recovered_clocks = np.zeros(len(channels))
        self.nearest_pulses = np.zeros(len(channels))

        # this is only to keep pycharm happy...
        self.hist_buffer = np.zeros(self.tags_per_cycle)
        self.clocks_buffer = np.zeros(self.tags_per_cycle)
        self.recovered_clocks_buffer = np.zeros(self.tags_per_cycle)
        self.nearest_pulses_buffer = np.zeros(self.tags_per_cycle)

    def process(self):
        cycles = (len(self.timetags) // self.tags_per_cycle) + 1
        starts = np.arange(0, len(self.timetags), self.tags_per_cycle)
        ends = np.roll(starts, -1)
        ends[-1] = len(self.timetags)
        hist_idx = 0
        clock_idx = 0

        for start, end in zip(starts, ends):
            # in the swabian version I won't do this extracting out. There will just be the buffers,
            # print(start)
            # input
            self.tags_buffer = self.timetags[start:end]
            self.channels_buffer = self.channels[start:end]

            # output
            # self.hist_buffer = self.hist_tags[start:end] # this is just a view, not a new array I think
            self.hist_buffer = np.zeros(self.tags_per_cycle)
            self.clocks_buffer = np.zeros(self.tags_per_cycle)
            self.recovered_clocks_buffer = np.zeros(self.tags_per_cycle)
            self.nearest_pulses_buffer = np.zeros(self.tags_per_cycle)

            (
                self.clock0,
                self.period,
                self.phi_old,
                self.init,
            ) = RepeatedPll.fast_process(
                self.tags_buffer,
                self.channels_buffer,
                self.hist_buffer,
                self.clocks_buffer,  #
                self.recovered_clocks_buffer,  #
                self.nearest_pulses_buffer,  #
                self.clock_chan,
                self.data_chan,
                self.init,
                self.clock0,
                self.period,
                self.phi_old,
                self.deriv,
                self.prop,
                self.guard_period,
                self.phase,
                self.mult,
            )

            # in the realtime code for the swabian, you won't keep a giant array that corresponds to self.hist_tags.
            # That's why here I'm using these lines to transfer the buffers into the large arrays.

            # this wont work they need to be variable length additions

            self.clocks[
                clock_idx : clock_idx + len(self.clocks_buffer)
            ] = self.clocks_buffer
            self.recovered_clocks[
                clock_idx : clock_idx + len(self.recovered_clocks_buffer)
            ] = self.recovered_clocks_buffer
            self.hist_tags[
                hist_idx : hist_idx + len(self.hist_buffer)
            ] = self.hist_buffer
            self.nearest_pulses[
                hist_idx : hist_idx + len(self.hist_buffer)
            ] = self.nearest_pulses_buffer

            hist_idx = hist_idx + len(self.hist_buffer)
            clock_idx = clock_idx + len(self.clocks_buffer)

        return self.clocks, self.recovered_clocks, self.hist_tags, self.nearest_pulses
        #  need: Clocks, RecoveredClocks, dataTags, nearestPulseTimes,

    @staticmethod
    @numba.jit(nopython=True, nogil=True)
    def fast_process(
        tags,
        channels,
        hist_buffer,
        clocks_buffer,
        recovered_clocks_buffer,
        nearest_pulses_buffer,
        clock_chan,
        data_chan,
        init,
        clock0,
        period,
        phi_old,
        deriv,
        prop,
        guard_period,
        phase,
        mult,
    ):
        # is the numpy array cleared after each call? That's probably the most reasonable.
        # might be more efficient if I initialize it in process, and then just clear it and re-use it. I know what the
        # max number of tags per fast_process cycle is.

        freq = 1 / period

        if init:
            # need a rough estimate of the period and frequency to start.
            j = 0
            clock_portion = np.zeros(1000)
            for i in range(1000):
                if channels[i] == clock_chan:
                    clock_portion[j] = tags[i]
                    j = j + 1
            j = 0

            # Initial Estimates
            clock_portion = clock_portion[clock_portion > 0]  # cut off extra zeros
            period = (clock_portion[-1] - clock_portion[0]) / (len(clock_portion) - 1)
            freq = 1 / period
            init = 0
            clock0 = -1

        j = 0  # I don't think I even need j...
        k = 0
        for tag, channel in zip(tags, channels):
            if channel == clock_chan:
                currentClock = tag
                clocks_buffer[j] = currentClock
                if clock0 == -1:
                    clock0 = currentClock - period

                arg = ((currentClock - (clock0 + period)) / period) * 2 * math.pi
                phi0 = math.sin(arg)
                filterr = phi0 + (phi0 - phi_old) * deriv
                freq = freq - filterr * prop
                clock0 = clock0 + (1 / freq)  # add one period
                recovered_clocks_buffer[j] = clock0
                period = 1 / freq
                phi_old = phi0
                j = j + 1

            if channel == data_chan:
                if clock0 != -1 and j >= guard_period:

                    hist_buffer[k] = tag
                    hist_tag = tag - clock0  # IMPORTATNT!
                    # hist_tag, sub_period = RepeatedPll.wrap_hist(hist_tag, mult, period)
                    sub_period = period / mult

                    # with these lines, cycles (below) is always going to be about 1
                    # minor_cycles = hist_tag // sub_period            # for mult method
                    # hist_tag = hist_tag - sub_period * minor_cycles  # for mult method

                    cycles = (hist_tag + phase) / sub_period  # for central method
                    cycles = round(cycles)  # for central method
                    nearest_pulses_buffer[k] = (
                        cycles * sub_period + clock0
                    )  # for central method
                    k = k + 1
                else:
                    # no usable recovered clock available yet. Throw out that data
                    continue

        clocks_buffer = clocks_buffer[clocks_buffer != 0]
        recovered_clocks_buffer = recovered_clocks_buffer[recovered_clocks_buffer != 0]
        hist_buffer = hist_buffer[hist_buffer != 0]
        nearest_pulses_buffer = nearest_pulses_buffer[nearest_pulses_buffer != 0]
        return (
            clock0,
            period,
            phi_old,
            init,
        )  # hist_buffer, clocks_buffer, recovered_clocks_buffer, nearest_pulses_buffer
