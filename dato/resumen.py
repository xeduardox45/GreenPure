from geopy.geocoders import Nominatim

#Clases de objetos resumen
class DatoResumido:
    def __init__(self, id, fecha, pais, ciudad, calidadAVG, ubicaciones):
        self.id = id
        self.fecha = fecha
        self.pais = pais
        self.ciudad = ciudad
        self.calidadAVG = calidadAVG
        self.ubicaciones = ubicaciones
class ElementoResumido:
    def __init__(self, distrito, datos):
        self.distrito = distrito
        self.datos = datos
class CaracteristicasElemento:
    def __init__(self, latitud, longitud, calidad, hora, humedad, temperatura, calor, concentracion, sensorHumo, sensorMetano):
        self.latitud = latitud
        self.longitud = longitud
        self.calidad = calidad
        self.hora = hora
        self.humedad = humedad
        self.temperatura = temperatura
        self.calor = calor
        self.concentracion = concentracion
        self.sensorHumo = sensorHumo
        self.sensorMetano = sensorMetano
        
#Listas para receptar los objetos resumidos
elementosDato = []
caracteristicas = []
datosResumidos = []
resumenParcial = []
resumenFinal = []

#Métodos de localización
def obtenerPais(location, id):
    try: 
        pais = location.raw['address']['country']
    except:
        pais = str(id) + "-No disponible"
    return pais

def obtenerCiudad(location, id):
    try:
        ciudad = location.raw['address']['state']
    except:
        try:
            ciudad = location.raw['address']['city']
        except:
            try:
                ciudad = location.raw['address']['country']
            except:
                ciudad = str(id) + "-No disponible"
    return ciudad

def obtenerDistrito(location, id):
    try:
        distrito = location.raw['address']['town']
    except:
        try:
            distrito = location.raw['address']['road']
        except:
            try:
                distrito = location.raw['address']['county']
            except:
                distrito = str(id) + "-No disponible"
    return distrito

#Métodos de resumen
def crearArregloResumen(latitud, longitud, calidadAVG, hora, humedad, temperatura, calor, concentracion, sensorHumo, sensorMetano, distrito, idDato, fecha, pais, ciudad, calidad):
    #Tercer nivel
    caracteristicasElemento = CaracteristicasElemento(latitud, longitud, calidadAVG, hora, humedad, temperatura, calor, concentracion, sensorHumo, sensorMetano)
    caracteristicas.append(caracteristicasElemento)
    #Segundo nivel
    elementoResumido = ElementoResumido(distrito, caracteristicas)
    elementosDato.append(elementoResumido)
    #Primer nivel
    datoResumido = DatoResumido(idDato, fecha, pais, ciudad, calidad, elementosDato)
    return datoResumido

def correccionOrientacionResumen(datosResumidos, paisesCiudades, distritos):
    #Corrección de datos repetidos de primer nivel
    listaRevisada = []
    resumenNivel1 = []
    for item in datosResumidos:
        if str(item.pais + item.ciudad) not in listaRevisada:
            listaRevisada.append(str(item.pais + item.ciudad))
            resumenNivel1.append(item)
    #Corrección de datos repetidos de segundo nivel
    listaRevisada = []
    resumenNivel2 = []
    newResumenUbicaciones = []
    for item in resumenNivel1:
        for item2 in item.ubicaciones:
            if item2.distrito not in listaRevisada:
                listaRevisada.append(item2.distrito)
                resumenNivel2.append(item2)
        newResumenUbicaciones.append(DatoResumido(item.id, item.fecha, item.pais, item.ciudad, item.calidadAVG, resumenNivel2))
    #Orientación de datos de tercer nivel
    resumenNivel3 = []
    newResumenDatos = []
    for item in newResumenUbicaciones:
        for item2 in item.ubicaciones:
            contador=0
            for item3 in item2.datos:
                if item2.distrito == distritos[contador]:
                    resumenNivel3.append(item3)
                contador = contador + 1
            newResumenDatos.append(ElementoResumido(item2.distrito, resumenNivel3))
            resumenNivel3 = []
        resumenParcial.append(DatoResumido(item.id, item.fecha, item.pais, item.ciudad, item.calidadAVG, newResumenDatos))
        newResumenDatos = []
    #Orientación de datos de segundo nivel
    resumenNivel2 = []
    for item in resumenParcial:
        contador = 0
        for item2 in item.ubicaciones:
            for item3 in item2.datos:
                if item2.distrito == distritos[contador] and str(item.pais+item.ciudad) == paisesCiudades[contador]:
                    resumenNivel2.append(item2)
                contador = contador + 1
        resumenFinal.append(DatoResumido(item.id, item.fecha, item.pais, item.ciudad, item.calidadAVG, resumenNivel2))
        resumenNivel2 = []
    #Corrección de datos repetidos por la orientacion
    listaRevisada = []
    resumenNivel2 = []
    resumenFinalOrdenado = []
    for item in resumenFinal:
        for item2 in item.ubicaciones:
            if item2.distrito not in listaRevisada:
                listaRevisada.append(item2.distrito)
                resumenNivel2.append(item2)
        resumenFinalOrdenado.append(DatoResumido(item.id, item.fecha, item.pais, item.ciudad, item.calidadAVG, resumenNivel2))
        resumenNivel2 = []
    return resumenFinalOrdenado