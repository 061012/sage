r"""
Common Transducers (Finite State Machines Generators)

Transducers in Sage can be built through the ``transducers``
object. It contains generators for common finite state machines. For example,

::

    sage: I = transducers.Identity([0, 1, 2])

generates an identity transducer on the alphabet `\{0, 1, 2\}`.

To construct transducers manually, you can use the class
:class:`Transducer`. See :mod:`~sage.combinat.finite_state_machine`
for more details and a lot of examples.

**Transducers**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~TransducerGenerators.Identity` | Returns a transducer realizing the identity map.
    :meth:`~TransducerGenerators.abs` | Returns a transducer realizing absolute value.
    :meth:`~TransducerGenerators.operator` | Returns a transducer realizing a binary operation.
    :meth:`~TransducerGenerators.all` | Returns a transducer realizing logical ``and``.
    :meth:`~TransducerGenerators.any` | Returns a transducer realizing logical ``or``.
    :meth:`~TransducerGenerators.add` | Returns a transducer realizing addition.
    :meth:`~TransducerGenerators.sub` | Returns a transducer realizing subtraction.
    :meth:`~TransducerGenerators.CountSubblockOccurrences` | Returns a transducer counting the occurrences of a subblock.
    :meth:`~TransducerGenerators.Wait` | Returns a transducer writing ``False`` until first (or k-th) true input is read.
    :meth:`~TransducerGenerators.weight` | Returns a transducer realizing the Hamming weight
    :meth:`~TransducerGenerators.GrayCode` | Returns a transducer realizing binary Gray code.
    :meth:`~TransducerGenerators.Recursion` | Returns a transducer defined by recursions

AUTHORS:

- Clemens Heuberger (2014-04-07): initial version
- Sara Kropf (2014-04-10): some changes in TransducerGenerator
- Daniel Krenn (2014-04-15): improved common docstring during review
- Clemens Heuberger, Daniel Krenn, Sara Kropf (2014-04-16--2014-05-02):
  A couple of improvements. Details see
  #16141, #16142, #16143, #16186.
- Sara Kropf (2014-04-29): weight transducer
- Clemens Heuberger, Daniel Krenn (2014-07-18): transducers Wait, all,
  any
- Clemens Heuberger (2014-08-10): transducer Recursion

ACKNOWLEDGEMENT:

- Clemens Heuberger, Daniel Krenn and Sara Kropf are supported by the
  Austrian Science Fund (FWF): P 24644-N26.

Functions and methods
---------------------

"""
#*****************************************************************************
#       Copyright (C) 2014 Clemens Heuberger <clemens.heuberger@aau.at>
#                     2014 Daniel Krenn <dev@danielkrenn.at>
#                     2014 Sara Kropf <sara.kropf@aau.at>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                http://www.gnu.org/licenses/
#*****************************************************************************

import collections
import operator

from sage.combinat.finite_state_machine import Transducer
from sage.rings.integer_ring import ZZ
from sage.rings.rational_field import QQ

