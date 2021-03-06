# distutils: depends = sage/geometry/polyhedron/combinatorial_polyhedron/bit_vector_operations.cc
# distutils: language = c++
# distutils: extra_compile_args = -std=c++11

r"""
Combinatorial face of a polyhedron

This module provides the combinatorial type of a polyhedral face.

.. SEEALSO::

    :mod:`sage.geometry.polyhedron.combinatorial_polyhedron.base`,
    :mod:`sage.geometry.polyhedron.combinatorial_polyhedron.face_iterator`.

EXAMPLES:

Obtain a face from a face iterator::

    sage: P = polytopes.cube()
    sage: C = CombinatorialPolyhedron(P)
    sage: it = C.face_iter()
    sage: face = next(it); face
    A 2-dimensional face of a 3-dimensional combinatorial polyhedron

Obtain a face from a face lattice index:

    sage: P = polytopes.simplex(2)
    sage: C = CombinatorialPolyhedron(P)
    sage: sorted(C.face_lattice()._elements)
    [0, 1, 2, 3, 4, 5, 6, 7]
    sage: face = C.face_by_face_lattice_index(0); face
    A -1-dimensional face of a 2-dimensional combinatorial polyhedron

Obtain further information regarding a face::

    sage: P = polytopes.octahedron()
    sage: C = CombinatorialPolyhedron(P)
    sage: it = C.face_iter(2)
    sage: face = next(it); face
    A 2-dimensional face of a 3-dimensional combinatorial polyhedron
    sage: face.ambient_Vrepresentation()
    (A vertex at (0, 0, 1), A vertex at (0, 1, 0), A vertex at (1, 0, 0))
    sage: face.n_ambient_Vrepresentation()
    3
    sage: face.ambient_H_indices()
    (5,)
    sage: face.dimension()
    2
    sage: face.ambient_dimension()
    3

.. SEEALSO::

    :class:`sage.geometry.polyhedron.combinatorial_polyhedron.base.CombinatorialPolyhedron`.

AUTHOR:

- Jonathan Kliem (2019-05)
"""

#*****************************************************************************
#       Copyright (C) 2019 Jonathan Kliem <jonathan.kliem@fu-berlin.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.misc.superseded        import deprecated_function_alias

import numbers
from sage.rings.integer         cimport smallInteger
from .conversions               cimport bit_rep_to_Vrep_list
from .base                      cimport CombinatorialPolyhedron
from .polyhedron_face_lattice   cimport PolyhedronFaceLattice
from libc.string                cimport memcpy

cdef extern from "bit_vector_operations.cc":
    cdef size_t count_atoms(uint64_t *A, size_t face_length)
#        Return the number of atoms/vertices in A.
#        This is the number of set bits in A.
#        ``face_length`` is the length of A in terms of uint64_t.

    cdef size_t bit_rep_to_coatom_rep(
            uint64_t *face, uint64_t **coatoms, size_t n_coatoms,
            size_t face_length, size_t *output)
#        Write the coatom-representation of face in output. Return length.
#        ``face_length`` is the length of ``face`` and ``coatoms[i]``
#        in terms of uint64_t.
#        ``n_coatoms`` length of ``coatoms``.

cdef extern from "Python.h":
    int unlikely(int) nogil  # Defined by Cython

