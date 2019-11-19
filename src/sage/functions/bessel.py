r"""
Bessel Functions

This module provides symbolic Bessel and Hankel functions, and their
spherical versions. These functions use the `mpmath library`_ for numerical
evaluation and Maxima, GiNaC, Pynac for symbolics.

The main objects which are exported from this module are:

 * :meth:`bessel_J(n, x) <Function_Bessel_J>` -- The Bessel J function
 * :meth:`bessel_Y(n, x) <Function_Bessel_Y>` -- The Bessel Y function
 * :meth:`bessel_I(n, x) <Function_Bessel_I>` -- The Bessel I function
 * :meth:`bessel_K(n, x) <Function_Bessel_K>` -- The Bessel K function
 * :meth:`Bessel(...) <Bessel>`   -- A factory function for producing Bessel functions of
   various kinds and orders
 * :meth:`hankel1(nu, z) <Function_Hankel1>`  -- The Hankel function of the first kind
 * :meth:`hankel2(nu, z) <Function_Hankel2>`  -- The Hankel function of the second kind
 * :meth:`struve_H(nu, z) <Function_Struve_H>`  -- The Struve function
 * :meth:`struve_L(nu, z) <Function_Struve_L>`  -- The modified Struve function
 * :meth:`spherical_bessel_J(n, z) <SphericalBesselJ>` -- The Spherical Bessel J function
 * :meth:`spherical_bessel_Y(n, z) <SphericalBesselY>` -- The Spherical Bessel J function
 * :meth:`spherical_hankel1(n, z) <SphericalHankel1>` -- The Spherical Hankel function of the first kind
 * :meth:`spherical_hankel2(n, z) <SphericalHankel2>` -- The Spherical Hankel function of the second kind

-  Bessel functions, first defined by the Swiss mathematician
   Daniel Bernoulli and named after Friedrich Bessel, are canonical
   solutions y(x) of Bessel's differential equation:

   .. MATH::

         x^2 \frac{d^2 y}{dx^2} + x \frac{dy}{dx} + \left(x^2 - \nu^2\right)y =
         0,

   for an arbitrary complex number `\nu` (the order).

-  In this module, `J_\nu` denotes the unique solution of Bessel's equation
   which is non-singular at `x = 0`. This function is known as the Bessel
   Function of the First Kind. This function also arises as a special case
   of the hypergeometric function `{}_0F_1`:

   .. MATH::

        J_\nu(x) = \frac{x^n}{2^\nu \Gamma(\nu + 1)} {}_0F_1(\nu +
        1, -\frac{x^2}{4}).

-  The second linearly independent solution to Bessel's equation (which is
   singular at `x=0`) is denoted by `Y_\nu` and is called the Bessel
   Function of the Second Kind:

   .. MATH::

        Y_\nu(x) = \frac{ J_\nu(x) \cos(\pi \nu) -
        J_{-\nu}(x)}{\sin(\pi \nu)}.

-  There are also two commonly used combinations of the Bessel J and Y
   Functions. The Bessel I Function, or the Modified Bessel Function of the
   First Kind, is defined by:

   .. MATH::

       I_\nu(x) = i^{-\nu} J_\nu(ix).

   The Bessel K Function, or the Modified Bessel Function of the Second Kind,
   is defined by:

   .. MATH::

       K_\nu(x) = \frac{\pi}{2} \cdot \frac{I_{-\nu}(x) -
       I_n(x)}{\sin(\pi \nu)}.

   We should note here that the above formulas for Bessel Y and K functions
   should be understood as limits when `\nu` is an integer.

-  It follows from Bessel's differential equation that the derivative of
   `J_n(x)` with respect to `x` is:

   .. MATH::

       \frac{d}{dx} J_n(x) = \frac{1}{x^n} \left(x^n J_{n-1}(x) - n x^{n-1}
       J_n(z) \right)

-  Another important formulation of the two linearly independent
   solutions to Bessel's equation are the Hankel functions
   `H_\nu^{(1)}(x)` and `H_\nu^{(2)}(x)`,
   defined by:

   .. MATH::

         H_\nu^{(1)}(x) = J_\nu(x) + i Y_\nu(x)

   .. MATH::

         H_\nu^{(2)}(x) = J_\nu(x) - i Y_\nu(x)

   where `i` is the imaginary unit (and `J_*` and
   `Y_*` are the usual J- and Y-Bessel functions). These
   linear combinations are also known as Bessel functions of the third
   kind; they are also two linearly independent solutions of Bessel's
   differential equation. They are named for Hermann Hankel.

-  When solving for separable solutions of Laplace's equation in
   spherical coordinates, the radial equation has the form:

   .. MATH::

         x^2 \frac{d^2 y}{dx^2} + 2x \frac{dy}{dx} + [x^2 - n(n+1)]y = 0.

   The spherical Bessel functions `j_n` and `y_n`,
   are two linearly independent solutions to this equation. They are
   related to the ordinary Bessel functions `J_n` and
   `Y_n` by:

   .. MATH::

         j_n(x) = \sqrt{\frac{\pi}{2x}} J_{n+1/2}(x),

   .. MATH::

         y_n(x) = \sqrt{\frac{\pi}{2x}} Y_{n+1/2}(x) = (-1)^{n+1} \sqrt{\frac{\pi}{2x}} J_{-n-1/2}(x).

EXAMPLES:

    Evaluate the Bessel J function symbolically and numerically::

        sage: bessel_J(0, x)
        bessel_J(0, x)
        sage: bessel_J(0, 0)
        1
        sage: bessel_J(0, x).diff(x)
        -1/2*bessel_J(1, x) + 1/2*bessel_J(-1, x)

        sage: N(bessel_J(0, 0), digits = 20)
        1.0000000000000000000
        sage: find_root(bessel_J(0,x), 0, 5)
        2.404825557695773

    Plot the Bessel J function::

        sage: f(x) = Bessel(0)(x); f
        x |--> bessel_J(0, x)
        sage: plot(f, (x, 1, 10))
        Graphics object consisting of 1 graphics primitive

    Visualize the Bessel Y function on the complex plane
    (set plot_points to a higher value to get more detail)::

        sage: complex_plot(bessel_Y(0, x), (-5, 5), (-5, 5), plot_points=20)
        Graphics object consisting of 1 graphics primitive

    Evaluate a combination of Bessel functions::

        sage: f(x) = bessel_J(1, x) - bessel_Y(0, x)
        sage: f(pi)
        bessel_J(1, pi) - bessel_Y(0, pi)
        sage: f(pi).n()
        -0.0437509653365599
        sage: f(pi).n(digits=50)
        -0.043750965336559909054985168023342675387737118378169

    Symbolically solve a second order differential equation with initial
    conditions `y(1) = a` and `y'(1) = b` in terms of Bessel functions::

        sage: y = function('y')(x)
        sage: a, b = var('a, b')
        sage: diffeq = x^2*diff(y,x,x) + x*diff(y,x) + x^2*y == 0
        sage: f = desolve(diffeq, y, [1, a, b]); f
        (a*bessel_Y(1, 1) + b*bessel_Y(0, 1))*bessel_J(0, x)/(bessel_J(0,
        1)*bessel_Y(1, 1) - bessel_J(1, 1)*bessel_Y(0, 1)) -
        (a*bessel_J(1, 1) + b*bessel_J(0, 1))*bessel_Y(0, x)/(bessel_J(0,
        1)*bessel_Y(1, 1) - bessel_J(1, 1)*bessel_Y(0, 1))


    For more examples, see the docstring for :meth:`Bessel`.

AUTHORS:

    - Some of the documentation here has been adapted from David Joyner's
      original documentation of Sage's special functions module (2006).

REFERENCES:

- [AS-Bessel]_

- [AS-Spherical]_

- [AS-Struve]_

- [DLMF-Bessel]_

- [DLMF-Struve]_

.. _`mpmath library`: http://mpmath.org

- [WP-Bessel]_

- [WP-Struve]_
"""
# ****************************************************************************
#       Copyright (C) 2013 Benjamin Jones <benjaminfjones@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  https://www.gnu.org/licenses/
# ****************************************************************************
from __future__ import print_function

from sage.functions.other import sqrt
from sage.functions.log import exp
from sage.functions.hyperbolic import sinh, cosh
from sage.functions.trig import sin, cos
from sage.libs.mpmath import utils as mpmath_utils
from sage.misc.latex import latex
from sage.rings.all import Integer, ZZ, QQ
from sage.structure.element import get_coercion_model
from sage.symbolic.constants import pi
from sage.symbolic.ring import SR
from sage.symbolic.function import BuiltinFunction
from sage.symbolic.expression import Expression


