r"""
Filtered Modules With Basis

A *filtered module with basis* over a commutative ring `R`
means (for the purpose of this code) a filtered `R`-module
`M` with filtration `(F_i)_{i \in I}` (typically `I = \NN`)
endowed with a basis `(b_j)_{j \in J}` of `M` and a partition
`J = \bigsqcup_{i \in I} J_i` of the set `J` (it is allowed
that some `J_i` are empty) such that for every `n \in I`,
the subfamily `(b_j)_{j \in U_n}`, where
`U_n = \bigcup_{i \leq n} J_i`, is a basis of the
`R`-submodule `F_n`.

For every `i \in I`, the `R`-submodule of `M` spanned by
`(b_j)_{j \in J_i}` is called the `i`-*th graded component*
(aka the `i`-*th homogeneous component*) of the filtered
module with basis `M`; the elements of this submodule are
referred to as *homogeneous elements of degree* `i`.
"""
#*****************************************************************************
#  Copyright (C) 2014 Travis Scrimshaw <tscrim at ucdavis.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.categories.filtered_modules import FilteredModulesCategory

class FilteredModulesWithBasis(FilteredModulesCategory):
    r"""
    The category of filtered modules with a distinguished basis.

    A *filtered module with basis* over a commutative ring `R`
    means (for the purpose of this code) a filtered `R`-module
    `M` with filtration `(F_i)_{i \in I}` (typically `I = \NN`)
    endowed with a basis `(b_j)_{j \in J}` of `M` and a partition
    `J = \bigsqcup_{i \in I} J_i` of the set `J` (it is allowed
    that some `J_i` are empty) such that for every `n \in I`,
    the subfamily `(b_j)_{j \in U_n}`, where
    `U_n = \bigcup_{i \leq n} J_i`, is a basis of the
    `R`-submodule `F_n`.

    For every `i \in I`, the `R`-submodule of `M` spanned by
    `(b_j)_{j \in J_i}` is called the `i`-*th graded component*
    (aka the `i`-*th homogeneous component*) of the filtered
    module with basis `M`; the elements of this submodule are
    referred to as *homogeneous elements of degree* `i`.
    The `R`-module `M` is the direct sum of its `i`-th graded
    components over all `i \in I`, and thus becomes a graded
    `R`-module with basis.
    Conversely, any graded `R`-module with basis canonically
    becomes a filtered `R`-module with basis (by defining
    `F_n = \bigoplus_{i \leq n} G_i` where `G_i` is the `i`-th
    graded component, and defining `J_i` as the indexing set
    of the basis of the `i`-th graded component). Hence, the
    notion of a filtered `R`-module with basis is equivalent
    to the notion of a graded `R`-module with basis.

    However, the *category* of filtered `R`-modules with basis is not
    the category of graded `R`-modules with basis. Indeed, the *morphisms*
    of filtered `R`-modules with basis are defined to be morphisms of
    `R`-modules which send each `F_n` of the domain to the corresponding
    `F_n` of the target; in contrast, the morphisms of graded `R`-modules
    with basis must preserve each homogeneous component. Also,
    the notion of a filtered algebra with basis differs from
    that of a graded algebra with basis.

    .. NOTE::

        Currently, to make use of the functionality of this class,
        an instance of ``FilteredModulesWithBasis`` should fulfill
        the contract of a :class:`CombinatorialFreeModule` (most
        likely by inheriting from it). It should also have the
        indexing set `J` encoded as its ``_indices`` attribute,
        and ``_indices.subset(basis=i)`` should yield the subset
        `J_i` (as an iterable). If the latter conditions are not
        satisfied, then :meth:`basis` must be overridden.

    .. TODO::

        This deserves to be handled better, and the contracts
        involved might also profit from some explicit writing-up.

    EXAMPLES::

        sage: C = ModulesWithBasis(ZZ).Filtered(); C
        Category of filtered modules with basis over Integer Ring
        sage: sorted(C.super_categories(), key=str)
        [Category of filtered modules over Integer Ring,
         Category of modules with basis over Integer Ring]
        sage: C is ModulesWithBasis(ZZ).Filtered()
        True

    TESTS::

        sage: TestSuite(C).run()
    """
    class ParentMethods:

        # TODO: which syntax do we prefer?
        # A.basis(degree = 3)
        # A.basis().subset(degree=3)

        # This is related to the following design question:
        # If F = (f_i)_{i\in I} is a family, should ``F.subset(degree = 3)``
        # be the elements of F of degree 3 or those whose index is of degree 3?

        def basis(self, d=None):
            r"""
            Return the basis for (the ``d``-th homogeneous component
            of) ``self``.

            INPUT:

            - ``d`` -- (optional, default ``None``) nonnegative integer
              or ``None``

            OUTPUT:

            If ``d`` is ``None``, returns the basis of the module.
            Otherwise, returns the basis of the homogeneous component
            of degree ``d`` (i.e., the subfamily of the basis of the
            whole module which consists only of the basis vectors
            lying in `F_d \setminus \bigcup_{i<d} F_i`).

            EXAMPLES::

                sage: A = ModulesWithBasis(ZZ).Filtered().example()
                sage: A.basis(4)
                Lazy family (Term map from Partitions to An example of a filtered module with basis: the free module on partitions over Integer Ring(i))_{i in Partitions of the integer 4}

            Without arguments, the full basis is returned::

                sage: A.basis()
                Lazy family (Term map from Partitions to An example of a filtered module with basis: the free module on partitions over Integer Ring(i))_{i in Partitions}
                sage: A.basis()
                Lazy family (Term map from Partitions to An example of a filtered module with basis: the free module on partitions over Integer Ring(i))_{i in Partitions}
            """
            from sage.sets.family import Family
            if d is None:
                return Family(self._indices, self.monomial)
            else:
                return Family(self._indices.subset(size=d), self.monomial)

    class ElementMethods:

        def is_homogeneous(self):
            r"""
            Return whether ``self`` is homogeneous.

            EXAMPLES::

                sage: A = ModulesWithBasis(ZZ).Filtered().example()
                sage: x=A(Partition((3,2,1)))
                sage: y=A(Partition((4,4,1)))
                sage: z=A(Partition((2,2,2)))
                sage: (3*x).is_homogeneous()
                True
                sage: (x - y).is_homogeneous()
                False
                sage: (x+2*z).is_homogeneous()
                True
            """
            degree_on_basis = self.parent().degree_on_basis
            degree = None
            for m in self.support():
                if degree is None:
                    degree = degree_on_basis(m)
                else:
                    if degree != degree_on_basis(m):
                        return False
            return True

        def degree(self):
            r"""
            The degree of a nonzero homogeneous element ``self`` in the
            filtered module.

            .. NOTE::

                This raises an error if the element is not homogeneous.
                Another implementation option would be to return the
                maximum of the degrees of the homogeneous summands.

            EXAMPLES::

                sage: A = ModulesWithBasis(ZZ).Filtered().example()
                sage: x = A(Partition((3,2,1)))
                sage: y = A(Partition((4,4,1)))
                sage: z = A(Partition((2,2,2)))
                sage: x.degree()
                6
                sage: (x + 2*z).degree()
                6
                sage: (y - x).degree()
                Traceback (most recent call last):
                ...
                ValueError: element is not homogeneous
            """
            if not self.support():
                raise ValueError("the zero element does not have a well-defined degree")
            if not self.is_homogeneous():
                raise ValueError("element is not homogeneous")
            return self.parent().degree_on_basis(self.leading_support())

