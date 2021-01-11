from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Datos
from .serializers import *
from django.shortcuts import render
from geopy.geocoders import Nominatim

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

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

@csrf_exempt
def Datos_list(request):
    """
    List all code serie, or create a new serie.
    """
    if request.method == 'GET':
        datos = Datos.objects.all()
        serializer = DatosSerializer(datos, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DatosSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
@csrf_exempt
def Dato_detail(request, pk):
    """
    Retrieve, update or delete a serie.
    """
    try:
        datos = Datos.objects.get(pk=pk)
    except Datos.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DatosSerializer(datos)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DatosSerializer(Datos, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        Datos.delete()
        return HttpResponse(status=204)

@csrf_exempt
def Datos_resumen(request):
    """
    List all code serie, or create a new serie.
    """
    if request.method == 'GET':
        datos = Datos.objects.all()
        serializer = DatosResumenSerializer(datos, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DatosResumenSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

def resumen(request):
    datos = Datos.objects.all()
    #Listas para receptar los objetos resumidos
    datosResumidos = []
    elementosDato = []
    caracteristicas = []
    resumenParcial = []
    resumenFinal = []
    #Listas para guardar variables de orientación de datos
    distritos = []
    paisesCiudades = []
    #Variable contador
    cont = 0
    for dato in datos:  
        cont = cont+1
        #Primer nivel de datos
        fecha = str(dato.fecha)[:10]
        geolocator = Nominatim(user_agent="GreenPure")
        location = geolocator.reverse(str(dato.Latitud) + "," + str(dato.Longitud))
        pais = location.raw['address']['country']
        try:
            ciudad = location.raw['address']['state']
        except:
            ciudad = str(pais+" - No disponible")
        paisesCiudades.append(pais+ciudad)
        #Segundo nivel de datos
        try:
            distrito = location.raw['address']['town']
        except:
            distrito = str(ciudad+".")
        distritos.append(distrito)
        #Tercer nivel de datos
        calidad = 12
        hora = str(dato.fecha)[11:19]
        humedad = dato.Humedad
        temperatura = dato.Temperatura
        calor = dato.Calor
        concentracion = dato.Concentracion
        sensorHumo = dato.SensorHumo
        sensorMetano = dato.SensorMetano
        #Creación del arreglo entero
        #Tercer nivel
        caracteristicasElemento = CaracteristicasElemento(dato.Latitud, dato.Longitud, calidad, hora, humedad, temperatura, calor, concentracion, sensorHumo, sensorMetano)
        caracteristicas.append(caracteristicasElemento)
        #Segundo nivel
        elementoResumido = ElementoResumido(distrito, caracteristicas)
        elementosDato.append(elementoResumido)
        #Primer nivel
        datoResumido = DatoResumido(cont, fecha, pais, ciudad, 21, elementosDato)
        datosResumidos.append(datoResumido)
        if cont==len(datos):
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
    #Serialización de datos
    serializer = DatosResumenSerializer(resumenFinalOrdenado, many=True)
    return JSONResponse(serializer.data)

def humedad(request):
    elementos = Datos.objects.all()
    geolocator = Nominatim(user_agent="GreenPure")
    location = geolocator.reverse("-16.3745735,-71.512105")
    context = {
        "elementos": elementos,
        "prueba": location.address
    }
    return render(request, 'index.html', context)