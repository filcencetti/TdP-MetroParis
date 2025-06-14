from database.DAO import DAO
import networkx as nx
import geopy.distance

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._graph = nx.DiGraph()
        self._idMap = {}
        for node in self._fermate:
            self._idMap[node.id_fermata] = node

    def buildWeightedGraph(self):
        self._graph.clear()
        self._graph.add_nodes_from(self._fermate)
        for edge in DAO.getWeightedEdges():
            self._graph.add_edge(self._idMap[edge[0]], self._idMap[edge[1]], weight=edge[2])

    def buildOrientedGraph(self):
        self._graph.clear()
        self._graph.add_nodes_from(self._fermate)
        for edge in DAO.getOrientedEdges():
            weight = self.getDistance(self._idMap[edge[0]],self._idMap[edge[1]],edge[2])
            if self._graph.has_edge(self._idMap[edge[0]], self._idMap[edge[1]]):
                if self._graph[self._idMap[edge[0]]][self._idMap[edge[1]]]["weight"] < weight:
                    self._graph[self._idMap[edge[0]]][self._idMap[edge[1]]]["weight"] = weight
            else:
                self._graph.add_edge(self._idMap[edge[0]], self._idMap[edge[1]], weight=weight)

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

    def getDistance(self, u, v, vel):
        dist = geopy.distance.distance((u.coordX, u.coordY),
                                       (v.coordX, v.coordY)).km  # in km
        time = dist / vel * 60  # in minuti
        return time

    def getPath(self, stazP, stazA):
        return nx.dijkstra_path(self._graph, stazP, stazA)


    @property
    def fermate(self):
        return self._fermate