#        .. TODO::
#
#            maximal_degree. This actually does not depend on the basis
#            and can probably be copied, up to doctests, from
#            filtered_algebras_with_basis.py.

        def homogeneous_component(self, n):
            """
            Return the homogeneous component of degree ``n`` of this
            element.

            Let `m` be an element of a filtered `R`-module `M` with
            basis. Then, `m` can be uniquely written in the form
            `m = \sum_{i \in I} m_i`, where each `m_i` is a
            homogeneous element of degree `i`. For `n \in I`, we
            define the homogeneous component of degree `n` of the
            element `m` to be `m_n`.

            EXAMPLES::

                sage: A = ModulesWithBasis(ZZ).Filtered().example()
                sage: x = A.an_element(); x
                2*P[] + 2*P[1] + 3*P[2]
                sage: x.homogeneous_component(-1)
                0
                sage: x.homogeneous_component(0)
                2*P[]
                sage: x.homogeneous_component(1)
                2*P[1]
                sage: x.homogeneous_component(2)
                3*P[2]
                sage: x.homogeneous_component(3)
                0

            TESTS:

            Check that this really returns ``A.zero()`` and not a plain ``0``::

                sage: x.homogeneous_component(3).parent() is A
                True
            """
            degree_on_basis = self.parent().degree_on_basis
            return self.parent().sum_of_terms((i, c)
                                              for (i, c) in self
                                              if degree_on_basis(i) == n)

        def truncate(self, n):
            """
            Return the sum of the homogeneous components of degree
            strictly less than ``n`` of ``self``.

            See :meth:`homogeneous_component` for the notion of a
            homogeneous component.

            EXAMPLES::

                sage: A = ModulesWithBasis(ZZ).Filtered().example()
                sage: x = A.an_element(); x
                2*P[] + 2*P[1] + 3*P[2]
                sage: x.truncate(0)
                0
                sage: x.truncate(1)
                2*P[]
                sage: x.truncate(2)
                2*P[] + 2*P[1]
                sage: x.truncate(3)
                2*P[] + 2*P[1] + 3*P[2]

            TESTS:

            Check that this really return ``A.zero()`` and not a plain ``0``::

                sage: x.truncate(0).parent() is A
                True
            """
            degree_on_basis = self.parent().degree_on_basis
            return self.parent().sum_of_terms((i, c) for (i, c) in self
                                              if degree_on_basis(i) < n)

