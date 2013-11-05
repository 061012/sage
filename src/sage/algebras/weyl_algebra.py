r"""
Weyl Algebras

AUTHORS:

- Travis Scrimshaw (2013-09-06): Initial version
"""

#*****************************************************************************
#  Copyright (C) 2013 Travis Scrimshaw <tscrim at ucdavis.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.misc.cachefunc import cached_method
from sage.misc.latex import latex
from sage.structure.element import AlgebraElement
from sage.structure.unique_representation import UniqueRepresentation
from copy import copy
from sage.categories.rings import Rings
from sage.categories.algebras_with_basis import AlgebrasWithBasis
from sage.categories.commutative_algebras import Algebras
from sage.rings.ring import Algebra

def repr_from_monomials(monomials, term_repr, use_latex=False):
    r"""
    Return a representation from the dictionary ``monomials``.

    INPUT:

    - ``monomials`` -- a list of pairs ``[m, c]`` where ``m`` is the index
      and ``c`` is the cofficient
    - ``term_repr`` -- a function which returns a string given an index
    - ``use_latex`` -- (default: ``False``) if ``True`` then the output is
      in latex format

    EXAMPLES::

        sage: from sage.algebras.weyl_algebra import repr_from_monomials
        sage: R.<x,y,z> = QQ[]
        sage: d = [(z, 4/7), (y, sqrt(2)), (x, -5)]
        sage: repr_from_monomials(d, lambda m: repr(m))
        '4/7*z + sqrt(2)*y - 5*x'
        sage: repr_from_monomials([], lambda m: repr(m))
        '0'
        sage: repr_from_monomials(d, lambda m: latex(m), True)
        '\\frac{4}{7} z + \\sqrt{2} y - 5 x'
    """
    if len(monomials) == 0:
        return '0'

    ret = ''
    for m,c in monomials:
        # Get the monomial portion
        term = term_repr(m)

        # Determine what to do with the coefficient
        if use_latex:
            coeff = latex(c)
        else:
            coeff = repr(c)
        if len(term) == 0 or term == '1':
            term = coeff
        else:
            atomic_repr = c.parent()._repr_option('element_is_atomic')
            if not atomic_repr and (coeff.find("+") != -1 or coeff.find("-") > 0):
                if use_latex:
                    term = '\\left(' + coeff + '\\right) ' + term
                else:
                    term = '(' + coeff + ')*' + term
            else:
                if use_latex:
                    term = coeff + ' ' + term
                else:
                    term = coeff + '*' + term

        # Append this term with the correct sign
        if len(ret) != 0:
            if term[0] == '-':
                ret += ' - ' + term[1:]
            else:
                ret += ' + ' + term
        else:
            ret = term
    import re
    ret = ret.replace("+ -", "-")
    ret = re.sub(r'1(\.0+)?[\* ]', '', ret)
    ret = re.sub(r'-1(\.0+)?[\* ]', '-', ret)
    return ret

