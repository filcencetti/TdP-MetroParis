# File per verificare il grafo primadi collegarlo all'interfaccia grafica
from model.model import Model
model = Model()
model.buildGraph()
print(f"Num nodi: {model.getNumNodi()}")
print(f"Num archi: {model.getNumArchi()}")