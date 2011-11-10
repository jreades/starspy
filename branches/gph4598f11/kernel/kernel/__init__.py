"""
:mod: 'kernel' --- Calculating Kernel Density Approximations
============================================================

"""
__all__ = []

import triangular
import uniform
import quadratic
import epanechnikov
import quartic
import bisquare
import gaussian

__all__ += triangular.__all__
__all__ += uniform.__all__
__all__ += quadratic.__all__
__all__ += epanechnikov.__all__
__all__ += quartic.__all__
__all__ += bisquare.__all__
__all__ += gaussian.__all__
