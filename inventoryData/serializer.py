from inventoryData.models import Boxes
from rest_framework import serializers

class BoxSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    
    class Meta:
        model = Boxes
        fields = ['id', 'length', 'width', 'height', 'area', 'volume', 'created_by', 'created_at']

class UserBoxSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Boxes
        fields = ['id', 'length', 'width', 'height', 'area', 'volume']