class Function_Bessel_J(BuiltinFunction):
    r"""
    The Bessel J Function, denoted by bessel_J(`\nu`, x) or `J_\nu(x)`.
    As a Taylor series about `x=0` it is equal to:

    .. MATH::

        J_\nu(x) = \sum_{k=0}^\infty \frac{(-1)^k}{k! \Gamma(k+\nu+1)}
        \left(\frac{x}{2}\right)^{2k+\nu}

    The parameter `\nu` is called the order and may be any real or
    complex number; however, integer and half-integer values are most
    common. It is defined for all complex numbers `x` when `\nu`
    is an integer or greater than zero and it diverges as `x \to 0`
    for negative non-integer values of `\nu`.

    For integer orders `\nu = n` there is an integral representation:

    .. MATH::

        J_n(x) = \frac{1}{\pi} \int_0^\pi \cos(n t - x \sin(t)) \; dt

    This function also arises as a special case of the hypergeometric
    function `{}_0F_1`:

    .. MATH::

        J_\nu(x) = \frac{x^n}{2^\nu \Gamma(\nu + 1)} {}_0F_1\left(\nu +
        1, -\frac{x^2}{4}\right).

    EXAMPLES::

        sage: bessel_J(1.0, 1.0)
        0.440050585744933
        sage: bessel_J(2, I).n(digits=30)
        -0.135747669767038281182852569995

        sage: bessel_J(1, x)
        bessel_J(1, x)
        sage: n = var('n')
        sage: bessel_J(n, x)
        bessel_J(n, x)

    Examples of symbolic manipulation::

        sage: a = bessel_J(pi, bessel_J(1, I)); a
        bessel_J(pi, bessel_J(1, I))
        sage: N(a, digits=20)
        0.00059023706363796717363 - 0.0026098820470081958110*I

        sage: f = bessel_J(2, x)
        sage: f.diff(x)
        -1/2*bessel_J(3, x) + 1/2*bessel_J(1, x)

    Comparison to a well-known integral representation of `J_1(1)`::

        sage: A = numerical_integral(1/pi*cos(x - sin(x)), 0, pi)
        sage: A[0]  # abs tol 1e-14
        0.44005058574493355
        sage: bessel_J(1.0, 1.0) - A[0] < 1e-15
        True

    Integration is supported directly and through Maxima::

        sage: f = bessel_J(2, x)
        sage: f.integrate(x)
        1/24*x^3*hypergeometric((3/2,), (5/2, 3), -1/4*x^2)
        sage: m = maxima(bessel_J(2, x))
        sage: m.integrate(x)
        (hypergeometric([3/2],[5/2,3],-_SAGE_VAR_x^2/4)*_SAGE_VAR_x^3)/24

    Visualization (set plot_points to a higher value to get more detail)::

        sage: plot(bessel_J(1,x), (x,0,5), color='blue')
        Graphics object consisting of 1 graphics primitive
        sage: complex_plot(bessel_J(1, x), (-5, 5), (-5, 5), plot_points=20)
        Graphics object consisting of 1 graphics primitive

    ALGORITHM:

        Numerical evaluation is handled by the mpmath library. Symbolics are
        handled by a combination of Maxima and Sage (Ginac/Pynac).

    Check whether the return value is real whenever the argument is real (:trac:`10251`)::

        sage: bessel_J(5, 1.5) in RR
        True

    REFERENCES:

    - [AS-Bessel]_

    - [DLMF-Bessel]_

    - [AS-Bessel]_
    """
    def __init__(self):
        """
        See the docstring for :meth:`Function_Bessel_J`.

        EXAMPLES::

            sage: sage.functions.bessel.Function_Bessel_J()
            bessel_J
            sage: bessel_J(x, x)._sympy_()
            besselj(x, x)
        """
        BuiltinFunction.__init__(self, 'bessel_J', nargs=2,
                                 conversions=dict(mathematica='BesselJ',
                                                  maxima='bessel_j',
                                                  sympy='besselj',
                                                  fricas='besselJ',
                                                  giac='BesselJ'))

    def _eval_(self, n, x):
        """
        EXAMPLES::

            sage: n = var('n')
            sage: bessel_J(0, 0)
            1
            sage: bessel_J(I, 0)
            bessel_J(I, 0)
            sage: bessel_J(5/2, 0)
            0
            sage: bessel_J(-5/2, 0)
            Infinity
            sage: bessel_J(1/2, x)
            sqrt(2)*sqrt(1/(pi*x))*sin(x)
            sage: bessel_J(-1/2, x)
            sqrt(2)*sqrt(1/(pi*x))*cos(x)
            sage: bessel_J(n, 0)
            bessel_J(n, 0)
        """
        from sage.rings.infinity import unsigned_infinity
        if not isinstance(x, Expression) and x == 0:
            if n == 0:
                return ZZ(1)
            elif n.real() > 0 or n in ZZ:
                return ZZ(0)
            elif n.real() < 0:
                return unsigned_infinity
        if n == QQ(1)/2:
            return sqrt(2/pi/x) * sin(x)
        elif n == QQ(-1)/2:
            return sqrt(2/pi/x) * cos(x)

    def _evalf_(self, n, x, parent=None, algorithm=None):
        """
        EXAMPLES::

            sage: bessel_J(0.0, 1.0)
            0.765197686557967
            sage: bessel_J(0, 1).n(digits=20)
            0.76519768655796655145
            sage: bessel_J(0.5, 1.5)
            0.649838074753747

        Check for correct rounding (:trac:`17122`)::

            sage: R = RealField(113)
            sage: a = R("8.935761195587725798762818805462843676e-01")
            sage: aa = RealField(200)(a)
            sage: for n in [-10..10]:
            ....:     b = bessel_J(R(n), a)
            ....:     bb = R(bessel_J(n, aa))
            ....:     if b != bb:
            ....:         print((n, b-bb))
        """
        if parent is not None:
            x = parent(x)

        try:
            return x.jn(Integer(n))
        except Exception:
            pass

        n, x = get_coercion_model().canonical_coercion(n, x)
        import mpmath
        return mpmath_utils.call(mpmath.besselj, n, x, parent=parent)

    def _derivative_(self, n, x, diff_param):
        """
        Return the derivative of the Bessel J function.

        EXAMPLES::

            sage: f(z) = bessel_J(10, z)
            sage: derivative(f, z)
            z |--> -1/2*bessel_J(11, z) + 1/2*bessel_J(9, z)
            sage: nu = var('nu')
            sage: bessel_J(nu, z).diff(nu)
            Traceback (most recent call last):
            ...
            NotImplementedError: derivative with respect to order

        """
        if diff_param == 1:
            return (bessel_J(n - 1, x) - bessel_J(n + 1, x)) / Integer(2)
        else:
            raise NotImplementedError('derivative with respect to order')

    def _print_latex_(self, n, z):
        """
        Custom ``_print_latex_`` method.

        EXAMPLES::

            sage: latex(bessel_J(1, x))
            J_{1}(x)
        """
        return r"J_{%s}(%s)" % (latex(n), latex(z))

bessel_J = Function_Bessel_J()


