from datetime import datetime
from os import path, makedirs
import os
import time

def archivoRuta(dir, fileReq):
    
    # ========== Crear nuevo nombre para el archivo ==========
    dateTime = datetime.now()
    f = fileReq
    extension = f".{f.filename.split('.')[len(f.filename.split('.'))-1]}"
    fileNameNew = f"{str(time.mktime(dateTime.timetuple())).replace('.0', '')}{extension}"
    
    # ========== Ruta principal ==========
    rootRoute = path.dirname(path.abspath(__file__))
    separador = path.sep
    rootRoute = separador.join(rootRoute.split(separador)[:-1])

    # ========== Crear directorios ==========
    routeArray = dir.split("\\")
    routeArray = [elemento for elemento in routeArray if elemento]
    createRoute = ""
    for elemnt in routeArray:
        bars = "/" if os.name != 'nt' else "\\"
        createRoute = createRoute + f"{bars}{elemnt}"
        if not path.exists(f"{rootRoute}{createRoute}"):
            makedirs(f"{rootRoute}{createRoute}")
    
    # ========== Ruta final ==========
    if os.name != 'nt':
        dir = dir.replace("\\", "/")
        dir = f"{rootRoute}{dir}{fileNameNew}"
    else:
        dir = f"{rootRoute}{dir}{fileNameNew}"
        
    return dir, fileNameNew


def enviarArchivo(route):
    
    # ========== Ruta principal ==========
    rootRoute = path.dirname(path.abspath(__file__))
    separador = path.sep
    rootRoute = separador.join(rootRoute.split(separador)[:-1])
    
    # ========== Ruta final ==========
    if os.name != 'nt':
        route = route.replace("\\", "/")
        route = f"{rootRoute}{route}"
    else:
        route = f"{rootRoute}{route}"
        
    return route