from rest_framework.serializers import ModelSerializer, CharField
from .models import Property, Reservation


class PropertySerializer(ModelSerializer):
    
    class Meta:
        model = Property
        fields = [
            'description',
            'prop_type',
            'address',
            'rooms',
            'baths',
            'parking',
            'max_guests',
            'is_available',
            'first_day_available',
            'rate',
            'owner',
                ]
    def create(self, validated_data):
        # print(self.context['reqeust'].user)
        return super().create(validated_data)

class ReservationSerializer(ModelSerializer):

    class Meta:
        model = Reservation
        fields = [
            'check_in',
            'check_out',
            'num_days',
            'numGuests',
            'property_id',
            'customer_id',
            'owner_id',
            'status',
        ]
    
    def create(self, validated_data):
        return super().create(validated_data)
    


