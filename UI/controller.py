import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self,e):
        # self._model.buildGraph()
        self._model.buildOrientedGraph()
        self._view._ddStazPartenza.disabled = False
        self._view.lst_result.controls.append(ft.Text("Grafo creato correttamente!!!"))
        self._view.lst_result.controls.append(ft.Text(f"Numero di nodi: {self._model._graph.number_of_nodes()} \n"
                                                      f"Numero di archi: {self._model._graph.number_of_edges()}"))
        self._view.update_page()

    def handleRaggiungibili(self):
        bfs_result = self._model.bfsSearch(self._fermataPartenza)
        dfs_result = self._model.dfsSearch(self._fermataPartenza)
        self._view.lst_result.controls.append(ft.Text("Risultato ricerca BFS"))
        for node in bfs_result:
            self._view.lst_result.controls.append(ft.Text(node))
        self._view.lst_result.controls.append(ft.Text("Risultato ricerca DFS"))
        for edge in dfs_result:
            self._view.lst_result.controls.append(ft.Text(edge))
        self._view._ddStazArrivo.disabled = False
        self._view.update_page()

    def handleCercaRaggiungibili(self,e):
        self._view.lst_result.controls.clear()
        path = self._model.getPath(self._fermataPartenza,self._fermataArrivo)
        self._view.lst_result.controls.append(ft.Text(f"Percorso più breve tra {self._fermataPartenza} e {self._fermataArrivo}"))
        for node in path:
            self._view.lst_result.controls.append(ft.Text(node))
        self._view.update_page()

    def loadFermate(self, dd: ft.Dropdown()):
        fermate = self._model.fermate

        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Partenza))
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))

    def read_DD_Partenza(self,e):
        print("read_DD_Partenza called ")
        if e.control.data is None:
            self._fermataPartenza = None
        else:
            self._fermataPartenza = e.control.data
            self.handleRaggiungibili()

    def read_DD_Arrivo(self,e):
        print("read_DD_Arrivo called ")
        if e.control.data is None:
            self._fermataArrivo = None
        else:
            self._fermataArrivo = e.control.data
            self._view._btnCalcola.disabled = False
            self.handleRaggiungibili()
