#emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
#ex: set sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the PyMVPA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Misc. functions (in the mathematical sense)"""

__docformat__ = 'restructuredtext'

import numpy as N


def singleGammaHRF(t, A=5.4, W=5.2, K=1.0):
    """Hemodynamic response function model.

    The version consists of a single gamma function (also see
    doubleGammaHRF()).

    :Parameters:
      t: float
        Time.
      A: float
        Time to peak.
      W: float
        Full-width at half-maximum.
      K: float
        Scaling factor.
    """
    A = float(A)
    W = float(W)
    K = float(K)
    return K * (t / A) ** ((A ** 2) / (W ** 2) * 8.0 * N.log(2.0)) \
           * N.e ** ((t - A) / -((W ** 2) / A / 8.0 / N.log(2.0)))


def doubleGammaHRF(t, A1=5.4, W1=5.2, K1=1.0, A2=10.8, W2=7.35, K2=0.35):
    """Hemodynamic response function model.

    The version is using two gamma functions (also see singleGammaHRF()).

    :Parameters:
      t: float
        Time.
      A: float
        Time to peak.
      W: float
        Full-width at half-maximum.
      K: float
        Scaling factor.

    Parameters A, W and K exists individually for each of both gamma
    functions.
    """
    A1 = float(A1)
    W1 = float(W1)
    K1 = float(K1)
    A2 = float(A2)
    W2 = float(W2)
    K2 = float(K2)
    return singleGammaHRF(t, A1, W1, K1) - singleGammaHRF(t, A2, W2, K1)


def leastSqFit(fx, params, y, x=None, **kwargs):
    """Simple convenience wrapper around SciPy's optimize.leastsq.

    The advantage of using this wrapper instead of optimize.leastsq directly
    is, that it automatically constructs an appropriate error function and
    easily deals with 2d data arrays, i.e. each column with multiple values for
    the same function argument (`x`-value).

    :Parameters:
      fx: functor
        Function to be fitted to the data. It has to take a vector with
        function arguments (`x`-values) as the first argument, followed by
        an arbitrary number of (to be fitted) parameters.
      params: sequence
        Sequence of start values for all to be fitted parameters. During
        fitting all parameters in this sequences are passed to the function
        in the order in which they appear in this sequence.
      y: 1d or 2d array
        The data the function is fitted to. In the case of a 2d array, each
        column in the array is considered to be multiple observations or
        measurements of function values for the same `x`-value.
      x: Corresponding function arguments (`x`-values) for each datapoint, i.e.
        element in `y` or columns in `y', in the case of `y` being a 2d array.
        If `x` is not provided it will be generated by `N.arange(m)`, where
        `m` is either the length of `y` or the number of columns in `y`, if
        `y` is a 2d array.
      **kwargs:
        All additonal keyword arguments are passed to `fx`.

    :Returns:
      Tuple as returned by scipy.optimize.leastsq, i.e. 2-tuple with list of
      final (fitted) parameters of `fx` and an integer value indicating success
      or failure of the fitting procedure (see leastsq docs for more
      information).
    """
    # import here to not let the whole module depend on SciPy
    from scipy.optimize import leastsq

    y = N.asanyarray(y)

    if len(y.shape) > 1:
        nsamp, ylen = y.shape
    else:
        nsamp, ylen = (1, len(y))

    # contruct matching x-values if necessary
    if x is None:
        x = N.arange(ylen)

    # transform x and y into 1d arrays
    if nsamp > 1:
        x = N.array([x] * nsamp).ravel()
        y = y.ravel()

    # define error function
    def efx(p):
        err = y - fx(x, *p, **kwargs)
        return err

    # do fit
    return leastsq(efx, params)
