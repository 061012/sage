"""
Lie Algebras Given By Structure Coefficients

AUTHORS:

- Travis Scrimshaw (2013-05-03): Initial version
"""

#*****************************************************************************
#  Copyright (C) 2013 Travis Scrimshaw <tscrim@ucdavis.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty
#    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU General Public License for more details; the full text
#  is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from copy import copy
from sage.misc.cachefunc import cached_method
from sage.misc.lazy_attribute import lazy_attribute
from sage.misc.misc import repr_lincomb
from sage.structure.indexed_generators import IndexedGenerators
from sage.structure.parent import Parent
from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.element_wrapper import ElementWrapper

from sage.categories.algebras import Algebras
from sage.categories.lie_algebras import LieAlgebras
from sage.categories.finite_dimensional_lie_algebras_with_basis import FiniteDimensionalLieAlgebrasWithBasis

from sage.algebras.free_algebra import FreeAlgebra
from sage.algebras.lie_algebras.lie_algebra_element import LieAlgebraElement
from sage.algebras.lie_algebras.lie_algebra import FinitelyGeneratedLieAlgebra
#from sage.algebras.lie_algebras.subalgebra import LieSubalgebra
#from sage.algebras.lie_algebras.ideal import LieAlgebraIdeal
#from sage.algebras.lie_algebras.quotient import QuotientLieAlgebra
from sage.rings.all import ZZ
from sage.rings.ring import Ring
from sage.rings.integer import Integer
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.rings.infinity import infinity
from sage.matrix.matrix_space import MatrixSpace
from sage.matrix.constructor import matrix
from sage.modules.free_module_element import vector
from sage.modules.free_module import FreeModule, span
from sage.sets.family import Family, AbstractFamily

# TODO: Much of this could be moved to (FiniteDimensional)LieAlgebrasWithBasis
class LieAlgebraWithStructureCoefficients(FinitelyGeneratedLieAlgebra, IndexedGenerators):
    r"""
    A Lie algebra with a set of specified structure coefficients.

    The structure coefficients are specified as a dictionary whose keys are
    pairs of generators and values are dictionaries of generators mapped
    to coefficients.

    EXAMPLES:

    We create the Lie algebra of `\QQ^3` under the Lie bracket defined
    by `\times` (cross-product)::

        sage: L = LieAlgebra(QQ, 'x,y,z', {('x','y'):{'z':1}, ('y','z'):{'x':1}, ('z','x'):{'y':1}})
        sage: (x,y,z) = L.gens()
        sage: L.bracket(x, y)
        z
        sage: L.bracket(y, x)
        -z
    """
    @staticmethod
    def __classcall_private__(cls, R, s_coeff, names=None, index_set=None, **kwds):
        """
        Normalize input to ensure a unique representation.

        EXAMPLES::

            sage: L1 = LieAlgebra(QQ, 'x,y', {('x','y'):{'x':1}})
            sage: L2 = LieAlgebra(QQ, 'x,y', {('y','x'):{'x':-1}})
            sage: L1 is L2
            True
        """
        s_coeff = LieAlgebraWithStructureCoefficients._standardize_s_coeff(s_coeff)
        if len(s_coeff) == 0:
            return AbelianLieAlgebra(R, names, index_set, **kwds)

        if names is None:
            if index_set is None:
                raise ValueError("either the names or the index set must be specified")
            if len(index_set) <= 1:
                return AbelianLieAlgebra(R, names, index_set, **kwds)
        elif len(names) <= 1:
            return AbelianLieAlgebra(R, names, index_set, **kwds)

        return super(LieAlgebraWithStructureCoefficients, cls).__classcall__(
            cls, R, s_coeff, tuple(names), index_set, **kwds)

    @staticmethod
    def _standardize_s_coeff(s_coeff):
        """
        Helper function to standardize ``s_coeff`` into the appropriate tuple
        of tuples. Strips items with coefficients of 0 and duplicate entries.
        This does not check the Jacobi relation (nor antisymmetry if the
        cardinality is infinite).
        """
        # Try to handle infinite basis (once/if supported)
        #if isinstance(s_coeff, AbstractFamily) and s_coeff.cardinality() == infinity:
        #    return s_coeff

        sc = {}
        # Make sure the first gen is smaller than the second in each key
        for k in s_coeff.keys():
            v = s_coeff[k]
            if isinstance(v, dict):
                v = v.items()

            if k[0] > k[1]:
                key = (k[1], k[0])
                vals = tuple((g, -val) for g, val in v if val != 0)
            else:
                assert k[0] < k[1], "elements {} not ordered".format(k)
                key = tuple(k)
                vals = tuple((g, val) for g, val in v if val != 0)

            if key in sc.keys() and sorted(sc[key]) != sorted(vals):
                raise ValueError("non-equal brackets")

            if len(vals) > 0:
                sc[key] = vals
        return Family(sc)

    def __init__(self, R, s_coeff, names, index_set, category=None, prefix='',
                 bracket=False, latex_bracket=False, string_quotes=False, **kwds):
        """
        Initialize ``self``.

        EXAMPLES::

            sage: L = LieAlgebra(QQ, 'x,y', {('x','y'): {'x':1}})
            sage: TestSuite(L).run()
        """
        cat = LieAlgebras(R).WithBasis().FiniteDimensional().or_subcategory(category)
        FinitelyGeneratedLieAlgebra.__init__(self, R, names, index_set, cat)
        IndexedGenerators.__init__(self, self._indices, prefix=prefix,
                                   bracket=bracket, latex_bracket=latex_bracket,
                                   string_quotes=string_quotes, **kwds)

        # Transform the values in the structure coefficients to elements
        self._s_coeff = Family({k: self._from_dict(dict(s_coeff[k]))
                                for k in s_coeff.keys()})

    # For compatibility with CombinatorialFreeModuleElement
    _repr_term = IndexedGenerators._repr_generator
    _latex_term = IndexedGenerators._latex_generator

    def basis(self):
        """
        Return the basis of ``self``.

        EXAMPLES::

            sage: L = LieAlgebra(QQ, 'x,y', {('x','y'):{'x':1}})
            sage: L.basis()
            Finite family {'y': y, 'x': x}
        """
        return Family({i: self.monomial(i) for i in self._indices})

    def structure_coefficients(self):
        """
        Return the dictonary of structure coefficients of ``self``.

        EXAMPLES::

            sage: L = LieAlgebra(QQ, 'x,y', {('x','y'):{'x':1}})
            sage: L.structure_coefficients()
            Finite family {('x', 'y'): x}
        """
        return self._s_coeff

    def dimension(self):
        """
        Return the dimension of ``self``.

        EXAMPLES::

            sage: L = LieAlgebra(QQ, 'x,y', {('x','y'):{'x':1}})
            sage: L.dimension()
            2
        """
        return self.basis().cardinality()

    def bracket_on_basis(self, x, y):
        """
        Return the Lie bracket of ``[x, y]``.

        EXAMPLES::

            sage: L.<x,y,z> = LieAlgebra(QQ, {('x','y'):{'z':1}, ('y','z'):{'x':1}, ('z','x'):{'y':1}})
            sage: L.bracket_on_basis('x', 'y')
            z
            sage: L.bracket_on_basis('y', 'x')
            -z
            sage: L.bracket(x + y - z, x - y + z)
            -2*y - 2*z
        """
        comp = self._print_options['generator_cmp']
        ordered = True
        if comp(x, y) > 0: # x > y
            x,y = y,x
            ordered = False
        b = (x, y)
        try:
            val = self._s_coeff[b]
        except KeyError:
            return self.zero()
        if ordered:
            return val
        return -val

    def free_module(self, sparse=True):
        """
        Return ``self`` as a free module.

        EXAMPLES::

            sage: L.<x,y,z> = LieAlgebra(QQ, {('x','y'):{'z':1}, ('y','z'):{'x':1}, ('z','x'):{'y':1}})
            sage: L.free_module()
            Sparse vector space of dimension 3 over Rational Field
        """
        # TODO: Make this return a free module with the same index set as ``self``
        return FreeModule(self.base_ring(), self.dimension(), sparse=sparse)

    class Element(LieAlgebraElement):
        """
        An element of a Lie algebra given by structure coefficients.
        """

        #def _bracket_(self, y):
        #    """
        #    Return the Lie bracket ``[self, y]``.
        #    """
        #    P = self.parent()
        #    return P.sum(cx * cy * P.bracket_on_basis(mx, my)
        #                 for mx,cx in self for my,cy in y)

        def to_vector(self):
            """
            Return ``self`` as a vector.
            """
            V = self.parent().free_module()
            return V([self[k] for k in self.parent()._ordered_indices])

