#*****************************************************************************
#       Copyright (C) 2007 Mike Hansen <mhansen@gmail.com>,
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from combinat import CombinatorialClass
import sage.graphs.graph as graph


def GraphPaths(g, source=None, target=None):
    """
    Returns the combinatorial class of paths in the
    directed graph g.

    EXAMPLES:
        sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)

      If source and target are not given, then the returned class contains all
      paths (including trivial paths containing only one vertex).

        sage: p = GraphPaths(G); p
        Paths in Multi-digraph on 5 vertices
        sage: p.count()
        37
        sage: p.random() #random
        [3, 4, 5]


      If the source is specified, then the returned class contains all of the paths
      starting at the vertex source (including the trivial path).

         sage: p = GraphPaths(G, source=3); p
         Paths in Multi-digraph on 5 vertices starting at 3
         sage: p.list()
         [[3], [3, 4], [3, 4, 5], [3, 4, 5]]


      If the target is specified, then the returned class contains all of the paths
      ending at the vertex target (including the trivial path).

        sage: p = GraphPaths(G, target=3); p
        Paths in Multi-digraph on 5 vertices ending at 3
        sage: p.count()
        5
        sage: p.list()
        [[3], [1, 3], [2, 3], [1, 2, 3], [1, 2, 3]]


      If both the target and source are specified, then the returned class
      contains all of the paths from source to target.

        sage: p = GraphPaths(G, source=1, target=3); p
        Paths in Multi-digraph on 5 vertices starting at 1 and ending at 3
        sage: p.count()
        3
        sage: p.list()
        [[1, 2, 3], [1, 2, 3], [1, 3]]

    """
    if not isinstance(g, graph.DiGraph):
        raise TypeError, "g must be a DiGraph"
    if source is None and target is None:
        return GraphPaths_all(g)
    elif source is not None and target is None:
        if source not in g:
            raise ValueError, "source must be in g"
        return GraphPaths_s(g, source)
    elif source is None and target is not None:
        if target not in g:
            raise ValueError, "target must be in g"
        return GraphPaths_t(g, target)
    else:
        if source not in g:
            raise ValueError, "source must be in g"
        if target not in g:
            raise ValueError, "target must be in g"
        return GraphPaths_st(g, source, target)

class GraphPaths_common:
    def outgoing_edges(self, v):
        """
        Returns a list of v's outgoing edges.

        EXAMPLES:
            sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
            sage: p = GraphPaths(G)
            sage: p.outgoing_edges(2)
            [(2, 3, None), (2, 4, None)]
        """
        return [i for i in self.graph.outgoing_edge_iterator(v)]

    def incoming_edges(self, v):
        """
        Returns a list of v's incoming edges.

        EXAMPLES:
            sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
            sage: p = GraphPaths(G)
            sage: p.incoming_edges(2)
            [(1, 2, None), (1, 2, None)]
        """
        return [i for i in self.graph.incoming_edge_iterator(v)]

    def outgoing_paths(self, v):
        """
        Returns a list of the paths that start at v.
        """
        source = v
        source_paths = [ [v] ]
        for e in self.outgoing_edges(v):
            target = e[1]
            target_paths = self.outgoing_paths(target)
            target_paths = [ [v]+path  for path in target_paths]

            source_paths += target_paths

        return source_paths


    def incoming_paths(self, v):
        """
        Returns a list of paths that end at v.
        """
        target = v
        target_paths = [ [v] ]
        for e in self.incoming_edges(v):
            source = e[0]
            source_paths = self.incoming_paths(source)
            source_paths = [ path + [v] for path in source_paths ]
            target_paths += source_paths
        return target_paths

    def paths_from_source_to_target(self, source, target):
        """
        Returns a list of paths from source to target.
        """
        source_paths = self.outgoing_paths(source)
        paths = []
        for path in source_paths:
            if path[-1] == target:
                paths.append(path)
        return paths

    def paths(self):
        paths = []
        for source in self.graph.vertices():
            paths += self.outgoing_paths(source)
        return paths