cdef class CombinatorialFace(SageObject):
    r"""
    A class of the combinatorial type of a polyhedral face.

    EXAMPLES:

    Obtain a combinatorial face from a face iterator::

        sage: P = polytopes.cyclic_polytope(5,8)
        sage: C = CombinatorialPolyhedron(P)
        sage: it = C.face_iter()
        sage: next(it)
        A 0-dimensional face of a 5-dimensional combinatorial polyhedron

    Obtain a combinatorial face from an index of the face lattice::

        sage: F = C.face_lattice()
        sage: F._elements[3]
        29
        sage: C.face_by_face_lattice_index(29)
        A 1-dimensional face of a 5-dimensional combinatorial polyhedron

    Obtain the dimension of a combinatorial face::

        sage: face = next(it)
        sage: face.dimension()
        0

    The dimension of the polyhedron::

        sage: face.ambient_dimension()
        5

    The Vrepresentation::

        sage: face.ambient_Vrepresentation()
        (A vertex at (6, 36, 216, 1296, 7776),)
        sage: face.ambient_V_indices()
        (6,)
        sage: face.n_ambient_Vrepresentation()
        1

    The Hrepresentation::

        sage: face.ambient_Hrepresentation()
        (An inequality (60, -112, 65, -14, 1) x + 0 >= 0,
         An inequality (180, -216, 91, -16, 1) x + 0 >= 0,
         An inequality (360, -342, 119, -18, 1) x + 0 >= 0,
         An inequality (840, -638, 179, -22, 1) x + 0 >= 0,
         An inequality (-2754, 1175, -245, 25, -1) x + 2520 >= 0,
         An inequality (504, -450, 145, -20, 1) x + 0 >= 0,
         An inequality (-1692, 853, -203, 23, -1) x + 1260 >= 0,
         An inequality (252, -288, 113, -18, 1) x + 0 >= 0,
         An inequality (-844, 567, -163, 21, -1) x + 420 >= 0,
         An inequality (84, -152, 83, -16, 1) x + 0 >= 0,
         An inequality (-210, 317, -125, 19, -1) x + 0 >= 0)
        sage: face.ambient_H_indices()
        (3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19)
        sage: face.n_ambient_Hrepresentation()
        11
    """
    def __init__(self, data, dimension=None, index=None):
        r"""
        Initialize :class:`CombinatorialFace`.

        See :class:`CombinatorialFace`.

        TESTS::

            sage: C = CombinatorialPolyhedron([[0,1,2],[0,1,3],
            ....: [0,2,3],[1,2,3]])
            sage: it = C.face_iter()
            sage: next(it)     # indirect doctest
            A 2-dimensional face of a 3-dimensional combinatorial polyhedron

            sage: C.face_by_face_lattice_index(0)
            A -1-dimensional face of a 3-dimensional combinatorial polyhedron

            sage: TestSuite(sage.geometry.polyhedron.combinatorial_polyhedron.combinatorial_face.CombinatorialFace).run()
        """
        cdef FaceIterator it
        cdef PolyhedronFaceLattice all_faces

        if isinstance(data, FaceIterator):
            assert dimension is None and index is None, "dimension and index must be ``None``, when providing a face iterator"

            # Copy data from FaceIterator.
            it = data
            self._dual              = it.dual
            self.face_mem           = ListOfFaces(1, it.structure.face_length*64)
            self.face               = self.face_mem.data[0]
            memcpy(self.face, it.structure.face, it.structure.face_length*8)
            self._mem               = MemoryAllocator()
            self._dimension         = it.structure.current_dimension
            self._ambient_dimension = it.structure.dimension
            self.face_length        = it.structure.face_length
            self._ambient_Vrep      = it._Vrep
            self._ambient_facets    = it._facet_names
            self._equalities        = it._equalities
            self.atoms              = it.atoms
            self.coatoms            = it.coatoms
            self._hash_index        = it.structure._index

        elif isinstance(data, PolyhedronFaceLattice):
            all_faces = data
            assert isinstance(dimension, numbers.Integral), "dimension must be an integer"
            assert isinstance(index, numbers.Integral), "index must be an integer"
            assert -1 <= dimension <= all_faces.dimension, "dimension must be a face dimension of the polyhedron"
            assert 0 <= index < all_faces.f_vector[dimension + 1], "index is out of range"

            # Copy data from PolyhedronFaceLattice.
            self._dual              = all_faces.dual
            self.face_mem           = ListOfFaces(1, all_faces.face_length*64)
            self.face               = self.face_mem.data[0]
            memcpy(self.face, all_faces.faces[dimension+1][index], all_faces.face_length*8)
            self._mem               = MemoryAllocator()
            self._dimension         = dimension
            self._ambient_dimension = all_faces.dimension
            self.face_length        = all_faces.face_length
            self._ambient_Vrep      = all_faces._Vrep
            self._ambient_facets    = all_faces._facet_names
            self._equalities        = all_faces._equalities
            self.atoms              = all_faces.atoms
            self.coatoms            = all_faces.coatoms

            self._hash_index = index
            for i in range(-1,dimension):
                self._hash_index += all_faces.f_vector[i+1]
        else:
            raise NotImplementedError("data must be face iterator or a list of all faces")

    def _repr_(self):
        r"""
        Return a description of the combinatorial face.

        EXAMPLES::

            sage: P = polytopes.permutahedron(6)
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter(dimension=3, dual=False)
            sage: face = next(it)
            sage: face.__repr__()
            'A 3-dimensional face of a 5-dimensional combinatorial polyhedron'
            sage: it = C.face_iter(dimension=3, dual=True)
            sage: face = next(it)
            sage: face.__repr__()
            'A 3-dimensional face of a 5-dimensional combinatorial polyhedron'
        """
        return "A {}-dimensional face of a {}-dimensional combinatorial polyhedron"\
                .format(self.dimension(), self.ambient_dimension())

    def __reduce__(self):
        r"""
        Override __reduce__ to indicate that pickle/unpickle will not work.

        EXAMPLES::

            sage: P = polytopes.simplex()
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter()
            sage: face = next(it)
            sage: face1 = loads(face.dumps())
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError

    def __hash__(self):
        r"""
        Return an index for the face.

        If the face was constructed from a :class:`sage.geometry.polyhedron.combinatorial_polyhedron.face_iterator.FaceIterator`,
        then this is the index of the occurence in the iterator.

        If the face was constructed from
        :meth:`sage:geometry.polyhedron.combinatorial_polyhedronn.base.CombinatorialPolyhedron.face_by_face_lattice_index`,
        then this the index in the level set plus the number of lower dimension (or higher dimension).

        EXAMPLES::

            sage: P = polytopes.simplex(2)
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter()
            sage: [hash(face) for face in it]
            [1, 2, 3, 4, 5, 6]

        TESTS::

            sage: P = polytopes.permutahedron(5)
            sage: C = CombinatorialPolyhedron(P)
            sage: F = C.face_lattice()
            sage: G = F.relabel(C.face_by_face_lattice_index)

            sage: P = polytopes.cyclic_polytope(4,10)
            sage: C = CombinatorialPolyhedron(P)
            sage: F = C.face_lattice()
            sage: G = F.relabel(C.face_by_face_lattice_index)
        """
        return self._hash_index

    def dimension(self):
        r"""
        Return the dimension of the face.

        EXAMPLES::

            sage: P = polytopes.associahedron(['A', 3])
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter()
            sage: face = next(it)
            sage: face.dimension()
            2

        ``dim`` is an alias::

            sage: face.dim()
            2
        """
        if self._dual:
            return smallInteger(self._ambient_dimension - self._dimension - 1)
        else:
            return smallInteger(self._dimension)

    dim = dimension

    def ambient_dimension(self):
        r"""
        Return the dimension of the polyhedron.

        EXAMPLES::

            sage: P = polytopes.cube()
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter()
            sage: face = next(it)
            sage: face.ambient_dimension()
            3
        """
        return smallInteger(self._ambient_dimension)

    def ambient_Vrepresentation(self):
        r"""
        Return the Vrepresentation objects of the ambient polyhedron
        defining the face.

        It consists of the vertices/rays/lines
        that face contains.

        EXAMPLES::

            sage: P = polytopes.permutahedron(5)
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter(dimension=2)
            sage: face = next(it)
            sage: face.ambient_Vrepresentation()
            (A vertex at (4, 1, 5, 2, 3),
             A vertex at (4, 2, 5, 1, 3),
             A vertex at (5, 1, 4, 2, 3),
             A vertex at (5, 2, 4, 1, 3))
            sage: face = next(it)
            sage: face.ambient_Vrepresentation()
            (A vertex at (4, 1, 5, 2, 3),
             A vertex at (4, 1, 5, 3, 2),
             A vertex at (5, 1, 4, 2, 3),
             A vertex at (5, 1, 4, 3, 2))

            sage: C = CombinatorialPolyhedron([[0,1,2],[0,1,3],[0,2,3],[1,2,3]])
            sage: it = C.face_iter()
            sage: for face in it: (face.dimension(), face.ambient_Vrepresentation())
            (2, (1, 2, 3))
            (2, (0, 2, 3))
            (2, (0, 1, 3))
            (2, (0, 1, 2))
            (1, (2, 3))
            (1, (1, 3))
            (1, (1, 2))
            (0, (3,))
            (0, (2,))
            (0, (1,))
            (1, (0, 3))
            (1, (0, 2))
            (0, (0,))
            (1, (0, 1))

        .. SEEALSO::

            :meth:`ambient_V_indices`.
        """
        if not self._ambient_Vrep:
            # There are no names, so we return indices instead.
            return self.ambient_V_indices()
        cdef size_t length
        if self._dual:
            # if dual, the Vrepresentation corresponds to the coatom-representation
            length = self.set_coatom_rep()
            return tuple(self._ambient_Vrep[self.coatom_rep[i]]
                         for i in range(length))
        else:
            # if not dual, the Vrepresentation corresponds to the atom-representation
            length = self.set_atom_rep()
            return tuple(self._ambient_Vrep[self.atom_rep[i]]
                         for i in range(length))

    def ambient_V_indices(self):
        r"""
        Return the indices of the Vrepresentation
        objects of the ambient polyhedron defining the face.

        EXAMPLES::

            sage: P = polytopes.permutahedron(5)
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter(dimension=2)
            sage: face = next(it)
            sage: next(it).ambient_V_indices()
            (76, 77, 100, 101)
            sage: next(it).ambient_V_indices()
            (76, 77, 82, 83, 88, 89)

            sage: C = CombinatorialPolyhedron([[0,1,2],[0,1,3],[0,2,3],[1,2,3]])
            sage: it = C.face_iter()
            sage: for face in it: (face.dimension(), face.ambient_V_indices())
            (2, (1, 2, 3))
            (2, (0, 2, 3))
            (2, (0, 1, 3))
            (2, (0, 1, 2))
            (1, (2, 3))
            (1, (1, 3))
            (1, (1, 2))
            (0, (3,))
            (0, (2,))
            (0, (1,))
            (1, (0, 3))
            (1, (0, 2))
            (0, (0,))
            (1, (0, 1))

        .. SEEALSO::

            :meth:`ambient_Vrepresentation`.
        """
        cdef size_t length
        if self._dual:
            # if dual, the Vrepresentation corresponds to the coatom-representation
            length = self.set_coatom_rep()
            return tuple(smallInteger(self.coatom_rep[i])
                         for i in range(length))
        else:
            # if not dual, the Vrepresentation corresponds to the atom-representation
            length = self.set_atom_rep()
            return tuple(smallInteger(self.atom_rep[i])
                         for i in range(length))

    def Vrepr(self, names=True):
        r"""
        The method is deprecated. Use one of the following:
        - :meth:`CombinatorialFace.ambient_Vrepresentation`
        - :meth:`CombinatorialFace.ambient_V_indices`

        Return the vertex-representation of the current face.

        The vertex-representation consists of
        the ``[vertices, rays, lines]`` that face contains.

        INPUT:

        - ``names`` -- if ``True`` returns the names of the ``[vertices, rays, lines]``
          as given on initialization of the :class:`~sage.geometry.polyhedron.combinatorial_polyhedron.base.CombinatorialPolyhedron`

        TESTS::

            sage: P = polytopes.permutahedron(5)
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter(dimension=2)
            sage: face = next(it)
            sage: face.Vrepr()
            doctest:...: DeprecationWarning: the method Vrepr of CombinatorialPolyhedron is deprecated; use ambient_V_indices or ambient_Vrepresentation
            See https://trac.sagemath.org/28616 for details.
            (A vertex at (4, 1, 5, 2, 3),
             A vertex at (4, 2, 5, 1, 3),
             A vertex at (5, 1, 4, 2, 3),
             A vertex at (5, 2, 4, 1, 3))
        """
        from sage.misc.superseded import deprecation
        deprecation(28616, "the method Vrepr of CombinatorialPolyhedron is deprecated; use ambient_V_indices or ambient_Vrepresentation", 3)
        if names:
            return self.ambient_Vrepresentation()
        else:
            return self.ambient_V_indices()

    def n_ambient_Vrepresentation(self):
        r"""
        Return the length of the :meth:`CombinatorialFace.ambient_V_indices`.

        Might be faster than then using ``len``.

        EXAMPLES::

            sage: P = polytopes.cube()
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter()
            sage: all(face.n_ambient_Vrepresentation() == len(face.ambient_Vrepresentation()) for face in it)
            True

        TESTS::

            sage: P = polytopes.cube()
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter()
            sage: face = next(it)
            sage: _ = face.n_Vrepr()
            doctest:...: DeprecationWarning: n_Vrepr is deprecated. Please use n_ambient_Vrepresentation instead.
            See https://trac.sagemath.org/28614 for details.
        """
        if self._dual:
            return smallInteger(self.set_coatom_rep())
        else:
            return smallInteger(self.n_atom_rep())

    n_Vrepr = deprecated_function_alias(28614, n_ambient_Vrepresentation)

    def ambient_Hrepresentation(self):
        r"""
        Return the Hrepresentation objects of the ambient polyhedron
        defining the face.

        It consists of the facets/inequalities that contain the face
        and the equalities defining the ambient polyhedron.

        EXAMPLES::

            sage: P = polytopes.permutahedron(5)
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter(2)
            sage: next(it).ambient_Hrepresentation()
            (An inequality (0, 1, 0, 1, 0) x - 3 >= 0,
             An inequality (0, 1, 0, 1, 1) x - 6 >= 0,
             An equation (1, 1, 1, 1, 1) x - 15 == 0)
            sage: next(it).ambient_Hrepresentation()
            (An inequality (0, 1, 0, 0, 0) x - 1 >= 0,
             An inequality (0, 1, 0, 1, 1) x - 6 >= 0,
             An equation (1, 1, 1, 1, 1) x - 15 == 0)

            sage: P = polytopes.cyclic_polytope(4,6)
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter()
            sage: next(it).ambient_Hrepresentation()
            (An inequality (-20, 29, -10, 1) x + 0 >= 0,
             An inequality (60, -47, 12, -1) x + 0 >= 0,
             An inequality (30, -31, 10, -1) x + 0 >= 0,
             An inequality (10, -17, 8, -1) x + 0 >= 0,
             An inequality (-154, 71, -14, 1) x + 120 >= 0,
             An inequality (-78, 49, -12, 1) x + 40 >= 0)
            sage: next(it).ambient_Hrepresentation()
            (An inequality (-50, 35, -10, 1) x + 24 >= 0,
             An inequality (-12, 19, -8, 1) x + 0 >= 0,
             An inequality (-20, 29, -10, 1) x + 0 >= 0,
             An inequality (60, -47, 12, -1) x + 0 >= 0,
             An inequality (-154, 71, -14, 1) x + 120 >= 0,
             An inequality (-78, 49, -12, 1) x + 40 >= 0)

        .. SEEALSO::

            :meth:`ambient_H_indices`.
        """
        if not self._ambient_facets:
            # There are no names, so we return indices instead.
            return self.ambient_H_indices()
        cdef size_t length
        if not self._dual:
            # if not dual, the facet-representation corresponds to the coatom-representation
            length = self.set_coatom_rep()  # fill self.coatom_repr_face
            return tuple(self._ambient_facets[self.coatom_rep[i]]
                         for i in range(length)) + self._equalities
        else:
            # if dual, the facet-representation corresponds to the atom-representation
            length = self.set_atom_rep()  # fill self.atom_repr_face
            return tuple(self._ambient_facets[self.atom_rep[i]]
                         for i in range(length)) + self._equalities

    def ambient_H_indices(self):
        r"""
        Return the indices of the Hrepresentation objects
        of the ambient polyhedron defining the face.

        EXAMPLES::

            sage: P = polytopes.permutahedron(5)
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter(2)
            sage: next(it).ambient_H_indices()
            (28, 29)
            sage: next(it).ambient_H_indices()
            (25, 29)

            sage: P = polytopes.cyclic_polytope(4,6)
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter()
            sage: _ = next(it); _ = next(it)
            sage: next(it).ambient_H_indices()
            (0, 1, 2, 4, 5, 7)
            sage: next(it).ambient_H_indices()
            (0, 1, 5, 6, 7, 8)
            sage: next(it).ambient_H_indices()
            (0, 1, 2, 3, 6, 8)
            sage: [next(it).dimension() for _ in range(2)]
            [0, 1]
            sage: face = next(it)
            sage: face.ambient_H_indices()
            (4, 5, 7)

        .. SEEALSO::

            :meth:`ambient_Hrepresentation`.
        """
        cdef size_t length
        if not self._dual:
            # if not dual, the facet-representation corresponds to the coatom-representation
            length = self.set_coatom_rep()  # fill self.coatom_repr_face
            return tuple(smallInteger(self.coatom_rep[i])
                         for i in range(length))
        else:
            # if dual, the facet-representation corresponds to the atom-representation
            length = self.set_atom_rep()  # fill self.atom_repr_face
            return tuple(smallInteger(self.atom_rep[i])
                         for i in range(length))

    def Hrepr(self, names=True):
        r"""
        The method is deprecated. Use one of the following:
        - :meth:`CombinatorialFace.ambient_Hrepresentation`
        - :meth:`CombinatorialFace.ambient_H_indices`

        Return the Hrepresentation of the face.

        If ``names`` is ``False`` this is just the indices
        of the facets the face is contained in.
        If ``names`` is ``True`` this the defining facets
        and equations of the face.

        The facet-representation consists of the facets
        that contain the face and of the equalities of the polyhedron.

        INPUT:

        - ``names`` -- if ``True`` returns the names of the ``[facets, equations]``
          as given on initialization of :class:`~sage.geometry.polyhedron.combinatorial_polyhedron.base.CombinatorialPolyhedron`

        TESTS::

            sage: P = polytopes.permutahedron(5)
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter(2)
            sage: next(it).Hrepr()
            doctest:...: DeprecationWarning: the method Hrepr of CombinatorialPolyhedron is deprecated; use ambient_H_indices or ambient_Hrepresentation
            See https://trac.sagemath.org/28616 for details.
            (An inequality (0, 1, 0, 1, 0) x - 3 >= 0,
             An inequality (0, 1, 0, 1, 1) x - 6 >= 0,
             An equation (1, 1, 1, 1, 1) x - 15 == 0)
        """
        from sage.misc.superseded import deprecation
        deprecation(28616, "the method Hrepr of CombinatorialPolyhedron is deprecated; use ambient_H_indices or ambient_Hrepresentation", 3)
        if names:
            return self.ambient_Hrepresentation()
        else:
            return self.ambient_H_indices()

    def n_ambient_Hrepresentation(self):
        r"""
        Return the length of the :meth:`CombinatorialFace.ambient_H_indices`.

        Might be faster than then using ``len``.

        EXAMPLES::

            sage: P = polytopes.cube()
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter()
            sage: all(face.n_ambient_Hrepresentation() == len(face.ambient_Hrepresentation()) for face in it)
            True

        TESTS::

            sage: P = polytopes.cube()
            sage: C = CombinatorialPolyhedron(P)
            sage: it = C.face_iter()
            sage: face = next(it)
            sage: _ = face.n_Hrepr()
            doctest:...: DeprecationWarning: n_Hrepr is deprecated. Please use n_ambient_Hrepresentation instead.
            See https://trac.sagemath.org/28614 for details.
        """
        if not self._dual:
            return smallInteger(self.set_coatom_rep())
        else:
            return smallInteger(self.n_atom_rep())

    n_Hrepr = deprecated_function_alias(28614, n_ambient_Hrepresentation)

    cdef size_t n_atom_rep(self) except -1:
        r"""
        Compute the number of atoms in the current face by counting the
        number of set bits.
        """
        if self.face:
            return count_atoms(self.face, self.face_length)

        # The face was not initialized properly.
        raise LookupError("``FaceIterator`` does not point to a face")

    cdef size_t set_coatom_rep(self) except -1:
        r"""
        Set ``coatom_rep`` to be the coatom-representation of the current face.
        Return its length.
        """
        cdef size_t n_coatoms = self.coatoms.n_faces
        cdef uint64_t **coatoms = self.coatoms.data
        cdef size_t face_length = self.face_length
        if not self.coatom_rep:
            self.coatom_rep = <size_t *> self._mem.allocarray(self.coatoms.n_faces, sizeof(size_t))
        return bit_rep_to_coatom_rep(self.face, coatoms, n_coatoms,
                                       face_length, self.coatom_rep)

    cdef size_t set_atom_rep(self) except -1:
        r"""
        Set ``atom_rep`` to be the atom-representation of the current face.
        Return its length.
        """
        cdef size_t face_length = self.face_length
        if not self.atom_rep:
            self.atom_rep = <size_t *> self._mem.allocarray(self.coatoms.n_atoms, sizeof(size_t))
        return bit_rep_to_Vrep_list(self.face, self.atom_rep, face_length)

