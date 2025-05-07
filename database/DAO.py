from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def basConnessione(u:Fermata,v:Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """Select *
                from connessione c
                where c.id_stazP = %s and c.id_stazA = %s"""
        cursor.execute(query,(u.id_fermata,v.id_fermata))

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result) > 0 # se len = 0 non ho un arco e
                               # non aggiungo, altrimenti aggiungo
    @staticmethod
    def getVicini(u:Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """Select *
                from connessione c
                where c.id_stazP = %s"""
        cursor.execute(query,(u.id_fermata,))

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """Select *
                from connessione c"""
        cursor.execute(query,)

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result