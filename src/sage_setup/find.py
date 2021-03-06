"""
Recursive Directory Contents
"""
#*****************************************************************************
#       Copyright (C) 2014 Volker Braun <vbraun.name@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************


import importlib.machinery
import importlib.util

import os

from collections import defaultdict

def read_distribution(src_file):
    """
    Parse ``src_file`` for a ``# sage_setup: distribution = PKG`` directive.

    INPUT:

    - ``src_file`` -- file name of a Python or Cython source file

    OUTPUT:

    - a string, the name of the distribution package (``PKG``); or the empty
      string if no directive was found.

    EXAMPLES::

        sage: from sage.env import SAGE_SRC
        sage: from sage_setup.find import read_distribution
        sage: read_distribution(os.path.join(SAGE_SRC, 'sage', 'graphs', 'graph_decompositions', 'tdlib.pyx'))
        'sage-tdlib'
        sage: read_distribution(os.path.join(SAGE_SRC, 'sage', 'graphs', 'graph_decompositions', 'modular_decomposition.py'))
        ''
    """
    from Cython.Utils import open_source_file
    with open_source_file(src_file, error_handling='ignore') as fh:
        for line in fh:
            # Adapted from Cython's Build/Dependencies.py
            line = line.lstrip()
            if not line:
                continue
            if line[0] != '#':
                break
            line = line[1:].lstrip()
            kind = "sage_setup:"
            if line.startswith(kind):
                key, _, value = [s.strip() for s in line[len(kind):].partition('=')]
                if key == "distribution":
                    return value
    return ''

def find_python_sources(src_dir, modules=['sage'], distributions=None):
    """
    Find all Python packages and Python/Cython modules in the sources.

    INPUT:

    - ``src_dir`` -- root directory for the sources

    - ``modules`` -- (default: ``['sage']``) sequence of strings:
      the top-level directories in ``src_dir`` to be considered

    - ``distributions`` -- (default: ``None``) if not ``None``,
      should be a sequence or set of strings: only find modules whose
      ``distribution`` (from a ``# sage_setup: distribution = PACKAGE``
      directive in the module source file) is an element of
      ``distributions``.

    OUTPUT: Triple consisting of

    - the list of package names (corresponding to directories with
      ``__init__.py``),

    - Python module names (corresponding to other ``*.py`` files).

    - Cython extensions (corresponding to ``*.pyx`` files).

    Both use dot as separator.

    EXAMPLES::

        sage: from sage.env import SAGE_SRC
        sage: from sage_setup.find import find_python_sources
        sage: py_packages, py_modules, cy_modules = find_python_sources(SAGE_SRC)

    Ordinary package (with ``__init__.py``)::

        sage: ['sage.structure' in L for L in (py_packages, py_modules)]
        [True, False]

    Python module in an ordinary package::

        sage: ['sage.structure.formal_sum' in L for L in (py_packages, py_modules)]
        [False, True]

    Cython module in an ordinary package::

        sage: ['sage.structure.sage_object' in L for L in (py_packages, py_modules)]
        [False, False]

    Subdirectory without any Python files::

        sage: ['sage.doctest.tests' in L for L in (py_packages, py_modules)]
        [False, False]

    Filtering by distribution (distutils package)::

        sage: find_python_sources(SAGE_SRC, distributions=['sage-tdlib'])
        ([], [], [<distutils.extension.Extension('sage.graphs.graph_decompositions.tdlib')...>])

    Benchmarking::

        sage: timeit('find_python_sources(SAGE_SRC)',         # random output
        ....:        number=1, repeat=1)
        1 loops, best of 1: 30 ms per loop

        sage: timeit('find_python_sources(SAGE_SRC, distributions=[""])', # random output
        ....:        number=1, repeat=1)
        1 loops, best of 1: 850 ms per loop

        sage: find_python_sources(SAGE_SRC, modules=['sage_setup'])
        (['sage_setup', ...], [...'sage_setup.find'...], [])
    """
    from distutils.extension import Extension

    PYMOD_EXT = get_extensions('source')[0]
    INIT_FILE = '__init__' + PYMOD_EXT

    python_packages = []
    python_modules = []
    cython_modules = []

    cwd = os.getcwd()
    try:
        os.chdir(src_dir)
        for module in modules:
            for dirpath, dirnames, filenames in os.walk(module):
                package = dirpath.replace(os.path.sep, '.')
                if INIT_FILE in filenames:
                    # Ordinary package.
                    if distributions is None or '' in distributions:
                        python_packages.append(package)
                else:
                    continue

                def is_in_distributions(filename):
                    if distributions is None:
                        return True
                    distribution = read_distribution(os.path.join(dirpath, filename))
                    return distribution in distributions

                for filename in filenames:
                    base, ext = os.path.splitext(filename)
                    if ext == PYMOD_EXT and base != '__init__':
                        if is_in_distributions(filename):
                            python_modules.append(package + '.' + base)
                    if ext == '.pyx':
                        if is_in_distributions(filename):
                            cython_modules.append(Extension(package + '.' + base,
                                                            sources=[os.path.join(dirpath, filename)]))

    finally:
        os.chdir(cwd)
    return python_packages, python_modules, cython_modules