class Function_Bessel_Y(BuiltinFunction):
    r"""
    The Bessel Y functions, also known as the Bessel functions of the second
    kind, Weber functions, or Neumann functions.

    `Y_\nu(z)` is a holomorphic function of `z` on the complex plane,
    cut along the negative real axis. It is singular at `z = 0`. When `z`
    is fixed, `Y_\nu(z)` is an entire function of the order `\nu`.

    DEFINITION:

    .. MATH::

        Y_n(z) = \frac{J_\nu(z) \cos(\nu z) -
        J_{-\nu}(z)}{\sin(\nu z)}

    Its derivative with respect to `z` is:

    .. MATH::

        \frac{d}{dz} Y_n(z) = \frac{1}{z^n} \left(z^n Y_{n-1}(z) - n z^{n-1}
        Y_n(z) \right)

    EXAMPLES::

        sage: bessel_Y(1, x)
        bessel_Y(1, x)
        sage: bessel_Y(1.0, 1.0)
        -0.781212821300289
        sage: n = var('n')
        sage: bessel_Y(n, x)
        bessel_Y(n, x)
        sage: bessel_Y(2, I).n()
        1.03440456978312 - 0.135747669767038*I
        sage: bessel_Y(0, 0).n()
        -infinity
        sage: bessel_Y(0, 1).n(128)
        0.088256964215676957982926766023515162828

    Examples of symbolic manipulation::

        sage: a = bessel_Y(pi, bessel_Y(1, I)); a
        bessel_Y(pi, bessel_Y(1, I))
        sage: N(a, digits=20)
        4.2059146571791095708 + 21.307914215321993526*I

        sage: f = bessel_Y(2, x)
        sage: f.diff(x)
        -1/2*bessel_Y(3, x) + 1/2*bessel_Y(1, x)

    High precision and complex valued inputs (see :trac:`4230`)::

        sage: bessel_Y(0, 1).n(128)
        0.088256964215676957982926766023515162828
        sage: bessel_Y(0, RealField(200)(1))
        0.088256964215676957982926766023515162827817523090675546711044
        sage: bessel_Y(0, ComplexField(200)(0.5+I))
        0.077763160184438051408593468823822434235010300228009867784073 + 1.0142336049916069152644677682828326441579314239591288411739*I

    Visualization (set plot_points to a higher value to get more detail)::

        sage: plot(bessel_Y(1,x), (x,0,5), color='blue')
        Graphics object consisting of 1 graphics primitive
        sage: complex_plot(bessel_Y(1, x), (-5, 5), (-5, 5), plot_points=20)
        Graphics object consisting of 1 graphics primitive

    ALGORITHM:

        Numerical evaluation is handled by the mpmath library. Symbolics are
        handled by a combination of Maxima and Sage (Ginac/Pynac).

    TESTS:

    Check whether the return value is real whenever the argument is real (:trac:`10251`)::

        sage: bessel_Y(5, 1.5) in RR
        True

    Coercion works correctly (see :trac:`17130`)::

        sage: r = bessel_Y(RealField(200)(1), 1.0); r
        -0.781212821300289
        sage: parent(r)
        Real Field with 53 bits of precision
        sage: r = bessel_Y(RealField(200)(1), 1); r
        -0.78121282130028871654715000004796482054990639071644460784383
        sage: parent(r)
        Real Field with 200 bits of precision

    REFERENCES:

    - [AS-Bessel]_

    - [DLMF-Bessel]_

    - [WP-Bessel]_
    """
    def __init__(self):
        """
        See the docstring for :meth:`Function_Bessel_Y`.

        EXAMPLES::

            sage: sage.functions.bessel.Function_Bessel_Y()(0, x)
            bessel_Y(0, x)
            sage: bessel_Y(x, x)._sympy_()
            bessely(x, x)
        """
        BuiltinFunction.__init__(self, 'bessel_Y', nargs=2,
                                 conversions=dict(mathematica='BesselY',
                                                  maxima='bessel_y',
                                                  sympy='bessely',
                                                  fricas='besselY',
                                                  giac='BesselY'))

    def _eval_(self, n, x):
        """
        EXAMPLES::

            sage: bessel_Y(1, 0)
            Infinity
            sage: bessel_Y(I,0)
            bessel_Y(I, 0)
            sage: bessel_Y(1/2, x)
            -sqrt(2)*sqrt(1/(pi*x))*cos(x)
            sage: bessel_Y(-1/2, x)
            sqrt(2)*sqrt(1/(pi*x))*sin(x)

        TESTS::

            sage: bessel_Y(0, 0)
            -Infinity
        """
        from sage.rings.infinity import infinity, unsigned_infinity
        if not isinstance(x, Expression) and x == 0:
            if n == 0:
                return -infinity
            elif n.real() > 0 or n.real() < 0:
                return unsigned_infinity
        if n == QQ(1)/2:
            return -sqrt(2/pi/x) * cos(x)
        elif n == QQ(-1)/2:
            return sqrt(2/pi/x) * sin(x)

    def _evalf_(self, n, x, parent=None, algorithm=None):
        """
        EXAMPLES::

            sage: bessel_Y(0.5, 1.5)
            -0.0460831658930974
            sage: bessel_Y(1.0+2*I, 3.0+4*I)
            0.699410324467538 + 0.228917940896421*I
            sage: bessel_Y(0, 1).n(256)
            0.08825696421567695798292676602351516282781752309067554671104384761199978932351

        Check for correct rounding (:trac:`17122`)::

            sage: R = RealField(113)
            sage: a = R("8.935761195587725798762818805462843676e-01")
            sage: aa = RealField(200)(a)
            sage: for n in [-10..10]:
            ....:     b = bessel_Y(R(n), a)
            ....:     bb = R(bessel_Y(n, aa))
            ....:     if b != bb:
            ....:         print((n, b-bb))
        """
        if parent is not None:
            x = parent(x)

        try:
            return x.yn(Integer(n))
        except Exception:
            pass

        n, x = get_coercion_model().canonical_coercion(n, x)
        import mpmath
        return mpmath_utils.call(mpmath.bessely, n, x, parent=parent)

    def _derivative_(self, n, x, diff_param):
        """
        Return the derivative of the Bessel Y function.

        EXAMPLES::

            sage: f(x) = bessel_Y(10, x)
            sage: derivative(f, x)
            x |--> -1/2*bessel_Y(11, x) + 1/2*bessel_Y(9, x)
            sage: nu = var('nu')
            sage: bessel_Y(nu, x).diff(nu)
            Traceback (most recent call last):
            ...
            NotImplementedError: derivative with respect to order
        """
        if diff_param == 1:
            return (bessel_Y(n - 1, x) - bessel_Y(n + 1, x)) / Integer(2)
        else:
            raise NotImplementedError('derivative with respect to order')

    def _print_latex_(self, n, z):
        """
        Custom ``_print_latex_`` method.

        EXAMPLES::

            sage: latex(bessel_Y(1, x))
            Y_{1}(x)
        """
        return r"Y_{%s}(%s)" % (latex(n), latex(z))

bessel_Y = Function_Bessel_Y()


class Function_Bessel_I(BuiltinFunction):
    r"""
    The Bessel I function, or the Modified Bessel Function of the First Kind.

    DEFINITION:

    .. MATH::

        I_\nu(x) = i^{-\nu} J_\nu(ix)

    EXAMPLES::

        sage: bessel_I(1, x)
        bessel_I(1, x)
        sage: bessel_I(1.0, 1.0)
        0.565159103992485
        sage: n = var('n')
        sage: bessel_I(n, x)
        bessel_I(n, x)
        sage: bessel_I(2, I).n()
        -0.114903484931900

    Examples of symbolic manipulation::

        sage: a = bessel_I(pi, bessel_I(1, I))
        sage: N(a, digits=20)
        0.00026073272117205890524 - 0.0011528954889080572268*I

        sage: f = bessel_I(2, x)
        sage: f.diff(x)
        1/2*bessel_I(3, x) + 1/2*bessel_I(1, x)

    Special identities that bessel_I satisfies::

        sage: bessel_I(1/2, x)
        sqrt(2)*sqrt(1/(pi*x))*sinh(x)
        sage: eq = bessel_I(1/2, x) == bessel_I(0.5, x)
        sage: eq.test_relation()
        True
        sage: bessel_I(-1/2, x)
        sqrt(2)*sqrt(1/(pi*x))*cosh(x)
        sage: eq = bessel_I(-1/2, x) == bessel_I(-0.5, x)
        sage: eq.test_relation()
        True

    Examples of asymptotic behavior::

        sage: limit(bessel_I(0, x), x=oo)
        +Infinity
        sage: limit(bessel_I(0, x), x=0)
        1

    High precision and complex valued inputs::

        sage: bessel_I(0, 1).n(128)
        1.2660658777520083355982446252147175376
        sage: bessel_I(0, RealField(200)(1))
        1.2660658777520083355982446252147175376076703113549622068081
        sage: bessel_I(0, ComplexField(200)(0.5+I))
        0.80644357583493619472428518415019222845373366024179916785502 + 0.22686958987911161141397453401487525043310874687430711021434*I

    Visualization (set plot_points to a higher value to get more detail)::

        sage: plot(bessel_I(1,x), (x,0,5), color='blue')
        Graphics object consisting of 1 graphics primitive
        sage: complex_plot(bessel_I(1, x), (-5, 5), (-5, 5), plot_points=20)
        Graphics object consisting of 1 graphics primitive

    ALGORITHM:

        Numerical evaluation is handled by the mpmath library. Symbolics are
        handled by a combination of Maxima and Sage (Ginac/Pynac).

    TESTS::

        sage: N(bessel_I(1,1),500)
        0.565159103992485027207696027609863307328899621621092009480294489479255640964371134092664997766814410064677886055526302676857637684917179812041131208121

    Check whether the return value is real whenever the argument is real (:trac:`10251`)::

        sage: bessel_I(5, 1.5) in RR
        True

    REFERENCES:

    - [AS-Bessel]_

    - [DLMF-Bessel]_

    - [WP-Bessel]_
    """
    def __init__(self):
        """
        See the docstring for :meth:`Function_Bessel_I`.

        EXAMPLES::

            sage: bessel_I(1,x)
            bessel_I(1, x)
            sage: bessel_I(x, x)._sympy_()
            besseli(x, x)
        """
        BuiltinFunction.__init__(self, 'bessel_I', nargs=2,
                                 conversions=dict(mathematica='BesselI',
                                                  maxima='bessel_i',
                                                  sympy='besseli',
                                                  fricas='besselI'))

    def _eval_(self, n, x):
        """
        EXAMPLES::

            sage: n,y = var('n,y')
            sage: bessel_I(y, x)
            bessel_I(y, x)
            sage: bessel_I(0, 0)
            1
            sage: bessel_I(7/2, 0)
            0
            sage: bessel_I(-7/2, 0)
            Infinity
            sage: bessel_I(1/2, 1)
            sqrt(2)*sinh(1)/sqrt(pi)
            sage: bessel_I(-1/2, pi)
            sqrt(2)*cosh(pi)/pi
            sage: bessel_I(n, 0)
            bessel_I(n, 0)
        """
        from sage.rings.infinity import unsigned_infinity
        if not isinstance(x, Expression) and x == 0:
            if n == 0:
                return ZZ(1)
            elif n.real() > 0 or n in ZZ:
                return ZZ(0)
            elif n.real() < 0:
                return unsigned_infinity
        if n == QQ(1)/2:
            return sqrt(2 / (pi * x)) * sinh(x)
        elif n == -QQ(1)/2:
            return sqrt(2 / (pi * x)) * cosh(x)


    def _evalf_(self, n, x, parent=None, algorithm=None):
        """
        EXAMPLES::

            sage: bessel_I(0.0, 1.0)
            1.26606587775201
            sage: bessel_I(1,3).n(digits=20)
            3.9533702174026093965
        """
        import mpmath
        return mpmath_utils.call(mpmath.besseli, n, x, parent=parent)

    def _derivative_(self, n, x, diff_param):
        """
        Return the derivative of the Bessel I function `I_n(x)` with respect
        to `x`.

        EXAMPLES::

            sage: f(z) = bessel_I(10, x)
            sage: derivative(f, x)
            z |--> 1/2*bessel_I(11, x) + 1/2*bessel_I(9, x)
            sage: nu = var('nu')
            sage: bessel_I(nu, x).diff(nu)
            Traceback (most recent call last):
            ...
            NotImplementedError: derivative with respect to order
        """
        if diff_param == 1:
            return (bessel_I(n - 1, x) + bessel_I(n + 1, x)) / Integer(2)
        else:
            raise NotImplementedError('derivative with respect to order')

    def _print_latex_(self, n, z):
        """
        Custom ``_print_latex_`` method.

        EXAMPLES::

            sage: latex(bessel_I(1, x))
            I_{1}(x)
        """
        return r"I_{%s}(%s)" % (latex(n), latex(z))