class WeylAlgebraElement(AlgebraElement):
    """
    An element in a Weyl algebra.
    """
    def __init__(self, parent, monomials):
        """
        Initialize ``self``.

        TESTS::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: dx,dy,dz = W.gens()
            sage: elt = ((x^3-z)*dx + dy)^2
            sage: TestSuite(elt).run()
        """
        AlgebraElement.__init__(self, parent)
        self.__monomials = monomials

    def _repr_(self):
        """
        Return a string representation of ``self``.

        TESTS::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: dx,dy,dz = W.gens()
            sage: ((x^3-z)*dx + dy)^2
            dy^2 + (3*x^5 - 3*x^2*z)*dx + (2*x^3 - 2*z)*dx*dy + (x^6 - 2*x^3*z + z^2)*dx^2
        """
        def term(m):
            ret = ''
            for i, power in enumerate(m):
                if power == 0:
                    continue
                name = self.parent().variable_names()[i]
                if len(ret) != 0:
                    ret += '*'
                if power == 1:
                    ret += '{}'.format(name)
                else:
                    ret += '{}^{}'.format(name, power)
            return ret
        return repr_from_monomials(sorted(self.__monomials.items()), term)

    def _latex_(self):
        r"""
        Return a `\LaTeX` representation of ``self``.

        TESTS::

            sage: R = PolynomialRing(QQ, 'x', 3)
            sage: x,y,z = R.gens()
            sage: W = WeylAlgebra(R)
            sage: dx0,dx1,dx2 = W.gens()
            sage: latex( ((x^3-z)*dx0 + dx1)^2 )
            \frac{\partial^{2}}{\partial x_{1}^{2}}
             + \left( 3 x_{0}^{5} - 3 x_{0}^{2} x_{2} \right) \frac{\partial}{\partial x_{0}}
             + \left( 2 x_{0}^{3} - 2 x_{2} \right) \frac{\partial^{2}}{\partial x_{0}\partial x_{1}}
             + \left( x_{0}^{6} - 2 x_{0}^{3} x_{2} + x_{2}^{2} \right) \frac{\partial^{2}}{\partial x_{0}^{2}}
        """
        def term(m):
            ret = ''
            total = sum(m)
            if total == 1:
                ret = '\\frac{\\partial}{'
            else:
                ret = '\\frac{\\partial^{' + repr(total) + '}}{'
            for i, power in enumerate(m):
                if power == 0:
                    continue
                name = self.parent().base_ring().gen(i)
                if power == 1:
                    ret += '\\partial {0}'.format(latex(name))
                else:
                    ret += '\\partial {0}^{{{1}}}'.format(latex(name), power)
            return ret + '}'
        return repr_from_monomials(sorted(self.__monomials.items()), term, True)

    def __eq__(self, rhs):
        """
        Check equality.

        TESTS::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: dx,dy,dz = W.gens()
            sage: dy*(x^3-y*z)*dx == -z*dx + x^3*dx*dy - y*z*dx*dy
            True
            sage: W.zero() == 0
            True
            sage: W.one() == 1
            True
            sage: W(x^3 - y*z) == x^3 - y*z
            True
        """
        if not isinstance(rhs, WeylAlgebra.Element):
            P = self.parent()
            c_term = tuple([0]*P.ngens())
            return self.__monomials.get(c_term, P.base_ring().zero()) == rhs
        return self.parent() is rhs.parent() and self.__monomials == rhs.__monomials

    def __ne__(self, rhs):
        """
        Check inequality.

        TESTS::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: dx,dy,dz = W.gens()
            sage: dx != dy
            True
            sage: W.one() != 1
            False
        """
        return not self.__eq__(rhs)

    def __neg__(self):
        """
        Return the negative of ``self``.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: dx,dy,dz = W.gens()
            sage: dy - (3*x - z)*dx
            dy + (-3*x + z)*dx
        """
        return self.__class__(self.parent(), {m:-c for m,c in self.__monomials.items()})

    def _add_(self, rhs):
        """
        Return ``self`` added to ``rhs``.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: dx,dy,dz = W.gens()
            sage: (dx*dy) + dz + x^3 - 2
            x^3 - 2 + dz + dx*dy
        """
        d = copy(self.__monomials)
        for m,c in rhs.__monomials.items():
            d[m] = d.get(m, 0) + c
            if d[m] == 0:
                del d[m]
        return self.__class__(self.parent(), d)

    def _mul_(self, rhs):
        """
        Return ``self`` multiplied by ``rhs``.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: dx,dy,dz = W.gens()
            sage: ((x^3-z)*dx + dy) * (dx*dz^2 - 10*x)
            -10*x^3 + 10*z - 10*x*dy + (-10*x^4 + 10*x*z)*dx + dx*dy*dz^2 + (x^3 - z)*dx^2*dz^2
        """
        d = {}
        for ml,cl in self.__monomials.items():
            for mr,cr in rhs.__monomials.items():
                for t,coeff in expand_derivative(cr, ml).items():
                    # multiply the resulting term by the RHS term
                    t = tuple(v + mr[i] for i,v in enumerate(t))
                    d[t] = d.get(t, 0) + cl * coeff
                    if d[t] == 0:
                        del d[t]
        return self.__class__(self.parent(), d)

    def _rmul_(self, lhs):
        """
        Multiply ``self`` on the right side of ``lhs``.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: dx,dy,dz = W.gens()
            sage: (x*y + z) * dx
            (x*y + z)*dx
        """
        if lhs == 0:
            return self.parent().zero()
        return self.__class__(self.parent(), {m: lhs*c for m,c in self.__monomials.items()})

    def _lmul_(self, rhs):
        """
        Multiply ``self`` on the left side of ``rhs``.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: dx,dy,dz = W.gens()
            sage: dx*(x*y + z)
            y + (x*y + z)*dx
        """
        d = {}
        for m,c in self.__monomials.items():
            for t,coeff in expand_derivative(rhs, m).items():
                d[t] = d.get(t, 0) + c * coeff
                if d[t] == 0:
                    del d[t]
        return self.__class__(self.parent(), d)

    def __iter__(self):
        """
        Return an iterator of ``self``.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: dx,dy,dz = W.gens()
            sage: list(dy - (3*x - z)*dx)
            [((0, 1, 0), 1), ((1, 0, 0), -3*x + z)]
        """
        return iter(self.list())

    def list(self):
        """
        Return ``self`` as a list.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: dx,dy,dz = W.gens()
            sage: elt = dy - (3*x - z)*dx
            sage: elt.list()
            [((0, 1, 0), 1), ((1, 0, 0), -3*x + z)]
        """
        return sorted(self.__monomials.items())