class AbelianLieAlgebra(LieAlgebraWithStructureCoefficients):
    r"""
    An abelian Lie algebra.

    A Lie algebra `\mathfrak{g}` is abelian if `[x, y] = 0` for all
    `x, y \in \mathfrak{g}`.

    EXAMPLES::

        sage: L.<x, y> = LieAlgebra(QQ, abelian=True)
        sage: L.bracket(x, y)
        0
    """
    def __init__(self, R, names=None, index_set=None, **kwds):
        """
        Initialize ``self``.

        EXAMPLES::

            sage: L = LieAlgebra(QQ, 3, 'x', abelian=True)
            sage: TestSuite(L).run()
        """
        LieAlgebraWithStructureCoefficients.__init__(self, R, Family({}), names, index_set, **kwds)

    def _repr_(self):
        """
        Return a string representation of ``self``.

        EXAMPLES::

            sage: LieAlgebra(QQ, 3, 'x', abelian=True)
            Abelian Lie algebra on 3 generators (x0, x1, x2) over Rational Field
        """
        gens = self.lie_algebra_generators()
        if gens.cardinality() == 1:
            return "Abelian Lie algebra on generator {} over {}".format(tuple(gens)[0], self.base_ring())
        return "Abelian Lie algebra on {} generators {} over {}".format(
            gens.cardinality(), tuple(gens), self.base_ring())

    def _construct_UEA(self):
        """
        Construct the universal enveloping algebra of ``self``.

        EXAMPLES::

            sage: L = LieAlgebra(QQ, 3, 'x', abelian=True)
            sage: L._construct_UEA()
            Multivariate Polynomial Ring in x0, x1, x2 over Rational Field
        """
        return PolynomialRing(self.base_ring(), self.variable_names())

    def is_abelian(self):
        """
        Return ``True`` since this is an abelian Lie algebra.

        EXAMPLES::

            sage: L = LieAlgebra(QQ, 3, 'x', abelian=True)
            sage: L.is_abelian()
            True
        """
        return True

    def bracket_on_basis(self, x, y):
        """
        Return the Lie bracket of basis elements indexed by ``x`` and ``y``.

        EXAMPLES::

            sage: L.<x,y> = LieAlgebra(QQ, abelian=True)
            sage: L.bracket_on_basis(x.leading_support(), y.leading_support())
            0
        """
        return self.zero()

    class Element(LieAlgebraElement):
        def _bracket_(self, y):
            """
            Return the Lie bracket ``[self, y]``.

            EXAMPLES::

                sage: L.<x, y> = LieAlgebra(QQ, abelian=True)
                sage: L.bracket(x, y)
                0
            """
            return self.parent().zero()

