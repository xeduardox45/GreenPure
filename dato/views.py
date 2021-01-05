from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Datos
from .serializers import DatosSerializer
from django.shortcuts import render

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
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
        serializer = DatasSerializer(data=data)
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

def humedad(request):
    elementos = Datos.objects.all()
    context = {
        "elementos": elementos
    }
    return render(request, 'index.html', context)