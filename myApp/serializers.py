from rest_framework import serializers
from .models import Insumo, Orden, OrdenItem

# --- API 1: Insumos (CRUD) ---
class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'


# --- API 2 y 3: Pedidos ---
class OrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = '__all__'



class OrdenItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenItem
        fields = '__all__'
