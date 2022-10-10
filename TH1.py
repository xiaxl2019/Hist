#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt


class TH1():
    def __init__(self, bins, xmin, xmax):
        self.xmin = xmin
        self.xmax = xmax
        self.bin_edge = np.linspace(xmin, xmax, bins + 1)

        self._sumw = np.zeros(bins)
        self._sumw2 = np.zeros(bins)

    @property
    def x(self):
        return (self.bin_edge[1:] + self.bin_edge[:-1]) / 2

    @property
    def y(self):
        return self._sumw

    @property
    def err(self):
        return np.sqrt(self._sumw2)

    def Fill(self, x, wt=1):
        if self.xmin < x < self.xmax:
            i = np.searchsorted(self.bin_edge, x) - 1
            self._sumw[i] += wt
            self._sumw2[i] += wt**2

    def Scale(self, factor):
        self._sumw *= factor
        self._sumw2 *= factor**2

    def Normalize(self, method='density'):
        if method == 'density':
            factor = np.sum(self.y) * np.diff(self.bin_edge)
        elif method == 'count':
            factor = np.sum(self.y)
        else:
            return
        self.Scale(1 / factor)
