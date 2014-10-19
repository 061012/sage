r"""
Graded algebras with basis
"""
#*****************************************************************************
#  Copyright (C) 2008      Teresa Gomez-Diaz (CNRS) <Teresa.Gomez-Diaz@univ-mlv.fr>
#                2008-2011 Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.categories.graded_modules import GradedModulesCategory

class GradedAlgebrasWithBasis(GradedModulesCategory):
    """
    The category of graded algebras with a distinguished basis

    EXAMPLES::

        sage: C = GradedAlgebrasWithBasis(ZZ); C
        Category of graded algebras with basis over Integer Ring
        sage: sorted(C.super_categories(), key=str)
        [Category of filtered algebras with basis over Integer Ring,
         Category of graded algebras over Integer Ring,
         Category of graded modules with basis over Integer Ring]

    TESTS::

        sage: TestSuite(C).run()
    """
    def extra_super_categories(self):
        r"""
        Adds :class:`FilteredAlgebras` to the super categories of ``self``
        since every graded algebra admits a filtraion.

        EXAMPLES::

            sage: GradedAlgebras(ZZ).extra_super_categories()
            [Category of filtered algebras over Integer Ring]
        """
        from sage.categories.filtered_algebras_with_basis import FilteredAlgebrasWithBasis
        return [FilteredAlgebrasWithBasis(self.base_ring())]

    class ParentMethods:
        # This needs to be copied in GradedAlgebras because we need to have
        #   FilteredAlgebrasWithBasis as an extra super category
        def graded_algebra(self):
            """
            Return the associated graded algebra to ``self``.

            EXAMPLES::

                sage: m = SymmetricFunctions(QQ).m()
                sage: m.graded_algebra() is m
                True
            """
            return self

    class ElementMethods:
        pass

