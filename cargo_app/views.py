import datetime
import hashlib
import requests # type: ignore
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from cargo_app.models import Shipment, Category
from users.models import User
from rest_framework.decorators import api_view
from .serializers import CategorySerializer
from .models import CorporateShipment, CorporateUser


def sendCategories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)    

@api_view(['POST'])
def shipOrder(request):
    if request.method == 'POST':
        bank_receiptID = request.data['billNo']
    
        if checkPayment(bank_receiptID):
            last = CorporateShipment.objects.create(
                corporateID=CorporateUser.objects.filter(name=request.data['CompanyName']).first(), 
                customer_name=request.data['destname'], 
                customer_surname=request.data['destsurname'],
                source_address="Deuzon Logistics",
                destination_address=request.data['Destaddress'],
                categoryID=calculatePrice(request.data['totalQuantity'])[1],
                sending_date=datetime.date.today(),
                trackID="last"
            )
            track_code = hashlib.md5()
            track_code.update(str(last.id).encode())
            track_code.digest()
            track_number = str(track_code.hexdigest()[:12].upper())
            last.trackID = track_number
            last.save()
            return HttpResponse(track_number)
        else:
            return HttpResponse("Payment verification failed.", status=400)

def checkPayment(bank_receiptID):
    url = f'http://146.185.147.162/accounts/query/receipt/{bank_receiptID}/'
    r = requests.get(url)
    des_response = r.json()
    return des_response.get('IsExist', False)

def index(request):
    user_id = request.COOKIES.get('userid')
    shipment_list = Shipment.objects.filter(userID=user_id) if user_id else Shipment.objects.all()
    return render(request, 'shipments/list.html', {'userid': user_id, 'shipmentList': list(shipment_list)})

def addshipment(request):
    if request.method == 'POST':
        params = request.POST
        price, ctgry = calculatePrice(int(params['qnt']))
        user = User.objects.filter(id=int(request.COOKIES.get('userid'))).first()
        last = Shipment.objects.create(
            userID=user,
            source_address=params['source'],
            categoryID=ctgry,
            destination_address=params['dest'],
            sending_date=datetime.datetime.now(),
            trackID="asd",
            price=price
        )
        track_code = hashlib.md5()
        track_code.update(str(last.id).encode())
        track_code.digest()
        last.trackID = str(track_code.hexdigest()[:12].upper())
        last.save()
        return index(request)
    return render(request, 'shipments/new_shipment.html')

def details(request, pk):
    return render(request, 'shipments/details.html', {'userid': request.COOKIES.get('userid'), 'shipment': Shipment.objects.get(id=pk)})

def delete(request, pk):
    Shipment.objects.filter(id=pk).delete()
    return index(request)

def update(request, pk):
    shipment = Shipment.objects.get(id=pk)
    if request.method == 'POST':
        params = request.POST
        price, ctgry = calculatePrice(float(params['qnt']))
        shipment.source_address = params['source']
        shipment.destination_address = params['dest']
        shipment.categoryID = ctgry
        shipment.price = price
        shipment.save()
        return index(request)
    return render(request, 'shipments/update.html', {'userid': request.COOKIES.get('userid'), 'shipment': shipment, 'quantity': shipment.price})

def calculatePrice(quantity):
    quantity = int(quantity)
    price = quantity * 1 
    ctgry = None
    for c in Category.objects.all():
        if ctgry is None or c.quantity > quantity:
            ctgry = c
            price = quantity * c.cat_price
            break
    return price, ctgry

def gettrack(request):
    if request.method == 'POST':
        params = request.POST
        query_result = Shipment.objects.filter(trackID=params['trackid']).first()
        if not query_result:
            return render(request, "home/home.html", {'firms': CorporateUser.objects.all(), 'userid': request.COOKIES.get('userid'), 'message': 'Invalid track id.', 'messagetype': 2})
        return render(request, 'shipments/details.html', {'userid': request.COOKIES.get('userid'), 'shipment': query_result})

def getcorporatetrack(request):
    if request.method == 'POST':
        params = request.POST
        query_result = CorporateShipment.objects.filter(trackID=params['trackid']).first()
        if not query_result:
            return render(request, "home/home.html", {'firms': CorporateUser.objects.all(), 'userid': request.COOKIES.get('userid'), 'message': 'Invalid track id.', 'messagetype': 2})
        return render(request, 'shipments/cordetails.html', {'userid': request.COOKIES.get('userid'), 'shipment': query_result})

def listUserShipments(request, pk):
    return index(request)