bessel_I = Function_Bessel_I()


class Function_Bessel_K(BuiltinFunction):
    r"""
    The Bessel K function, or the modified Bessel function of the second kind.

    DEFINITION:

    .. MATH::

        K_\nu(x) = \frac{\pi}{2} \frac{I_{-\nu}(x)-I_\nu(x)}{\sin(\nu \pi)}

    EXAMPLES::

        sage: bessel_K(1, x)
        bessel_K(1, x)
        sage: bessel_K(1.0, 1.0)
        0.601907230197235
        sage: n = var('n')
        sage: bessel_K(n, x)
        bessel_K(n, x)
        sage: bessel_K(2, I).n()
        -2.59288617549120 + 0.180489972066962*I

    Examples of symbolic manipulation::

        sage: a = bessel_K(pi, bessel_K(1, I)); a
        bessel_K(pi, bessel_K(1, I))
        sage: N(a, digits=20)
        3.8507583115005220156 + 0.068528298579883425456*I

        sage: f = bessel_K(2, x)
        sage: f.diff(x)
        -1/2*bessel_K(3, x) - 1/2*bessel_K(1, x)

        sage: bessel_K(1/2, x)
        sqrt(1/2)*sqrt(pi)*e^(-x)/sqrt(x)
        sage: bessel_K(1/2, -1)
        -I*sqrt(1/2)*sqrt(pi)*e
        sage: bessel_K(1/2, 1)
        sqrt(1/2)*sqrt(pi)*e^(-1)

    Examples of asymptotic behavior::

        sage: bessel_K(0, 0.0)
        +infinity
        sage: limit(bessel_K(0, x), x=0)
        +Infinity
        sage: limit(bessel_K(0, x), x=oo)
        0

    High precision and complex valued inputs::

        sage: bessel_K(0, 1).n(128)
        0.42102443824070833333562737921260903614
        sage: bessel_K(0, RealField(200)(1))
        0.42102443824070833333562737921260903613621974822666047229897
        sage: bessel_K(0, ComplexField(200)(0.5+I))
        0.058365979093103864080375311643360048144715516692187818271179 - 0.67645499731334483535184142196073004335768129348518210260256*I

    Visualization (set plot_points to a higher value to get more detail)::

        sage: plot(bessel_K(1,x), (x,0,5), color='blue')
        Graphics object consisting of 1 graphics primitive
        sage: complex_plot(bessel_K(1, x), (-5, 5), (-5, 5), plot_points=20)
        Graphics object consisting of 1 graphics primitive

    ALGORITHM:

        Numerical evaluation is handled by the mpmath library. Symbolics are
        handled by a combination of Maxima and Sage (Ginac/Pynac).

    TESTS:

    Verify that :trac:`3426` is fixed:

    The Bessel K function can be evaluated numerically at complex orders::

        sage: bessel_K(10 * I, 10).n()
        9.82415743819925e-8

    For a fixed imaginary order and increasing, real, second component the
    value of Bessel K is exponentially decaying::

        sage: for x in [10, 20, 50, 100, 200]: print(bessel_K(5*I, x).n())
        5.27812176514912e-6
        3.11005908421801e-10
        2.66182488515423e-23 - 8.59622057747552e-58*I
        4.11189776828337e-45 - 1.01494840019482e-80*I
        1.15159692553603e-88 - 6.75787862113718e-125*I

    Check whether the return value is real whenever the argument is real (:trac:`10251`)::

        sage: bessel_K(5, 1.5) in RR
        True

    REFERENCES:

    - [AS-Bessel]_

    - [DLMF-Bessel]_

    - [WP-Bessel]_
    """
    def __init__(self):
        """
        See the docstring for :meth:`Function_Bessel_K`.

        EXAMPLES::

            sage: sage.functions.bessel.Function_Bessel_K()
            bessel_K
            sage: bessel_K(x, x)._sympy_()
            besselk(x, x)
        """
        BuiltinFunction.__init__(self, 'bessel_K', nargs=2,
                                 conversions=dict(mathematica='BesselK',
                                                  maxima='bessel_k',
                                                  sympy='besselk',
                                                  fricas='besselK'))

    def _eval_(self, n, x):
        """
        EXAMPLES::

            sage: n = var('n')
            sage: bessel_K(1, 0)
            Infinity
            sage: bessel_K(1/2, x)
            sqrt(1/2)*sqrt(pi)*e^(-x)/sqrt(x)
            sage: bessel_K(n, 0)
            bessel_K(n, 0)

        TESTS::

            sage: bessel_K(0, 0)
            +Infinity
        """
        from sage.rings.infinity import infinity, unsigned_infinity
        if not isinstance(x, Expression) and x == 0:
            if n == 0:
                return infinity
            elif n.real() > 0 or n.real() < 0:
                return unsigned_infinity
        if n == QQ(1)/2 or n == -QQ(1)/2 and x > 0:
            return sqrt(pi / 2) * exp(-x) * x ** (-Integer(1) / Integer(2))


    def _evalf_(self, n, x, parent=None, algorithm=None):
        """
        EXAMPLES::

            sage: bessel_K(0.0, 1.0)
            0.421024438240708
            sage: bessel_K(-1, 1).n(128)
            0.60190723019723457473754000153561733926
            sage: bessel_K(0, RealField(128)(1))
            0.42102443824070833333562737921260903614
        """
        import mpmath
        return mpmath_utils.call(mpmath.besselk, n, x, parent=parent)

    def _derivative_(self, n, x, diff_param):
        """
        Return the derivative of the Bessel K function.

        EXAMPLES::

            sage: f(x) = bessel_K(10, x)
            sage: derivative(f, x)
            x |--> -1/2*bessel_K(11, x) - 1/2*bessel_K(9, x)
            sage: nu = var('nu')
            sage: bessel_K(nu, x).diff(nu)
            Traceback (most recent call last):
            ...
            NotImplementedError: derivative with respect to order
        """
        if diff_param == 1:
            return -(bessel_K(n - 1, x) + bessel_K(n + 1, x)) / Integer(2)
        else:
            raise NotImplementedError('derivative with respect to order')

    def _print_latex_(self, n, z):
        """
        Custom ``_print_latex_`` method.

        EXAMPLES::

            sage: latex(bessel_K(1, x))
            K_{1}(x)
        """
        return r"K_{%s}(%s)" % (latex(n), latex(z))