class TransducerGenerators(object):
    r"""
    A class consisting of constructors for several common transducers.

    A list of all transducers in this database is available via tab
    completion. Type "``transducers.``" and then hit tab to see which
    transducers are available.

    The transducers currently in this class include:

    - :meth:`~Identity`
    - :meth:`~abs`
    - :meth:`~TransducerGenerators.operator`
    - :meth:`~all`
    - :meth:`~any`
    - :meth:`~add`
    - :meth:`~sub`
    - :meth:`~CountSubblockOccurrences`
    - :meth:`~Wait`
    - :meth:`~GrayCode`

    """

    def Identity(self, input_alphabet):
        """
        Returns the identity transducer realizing the identity map.

        INPUT:

        - ``input_alphabet`` -- a list or other iterable.

        OUTPUT:

        A transducer mapping each word over ``input_alphabet`` to
        itself.

        EXAMPLES::

            sage: T = transducers.Identity([0, 1])
            sage: sorted(T.transitions())
            [Transition from 0 to 0: 0|0,
             Transition from 0 to 0: 1|1]
            sage: T.initial_states()
            [0]
            sage: T.final_states()
            [0]
            sage: T.input_alphabet
            [0, 1]
            sage: T.output_alphabet
            [0, 1]
            sage: sage.combinat.finite_state_machine.FSMOldProcessOutput = False
            sage: T([0, 1, 0, 1, 1])
            [0, 1, 0, 1, 1]

        """
        return Transducer(
            [(0, 0, d, d) for d in input_alphabet],
            input_alphabet=input_alphabet,
            output_alphabet=input_alphabet,
            initial_states=[0],
            final_states=[0])

    def CountSubblockOccurrences(self, block, input_alphabet):
        """
        Returns a transducer counting the number of (possibly
        overlapping) occurrences of a block in the input.

        INPUT:

        - ``block`` -- a list (or other iterable) of letters.

        - ``input_alphabet`` -- a list or other iterable.

        OUTPUT:

        A transducer counting (in unary) the number of occurrences of the given
        block in the input.  Overlapping occurrences are counted several
        times.

        Denoting the block by `b_0\ldots b_{k-1}`, the input word by
        `i_0\ldots i_L` and the output word by `o_0\ldots o_L`, we
        have `o_j = 1` if and only if `i_{j-k+1}\ldots i_{j} = b_0\ldots
        b_{k-1}`. Otherwise, `o_j = 0`.

        EXAMPLES:

        #.  Counting the number of ``10`` blocks over the alphabet
            ``[0, 1]``::

                sage: T = transducers.CountSubblockOccurrences(
                ....:     [1, 0],
                ....:     [0, 1])
                sage: sorted(T.transitions())
                [Transition from () to (): 0|0,
                 Transition from () to (1,): 1|0,
                 Transition from (1,) to (): 0|1,
                 Transition from (1,) to (1,): 1|0]
                sage: T.input_alphabet
                [0, 1]
                sage: T.output_alphabet
                [0, 1]
                sage: T.initial_states()
                [()]
                sage: T.final_states()
                [(), (1,)]

            Check some sequence::

                sage: sage.combinat.finite_state_machine.FSMOldProcessOutput = False
                sage: T([0, 1, 0, 1, 1, 0])
                [0, 0, 1, 0, 0, 1]

        #.  Counting the number of ``11`` blocks over the alphabet
            ``[0, 1]``::

                sage: T = transducers.CountSubblockOccurrences(
                ....:     [1, 1],
                ....:     [0, 1])
                sage: sorted(T.transitions())
                [Transition from () to (): 0|0,
                 Transition from () to (1,): 1|0,
                 Transition from (1,) to (): 0|0,
                 Transition from (1,) to (1,): 1|1]

            Check some sequence::

                sage: sage.combinat.finite_state_machine.FSMOldProcessOutput = False
                sage: T([0, 1, 0, 1, 1, 0])
                [0, 0, 0, 0, 1, 0]

        #.  Counting the number of ``1010`` blocks over the
            alphabet ``[0, 1, 2]``::

                sage: T = transducers.CountSubblockOccurrences(
                ....:     [1, 0, 1, 0],
                ....:     [0, 1, 2])
                sage: sorted(T.transitions())
                [Transition from () to (): 0|0,
                 Transition from () to (1,): 1|0,
                 Transition from () to (): 2|0,
                 Transition from (1,) to (1, 0): 0|0,
                 Transition from (1,) to (1,): 1|0,
                 Transition from (1,) to (): 2|0,
                 Transition from (1, 0) to (): 0|0,
                 Transition from (1, 0) to (1, 0, 1): 1|0,
                 Transition from (1, 0) to (): 2|0,
                 Transition from (1, 0, 1) to (1, 0): 0|1,
                 Transition from (1, 0, 1) to (1,): 1|0,
                 Transition from (1, 0, 1) to (): 2|0]
                sage: input =  [0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 2]
                sage: output = [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
                sage: sage.combinat.finite_state_machine.FSMOldProcessOutput = False
                sage: T(input) == output
                True

        """
        block_as_tuple = tuple(block)

        def starts_with(what, pattern):
            return len(what) >= len(pattern) \
                and what[:len(pattern)] == pattern

        def transition_function(read, input):
            current = read + (input, )
            if starts_with(block_as_tuple, current) \
                    and len(block_as_tuple) > len(current):
                return (current, 0)
            else:
                k = 1
                while not starts_with(block_as_tuple, current[k:]):
                    k += 1
                return (current[k:], int(block_as_tuple == current))

        T = Transducer(
            transition_function,
            input_alphabet=input_alphabet,
            output_alphabet=[0, 1],
            initial_states=[()])
        for s in T.iter_states():
            s.is_final = True
        return T

    def Wait(self, input_alphabet, threshold=1):
        r"""
        Writes ``False`` until reading the ``threshold``-th occurrence
        of a true input letter; then writes ``True``.

        INPUT:

        - ``input_alphabet`` -- a list or other iterable.

        - ``threshold`` -- a positive integer specifying how many
          occurrences of ``True`` inputs are waited for.

        OUTPUT:

        A transducer writing ``False`` until the ``threshold``-th true
        (Python's standard conversion to boolean is used to convert the
        actual input to boolean) input is read. Subsequently, the
        transducer writes ``True``.

        EXAMPLES::

            sage: T = transducers.Wait([0, 1])
            sage: T([0, 0, 1, 0, 1, 0])
            [False, False, True, True, True, True]
            sage: T2 = transducers.Wait([0, 1], threshold=2)
            sage: T2([0, 0, 1, 0, 1, 0])
            [False, False, False, False, True, True]
        """
        def transition(state, input):
            if state == threshold:
                return (threshold, True)
            if not input:
                return (state, False)
            return (state + 1, state + 1 == threshold)

        T = Transducer(transition,
                       input_alphabet=input_alphabet,
                       initial_states=[0])
        for s in T.iter_states():
            s.is_final = True

        return T


    def operator(self, operator, input_alphabet, number_of_operands=2):
        r"""
        Returns a transducer which realizes an operation
        on tuples over the given input alphabet.

        INPUT:

        - ``operator`` -- operator to realize. It is a function which
          takes ``number_of_operands`` input arguments (each out of
          ``input_alphabet``).

        - ``input_alphabet``  -- a list or other iterable.

        - ``number_of_operands`` -- (default: `2`) it specifies the number
          of input arguments the operator takes.

        OUTPUT:

        A transducer mapping an input letter `(i_1, \dots, i_n)` to
        `\mathrm{operator}(i_1, \dots, i_n)`. Here, `n` equals
        ``number_of_operands``.

        The input alphabet of the generated transducer is the cartesian
        product of ``number_of_operands`` copies of ``input_alphabet``.

        EXAMPLE:

        The following binary transducer realizes component-wise
        addition (this transducer is also available as :meth:`.add`)::

            sage: import operator
            sage: T = transducers.operator(operator.add, [0, 1])
            sage: T.transitions()
            [Transition from 0 to 0: (0, 0)|0,
             Transition from 0 to 0: (0, 1)|1,
             Transition from 0 to 0: (1, 0)|1,
             Transition from 0 to 0: (1, 1)|2]
            sage: T.input_alphabet
            [(0, 0), (0, 1), (1, 0), (1, 1)]
            sage: T.initial_states()
            [0]
            sage: T.final_states()
            [0]
            sage: T([(0, 0), (0, 1), (1, 0), (1, 1)])
            [0, 1, 1, 2]

        Note that for a unary operator the input letters of the
        new transducer are tuples of length `1`::

            sage: T = transducers.operator(abs,
            ....:                          [-1, 0, 1],
            ....:                          number_of_operands=1)
            sage: T([-1, 1, 0])
            Traceback (most recent call last):
            ...
            ValueError: Invalid input sequence.
            sage: T([(-1,), (1,), (0,)])
            [1, 1, 0]

        Compare this with the transducer generated by :meth:`.abs`::

            sage: T = transducers.abs([-1, 0, 1])
            sage: T([-1, 1, 0])
            [1, 1, 0]
        """
        from itertools import product

        def transition_function(state, operands):
            return (0, operator(*operands))
        pairs = list(product(input_alphabet, repeat=number_of_operands))
        return Transducer(transition_function,
                          input_alphabet=pairs,
                          initial_states=[0],
                          final_states=[0])


    def all(self, input_alphabet, number_of_operands=2):
        """
        Returns a transducer which realizes logical ``and`` over the given
        input alphabet.

        INPUT:

        - ``input_alphabet``  -- a list or other iterable.

        - ``number_of_operands`` -- (default: `2`) specifies the number
          of input arguments for the ``and`` operation.

        OUTPUT:

        A transducer mapping an input word
        `(i_{01}, \ldots, i_{0d})\ldots (i_{k1}, \ldots, i_{kd})` to the word
        `(i_{01} \land \cdots \land i_{0d})\ldots (i_{k1} \land \cdots \land i_{kd})`.

        The input alphabet of the generated transducer is the cartesian
        product of ``number_of_operands`` copies of ``input_alphabet``.

        EXAMPLE:

        The following transducer realizes letter-wise
        logical ``and``::

            sage: T = transducers.all([False, True])
            sage: T.transitions()
            [Transition from 0 to 0: (False, False)|False,
             Transition from 0 to 0: (False, True)|False,
             Transition from 0 to 0: (True, False)|False,
             Transition from 0 to 0: (True, True)|True]
            sage: T.input_alphabet
            [(False, False), (False, True), (True, False), (True, True)]
            sage: T.initial_states()
            [0]
            sage: T.final_states()
            [0]
            sage: T([(False, False), (False, True), (True, False), (True, True)])
            [False, False, False, True]

        More than two operands and other input alphabets (with
        conversion to boolean) are also possible::

            sage: T3 = transducers.all([0, 1], number_of_operands=3)
            sage: T3([(0, 0, 0), (1, 0, 0), (1, 1, 1)])
            [False, False, True]
        """
        return self.operator(lambda *args: all(args),
                             input_alphabet, number_of_operands)


    def any(self, input_alphabet, number_of_operands=2):
        """
        Returns a transducer which realizes logical ``or`` over the given
        input alphabet.

        INPUT:

        - ``input_alphabet``  -- a list or other iterable.

        - ``number_of_operands`` -- (default: `2`) specifies the number
          of input arguments for the ``or`` operation.

        OUTPUT:

        A transducer mapping an input word
        `(i_{01}, \ldots, i_{0d})\ldots (i_{k1}, \ldots, i_{kd})` to the word
        `(i_{01} \lor \cdots \lor i_{0d})\ldots (i_{k1} \lor \cdots \lor i_{kd})`.

        The input alphabet of the generated transducer is the cartesian
        product of ``number_of_operands`` copies of ``input_alphabet``.

        EXAMPLE:

        The following transducer realizes letter-wise
        logical ``or``::

            sage: T = transducers.any([False, True])
            sage: T.transitions()
            [Transition from 0 to 0: (False, False)|False,
             Transition from 0 to 0: (False, True)|True,
             Transition from 0 to 0: (True, False)|True,
             Transition from 0 to 0: (True, True)|True]
            sage: T.input_alphabet
            [(False, False), (False, True), (True, False), (True, True)]
            sage: T.initial_states()
            [0]
            sage: T.final_states()
            [0]
            sage: T([(False, False), (False, True), (True, False), (True, True)])
            [False, True, True, True]

        More than two operands and other input alphabets (with
        conversion to boolean) are also possible::

            sage: T3 = transducers.any([0, 1], number_of_operands=3)
            sage: T3([(0, 0, 0), (1, 0, 0), (1, 1, 1)])
            [False, True, True]
        """
        return self.operator(lambda *args: any(args),
                             input_alphabet, number_of_operands)



    def add(self, input_alphabet, number_of_operands=2):
        """
        Returns a transducer which realizes addition on pairs over the
        given input alphabet.

        INPUT:

        - ``input_alphabet``  -- a list or other iterable.

        - ``number_of_operands`` -- (default: `2`) it specifies the number
          of input arguments the operator takes.

        OUTPUT:

        A transducer mapping an input word
        `(i_{01}, \ldots, i_{0d})\ldots (i_{k1}, \ldots, i_{kd})` to the word
        `(i_{01} + \cdots + i_{0d})\ldots (i_{k1} + \cdots + i_{kd})`.

        The input alphabet of the generated transducer is the cartesian
        product of ``number_of_operands`` copies of ``input_alphabet``.

        EXAMPLE:

        The following transducer realizes letter-wise
        addition::

            sage: T = transducers.add([0, 1])
            sage: T.transitions()
            [Transition from 0 to 0: (0, 0)|0,
             Transition from 0 to 0: (0, 1)|1,
             Transition from 0 to 0: (1, 0)|1,
             Transition from 0 to 0: (1, 1)|2]
            sage: T.input_alphabet
            [(0, 0), (0, 1), (1, 0), (1, 1)]
            sage: T.initial_states()
            [0]
            sage: T.final_states()
            [0]
            sage: T([(0, 0), (0, 1), (1, 0), (1, 1)])
            [0, 1, 1, 2]

        More than two operands can also be handled::

            sage: T3 = transducers.add([0, 1], number_of_operands=3)
            sage: T3.input_alphabet
            [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
             (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
            sage: T3([(0, 0, 0), (0, 1, 0), (0, 1, 1), (1, 1, 1)])
            [0, 1, 2, 3]
        """
        return self.operator(lambda *args: sum(args),
                             input_alphabet,
                             number_of_operands=number_of_operands)


    def sub(self, input_alphabet):
        """
        Returns a transducer which realizes subtraction on pairs over
        the given input alphabet.

        INPUT:

        - ``input_alphabet``  -- a list or other iterable.

        OUTPUT:

        A transducer mapping an input word `(i_0, i'_0)\ldots (i_k, i'_k)`
        to the word `(i_0 - i'_0)\ldots (i_k - i'_k)`.

        The input alphabet of the generated transducer is the cartesian
        product of two copies of ``input_alphabet``.

        EXAMPLE:

        The following transducer realizes letter-wise
        subtraction::

            sage: T = transducers.sub([0, 1])
            sage: T.transitions()
            [Transition from 0 to 0: (0, 0)|0,
             Transition from 0 to 0: (0, 1)|-1,
             Transition from 0 to 0: (1, 0)|1,
             Transition from 0 to 0: (1, 1)|0]
            sage: T.input_alphabet
            [(0, 0), (0, 1), (1, 0), (1, 1)]
            sage: T.initial_states()
            [0]
            sage: T.final_states()
            [0]
            sage: T([(0, 0), (0, 1), (1, 0), (1, 1)])
            [0, -1, 1, 0]
        """
        return self.operator(operator.sub, input_alphabet)

    def weight(self, input_alphabet, zero=0):
        r"""
        Returns a transducer which realizes the Hamming weight of the input
        over the given input alphabet.

        INPUT:

        - ``input_alphabet`` -- a list or other iterable.

        - ``zero`` -- the zero symbol in the alphabet used

        OUTPUT:

        A transducer mapping `i_0\ldots i_k` to `(i_0\neq 0)\ldots(i_k\neq 0)`.

        The Hamming weight is defined as the number of non-zero digits in the
        input sequence over the alphabet ``input_alphabet`` (see
        :wikipedia:`Hamming_weight`). The output sequence of the transducer is
        a unary encoding of the Hamming weight. Thus the sum of the output
        sequence is the Hamming weight of the input.

        EXAMPLES::

            sage: W = transducers.weight([-1, 0, 2])
            sage: W.transitions()
            [Transition from 0 to 0: -1|1,
             Transition from 0 to 0: 0|0,
             Transition from 0 to 0: 2|1]
            sage: unary_weight = W([-1, 0, 0, 2, -1])
            sage: unary_weight
            [1, 0, 0, 1, 1]
            sage: weight = add(unary_weight)
            sage: weight
            3

        Also the joint Hamming weight can be computed::

            sage: v1 = vector([-1, 0])
            sage: v0 = vector([0, 0])
            sage: W = transducers.weight([v1, v0])
            sage: unary_weight = W([v1, v0, v1, v0])
            sage: add(unary_weight)
            2

        For the input alphabet ``[-1, 0, 1]`` the weight transducer is the
        same as the absolute value transducer
        :meth:`~TransducerGenerators.abs`::

            sage: W = transducers.weight([-1, 0, 1])
            sage: A = transducers.abs([-1, 0, 1])
            sage: W == A
            True

        For other input alphabets, we can specify the zero symbol::

            sage: W = transducers.weight(['a', 'b'], zero='a')
            sage: add(W(['a', 'b', 'b']))
            2
        """
        def weight(state, input):
            weight = int(input != zero)
            return (0, weight)
        return Transducer(weight, input_alphabet=input_alphabet,
                          initial_states=[0],
                          final_states=[0])


    def abs(self, input_alphabet):
        """
        Returns a transducer which realizes the letter-wise
        absolute value of an input word over the given input alphabet.

        INPUT:

        - ``input_alphabet``  -- a list or other iterable.

        OUTPUT:

        A transducer mapping `i_0\ldots i_k`
        to `|i_0|\ldots |i_k|`.

        EXAMPLE:

        The following transducer realizes letter-wise
        absolute value::

            sage: T = transducers.abs([-1, 0, 1])
            sage: T.transitions()
            [Transition from 0 to 0: -1|1,
             Transition from 0 to 0: 0|0,
             Transition from 0 to 0: 1|1]
            sage: T.initial_states()
            [0]
            sage: T.final_states()
            [0]
            sage: T([-1, -1, 0, 1])
            [1, 1, 0, 1]

        """
        return Transducer(lambda state, input: (0, abs(input)),
                          input_alphabet=input_alphabet,
                          initial_states=[0],
                          final_states=[0])


    def GrayCode(self):
        """
        Returns a transducer converting the standard binary
        expansion to Gray code.

        INPUT:

        Nothing.

        OUTPUT:

        A transducer.

        Cf. the :wikipedia:`Gray_code` for a description of the Gray code.

        EXAMPLE::

            sage: G = transducers.GrayCode()
            sage: G
            Transducer with 3 states
            sage: sage.combinat.finite_state_machine.FSMOldProcessOutput = False
            sage: for v in srange(0, 10):
            ....:     print v, G(v.digits(base=2))
            0 []
            1 [1]
            2 [1, 1]
            3 [0, 1]
            4 [0, 1, 1]
            5 [1, 1, 1]
            6 [1, 0, 1]
            7 [0, 0, 1]
            8 [0, 0, 1, 1]
            9 [1, 0, 1, 1]

        In the example :ref:`Gray Code <finite_state_machine_gray_code_example>`
        in the documentation of the
        :mod:`~sage.combinat.finite_state_machine` module, the Gray code
        transducer is derived from the algorithm converting the binary
        expansion to the Gray code. The result is the same as the one
        given here.
        """
        z = ZZ(0)
        o = ZZ(1)
        return Transducer([[0, 1, z, None],
                           [0, 2, o, None],
                           [1, 1, z, z],
                           [1, 2, o, o],
                           [2, 1, z, o],
                           [2, 2, o, z]],
                          initial_states=[0],
                          final_states=[1],
                          with_final_word_out=[0])

    def Recursion(self, recursions, function, var, base,
                  input_alphabet=None, output_rings=[ZZ, QQ]):
        """
        Return a transducer realizing the given recursion when reading
        the digit expansion with base ``base``.

        INPUT:

        - ``recursions`` -- list or iterable of equations. Each
          equation has the form ``f(base^K * n + r) == f(base^k * n +
          s) + t`` for some integers ``0 <= k < K``, ``r`` and some
          ``t`` or of the form ``f(r) == t`` for some integer ``r``
          and some ``t``.

        - ``function`` -- symbolic function ``f`` occuring in the
          recursions.

        - ``var`` -- symbolic variable.

        - ``base`` -- base of the digit expansion.

        - ``input_alphabet`` -- (default: ``None``) a list of digits
          to be used as the input alphabet. If ``None`` and the base
          is an integer, ``input_alphabet`` is chosen to be
          ``range(base.abs())``.

        - ``output_rings`` -- (default: ``[ZZ, QQ]``) a list of
          rings. The output labels are coerced in the first ring of
          the list in which they are contained. If they are not
          contained in any ring, they remain in whatever ring they are
          after parsing the recursions, typically the symbolic ring or
          Python ``int``.

        OUTPUT:

        A transducer ``T``.

        The transducer is constructed such that ``T(expansion) ==
        f(n)`` if ``expansion`` is the digit expansion of ``n`` to the
        base ``base`` with the given input alphabet as set of digits.

        The formal equations and initial conditions in the recursion
        have to be selected such that ``f`` is uniquely defined.

        EXAMPLES:

        -   The following example computes the binary sum of digits. ::

                sage: function('f')
                f
                sage: var('n')
                n
                sage: T = transducers.Recursion([
                ....:     f(2*n + 1) == f(n) + 1,
                ....:     f(2*n) == f(n),
                ....:     f(0) == 0],
                ....:     f, n, 2)
                sage: T.transitions()
                [Transition from (0, 0) to (0, 0): 0|0,
                 Transition from (0, 0) to (0, 0): 1|1]

            As no ``output_rings`` have been specified, the output labels
            are coerced into ``ZZ``::

                sage: for t in T.transitions():
                ....:     print t.word_out[0].parent()
                Integer Ring
                Integer Ring

            In contrast, if ``output_rings`` is set to the empty list, the
            results are not coerced::

                sage: T = transducers.Recursion([
                ....:     f(2*n + 1) == f(n) + 1,
                ....:     f(2*n) == f(n),
                ....:     f(0) == 0],
                ....:     f, n, 2, output_rings=[])
                sage: T.transitions()[0].word_out[0].parent()
                Traceback (most recent call last):
                ...
                AttributeError: 'int' object has no attribute 'parent'
                sage: T.transitions()[1].word_out[0].parent()
                Symbolic Ring

            Finally, we use a somewhat questionable coercion::

                sage: T = transducers.Recursion([
                ....:     f(2*n + 1) == f(n) + 1,
                ....:     f(2*n) == f(n),
                ....:     f(0) == 0],
                ....:     f, n, 2, output_rings=[GF(5)])
                sage: for t in T.transitions():
                ....:     print t.word_out[0], t.word_out[0].parent()
                0 Finite Field of size 5
                1 Finite Field of size 5

        -   The following example computes the Hamming weight of the
            non-adjacent form, cf. the :wikipedia:`Non-adjacent_form`. ::

                sage: function('f')
                f
                sage: var('n')
                n
                sage: T = transducers.Recursion([
                ....:     f(4*n + 1) == f(n) + 1,
                ....:     f(4*n + 3) == f(n + 1) + 1,
                ....:     f(2*n) == f(n),
                ....:     f(0) == 0],
                ....:     f, n, 2)
                sage: T.transitions()
                [Transition from (0, 0) to (0, 0): 0|0,
                 Transition from (0, 0) to (1, 1): 1|-,
                 Transition from (1, 1) to (0, 0): 0|1,
                 Transition from (1, 1) to (1, 0): 1|1,
                 Transition from (1, 0) to (1, 1): 0|-,
                 Transition from (1, 0) to (1, 0): 1|0]
                sage: [(s.label(), s.final_word_out)
                ....:  for s in T.iter_final_states()]
                [((0, 0), [0]),
                 ((1, 1), [1, 0]),
                 ((1, 0), [1, 0])]

        .. TODO::

            Extend the method to

            - non-integral bases,

            - non-positive residues, e.g. allow ``f(4*n - 1) == f(n) - 1``,

            - higher dimensions,

            - output words of length `> 1`---currently, some
              work-around with a symbolic function would somehow work.

        TESTS:

            The following tests check that the equations are well-formed::

                sage: transducers.Recursion([f(4*n + 1)], f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: f(4*n + 1) is not an equation with ==.

            ::

                sage: transducers.Recursion([f(n) + 1 == f(2*n)],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: f(n) + 1 is not an evaluation of f.

            ::

                sage: transducers.Recursion([f(2*n, 5) == 3],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: f(2*n, 5) does not have one argument.

            ::

                sage: transducers.Recursion([f(1/n) == f(n) + 3],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ....:
                ValueError: Could not convert 1/n to a polynomial in n.

            ::

                sage: transducers.Recursion([f(n^2 + 5) == 3],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: n^2 + 5 is not a polynomial of degree 1.

            ::

                sage: transducers.Recursion([f(3*n + 5) == f(n) + 7],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: 3 is not a power of 2.

            ::

                sage: transducers.Recursion([f(n + 5) == f(n) + 7],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: 1 is less than 2.

            ::

                sage: transducers.Recursion([f(2*n + 5) == f(n) + 7],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: 0 <= 5 < 2 does not hold.

            ::

                sage: transducers.Recursion(
                ....:     [f(2*n + 1) == f(n + 1) + f(n) + 2],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: f(n + 1) + f(n) + 2 does not contain
                exactly one summand which is an evaluation of f.

            ::

                sage: transducers.Recursion([f(2*n + 1) == sin(n) + 2],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: sin(n) + 2 does not contain exactly one
                summand which is an evaluation of f.

            ::

                sage: transducers.Recursion([f(2*n + 1) == f(n) + n + 2],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: n + 2 contains n.

            ::

                sage: transducers.Recursion([f(2*n + 1) == sin(n)],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: sin(n) is not an evaluation of f.

            ::

                sage: transducers.Recursion([f(2*n + 1) == f(n, 2)],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: f(n, 2) does not have exactly one argument.

            ::

                sage: transducers.Recursion([f(2*n + 1) == f(1/n)],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: 1/n is not a polynomial in n.

            ::

                sage: transducers.Recursion([f(2*n + 1) == f(n^2 + 5)],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: n^2 + 5 is not a polynomial of degree 1.

            ::

                sage: transducers.Recursion([f(2*n + 1) == f(n^2 + 5)],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: n^2 + 5 is not a polynomial of degree 1.

            ::

                sage: transducers.Recursion([f(2*n + 1) == f(3*n + 5)],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: 3 is not a power of 2.

            ::

                sage: transducers.Recursion([f(2*n + 1) == f((1/2)*n + 5)],
                ....:     f, n, QQ(2))
                Traceback (most recent call last):
                ...
                ValueError: 1/2 is less than 1.

            ::

                sage: transducers.Recursion([f(2*n + 1) == f(2*n + 5)],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: 2 is greater or equal than 2.

            The following tests fail due to missing or superfluous recursions
            or initial conditions. ::

                sage: transducers.Recursion([f(2*n) == f(n)],
                ....:     f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: Missing recursions for input congruent to
                [1] modulo 2.

            ::

                sage: transducers.Recursion([f(2*n + 1) == f(n),
                ....:                        f(4*n) == f(2*n) + 1,
                ....:                        f(2*n) == f(n) +1],
                ....:                       f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: Conflicting rules congruent to 0 modulo 4.

            ::

                sage: transducers.Recursion([f(2*n + 1) == f(n) + 1,
                ....:                        f(2*n) == f(n),
                ....:                        f(0) == 0,
                ....:                        f(42) == 42], f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: Superfluous initial condition for 42.

            The following is an indication of a missing initial
            condition::

                sage: transducers.Recursion([f(2*n + 1) == f(n) + 1,
                ....:                        f(2*n) == f(n - 2) + 4,
                ....:                        f(0) == 0], f, n, 2)
                Traceback (most recent call last):
                ...
                ValueError: The finite state machine contains a cycle
                starting at state (-2, 0) with input label 0 and no
                final state.
        """
        from sage.functions.log import log

        Rule = collections.namedtuple('Rule', ['K', 'r', 'k', 's', 't'])
        RuleRight = collections.namedtuple('Rule', ['k', 's', 't'])
        initial_values = {}
        rules = []
        base_ring = base.parent()
        if input_alphabet is None and base in ZZ:
            input_alphabet = list(range(base.abs()))

        def is_scalar(expression):
            return var not in expression.variables()

        def coerce_output(output):
            for ring in output_rings:
                if output in ring:
                    return ring(output)
            return(output)

        def parse_equation(equation):
            if equation.operator() != operator.eq:
                raise ValueError("%s is not an equation with ==."
                                 % equation)
            assert len(equation.operands()) == 2, \
                "%s is not an equation with two operands." % equation
            (left_side, right_side) = equation.operands()

            if left_side.operator() != function:
                raise ValueError("%s is not an evaluation of %s."
                                 % (left_side, function))
            if len(left_side.operands()) !=1:
                raise ValueError("%s does not have one argument." %
                                 (left_side, ))

            try:
                polynomial_left=base_ring[var](left_side.operands()[0])
            except:
                raise ValueError("Could not convert %s to a polynomial "
                                 "in %s." % (left_side.operands()[0],
                                            var))
            if polynomial_left in base_ring and is_scalar(right_side):
                initial_values[polynomial_left] = right_side
                return

            if polynomial_left.degree() != 1:
                raise ValueError("%s is not a polynomial of degree 1."
                                 % (polynomial_left,))

            [r, base_power_K] = list(polynomial_left)
            K = log(base_power_K, base=base)
            try:
                K = K.simplify()
            except AttributeError:
                pass
            if K not in ZZ:
                raise ValueError("%s is not a power of %s."
                                 % (base_power_K, base))
            if K < 1:
                raise ValueError("%d is less than %d."
                                 % (base_power_K, base))
            if not 0 <= r < base_power_K:
                raise ValueError("0 <= %d < %d does not hold."
                                 % (r, base_power_K))

            if right_side.operator() == operator.add:
                function_calls = [o for o in right_side.operands()
                                  if o.operator() == function]
                other_terms = [o for o in right_side.operands()
                               if o.operator() != function]
                if len(function_calls) != 1:
                    raise ValueError(
                        "%s does not contain exactly one summand which "
                        "is an evaluation of %s."
                        % (right_side, function))
                next_function = function_calls[0]
                t = sum(other_terms)
                if not is_scalar(t):
                    raise ValueError("%s contains %s."
                                     % (t, var))
            else:
                next_function = right_side
                t = 0

            if next_function.operator() != function:
                raise ValueError("%s is not an evaluation of %s."
                                 % (next_function, function))
            if len(next_function.operands()) !=1:
                raise ValueError("%s does not have exactly one argument."
                                 % (next_function, ))

            try:
                polynomial_right = base_ring[var](next_function.operands()[0])
            except:
                raise ValueError("%s is not a polynomial in %s."
                                 % (next_function.operands()[0], var))
            if polynomial_right.degree() != 1:
                raise ValueError("%s is not a polynomial of degree 1."
                                 % (polynomial_right,))
            [s, base_power_k] = list(polynomial_right)
            k = log(base_power_k, base=base)
            try:
                k = k.simplify()
            except AttributeError:
                pass
            if k not in ZZ:
                raise ValueError("%s is not a power of %s."
                                 % (base_power_k, base))
            if k < 0:
                raise ValueError("%s is less than 1."
                                 % (base_power_k, ))
            if k >= K:
                raise ValueError("%d is greater or equal than %d."
                                 % (base_power_k, base_power_K))

            parsed_equation = function(base**K * var + r) == \
                function(base**k * var + s) + t
            assert equation == parsed_equation, \
                "Parsing of %s failed for unknown reasons." % (equation,)

            rule = Rule(K=K,r=r, k=k, s=s, t=coerce_output(t))
            rules.append(rule)


        for equation in recursions:
            parse_equation(equation)

        max_K = max(rule.K for rule in rules)

        residues = [[None for r in range(base**k)]
                    for k in range(max_K + 1)]
        for rule in rules:
            for m in range(max_K - rule.K + 1):
                for ell in range(base**m):
                    R = rule.r + 2**rule.K * ell
                    if residues[rule.K + m][R] is not None:
                        raise ValueError(
                            "Conflicting rules congruent to %d modulo %d."
                            % (R, base**(rule.K + m)))
                    residues[rule.K + m][R] = RuleRight(k=rule.k + m,
                                                        s=rule.s * base**m,
                                                        t=rule.t)

        missing_residues = [R
                            for R, rule in enumerate(residues[max_K])
                            if rule is None]
        if missing_residues:
            raise ValueError("Missing recursions for input congruent "
                             "to %s modulo %s." % (missing_residues,
                                                   base**max_K))

        def transition_function((carry, look_ahead), input):
            current = carry + input * base**look_ahead
            K = look_ahead + 1
            R = current % 2**K
            rule = residues[K][R]
            if rule is not None:
                n = (current - R) / base**K
                new_carry = n * base**rule.k + rule.s
                return ((new_carry, rule.k), rule.t)
            return ((current, K), [])

        T = Transducer(transition_function,
                       initial_states=[(0, 0)],
                       input_alphabet=input_alphabet)

        for key, value in initial_values.iteritems():
            found = False
            for state in T.iter_states():
                if state.label()[0] == key:
                    state.is_final = True
                    state.final_word_out = value
                    found = True
            if not found:
                raise ValueError("Superfluous initial condition for %s."
                                 % key)

        T.construct_final_word_out(0)

        missing_initial_conditions = [
            state.label()
            for state in T.iter_states()
            if not state.is_final]
        if missing_initial_conditions:
            # this does not currently deal with cycles which
            # will be more frequent.
            raise ValueError("Missing initial conditions for %s."
                             % (missing_initial_conditions,))

        return T


# Easy access to the transducer generators from the command line:
transducers = TransducerGenerators()
