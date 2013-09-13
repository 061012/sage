r"""
Euclidean domains

AUTHORS:

- Teresa Gomez-Diaz (2008): initial version

- Julian Rueth (2013-09-13): added euclidean degree, quotient remainder, and
  their tests

"""
#*****************************************************************************
#  Copyright (C) 2008 Teresa Gomez-Diaz (CNRS) <Teresa.Gomez-Diaz@univ-mlv.fr>
#                2013 Julian Rueth <julian.rueth@fsfe.org>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.categories.category import Category
from sage.categories.category_singleton import Category_singleton
from sage.categories.principal_ideal_domains import PrincipalIdealDomains
from sage.misc.cachefunc import cached_method
from sage.misc.abstract_method import abstract_method

class EuclideanDomains(Category_singleton):
    """
    The category of constructive euclidean domains, i.e., one can divide
    producing a quotient and a remainder where the remainder is either zero or
    its :meth:`ElementMethods.euclidean_degree` is smaller than the divisor.

    EXAMPLES::

      sage: EuclideanDomains()
      Category of euclidean domains
      sage: EuclideanDomains().super_categories()
      [Category of principal ideal domains]

    TESTS::

        sage: TestSuite(EuclideanDomains()).run()

    """
    def super_categories(self):
        """
        EXAMPLES::

            sage: EuclideanDomains().super_categories()
            [Category of principal ideal domains]
        """
        return [PrincipalIdealDomains()]

    class ParentMethods:
        def is_euclidean_domain(self):
            """
            Return True, since this in an object of the category of Euclidean domains.

            EXAMPLES::

                sage: Parent(QQ,category=EuclideanDomains()).is_euclidean_domain()
                True

            """
            return True

        def _test_euclidean_degree(self, **options):
            r"""
            Test that the assumptions on a euclidean degree are met.

            EXAMPLES::

                sage: R.<x> = QQ[]
                sage: R._test_euclidean_degree()

            .. SEEALSO:

                :meth:`_test_quo_rem`

            """
            tester = self._tester(**options)
            S = [s for s in tester.some_elements() if not s.is_zero()]

            min_degree = self.one().euclidean_degree()

            from sage.rings.all import NN
            for a in S:
                tester.assertIn(a.euclidean_degree(), NN)
                tester.assertGreaterEqual(a.euclidean_degree(), min_degree)
                tester.assertEqual(a.euclidean_degree() == min_degree, a.is_unit())

            from sage.combinat.cartesian_product import CartesianProduct
            for a,b in tester.some_elements(CartesianProduct(S,S)):
                tester.assertLessEqual(a.euclidean_degree(), (a*b).euclidean_degree())

        def _test_quo_rem(self, **options):
            r"""
            Test that the assumptions on a quotient with remainder of an
            euclidean domain are met.

            EXAMPLES::

                sage: R.<x> = QQ[]
                sage: R._test_quo_rem()

            .. SEEALSO:

                :meth:`_test_euclidean_degree`

            """
            tester = self._tester(**options)
            S = tester.some_elements()

            from sage.combinat.cartesian_product import CartesianProduct
            for a,b in tester.some_elements(CartesianProduct(S,S)):
                if b.is_zero():
                    tester.assertRaises(ZeroDivisionError, lambda: a.quo_rem(b))
                else:
                    q,r = a.quo_rem(b)
                    tester.assertIn(q, self)
                    tester.assertIn(r, self)
                    tester.assertEqual(a,q*b+r)
                    if r != 0:
                        tester.assertLess(r.euclidean_degree(), b.euclidean_degree())

    class ElementMethods:
        @abstract_method
        def euclidean_degree(self):
            r"""
            Return the degree of this element as an element of a euclidean
            domain, i.e., for elements `a`, `b` the euclidean degree `f`
            satisfies the usual properties:

            1. if `b` is not zero, then there are elements `q` and `r` such
            that `a=bq+r` with `r=0` or `f(r)<f(b)`
            2. if `a,b` are not zero, then `f(a)\le f(ab)`

            .. NOTE::

                The name ``euclidean_degree`` was chosen because the euclidean
                function has different names in different contexts, e.g.,
                absolute value for integers, degree for polynomials.

            OUTPUT:

            For non-zero elements, a natural number. For the zero element, this
            might raise an exception or produce some other output, depending on
            the implementation.

            EXAMPLES::

                sage: R.<x> = QQ[]
                sage: x.euclidean_degree()
                1
                sage: ZZ.one().euclidean_degree()
                1

            """
            pass

        @abstract_method
        def quo_rem(self, other):
            r"""
            Return the quotient and remainder of the division of this element
            by the non-zero element ``other``.

            INPUT::

            - ``other`` -- an element in the same euclidean domain

            OUTPUT

            EXAMPLES::

                sage: R.<x> = QQ[]
                sage: x.quo_rem(x)
                (1, 0)

            """
            pass