bessel_K = Function_Bessel_K()


# dictionary used in Bessel
bessel_type_dict = {'I': bessel_I, 'J': bessel_J, 'K': bessel_K, 'Y': bessel_Y}


def Bessel(*args, **kwds):
    """
    A function factory that produces symbolic I, J, K, and Y Bessel functions.
    There are several ways to call this function:

        - ``Bessel(order, type)``
        - ``Bessel(order)`` -- type defaults to 'J'
        - ``Bessel(order, typ=T)``
        - ``Bessel(typ=T)`` -- order is unspecified, this is a 2-parameter
          function
        - ``Bessel()`` -- order is unspecified, type is 'J'

    where ``order`` can be any integer and T must be one of the strings 'I',
    'J', 'K', or 'Y'.

    See the EXAMPLES below.

    EXAMPLES:

    Construction of Bessel functions with various orders and types::

        sage: Bessel()
        bessel_J
        sage: Bessel(1)(x)
        bessel_J(1, x)
        sage: Bessel(1, 'Y')(x)
        bessel_Y(1, x)
        sage: Bessel(-2, 'Y')(x)
        bessel_Y(-2, x)
        sage: Bessel(typ='K')
        bessel_K
        sage: Bessel(0, typ='I')(x)
        bessel_I(0, x)

    Evaluation::

        sage: f = Bessel(1)
        sage: f(3.0)
        0.339058958525936
        sage: f(3)
        bessel_J(1, 3)
        sage: f(3).n(digits=50)
        0.33905895852593645892551459720647889697308041819801

        sage: g = Bessel(typ='J')
        sage: g(1,3)
        bessel_J(1, 3)
        sage: g(2, 3+I).n()
        0.634160370148554 + 0.0253384000032695*I
        sage: abs(numerical_integral(1/pi*cos(3*sin(x)), 0.0, pi)[0] - Bessel(0, 'J')(3.0)) < 1e-15
        True

    Symbolic calculus::

        sage: f(x) = Bessel(0, 'J')(x)
        sage: derivative(f, x)
        x |--> -1/2*bessel_J(1, x) + 1/2*bessel_J(-1, x)
        sage: derivative(f, x, x)
        x |--> 1/4*bessel_J(2, x) - 1/2*bessel_J(0, x) + 1/4*bessel_J(-2, x)

    Verify that `J_0` satisfies Bessel's differential equation numerically
    using the ``test_relation()`` method::

        sage: y = bessel_J(0, x)
        sage: diffeq = x^2*derivative(y,x,x) + x*derivative(y,x) + x^2*y == 0
        sage: diffeq.test_relation(proof=False)
        True

    Conversion to other systems::

        sage: x,y = var('x,y')
        sage: f = maxima(Bessel(typ='K')(x,y))
        sage: f.derivative('_SAGE_VAR_x')
        (%pi*csc(%pi*_SAGE_VAR_x)*('diff(bessel_i(-_SAGE_VAR_x,_SAGE_VAR_y),_SAGE_VAR_x,1)-'diff(bessel_i(_SAGE_VAR_x,_SAGE_VAR_y),_SAGE_VAR_x,1)))/2-%pi*bessel_k(_SAGE_VAR_x,_SAGE_VAR_y)*cot(%pi*_SAGE_VAR_x)
        sage: f.derivative('_SAGE_VAR_y')
        -(bessel_k(_SAGE_VAR_x+1,_SAGE_VAR_y)+bessel_k(_SAGE_VAR_x-1,_SAGE_VAR_y))/2

    Compute the particular solution to Bessel's Differential Equation that
    satisfies `y(1) = 1` and `y'(1) = 1`, then verify the initial conditions
    and plot it::

        sage: y = function('y')(x)
        sage: diffeq = x^2*diff(y,x,x) + x*diff(y,x) + x^2*y == 0
        sage: f = desolve(diffeq, y, [1, 1, 1]); f
        (bessel_Y(1, 1) + bessel_Y(0, 1))*bessel_J(0, x)/(bessel_J(0,
        1)*bessel_Y(1, 1) - bessel_J(1, 1)*bessel_Y(0, 1)) - (bessel_J(1,
        1) + bessel_J(0, 1))*bessel_Y(0, x)/(bessel_J(0, 1)*bessel_Y(1, 1)
        - bessel_J(1, 1)*bessel_Y(0, 1))
        sage: f.subs(x=1).n() # numerical verification
        1.00000000000000
        sage: fp = f.diff(x)
        sage: fp.subs(x=1).n()
        1.00000000000000

        sage: f.subs(x=1).simplify_full() # symbolic verification
        1
        sage: fp = f.diff(x)
        sage: fp.subs(x=1).simplify_full()
        1

        sage: plot(f, (x,0,5))
        Graphics object consisting of 1 graphics primitive

    Plotting::

        sage: f(x) = Bessel(0)(x); f
        x |--> bessel_J(0, x)
        sage: plot(f, (x, 1, 10))
        Graphics object consisting of 1 graphics primitive

        sage: plot([ Bessel(i, 'J') for i in range(5) ], 2, 10)
        Graphics object consisting of 5 graphics primitives

        sage: G = Graphics()
        sage: G += sum([ plot(Bessel(i), 0, 4*pi, rgbcolor=hue(sin(pi*i/10))) for i in range(5) ])
        sage: show(G)

    A recreation of Abramowitz and Stegun Figure 9.1::

        sage: G  = plot(Bessel(0, 'J'), 0, 15, color='black')
        sage: G += plot(Bessel(0, 'Y'), 0, 15, color='black')
        sage: G += plot(Bessel(1, 'J'), 0, 15, color='black', linestyle='dotted')
        sage: G += plot(Bessel(1, 'Y'), 0, 15, color='black', linestyle='dotted')
        sage: show(G, ymin=-1, ymax=1)

    """
    # Determine the order and type of function from the arguments and keywords.
    # These are recorded in local variables: _type, _order, _system, _nargs.
    _type = None
    if len(args) == 0:    # no order specified
        _order = None
        _nargs = 2
    elif len(args) == 1:  # order is specified
        _order = args[0]
        _nargs = 1
    elif len(args) == 2:  # both order and type are positional arguments
        _order = args[0]
        _type = args[1]
        _nargs = 1
    else:
        raise ValueError("Too many arguments (%s given)" % str(len(args)))

    # check for type inconsistency
    if _type is not None and 'typ' in kwds and _type != kwds['typ']:
        raise ValueError("inconsistent types given")
    # record the function type
    if _type is None:
        if 'typ' in kwds:
            _type = kwds['typ']
        else:
            _type = 'J'
    if not (_type in ['I', 'J', 'K', 'Y']):
        raise ValueError("type must be one of I, J, K, Y")

    # return the function
    _f = bessel_type_dict[_type]
    if _nargs == 1:
        return lambda x: _f(_order, x)
    else:
        return _f