class GraphPaths_all(CombinatorialClass, GraphPaths_common):
    """
    EXAMPLES:
        sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
        sage: p = GraphPaths(G)
        sage: p.count()
        37
    """
    def __init__(self, g):
        """
        TESTS:
            sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
            sage: p = GraphPaths(G)
            sage: p == loads(dumps(p))
            True
        """
        self.graph = g

    def __repr__(self):
        """
        TESTS:
            sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
            sage: p = GraphPaths(G)
            sage: repr(p)
            'Paths in Multi-digraph on 5 vertices'
        """
        return "Paths in %s"%repr(self.graph)

    def list(self):
        return self.paths()

class GraphPaths_t(CombinatorialClass, GraphPaths_common):
    def __init__(self, g, target):
        """
        TESTS:
            sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
            sage: p = GraphPaths(G, target=4)
            sage: p == loads(dumps(p))
            True
        """
        self.graph = g
        self.target = target

    def __repr__(self):
        """
        TESTS:
            sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
            sage: p = GraphPaths(G, target=4)
            sage: repr(p)
            'Paths in Multi-digraph on 5 vertices ending at 4'
        """
        return "Paths in %s ending at %s"%(repr(self.graph), self.target)

    def list(self):
        """
        EXAMPLES:
            sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
            sage: p = GraphPaths(G, target=4)
            sage: p.list()
            [[4],
             [2, 4],
             [1, 2, 4],
             [1, 2, 4],
             [3, 4],
             [1, 3, 4],
             [2, 3, 4],
             [1, 2, 3, 4],
             [1, 2, 3, 4]]
        """
        return self.incoming_paths(self.target)

class GraphPaths_s(CombinatorialClass, GraphPaths_common):
    def __init__(self, g, source):
        """
        TESTS:
            sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
            sage: p = GraphPaths(G, 4)
            sage: p == loads(dumps(p))
            True
        """
        self.graph = g
        self.source = source

    def __repr__(self):
        """
        TESTS:
            sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
            sage: p = GraphPaths(G, 4)
            sage: repr(p)
            'Paths in Multi-digraph on 5 vertices starting at 4'
        """
        return "Paths in %s starting at %s"%(repr(self.graph), self.source)

    def list(self):
        """
        EXAMPLES:
            sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
            sage: p = GraphPaths(G, 4)
            sage: p.list()
            [[4], [4, 5], [4, 5]]
        """
        return self.outgoing_paths(self.source)

class GraphPaths_st(CombinatorialClass, GraphPaths_common):
    """
    EXAMPLES:
        sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
        sage: GraphPaths(G,1,2).count()
        2
        sage: GraphPaths(G,1,3).count()
        3
        sage: GraphPaths(G,1,4).count()
        5
        sage: GraphPaths(G,1,5).count()
        10
        sage: GraphPaths(G,2,3).count()
        1
        sage: GraphPaths(G,2,4).count()
        2
        sage: GraphPaths(G,2,5).count()
        4
        sage: GraphPaths(G,3,4).count()
        1
        sage: GraphPaths(G,3,5).count()
        2
        sage: GraphPaths(G,4,5).count()
        2
    """
    def __init__(self, g, source, target):
        """
        TESTS:
            sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
            sage: p = GraphPaths(G,1,2)
            sage: p == loads(dumps(p))
            True
        """
        self.graph = g
        self.source = source
        self.target = target

    def __repr__(self):
        """
        TESTS:
            sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
            sage: p = GraphPaths(G,1,2)
            sage: repr(p)
            'Paths in Multi-digraph on 5 vertices starting at 1 and ending at 2'
        """
        return "Paths in %s starting at %s and ending at %s"%(repr(self.graph), self.source, self.target)

    def list(self):
        """
        EXAMPLES:
            sage: G = DiGraph({1:[2,2,3], 2:[3,4], 3:[4], 4:[5,5]}, multiedges=True)
            sage: p = GraphPaths(G,1,2)
            sage: p.list()
            [[1, 2], [1, 2]]
        """
        return self.paths_from_source_to_target(self.source, self.target)
