from datetime import datetime
import geopy.distance

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMapFermate = {} #dizionario per associare le fermate al proprio id
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def getShortestPath(self, u, v): # cerco dijkstra dalla libreria e scelgo l'implementazione più utile (single_source_dijkstra)
        return nx.single_source_dijkstra(self._grafo, u, v)

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPEsatiTempi() # oppure addEdgesPesati o addEdgesPesatiV2

    def addEdgesPEsatiTempi(self):
        """AQggiunge archi con peso = tempo di percorrenza dell'arco"""
        self._grafo.clear_edges()
        allEdges = DAO.getAllEdgesVel()
        for e in allEdges:
            u = self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso = getTraversalTime(u,v,e[2])
            self._grafo.add_edge(u,v,weight=peso) # nella query seleziono la velocità massima quindi il peso è il minimo

    def addEdgesPesati(self): # alternativa = modificare la query
        self._grafo.clear_edges()
        allEdges = DAO.getAllEdges()
        for edge in allEdges:
            u = self._idMapFermate[edge.id_stazP]
            v = self._idMapFermate[edge.id_stazA]

            if self._grafo.has_edge(u, v):
                self._grafo[u][v]['weight'] += 1

            else:
                self._grafo.add_edge(u,v,weight=1)

    def addEdgesPesatiV2(self):
        self._grafo.clear_edges()
        allEdgesPesati = DAO.getallEdgesPesati()

        for e in allEdgesPesati:
            self._grafo.add_edge(
            self._idMapFermate[e[0]],
            self._idMapFermate[e[1]],
            weight= e[2])

    def getArchiPesoMaggiore(self):
        edges = self._grafo.edges(data=True) # data = True dato che mi servono pure i pesi
        res = []
        for e in edges:
            if self._grafo.get_edge_data(e[0],e[1])["weight"] > 1:
                res.append(e)

        print(res)
        return res

    # 4 alternative che ritornano gli stessi nodi
    def getBFSNodesFromTree(self,source):
        tree = nx.bfs_tree(self._grafo,source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi[1:]

    def getDFSNodesFromTree(self,source):
        tree = nx.dfs_tree(self._grafo,source)
        nodi = list(tree.nodes())
        return nodi[1:]

    def getBFSNodesFromEdges(self,source):
        archi = nx.bfs_edges(self._grafo,source)
        res = list()
        for u,v in archi:
            res.append(v)
        return res

    def getDFSNodesFromEdges(self,source):
        archi = nx.dfs_edges(self._grafo,source)
        res = list()
        for u,v in archi:
            res.append(v)
        return res


    def buildGraph(self):
        #Aggiungiamo i nodi
        self._grafo.add_nodes_from(self._fermate)

        # tic = datetime.now()
        # self.addEdges1()
        # toc =datetime.now()
        # print(toc-tic)
        #
        # tic = datetime.now()
        # self.addEdges2()
        # toc = datetime.now()
        # print(toc - tic)

        tic = datetime.now()
        self.addEdges3()
        toc = datetime.now()
        # print(toc - tic)


    def addEdges1(self):
        """Aggiungo gli archi citando con doppio ciclo sui nodi e
        testando se per ogni coppia esiste una connessione"""
        for u in self._fermate:
            for v in self._fermate:
                if DAO.basConnessione(u,v):
                    self._grafo.add_edge(u,v)


    def addEdges2(self) :
        """
        Ciclo solo una volta e faccio una query pert trovare tutti i vicini

        """
        for u in self._fermate:
            for v in DAO.getVicini(u):
                self._grafo.add_edge(u,self._idMapFermate[v.id_stazA])

    def addEdges3(self):
        """
        Faccio una query unica che prende tutti gli archi e poi ciclo qui

        """
        allEdges = DAO.getAllEdges()
        for edge in allEdges:
            u = self._idMapFermate[edge.id_stazP]
            v = self._idMapFermate[edge.id_stazA]
            self._grafo.add_edge(u,v)

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate

def getTraversalTime(u,v,vel):
    dist = geopy.distance.distance((u.coordX,u.coordY),
                                   (v.coordX,v.coordY)).km # in km
    time = dist/vel * 60 # in minuti
    return time

