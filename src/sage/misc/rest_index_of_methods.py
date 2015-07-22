r"""
ReST index of functions

This module implemens a function that generates a ReST index of functions from a
list of a class.

{INDEX_OF_FUNCTIONS}

"""

def gen_rest_table_index(list_of_entries,sort=True):
    r"""
    Return a ReST table describing a list of functions.

    INPUT:

    - ``list_of_entries`` -- a list of functions, or a class. In the latter
       case, all its methods are listed.

    - ``sort`` (boolean; ``True``) -- whether to sort the list of methods
      lexicographically.

    EXAMPLE::

        sage: from sage.misc.rest_index_of_methods import gen_rest_table_index
        sage: gen_rest_table_index([graphs.PetersenGraph])
        .. csv-table::
           :class: contentstable
           :widths: 30, 70
           :delim: |
        ...
           :func:`~sage.graphs.generators.smallgraphs.PetersenGraph` | The Petersen Graph is a named graph that consists of 10 vertices
        ...
    """
    import inspect

    # If input is a class/module, we list all its non-private and methods/functions
    if (inspect.isclass(list_of_entries) or
        inspect.ismodule(list_of_entries)):
        root = list_of_entries
        list_of_entries = [getattr(root,name) for name,f in root.__dict__.items() if
                           (not name.startswith('_')     and # private functions
                            not hasattr(f,'trac_number') and # deprecated functions
                            not inspect.isclass(f)       and # classes
                            inspect.getmodule(root) == inspect.getmodule(f))] # not imported from elsewhere

    assert isinstance(list_of_entries,list)

    s = (".. csv-table::\n"
         "   :class: contentstable\n"
         "   :widths: 30, 70\n"
         "   :delim: |\n\n")

    if sort:
        list_of_entries.sort(key=lambda x:getattr(x,'__name__',''))

    for e in list_of_entries:

        if inspect.ismethod(e):
            link = ":meth:`~"+str(e.im_class.__module__)+"."+str(e.im_class.__name__)+"."+e.__name__+"`"
        elif inspect.isfunction(e):
            link = ":func:`~"+str(e.__module__)+"."+str(e.__name__)+"`"
        else:
            continue

        # Descriptions of the method/function
        desc = e.__doc__.splitlines()
        desc = desc[0] if desc[0] else desc[1]

        s += "   {} | {}\n".format(link,desc.lstrip())

    return s+'\n'

__doc__ = __doc__.format(INDEX_OF_FUNCTIONS=gen_rest_table_index([gen_rest_table_index]))
