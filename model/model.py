from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._graph = nx.Graph()
        self._idMap = {}
        for node in self._fermate:
            self._idMap[node.id_fermata] = node

    def buildGraph(self):
        self._graph.clear()
        self._graph.add_nodes_from(self._fermate)

        # self.getAllEdges1()
        # print(self._graph.number_of_edges())
        # self._graph.remove_edges_from(self._graph.edges())
        # self.getAllEdges2()
        # print(self._graph.number_of_edges())
        # self._graph.remove_edges_from(self._graph.edges())
        self.getAllEdges3()
        print(self._graph.number_of_edges())

    def getAllEdges1(self):
        for node1 in self._graph.nodes():
            for node2 in self._graph.nodes():
                if DAO.hasConnessione(node1, node2):
                    self._graph.add_edge(node1, node2)
        return

    def getAllEdges2(self):
        for node in self._graph.nodes():
            neighbors = DAO.getNeighbors(node)
            for neighbor in neighbors:
                self._graph.add_edge(node, self._idMap[neighbor])
        return

    def getAllEdges3(self):
        allEdges = DAO.getAllEdges()
        for edge in allEdges:
            self._graph.add_edge(self._idMap[edge.id_stazP],self._idMap[edge.id_stazA])
        return

    def bfsSearch(self,source):
        tree = nx.bfs_tree(self._graph,source)
        return list(tree.nodes())

    def dfsSearch(self,source):
        tree = nx.dfs_tree(self._graph,source)
        return list(tree.nodes())


    @property
    def fermate(self):
        return self._fermate