class Function_Struve_H(BuiltinFunction):
    r"""
    The Struve functions, solutions to the non-homogeneous Bessel differential equation:

    .. MATH::

        x^2\frac{d^2y}{dx^2}+x\frac{dy}{dx}+(x^2-\alpha^2)y=\frac{4\bigl(\frac{x}{2}\bigr)^{\alpha+1}}{\sqrt\pi\Gamma(\alpha+\tfrac12)},

    .. MATH::

        \mathrm{H}_\alpha(x) = y(x)

    EXAMPLES::

        sage: struve_H(-1/2,x)
        sqrt(2)*sqrt(1/(pi*x))*sin(x)
        sage: struve_H(2,x)
        struve_H(2, x)
        sage: struve_H(1/2,pi).n()
        0.900316316157106

    REFERENCES:

    - [AS-Struve]_

    - [DLMF-Struve]_

    - [WP-Struve]_
    """
    def __init__(self):
        r"""
        EXAMPLES::

            sage: n = var('n')
            sage: maxima("struve_h(n,x);").sage()
            struve_H(n, x)
            sage: struve_H(7/5,1)._maxima_()
            struve_h(7/5,1)
            sage: loads(dumps(struve_H(n,x)))
            struve_H(n, x)
        """
        BuiltinFunction.__init__(self, 'struve_H', nargs=2,
                                 conversions=dict(maple='StruveH',
                                                  mathematica='StruveH',
                                                  maxima='struve_h',
                                                  fricas='struveH'))

    def _eval_(self, a, z):
        """
        EXAMPLES::

            sage: struve_H(0,0)
            0
            sage: struve_H(pi,0)
            0
            sage: struve_H(-1/2,x)
            sqrt(2)*sqrt(1/(pi*x))*sin(x)
            sage: struve_H(1/2,-1)
            -sqrt(2)*sqrt(-1/pi)*(cos(1) - 1)
            sage: struve_H(1/2,pi)
            2*sqrt(2)/pi
            sage: struve_H(2,x)
            struve_H(2, x)
            sage: struve_H(-3/2,x)
            -bessel_J(3/2, x)
        """
        from sage.symbolic.ring import SR
        if z.is_zero() \
                and (SR(a).is_numeric() or SR(a).is_constant()) \
                and a.real() >= -1:
                return ZZ(0)
        if a == -Integer(1)/2:
            from sage.functions.trig import sin
            return sqrt(2/(pi*z)) * sin(z)
        if a == Integer(1)/2:
            from sage.functions.trig import cos
            return sqrt(2/(pi*z)) * (1-cos(z))
        if a < 0 and not SR(a).is_integer() and SR(2*a).is_integer():
            from sage.rings.rational_field import QQ
            n = (a*(-2) - 1)/2
            return Integer(-1)**n * bessel_J(n+QQ(1)/2, z)

    def _evalf_(self, a, z, parent=None, algorithm=None):
        """
        EXAMPLES::

            sage: struve_H(1/2,pi).n()
            0.900316316157106
            sage: struve_H(1/2,pi).n(200)
            0.9003163161571060695551991910...
        """
        import mpmath
        return mpmath_utils.call(mpmath.struveh, a, z, parent=parent)

    def _derivative_(self, a, z, diff_param=None):
        """
        EXAMPLES::

            sage: diff(struve_H(3/2,x),x)
            -1/2*sqrt(2)*sqrt(1/(pi*x))*(cos(x) - 1) + 1/16*sqrt(2)*x^(3/2)/sqrt(pi) - 1/2*struve_H(5/2, x)
        """
        if diff_param == 0:
            raise ValueError("cannot differentiate struve_H in the first parameter")

        from .gamma import gamma
        from .other import sqrt
        return (z**a/(sqrt(pi)*2**a*gamma(a+Integer(3)/Integer(2)))-struve_H(a+1,z)+struve_H(a-1,z))/2

    def _print_latex_(self, a, z):
        """
        EXAMPLES::

            sage: latex(struve_H(2,x))
            H_{{2}}({x})
        """
        return r"H_{{%s}}({%s})" % (a, z)

struve_H = Function_Struve_H()

class Function_Struve_L(BuiltinFunction):
    r"""
    The modified Struve functions.

    .. MATH::

        \mathrm{L}_\alpha(x) = -i\cdot e^{-\frac{i\alpha\pi}{2}}\cdot\mathrm{H}_\alpha(ix)

    EXAMPLES::

        sage: struve_L(2,x)
        struve_L(2, x)
        sage: struve_L(1/2,pi).n()
        4.76805417696286
        sage: diff(struve_L(1,x),x)
        1/3*x/pi - 1/2*struve_L(2, x) + 1/2*struve_L(0, x)

    REFERENCES:

    - [AS-Struve]_

    - [DLMF-Struve]_

    - [WP-Struve]_
    """
    def __init__(self):
        r"""
        EXAMPLES::

            sage: n = var('n')
            sage: maxima("struve_l(n,x);").sage()
            struve_L(n, x)
            sage: struve_L(7/5,1)._maxima_()
            struve_l(7/5,1)
            sage: loads(dumps(struve_L(n,x)))
            struve_L(n, x)
        """
        BuiltinFunction.__init__(self, 'struve_L', nargs=2,
                                 conversions=dict(maple='StruveL',
                                                  mathematica='StruveL',
                                                  maxima='struve_l',
                                                  fricas='struveL'))

    def _eval_(self, a, z):
        """
        EXAMPLES::

            sage: struve_L(-2,0)
            struve_L(-2, 0)
            sage: struve_L(-1,0)
            0
            sage: struve_L(pi,0)
            0
            sage: struve_L(-1/2,x)
            sqrt(2)*sqrt(1/(pi*x))*sinh(x)
            sage: struve_L(1/2,1)
            sqrt(2)*(cosh(1) - 1)/sqrt(pi)
            sage: struve_L(2,x)
            struve_L(2, x)
            sage: struve_L(-3/2,x)
            -bessel_I(3/2, x)
        """
        from sage.symbolic.ring import SR
        if z.is_zero() \
                and (SR(a).is_numeric() or SR(a).is_constant()) \
                and a.real() >= -1:
                return ZZ(0)
        if a == -Integer(1)/2:
            from sage.functions.hyperbolic import sinh
            return sqrt(2/(pi*z)) * sinh(z)
        if a == Integer(1)/2:
            from sage.functions.hyperbolic import cosh
            return sqrt(2/(pi*z)) * (cosh(z)-1)
        if a < 0 and not SR(a).is_integer() and SR(2*a).is_integer():
            from sage.rings.rational_field import QQ
            n = (a*(-2) - 1)/2
            return Integer(-1)**n * bessel_I(n+QQ(1)/2, z)

    def _evalf_(self, a, z, parent=None, algorithm=None):
        """
        EXAMPLES::

            sage: struve_L(1/2,pi).n()
            4.76805417696286
            sage: struve_L(1/2,pi).n(200)
            4.768054176962864289162484345...
        """
        import mpmath
        return mpmath_utils.call(mpmath.struvel, a, z, parent=parent)

    def _derivative_(self, a, z, diff_param=None):
        """
        EXAMPLES::

            sage: diff(struve_L(1,x),x)
            1/3*x/pi - 1/2*struve_L(2, x) + 1/2*struve_L(0, x)
        """
        if diff_param == 0:
            raise ValueError("cannot differentiate struve_L in the first parameter")

        from .gamma import gamma
        from .other import sqrt
        return (z**a/(sqrt(pi)*2**a*gamma(a+Integer(3)/Integer(2)))-struve_L(a+1,z)+struve_L(a-1,z))/2

    def _print_latex_(self, a, z):
        """
            sage: latex(struve_L(2,x))
            L_{{2}}({x})
        """
        return r"L_{{%s}}({%s})" % (a, z)

struve_L = Function_Struve_L()


class Function_Hankel1(BuiltinFunction):
    r"""
    The Hankel function of the first kind

    DEFINITION:

    .. MATH::

        H_\nu^{(1)}(z) = J_{\nu}(z) + iY_{\nu}(z)

    EXAMPLES::

        sage: hankel1(3, x)
        hankel1(3, x)
        sage: hankel1(3, 4.)
        0.430171473875622 - 0.182022115953485*I
        sage: latex(hankel1(3, x))
        H_{3}^{(1)}\left(x\right)
        sage: hankel1(3., x).series(x == 2, 10).subs(x=3).n()  # abs tol 1e-12
        0.309062682819597 - 0.512591541605233*I
        sage: hankel1(3, 3.)
        0.309062722255252 - 0.538541616105032*I

    REFERENCES:

    - [AS-Bessel]_ see 9.1.6
    """
    def __init__(self):
        r"""
        TESTS::

            sage: hankel1(3, x)._sympy_()
            hankel1(3, x)
        """
        BuiltinFunction.__init__(self, 'hankel1', nargs=2,
                                 conversions=dict(maple='HankelH1',
                                                  mathematica='HankelH1',
                                                  maxima='hankel1',
                                                  sympy='hankel1',
                                                  fricas='hankelH1'))

    def _evalf_(self, nu, z, parent, algorithm=None):
        r"""
        TESTS::

            sage: hankel1(3, 3).n(100)
            0.30906272225525164361826019495 - 0.53854161610503161800470390534*I
            sage: hankel1(I, I).n()
            -0.886357449263715*I
        """
        from mpmath import hankel1
        return mpmath_utils.call(hankel1, nu, z, parent=parent)

    def _latex_(self):
        r"""
        TESTS::

            sage: latex(hankel1)
            H_{\nu}^{(1)}
        """
        return r'H_{\nu}^{(1)}'

    def _print_latex_(self, nu, z):
        r"""
        TESTS::

            sage: latex(hankel1(3, x))
            H_{3}^{(1)}\left(x\right)
        """
        return r"H_{{{}}}^{{(1)}}\left({}\right)".format(latex(nu), latex(z))

    def _derivative_(self, nu, z, diff_param):
        r"""
        TESTS::

            sage: y = var('y')
            sage: hankel1(x, y).diff(y)
            x*hankel1(x, y)/y - hankel1(x + 1, y)
        """
        if diff_param == 1:
            return (nu * hankel1(nu, z)) / z - hankel1(nu + 1, z)
        else:
            raise NotImplementedError('derivative with respect to order')

hankel1 = Function_Hankel1()


