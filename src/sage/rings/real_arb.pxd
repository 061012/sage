from sage.libs.arb.arb cimport arb_t
from sage.rings.real_mpfi cimport RealIntervalFieldElement
from sage.structure.parent cimport Parent
from sage.structure.element cimport Element

include 'mpfi.pxi'

cdef void mpfi_to_arb(arb_t target, const mpfi_t source, const unsigned long precision)
cdef void arb_to_mpfi(mpfi_t target, arb_t source, const unsigned long precision)

cdef class RealBallField_class(Parent):
    cdef unsigned long precision

cdef class RealBallElement(Element):
    cdef arb_t value
    cdef RealBallElement _new(self)
    cpdef RealIntervalFieldElement RealIntervalFieldElement(self)
    cpdef RealBallElement psi(self)
