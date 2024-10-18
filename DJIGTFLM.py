import numpy as np
import pandas as pd

class DJIGTFLM:
    def __init__(self, zjam, lista_actual, df_new_games):
        # Atributos
        self.zjam = zjam
        self.lista_actual = lista_actual
        self.df_new_games = df_new_games
    
    def typeCabinet(self, Material):
        if Material[0][:8][-1] == "1":
            return "Dual Screen"
        else:
            return "Portrait"
    
    def typeCabinet_lista(self, Material):
        if Material[1][:8][-1] == "1":
            return "Dual Screen"
        else:
            return "Portrait"

    def versionGame(self, Material):
        return Material[0][-3:]

    def versionGame_lista(self, Material):
        return Material[1][-3:]

    def statusOK(self, Material):
        if Material[5] in ["EXC", "EXC_FM", "EXC_TB", "PNH", "RET_BS", "RET_FT", "TCA", "TCS"]:
            return "OK"
        else:
            return "NO"

    def themeID(self, Material):
        return Material[0][:11][-3:]
    
    def themeID_lista(self, Material):
        return Material[1][:11][-3:]
    
    def DF_zjam(self):
        type_cabinet = []
        version_game = []
        status_ok = []
        theme_id = []
        for i in range(0, len(self.zjam)):
            theme_id.append(self.themeID(self.zjam.iloc[i]))
            type_cabinet.append(self.typeCabinet(self.zjam.iloc[i]))
            version_game.append(self.versionGame(self.zjam.iloc[i]))
            status_ok.append(self.statusOK(self.zjam.iloc[i]))
        return pd.DataFrame({"Material": list(self.zjam["Material"]), "GameTitle": list(self.zjam["Material Description"]),
                             "Them ID": theme_id, "Type Cabinet": type_cabinet, 
                             "Status" : list(self.zjam["Submission Status Code"]), "Status Ok": status_ok})
    def DF_listaActual(self):
        type_cabinet_lista = []
        version_game_lista = []
        theme_id_lista = []
        for i in range(0, len(self.lista_actual)):
            theme_id_lista.append(self.themeID_lista(self.lista_actual.iloc[i]))
            type_cabinet_lista.append(self.typeCabinet_lista(self.lista_actual.iloc[i]))
            version_game_lista.append(self.versionGame_lista(self.lista_actual.iloc[i]))
        return pd.DataFrame({"Material": list(self.lista_actual["COD.IDENTIFICACION"]), "Them ID": theme_id_lista, 
                             "Version": version_game_lista, "Type Cabinet": type_cabinet_lista})
    
    def df_newGames(self):
        df_listaActual = self.DF_listaActual()
        df_zjam = self.DF_zjam()
        type_cabinet_lista_newGames = []
        version_game_lista_newGames = []
        theme_id_lista_newGames = []
        for i in range(0, len(self.df_new_games)):
            theme_id_lista_newGames.append(self.themeID_lista(self.df_new_games.iloc[i]))
            type_cabinet_lista_newGames.append(self.typeCabinet_lista(self.df_new_games.iloc[i]))
            version_game_lista_newGames.append(self.versionGame_lista(self.df_new_games.iloc[i]))

        df_listaActual_newGames = pd.DataFrame({"Material": list(self.df_new_games["Material"]),
                      "Them ID": theme_id_lista_newGames,
                      "Version": version_game_lista_newGames,
                      "Type Cabinet": type_cabinet_lista_newGames})
        
        df_listaActual_newGames["Used"] = list(df_listaActual_newGames["Material"].isin(df_listaActual["Material"]))
        df_listaActual_newGames["Game used"] = list(df_listaActual_newGames["Them ID"].isin(df_listaActual["Them ID"]))
        df_listaActual_newGames = pd.merge(df_listaActual_newGames, df_zjam[["Material", "GameTitle", "Status", "Status Ok"]], on='Material', how='left')
        
        label = []
        for i in range(0, len(df_listaActual_newGames)):
            if(df_listaActual_newGames["Used"][i] == False and  df_listaActual_newGames["Game used"][i] == False):
                if df_listaActual_newGames["Status Ok"][i] == "OK":
                    label.append("OK")
                else:
                    label.append("No")
            elif(df_listaActual_newGames["Used"][i] == False and  df_listaActual_newGames["Game used"][i] == True):
                if df_listaActual_newGames["Status Ok"][i] == "OK":
                    label.append("Update version")
                else:
                    label.append("No")
            elif(df_listaActual_newGames["Used"][i] == True and  df_listaActual_newGames["Game used"][i] == True):
                label.append("No")

        df_listaActual_newGames["label"] = label
        return df_listaActual_newGames