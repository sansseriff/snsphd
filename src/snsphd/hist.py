import numpy as np
from scipy import special
from scipy.interpolate import UnivariateSpline
from scipy.stats import rv_continuous
from collections import namedtuple

from scipy.optimize import curve_fit
import math


# in the SNSPD ccommunity, we are often interested in gaussian-like response functions,
# and their width metrics like FWHM.

# these tools help with fitting of these response functions, and finding width metrics.


class SplineTool:
    def __init__(self, hist, _bins):
        if len(_bins) > len(hist):
            _bins = _bins[:-1]
        assert len(hist) == len(_bins)
        self.hist = np.array(hist)
        self.bins = np.array(_bins)
        self.y_scale = np.max(hist)
        self.norm_hist = hist / self.y_scale
        self.x_scale = self.bins[-1] - self.bins[0]
        self.norm_bins = self.bins / self.x_scale
        self.smoothing = 0
        self.spline = UnivariateSpline(self.norm_bins, self.norm_hist, s=self.smoothing)

    def plot_spline(self, plot_bins, smoothing):
        self.smoothing = smoothing
        self.spline.set_smoothing_factor(self.smoothing)
        norm_plot_bins = plot_bins / self.x_scale
        norm_plot_points = self.spline(norm_plot_bins)
        return plot_bins, norm_plot_points * self.y_scale

    def full_width_at_level(self, level, smoothing=None):
        assert level < 1
        if smoothing is not None:
            self.smoothing = smoothing

        # norm_hist goes from 0 to 1, but the max point (1) may not be a good estimate
        # for the max used for FWHM. Use the max of the spline instead.
        shifted_level = self.spline_max().y * level

        spline = UnivariateSpline(
            self.norm_bins, self.norm_hist - shifted_level, s=self.smoothing
        )
        roots = spline.roots()
        # print("roots before: ", roots)
        roots = roots * self.x_scale
        # print("xscale: ", self.x_scale)

        if len(roots) < 2:
            raise ValueError(f"There more or less than 2 roots: {roots}")
            # print("There more or less than 2 roots")
            # print("The roots are: ", roots)
            return 1
        if len(roots) > 2:
            print(f"There are more than 2 roots. They are: {roots}")
            root_1 = roots[np.argmax(np.diff(roots))]
            root_2 = roots[np.argmax(np.diff(roots)) + 1]
        if len(roots) == 2:
            root_1 = roots[0]
            root_2 = roots[1]

        height = self.y_scale * shifted_level
        RootData = namedtuple("RootData", "width left right height level")
        return RootData(
            width=root_2 - root_1, left=root_1, right=root_2, height=height, level=level
        )

    @staticmethod
    def quadratic_spline_roots(spl):
        # from: https://stackoverflow.com/questions/50371298/find-maximum-minimum-of-a-1d-interpolated-function
        roots = []
        knots = spl.get_knots()
        for a, b in zip(knots[:-1], knots[1:]):
            u, v, w = spl(a), spl((a + b) / 2), spl(b)
            t = np.roots([u + w - 2 * v, w - u, 2 * v])
            t = t[np.isreal(t) & (np.abs(t) <= 1)]
            roots.extend(t * (b - a) / 2 + (b + a) / 2)
        return np.array(roots)

    def spline_max(self):
        cr_pts = self.quadratic_spline_roots(self.spline.derivative())
        cr_pts = np.append(
            cr_pts, (self.norm_bins[0], self.norm_bins[-1])
        )  # also check the endpoints of the interval
        cr_vals = self.spline(cr_pts)
        min_index = np.argmin(cr_vals)
        max_index = np.argmax(cr_vals)
        MaxData = namedtuple("MaxData", "x y")
        return MaxData(x=cr_pts[max_index] * self.x_scale, y=cr_vals[max_index])

    def plot_width_at_level_arrows(
        self, plot, level, width_label=True, color="black", lw=1.5, alpha=1, ls="-"
    ):
        root_data = self.full_width_at_level(level)
        plot.annotate(
            text="",
            xy=(root_data.left, root_data.height),
            xytext=(root_data.right, root_data.height),
            arrowprops=dict(
                color=color,
                alpha=alpha,
                lw=lw,
                ls=ls,
                shrinkA=0,
                shrinkB=0,
                patchA=None,
                patchB=None,
                arrowstyle="<->",
            ),
            label=f"full width at {level} max",
            bbox=dict(pad=0),
        )
        center = (root_data.left + root_data.right) / 2
        if width_label:
            plot.annotate(
                f"{round(root_data.width, 2)}",
                xy=(center, root_data.height),
                color=color,
                alpha=alpha,
                xytext=(0, -1),
                fontsize=8,
                textcoords="offset points",
                horizontalalignment="center",
                verticalalignment="top",
            )

        # useful
        # https://stackoverflow.com/questions/23344891/matplotlib-set-pad-between-arrow-and-text-in-annotate-function
        return plot

    def sigma(self, smoothing=None):
        fwhm = self.full_width_at_level(0.5, smoothing).width
        return fwhm / 2.355

    def fwhm(self, smoothing=None):
        return self.full_width_at_level(0.5, smoothing).width

    def gaussian_fit(self):
        # curve_fit expects something more or less centered
        x_center = self.spline_max().x
        fwhm_width = self.full_width_at_level(0.5, 0.0001).width
        left_bound = x_center - fwhm_width * 3
        right_bound = x_center + fwhm_width * 3
        left_idx = np.searchsorted(self.bins, left_bound)
        right_idx = np.searchsorted(self.bins, right_bound)

        x_bias = np.average(self.bins[left_idx:right_idx])
        x_portion = self.bins[left_idx:right_idx] - x_bias
        y_portion = self.hist[left_idx:right_idx]
        popt, pcov = curve_fit(gaussian, x_portion, y_portion)
        popt[1] = popt[1] + x_bias

        return popt, pcov

    def plot_gaussian_fit(self):
        popt, pcov = self.gaussian_fit()
        return self.bins, gaussian(self.bins, *popt)


def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-(((x - mean) / stddev) ** 2))


# def find_nearest(array,value):
#     idx = np.searchsorted(array, value, side="left")
#     if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
#         return array[idx-1]
#     else:
#         return array[idx]


def gaussian_background(x, sigma, mu, back, l, r):
    "d was found by symbolically integrating in mathematica"
    n = back + (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(
        -0.5 * (((x - mu) / sigma) ** 2)
    )
    d = 0.5 * (
        2 * back * (-l + r)
        + special.erf((-l + mu) / (np.sqrt(2) * sigma))
        - special.erf((mu - r) / (np.sqrt(2) * sigma))
    )
    return n / d


class GaussianTool:
    class gaussian_bg(rv_continuous):
        "Gaussian distributionwithj Background parameter 'back'"

        def _pdf(self, x, sigma, mu, back):
            return gaussian_background(x, sigma, mu, back, self.a, self.b)
