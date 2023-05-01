from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, \
    ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Property, Reservation
from .serializers import PropertySerializer, ReservationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from notif.models import Notification
from notif.serializers import NotificationSerializer


# Create your views here.
class PropertyApiView(APIView):
    filter_backends=(DjangoFilterBackend,)
    #permission_classes = () 
    #authentication_classes = () 
    filterset_fields = ['parking', 'baths', 'rooms', 'owner']
    # will need to make this specific to one property
    def get(self, request, prop_id, *args, **kwargs): 
        try:
            properties = Property.objects.filter(id=prop_id)
            serializer = PropertySerializer(properties, many = True)
            return Response(serializer.data)
        except:
            return HttpResponse(status = 401)

    def post(self, request, *args, **kwargs):
        data = {
            'description' : request.data.get('description'),
            'prop_type' : request.data.get('prop_type') ,
            'address' : request.data.get('address'),
            'rooms' : request.data.get('rooms'),
            'baths' : request.data.get('baths'),
            'parking' : request.data.get('parking'),
            'max_guests' : request.data.get('max_guests'),
            'rate' : request.data.get('rate'),
            'owner' : request.user.id 
        }
        serializer = PropertySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return HttpResponse(status = 400)
    

    def put(self, request, prop_id, *args, **kwargs):
        try:
            property = Property.objects.get(id = prop_id, owner = request.user.id)
            data = {
                'description' : request.data.get('description'),
                'prop_type' : request.data.get('prop_type') ,
                'address' : request.data.get('address'),
                'rooms' : request.data.get('rooms'),
                'baths' : request.data.get('baths'),
                'parking' : request.data.get('parking'),
                'max_guests' : request.data.get('max_guests'),
                'rate' : request.data.get('rate'),
                'owner' : request.user.id,
            }
            serializer = PropertySerializer(property, data = data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return HttpResponse(status = 401)
    
    def delete(self, request, prop_id, *args, **kwargs):
        try:
            property = Property.objects.get(id = prop_id, owner = request.user.id)
            property.delete()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=401)

class PropertySearch(generics.ListAPIView):
    #permission_classes = () 
    queryset  = Property.objects.all()
    serializer_class  =  PropertySerializer
    filter_backends = [
        DjangoFilterBackend, 
        filters.OrderingFilter,
        ]
    name = 'property-search'

    filterset_fields = (
        'parking',
        'baths',
        'rooms',
        'owner',
    )

    ordering_fields = (
        'baths',
        'rooms',
    )

    



class ReservationApiView(APIView):

    # will need to make this specific to one reservations
    def get(self, request, prop_id, *args, **kwargs): 
        reservations = Reservation.objects.filter(id=prop_id)
        serializer = ReservationSerializer(reservations, many = True)
        return Response(serializer.data)
    

    def post(self, request, prop_id, *args, **kwargs):
        print("test")
        try:
            property = Property.objects.get(id = prop_id)
        except:
            return HttpResponse(status=408)
        owner_id = property.owner
        data = {
            'check_in' : request.data.get('check_in') ,
            'check_out' : request.data.get('check_out'),
            'num_days' : request.data.get('num_days'),
            'numGuests' : request.data.get('numGuests'),
            'property_id' : prop_id,
            'customer_id' : request.user.id,
            'owner_id' : owner_id,
            'status' : 'PENDING',
        }
        serializer = ReservationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'timestamp' : "2022-03-15T14:30:00Z",
                'is_read' : False,
                'message' : 'YOU HAVE A RESERVATION PENDIING',
                'id' : 1
            }
            notifseri = NotificationSerializer(data=data)
            if notifseri.is_valid():
                notifseri.save()
            return Response(serializer.data)
            

class ReservationsSearch(generics.ListAPIView):
    queryset  = Reservation.objects.all()
    serializer_class  =  ReservationSerializer
    filter_backends = [
        DjangoFilterBackend, 
        ]
    name = 'reservation-search'

    filterset_fields = (
        'status',
        'owner_id',
        'customer_id',
    )


@api_view(['GET'])
def cancelRes(request, res_id):
    if request.method == 'GET':
        # try:
            reservation = Reservation.objects.get(
                id = res_id, 
                customer_id = request.user.id
            )
            reservation.status = "CANCEL PENDING"
            serializer = ReservationSerializer(reservation, data = {status : "CANCEL PENDING"}, partial = True)
            data = {
                'timestamp' : "2022-03-15T14:30:00Z",
                'is_read' : False,
                'message' : 'YOU HAVE A CANCELLATION PENDIING',
                'id' : 1
            }
            notifseri = NotificationSerializer(data=data)
            if notifseri.is_valid():
                notifseri.save()
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        # except:
        #     return HttpResponse(code  = 401)
    else:
        return HttpResponse(status = 405 )


@api_view(['GET'])
def approveRes(reqeust, res_id, status):
    if reqeust.method == 'GET':
        try:
            reservation = Reservation.objects.get(
                id = res_id, 
                owner_id = reqeust.user.id
            )
        except:
            return HttpResponse(status = 401)
        
        # if status that is passed on is 1, the reservation is accepted
        # if status that is passed on is 2, the

        if status == 1:
            reservation.status = "ACCEPTED"
            serializer = ReservationSerializer(reservation, data = {status : "ACCEPTED"}, partial = True)
            if serializer.is_valid():
                serializer.save()
            
            # notificatoin
            return Response(serializer.data)
        elif status == 2:
            reservation.status = "REJECTED"
            serializer = ReservationSerializer(reservation, data = {status : "REJECTED"}, partial = True)
            if serializer.is_valid():
                serializer.save()
            # notification
            return Response(serializer.data)
        else:
            return HttpResponse(status = 400)
    else:
        return HttpResponse(status = 405)


@api_view(['GET'])
def approveCancel(request, res_id, status):
    if request.method == 'GET':
        try:
            reservation = Reservation.objects.get(
                id = res_id, 
                owner_id = request.user.id
            )
        except:
            return HttpResponse(status = 401)
        
        # if status that is passed on is 1, the reservation is accepted
        # if status that is passed on is 2, the

        if status == 1:
            reservation.status = "CANCEL ACCEPTED"
            serializer = ReservationSerializer(reservation, data = {status : "CANCEL ACCEPTED"}, partial = True)
            if serializer.is_valid():
                serializer.save()
            # notificatoin
            return Response(serializer.data)
        elif status == 2:
            reservation.status = "CANCEL REJECTED"
            serializer = ReservationSerializer(reservation, data = {status : "CANCEL REJECTED"}, partial = True)
            if serializer.is_valid():
                serializer.save()
            # notification
            return Response(serializer.data)
        else:
            return HttpResponse(status = 400)
    else:
        return HttpResponse(status = 405)

@api_view(['DELETE'])
def deleteRes(request, res_id):
    print(res_id)
    if request.method == 'DELETE':
        try:
            print(request.user.id)
            reservation = Reservation.objects.get(
                id = res_id, 
                owner_id = request.user.id
            )
        except:
            return HttpResponse(status = 404)
        reservation.delete()
        return HttpResponse(status = 200)
    else:
        return HttpResponse(status = 405)