class Function_Hankel2(BuiltinFunction):
    r"""
    The Hankel function of the second kind

    DEFINITION:

    .. MATH::

        H_\nu^{(2)}(z) = J_{\nu}(z) - iY_{\nu}(z)

    EXAMPLES::

        sage: hankel2(3, x)
        hankel2(3, x)
        sage: hankel2(3, 4.)
        0.430171473875622 + 0.182022115953485*I
        sage: latex(hankel2(3, x))
        H_{3}^{(2)}\left(x\right)
        sage: hankel2(3., x).series(x == 2, 10).subs(x=3).n()  # abs tol 1e-12
        0.309062682819597 + 0.512591541605234*I
        sage: hankel2(3, 3.)
        0.309062722255252 + 0.538541616105032*I

    REFERENCES:

    - [AS-Bessel]_ see 9.1.6
    """
    def __init__(self):
        r"""
        TESTS::

            sage: hankel2(3, x)._sympy_()
            hankel2(3, x)
        """
        BuiltinFunction.__init__(self, 'hankel2', nargs=2,
                                 conversions=dict(maple='HankelH2',
                                                  mathematica='HankelH2',
                                                  maxima='hankel2',
                                                  sympy='hankel2',
                                                  fricas='hankelH2'))

    def _evalf_(self, nu, z, parent, algorithm=None):
        r"""
        TESTS::

            sage: hankel2(3, 3).n(100)
            0.30906272225525164361826019495 + 0.53854161610503161800470390534*I
            sage: hankel2(I, I).n()
            0.790274862674015 + 0.444006335520019*I
        """
        from mpmath import hankel2
        return mpmath_utils.call(hankel2, nu, z, parent=parent)

    def _latex_(self):
        r"""
        TESTS::

            sage: latex(hankel2)
            H_{\nu}^{(2)}
        """
        return r'H_{\nu}^{(2)}'

    def _print_latex_(self, nu, z):
        r"""
        TESTS::

            sage: latex(hankel2(3, x))
            H_{3}^{(2)}\left(x\right)
        """
        return r"H_{{{}}}^{{(2)}}\left({}\right)".format(latex(nu), latex(z))

    def _derivative_(self, nu, z, diff_param):
        r"""
        TESTS::

            sage: y = var('y')
            sage: hankel2(x, y).diff(y)
            -1/2*hankel2(x + 1, y) + 1/2*hankel2(x - 1, y)
        """
        if diff_param == 1:
            return (Integer(1) / 2) * (hankel2(nu - 1, z) - hankel2(nu + 1, z))
        else:
            raise NotImplementedError('derivative with respect to order')

hankel2 = Function_Hankel2()


class SphericalBesselJ(BuiltinFunction):
    r"""
    The spherical Bessel function of the first kind

    DEFINITION:

    .. MATH::

        j_n(z) = \sqrt{\frac{\pi}{2z}} \,J_{n + \frac{1}{2}}(z)

    EXAMPLES::

        sage: spherical_bessel_J(3, x)
        spherical_bessel_J(3, x)
        sage: spherical_bessel_J(3 + 0.2 * I, 3)
        0.150770999183897 - 0.0260662466510632*I
        sage: spherical_bessel_J(3, x).series(x == 2, 10).subs(x=3).n()
        0.152051648665037
        sage: spherical_bessel_J(3, 3.)
        0.152051662030533
        sage: spherical_bessel_J(2.,3.)      # rel tol 1e-10
        0.2986374970757335
        sage: spherical_bessel_J(4, x).simplify()
        -((45/x^2 - 105/x^4 - 1)*sin(x) + 5*(21/x^2 - 2)*cos(x)/x)/x
        sage: integrate(spherical_bessel_J(1,x)^2,(x,0,oo))
        1/6*pi
        sage: latex(spherical_bessel_J(4, x))
        j_{4}\left(x\right)

    REFERENCES:

    - [AS-Spherical]_

    - [DLMF-Bessel]_

    - [WP-Bessel]_
    """
    def __init__(self):
        r"""
        TESTS::

            sage: spherical_bessel_J(3, x)._sympy_()
            jn(3, x)
        """
        BuiltinFunction.__init__(self, 'spherical_bessel_J', nargs=2,
                                 conversions=dict(mathematica=
                                                  'SphericalBesselJ',
                                                  maxima='spherical_bessel_j',
                                                  sympy='jn'))

    def _evalf_(self, n, z, parent, algorithm=None):
        r"""
        TESTS::

            sage: spherical_bessel_J(3, 3).n(100)
            0.15205166203053329097480571600
            sage: spherical_bessel_J(I, I).n()
            0.215520585196889 - 0.282308805801851*I
        """
        return mpmath_utils.call(spherical_bessel_f, 'besselj', n, z,
                                 parent=parent)

    def _latex_(self):
        r"""
        TESTS::

            sage: latex(spherical_bessel_J)
            j_n
        """
        return r'j_n'

    def _print_latex_(self, n, z):
        r"""
        TESTS::

            sage: latex(spherical_bessel_J(4, x))
            j_{4}\left(x\right)
        """
        return r"j_{{{}}}\left({}\right)".format(latex(n), latex(z))

    def _derivative_(self, n, z, diff_param):
        r"""
        TESTS::

            sage: y = var('y')
            sage: spherical_bessel_J(x, y).diff(y)
            -(x + 1)*spherical_bessel_J(x, y)/y + spherical_bessel_J(x - 1, y)
        """
        if SR(n).is_numeric() and not SR(n).is_integer():
            raise NotImplementedError('derivative of spherical function with noninteger index')
        if diff_param == 1:
            return (spherical_bessel_J(n - 1, z) -
                    ((n + 1) / z) * spherical_bessel_J(n, z))
        else:
            raise NotImplementedError('derivative with respect to order')

spherical_bessel_J = SphericalBesselJ()


class SphericalBesselY(BuiltinFunction):
    r"""
    The spherical Bessel function of the second kind

    DEFINITION:

    .. MATH::

        y_n(z) = \sqrt{\frac{\pi}{2z}} \,Y_{n + \frac{1}{2}}(z)

    EXAMPLES::

        sage: spherical_bessel_Y(3, x)
        spherical_bessel_Y(3, x)
        sage: spherical_bessel_Y(3 + 0.2 * I, 3)
        -0.505215297588210 - 0.0508835883281404*I
        sage: spherical_bessel_Y(-3, x).simplify()
        ((3/x^2 - 1)*sin(x) - 3*cos(x)/x)/x
        sage: spherical_bessel_Y(3 + 2 * I, 5 - 0.2 * I)
        -0.270205813266440 - 0.615994702714957*I
        sage: integrate(spherical_bessel_Y(0, x), x)
        -1/2*Ei(I*x) - 1/2*Ei(-I*x)
        sage: integrate(spherical_bessel_Y(1,x)^2,(x,0,oo))
        -1/6*pi
        sage: latex(spherical_bessel_Y(0, x))
        y_{0}\left(x\right)

    REFERENCES:

    - [AS-Spherical]_

    - [DLMF-Bessel]_

    - [WP-Bessel]_
    """
    def __init__(self):
        r"""
        TESTS::

            sage: spherical_bessel_Y(3, x)._sympy_()
            yn(3, x)
        """
        BuiltinFunction.__init__(self, 'spherical_bessel_Y', nargs=2,
                                 conversions=dict(mathematica=
                                                  'SphericalBesselY',
                                                  maxima='spherical_bessel_y',
                                                  sympy='yn'))

    def _evalf_(self, n, z, parent, algorithm=None):
        r"""
        TESTS::

            sage: spherical_bessel_Y(3, 3).n(100)
            -0.50802305570981460285684870920
            sage: spherical_bessel_Y(I, I).n()
            -0.174225389805399 + 1.36247234140312*I
        """
        return mpmath_utils.call(spherical_bessel_f, 'bessely', n, z,
                                 parent=parent)

    def _latex_(self):
        r"""
        TESTS::

            sage: latex(spherical_bessel_Y)
            y_n
        """
        return r'y_n'

    def _print_latex_(self, n, z):
        r"""
        TESTS::

            sage: latex(spherical_bessel_Y(4, x))
            y_{4}\left(x\right)
        """
        return r"y_{{{}}}\left({}\right)".format(latex(n), latex(z))

    def _derivative_(self, n, z, diff_param):
        r"""
        TESTS::

            sage: y = var('y')
            sage: spherical_bessel_Y(x, y).diff(y)
            -1/2*spherical_bessel_Y(x, y)/y -...
            1/2*spherical_bessel_Y(x + 1, y) + 1/2*spherical_bessel_Y(x - 1, y)
        """
        if SR(n).is_numeric() and not SR(n).is_integer():
            raise NotImplementedError('derivative of spherical function with noninteger index')
        if diff_param == 1:
            return (-spherical_bessel_Y(n, z) / (2 * z) +
                    (spherical_bessel_Y(n - 1, z) -
                     spherical_bessel_Y(n + 1, z)) / 2)
        else:
            raise NotImplementedError('derivative with respect to order')

