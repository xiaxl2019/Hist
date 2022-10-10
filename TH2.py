#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt


class TH2():
    def __init__(self, xbins, xmin, xmax, ybins, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.xbin_edge = np.linspace(xmin, xmax, xbins + 1)
        self.ybin_edge = np.linspace(ymin, ymax, ybins + 1)

        self._sumw = np.zeros((xbins, ybins))
        self._sumw2 = np.zeros((xbins, ybins))

    @property
    def x(self):
        return (self.xbin_edge[1:] + self.xbin_edge[:-1]) / 2

    @property
    def y(self):
        return (self.ybin_edge[1:] + self.ybin_edge[:-1]) / 2

    @property
    def z(self):
        return self._sumw

    @property
    def err(self):
        return np.sqrt(self._sumw2)

    def Fill(self, x, y, wt=1):
        if self.xmin < x < self.xmax and self.ymin < y < self.ymax:
            i = np.searchsorted(self.xbin_edge, x) - 1
            j = np.searchsorted(self.ybin_edge, y) - 1
            self._sumw[i, j] += wt
            self._sumw2[i, j] += wt**2

    def Scale(self, factor):
        self._sumw *= factor
        self._sumw2 *= factor**2

    def Normalize(self, method='density'):
        if method == 'density':
            factor = np.sum(self.z) * np.diff(self.xbin_edge) * np.diff(self.ybin_edge)
        elif method == 'count':
            factor = np.sum(self.z)
        else:
            return
        self.Scale(1 / factor)