def find_extra_files(src_dir, modules, cythonized_dir, special_filenames=[]):
    """
    Find all extra files which should be installed.

    These are (for each ``module`` in ``modules``):

    1. From ``src_dir/module``: all .pyx, .pxd and .pxi files and files
       listed in ``special_filenames``.
    2. From ``cythonized_dir/module``: all .h files (both the .h files
       from the sources, as well as all Cython-generated .h files).

    The directories are searched recursively, but only package
    directories (containing ``__init__.py`` or a Cython equivalent)
    are considered.

    INPUT:

    - ``src_dir`` -- root directory for the sources

    - ``modules`` -- sequence of strings:
      the top-level directories in ``src_dir`` to be considered

    - ``cythonized_dir`` -- the directory where the Cython-generated
      files are

    - ``special_filenames`` -- a list of filenames to be installed from
      ``src_dir``

    OUTPUT: dict with items ``{dir: files}`` where ``dir`` is a
    directory relative to ``src_dir`` and ``files`` is a list of
    filenames inside that directory.

    EXAMPLES::

        sage: from sage_setup.find import find_extra_files
        sage: from sage.env import SAGE_SRC
        sage: cythonized_dir = os.path.join(SAGE_SRC, "build", "cythonized")
        sage: extras = find_extra_files(SAGE_SRC, ["sage"], cythonized_dir)
        sage: extras["sage/libs/mpfr"]
        [...sage/libs/mpfr/types.pxd...]
        sage: extras["sage/ext/interpreters"]
        ['.../src/sage/ext/interpreters/wrapper_cdf.pxd', ...wrapper_cdf.h...]
    """
    from Cython.Utils import is_package_dir

    data_files = {}
    cy_exts = ('.pxd', '.pxi', '.pyx')

    cwd = os.getcwd()
    try:
        os.chdir(src_dir)
        for module in modules:
            for dir, dirnames, filenames in os.walk(module):
                if not is_package_dir(dir):
                    continue
                sdir = os.path.join(src_dir, dir)
                cydir = os.path.join(cythonized_dir, dir)

                files = [os.path.join(sdir, f) for f in filenames
                        if f.endswith(cy_exts) or f in special_filenames]
                if os.path.isdir(cydir):  # Not every directory contains Cython files
                    files += [os.path.join(cydir, f) for f in os.listdir(cydir)
                            if f.endswith(".h")]

                if files:
                    data_files[dir] = files
    finally:
        os.chdir(cwd)

    return data_files


