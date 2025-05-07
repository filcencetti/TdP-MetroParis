from datetime import datetime

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMapFermate = {} #dizionario per associare le fermate al proprio id
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

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
        print(toc - tic)


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