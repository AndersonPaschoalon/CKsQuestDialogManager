import timeit


class QuickTimer:

    def __init__(self):
        self.start = timeit.default_timer()

    def reset(self):
        self.start = timeit.default_timer()

    def delta(self):
        stop = timeit.default_timer()
        print('QuickTimer: {0} seconds'.format(stop - self.start))
        return stop - self.start