def installed_files_by_module(site_packages, modules=('sage',)):
    """
    Find all currently installed files

    INPUT:

    - ``site_packages`` -- string. The root Python path where the Sage
      library is being installed. If the path doesn't exist, returns
      an empty dictionary.

    - ``modules`` -- list/tuple/iterable of strings (default:
      ``('sage',)``). The top-level directory name(s) in
      ``site_packages``.

    OUTPUT:

    A dictionary whose keys are module names (``'sage.module.foo'``)
    and values are list of corresponding file names
    ``['sage/module/foo.py', 'sage/module/foo.pyc']`` relative to
    ``site_packages``.

    EXAMPLES::

        sage: from site import getsitepackages
        sage: site_packages = getsitepackages()[0]
        sage: from sage_setup.find import installed_files_by_module
        sage: files_by_module = installed_files_by_module(site_packages)
        sage: from sage.misc.sageinspect import loadable_module_extension
        sage: (f,) = files_by_module['sage.structure.sage_object']; f
        'sage/structure/sage_object...'
        sage: (f1, f2) = sorted(files_by_module['sage.structure'])
        sage: f1
        'sage/structure/__init__.py'
        sage: f2
        'sage/structure/....pyc'

    This takes about 30ms with warm cache:

        sage: timeit('installed_files_by_module(site_packages)',       # random output
        ....:        number=1, repeat=1)
        1 loops, best of 1: 29.6 ms per loop
    """

    module_files = defaultdict(set)
    module_exts = get_extensions()

    def add(module, filename, dirpath):
        # Find the longest extension that matches the filename
        best_ext = ''

        for ext in module_exts:
            if filename.endswith(ext) and len(ext) > len(best_ext):
                best_ext = ext

        if not best_ext:
            return

        base = filename[:-len(best_ext)]
        filename = os.path.join(dirpath, filename)

        if base != '__init__':
            module += '.' + base

        module_files[module].add(filename)

        cache_filename = importlib.util.cache_from_source(filename)
        if os.path.exists(cache_filename):
            module_files[module].add(cache_filename)

    cwd = os.getcwd()
    try:
        os.chdir(site_packages)
    except OSError:
        return module_files
    try:
        for module in modules:
            for dirpath, dirnames, filenames in os.walk(module):
                module_dir = '.'.join(dirpath.split(os.path.sep))

                if os.path.basename(dirpath) == '__pycache__':
                    continue

                for filename in filenames:
                    add(module_dir, filename, dirpath)
    finally:
        os.chdir(cwd)
    return module_files


def get_extensions(type=None):
    """
    Returns the filename extensions for different types of Python module files.

    By default returns all extensions, but can be filtered by type.  The
    possible types are 'source' (for pure Python sources), 'bytecode' (for
    compiled bytecode files (i.e. pyc files), or 'extension' for C extension
    modules.

    INPUT:

    - ``type`` -- the module type ('source', 'bytecode', or 'extension') or
      None

    EXAMPLES::

        sage: from sage_setup.find import get_extensions
        sage: get_extensions()  # random - depends on Python version
        ['.so', 'module.so', '.py', '.pyc']
        sage: get_extensions('source')
        ['.py']
        sage: get_extensions('bytecode')
        ['.pyc']
        sage: get_extensions('extension')  # random - depends on Python version
        ['.so', 'module.so']
    """

    if type:
        type = type.lower()
        if type not in ('source', 'bytecode', 'extension'):
            raise ValueError(
                "type must by one of 'source' (for Python sources), "
                "'bytecode' (for compiled Python bytecoe), or 'extension' "
                "(for C extension modules).")

    # Note: There is at least one case, for extension modules, where the
    # 'extension' does not begin with '.', but rather with 'module', for cases
    # in Python's stdlib, for example, where an extension module can be named
    # like "<modname>module.so".  This breaks things for us if we have a Cython
    # module literally named "module".
    return [ext for ext in _get_extensions(type) if ext[0] == '.']


def _get_extensions(type):
    """
    Python 3.3+ implementation of ``get_extensions()`` using the
    `importlib.extensions` module.
    """

    if type:
        return {'source': importlib.machinery.SOURCE_SUFFIXES,
                'bytecode': importlib.machinery.BYTECODE_SUFFIXES,
                'extension': importlib.machinery.EXTENSION_SUFFIXES}[type]

    return importlib.machinery.all_suffixes()