class WeylAlgebra(Algebra, UniqueRepresentation):
    r"""
    The Weyl algebra of a polynomial ring.

    REFERENCES:

    - :wikipedia:`Weyl_algebra`

    INPUT:

    -  ``R`` -- a (polynomial) ring

    EXAMPLES::
    """
    def __init__(self, R):
        r"""
        Initialize ``self``.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: TestSuite(W).run()
        """
        if R not in Rings():
            raise TypeError("argument R must be a ring")
        names = tuple('d' + n for n in R.variable_names())
        Algebra.__init__(self, R, names, category=AlgebrasWithBasis(R))

    def _repr_(self):
        r"""
        Return a string representation of ``self``.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: WeylAlgebra(R)
            The Weyl algebra of Multivariate Polynomial Ring in x, y, z over Rational Field
        """
        return "The Weyl algebra of {}".format(self.base_ring())

    def gen(self, i):
        """
        Return the ``i``-th generator of ``self``.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: [W.gen(i) for i in range(3)]
            [dx, dy, dz]
        """
        L = [0]*self.ngens()
        L[i] = 1
        return self.element_class(self, {tuple(L): self.base_ring().one()} )

    def ngens(self):
        """
        Return the number of generators of ``self``.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: W.ngens()
            3
        """
        return self.base_ring().ngens()

    @cached_method
    def one(self):
        """
        Return the multiplicative identity element `1`.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: W.one()
            1
        """
        return self.element_class( self, {tuple([0]*self.ngens()): self.base_ring().one()} )

    @cached_method
    def zero(self):
        """
        Return the additive identity element `0`.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: W = WeylAlgebra(R)
            sage: W.zero()
            0
        """
        return self.element_class(self, {})

    Element = WeylAlgebraElement

# Helper function
def expand_derivative(poly, exps):
    """
    Helper function that returns the expansion of ``poly`` by using
    derivative with respect to ``mon`` and return a dictionary representing
    an element in the Weyl algebra.

    INPUT:

    - ``poly`` -- a polynomial
    - ``exps`` -- the exponents of the derivatives

    EXAMPLES::

        sage: from sage.algebras.weyl_algebra import expand_derivative
        sage: R.<x,y,z> = QQ[]
        sage: expand_derivative(x*y - z, (1,0,1))
        {(1, 0, 0): -1, (0, 0, 1): y, (1, 0, 1): x*y - z}
        sage: expand_derivative(R(5), (1,0,1))
        {(1, 0, 1): 5}
    """
    if poly.is_constant():
        return {exps: poly}
    gens = poly.parent().gens()
    d = {tuple([0]*len(gens)): poly}
    for i,p in enumerate(exps):
        wrt = gens[i] # with respect to this generator
        for j in range(p):
            for m,c in d.items():
                deriv = c.derivative(wrt)
                L = list(m)
                L[i] += 1
                L = tuple(L)
                d[L] = d.get(L, 0) + d[m]
                if deriv == 0:
                    del d[m]
                else:
                    d[m] = deriv
    return d

