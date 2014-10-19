r"""
Graded Algebras
"""
#*****************************************************************************
#  Copyright (C) 2008      Teresa Gomez-Diaz (CNRS) <Teresa.Gomez-Diaz@univ-mlv.fr>
#                2008-2011 Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.categories.graded_modules import GradedModulesCategory

class GradedAlgebras(GradedModulesCategory):
    """
    The category of graded algebras

    EXAMPLES::

        sage: GradedAlgebras(ZZ)
        Category of graded algebras over Integer Ring
        sage: GradedAlgebras(ZZ).super_categories()
        [Category of filtered algebras over Integer Ring,
         Category of graded modules over Integer Ring]

    TESTS::

        sage: TestSuite(GradedAlgebras(ZZ)).run()
    """
    def extra_super_categories(self):
        r"""
        Adds :class:`FilteredAlgebras` to the super categories of ``self``
        since every graded algebra admits a filtraion.

        EXAMPLES::

            sage: GradedAlgebras(ZZ).extra_super_categories()
            [Category of filtered algebras over Integer Ring]
        """
        from sage.categories.filtered_algebras import FilteredAlgebras
        return [FilteredAlgebras(self.base_ring())]

    class ParentMethods:
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

