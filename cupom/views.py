from datetime import datetime
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 
from cupom.models import Record
from cupom.serializer import CupomSerializer
from django.http import JsonResponse
import pyqrcode 
import uuid

@api_view(['POST'])
def novoCupom(request):
    if request.method == 'POST':
        resp = JSONParser().parse(request)
        cupom_name = resp['cupom_name']
        hash_id = uuid.uuid4().hex
        cupom_name+= hash_id[0:3]
        s = f"https://bdbd-143-255-112-227.sa.ngrok.io/validar-cupom-qrcode/?cupom_name={cupom_name}"
        url = pyqrcode.create(s) 
        image_as_str = url.png_as_base64_str(scale=8)
        data = {'name':cupom_name, 'hash_id':hash_id, 'qr_code':image_as_str,}
        cupom_serializer = CupomSerializer(data=data)
        if cupom_serializer.is_valid():
            cupom_serializer.save()
            return JsonResponse(cupom_serializer.data) 
        return JsonResponse(cupom_serializer.errors)

@api_view(['GET'])
def validarCupomQrcode(request):
    if request.method == 'GET':
        cupom_name = request.GET.get('cupom_name')
        try:
            cupom = Record.objects.get(name=cupom_name)
        except:
            return JsonResponse({'status':'invalido', 'message':'Cupom informado não existe'})
   
        if cupom.date_use == None:
            data={'name':cupom.name, 'qr_code':cupom.qr_code, 'hash_id':cupom.hash_id, 'date_create':cupom.date_create, 'date_use':datetime.now()}
            cupom_serializer = CupomSerializer(cupom, data=data)
            if cupom_serializer.is_valid():
                cupom_serializer.save()
                return JsonResponse({'status':'valido', 'message':'Cupom foi validado em '+str(cupom.date_use)})
            else: 
                return JsonResponse({'status':'invalido'})
        else:
            return JsonResponse({'status':'invalido', 'message':'Cupom foi utilizado em '+str(cupom.date_use)})

@api_view(['POST'])
def validarCupomText(request):
    if request.method == 'POST':
        resp = JSONParser().parse(request)
        cupom_name = resp['cupom_name']
        person_name = resp['person_name'] 
        try:
            cupom = Record.objects.get(name=cupom_name)
        except:
            return JsonResponse({'status':'invalido', 'message':'Cupom informado não existe'})
   
        if cupom.date_use == None:
            data={'name':cupom.name, 'qr_code':cupom.qr_code, 'hash_id':cupom.hash_id, 'date_create':cupom.date_create, 'date_use':datetime.now(), 'person_name':person_name}
            cupom_serializer = CupomSerializer(cupom, data=data)
            if cupom_serializer.is_valid():
                cupom_serializer.save()
                return JsonResponse({'status':'valido', 'message':'Cupom foi validado em '+str(cupom.date_use), 'person_name':str(cupom.person_name)  })
            else: 
                return JsonResponse({'status':'invalido'})
        else:
            return JsonResponse({'status':'invalido', 'message':'Cupom foi utilizado em '+str(cupom.date_use), 'person_name':str(cupom.person_name) })
    



class RecordsViewSet(viewsets.ModelViewSet):
    """Exibindo todos os cupons registrados"""
    queryset = Record.objects.all()
    serializer_class = CupomSerializer