spherical_bessel_Y = SphericalBesselY()


class SphericalHankel1(BuiltinFunction):
    r"""
    The spherical Hankel function of the first kind

    DEFINITION:

    .. MATH::

        h_n^{(1)}(z) = \sqrt{\frac{\pi}{2z}} \,H_{n + \frac{1}{2}}^{(1)}(z)

    EXAMPLES::

        sage: spherical_hankel1(3, x)
        spherical_hankel1(3, x)
        sage: spherical_hankel1(3 + 0.2 * I, 3)
        0.201654587512037 - 0.531281544239273*I
        sage: spherical_hankel1(1, x).simplify()
        -(x + I)*e^(I*x)/x^2
        sage: spherical_hankel1(3 + 2 * I, 5 - 0.2 * I)
        1.25375216869913 - 0.518011435921789*I
        sage: integrate(spherical_hankel1(3, x), x)
        Ei(I*x) - 6*gamma(-1, -I*x) - 15*gamma(-2, -I*x) - 15*gamma(-3, -I*x)
        sage: latex(spherical_hankel1(3, x))
        h_{3}^{(1)}\left(x\right)

    REFERENCES:

    - [AS-Spherical]_

    - [DLMF-Bessel]_

    - [WP-Bessel]_
    """
    def __init__(self):
        r"""
        TESTS::

            sage: spherical_hankel1
            spherical_hankel1
        """
        BuiltinFunction.__init__(self, 'spherical_hankel1', nargs=2,
                                 conversions=dict(mathematica=
                                                  'SphericalHankelH1',
                                                  maxima='spherical_hankel1'))

    def _evalf_(self, n, z, parent, algorithm=None):
        r"""
        TESTS::

            sage: spherical_hankel1(3, 3).n(100)
            0.15205166203053329097480571600 - 0.50802305570981460285684870920*I
            sage: spherical_hankel1(I, I).n()
            -1.14695175620623 - 0.456534195607250*I
        """
        return mpmath_utils.call(spherical_bessel_f, 'hankel1', n, z,
                                 parent=parent)

    def _latex_(self):
        r"""
        TESTS::

            sage: latex(spherical_hankel1)
            h_n^{(1)}
        """
        return r'h_n^{(1)}'

    def _print_latex_(self, n, z):
        r"""
        TESTS::

            sage: latex(spherical_hankel1(4, x))
            h_{4}^{(1)}\left(x\right)
        """
        return r"h_{{{}}}^{{(1)}}\left({}\right)".format(latex(n), latex(z))

    def _derivative_(self, n, z, diff_param):
        r"""
        TESTS::

            sage: y = var('y')
            sage: spherical_hankel1(x, y).diff(y)
            -1/2*spherical_hankel1(x, y)/y -...
            1/2*spherical_hankel1(x + 1, y) + 1/2*spherical_hankel1(x - 1, y)
        """
        if SR(n).is_numeric() and not SR(n).is_integer():
            raise NotImplementedError('derivative of spherical function with noninteger index')
        if diff_param == 1:
            return (-spherical_hankel1(n, z) / (2 * z) +
                    (spherical_hankel1(n - 1, z) -
                     spherical_hankel1(n + 1, z)) / 2)
        else:
            raise NotImplementedError('derivative with respect to order')

spherical_hankel1 = SphericalHankel1()


class SphericalHankel2(BuiltinFunction):
    r"""
    The spherical Hankel function of the second kind

    DEFINITION:

    .. MATH::

        h_n^{(2)}(z) = \sqrt{\frac{\pi}{2z}} \,H_{n + \frac{1}{2}}^{(2)}(z)

    EXAMPLES::

        sage: spherical_hankel2(3, x)
        spherical_hankel2(3, x)
        sage: spherical_hankel2(3 + 0.2 * I, 3)
        0.0998874108557565 + 0.479149050937147*I
        sage: spherical_hankel2(1, x).simplify()
        -(x - I)*e^(-I*x)/x^2
        sage: spherical_hankel2(2,i).simplify()
        -e
        sage: spherical_hankel2(2,x).simplify()
        (-I*x^2 - 3*x + 3*I)*e^(-I*x)/x^3
        sage: spherical_hankel2(3 + 2*I, 5 - 0.2*I)
        0.0217627632692163 + 0.0224001906110906*I
        sage: integrate(spherical_hankel2(3, x), x)
        Ei(-I*x) - 6*gamma(-1, I*x) - 15*gamma(-2, I*x) - 15*gamma(-3, I*x)
        sage: latex(spherical_hankel2(3, x))
        h_{3}^{(2)}\left(x\right)

    REFERENCES:

    - [AS-Spherical]_

    - [DLMF-Bessel]_

    - [WP-Bessel]_
    """
    def __init__(self):
        r"""
        TESTS::

            sage: spherical_hankel2
            spherical_hankel2
        """
        BuiltinFunction.__init__(self, 'spherical_hankel2', nargs=2,
                                 conversions=dict(mathematica=
                                                  'SphericalHankelH2',
                                                  maxima='spherical_hankel2'))

    def _evalf_(self, n, z, parent, algorithm=None):
        r"""
        TESTS::

            sage: spherical_hankel2(3, 3).n(100)
            0.15205166203053329097480571600 + 0.50802305570981460285684870920*I
            sage: spherical_hankel2(I, I).n()
            1.57799292660001 - 0.108083415996452*I
        """
        return mpmath_utils.call(spherical_bessel_f, 'hankel2', n, z,
                                 parent=parent)

    def _latex_(self):
        r"""
        TESTS::

            sage: latex(spherical_hankel2)
            h_n^{(2)}
        """
        return r'h_n^{(2)}'

    def _print_latex_(self, n, z):
        r"""
        TESTS::

            sage: latex(spherical_hankel2(4, x))
            h_{4}^{(2)}\left(x\right)
        """
        return r"h_{{{}}}^{{(2)}}\left({}\right)".format(latex(n), latex(z))

    def _derivative_(self, n, z, diff_param):
        r"""
        TESTS::

            sage: y = var('y')
            sage: spherical_hankel2(x, y).diff(y)
            -1/2*spherical_hankel2(x, y)/y -...
            1/2*spherical_hankel2(x + 1, y) + 1/2*spherical_hankel2(x - 1, y)
            sage: spherical_hankel2(x, y).diff(x)
            Traceback (most recent call last):
            ...
            NotImplementedError: derivative with respect to order
            sage: spherical_hankel2(3/2, y).diff(y)
            Traceback (most recent call last):
            ...
            NotImplementedError: derivative of spherical function with noninteger index
        """
        if SR(n).is_numeric() and not SR(n).is_integer():
            raise NotImplementedError('derivative of spherical function with noninteger index')
        if diff_param == 1:
            return (-spherical_hankel2(n, z) / (2 * z) +
                    (spherical_hankel2(n - 1, z) -
                     spherical_hankel2(n + 1, z)) / 2)
        else:
            raise NotImplementedError('derivative with respect to order')

spherical_hankel2 = SphericalHankel2()


def spherical_bessel_f(F, n, z):
    r"""
    Numerically evaluate the spherical version, `f`, of the Bessel function `F`
    by computing `f_n(z) = \sqrt{\frac{1}{2}\pi/z} F_{n + \frac{1}{2}}(z)`.
    According to Abramowitz & Stegun, this identity holds for the Bessel
    functions `J`, `Y`, `K`, `I`, `H^{(1)}`, and `H^{(2)}`.

    EXAMPLES::

        sage: from sage.functions.bessel import spherical_bessel_f
        sage: spherical_bessel_f('besselj', 3, 4)
        mpf('0.22924385795503024')
        sage: spherical_bessel_f('hankel1', 3, 4)
        mpc(real='0.22924385795503024', imag='-0.21864196590306359')

    TESTS:

    Check that :trac:`28474` is fixed::

        sage: from sage.functions.bessel import spherical_bessel_f
        sage: spherical_bessel_f('besselj', 3, -4)
        mpc(real='-0.22924385795503024', imag='0.0')
        sage: spherical_bessel_f('bessely', 3, -4)
        mpc(real='-0.21864196590306359', imag='0.0')
    """
    from mpmath import mp
    ctx = mp
    prec = ctx.prec
    try:
        n = ctx.convert(n)
        z = ctx.convert(z)
        ctx.prec += 10
        Fz = getattr(ctx, F)(n + 0.5, z)
        hpi = 0.5 * ctx.pi()
        ctx.prec += 10
        sqrthpi = ctx.sqrt(hpi)
        sqrtz = ctx.sqrt(z)
        ctx.prec += 10
        quotient = sqrthpi / sqrtz
        ctx.prec += 10
        return quotient * Fz
    finally:
        ctx.prec = prec

