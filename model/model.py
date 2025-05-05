from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()

    def buildGraph(self):
        #Aggiungiamo i nodi
        self._grafo.add_nodes_from(self._fermate)
        self.addEdges1()

    def addEdges1(self):
        """Aggiungo gli archi citando con doppio ciclo sui nodi e
        testando se per ogni coppia esiste una connessione"""
        for u in self._fermate:
            for v in self._fermate:
                if DAO.basConnessione(u,v):
                    self._grafo.add_edge(u,v)
                    print(f"Aggiungo arco fra {u} e {v}")

    def addEdges2(self) :


    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate