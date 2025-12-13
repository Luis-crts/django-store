from rest_framework import serializers
from .models import Insumo, Orden, OrdenItem

# Validador de contacto
def validar_contacto(contacto):
    contacto = contacto.strip()

    if contacto.startswith("wp:"):
        numero = contacto[3:]
        if not numero.isdigit():
            raise serializers.ValidationError(
                "WhatsApp debe contener solo números. Ej: wp:56912345678"
            )

    elif contacto.startswith("ig:"):
        if not contacto[3:].startswith("@"):
            raise serializers.ValidationError(
                "Instagram debe ser ig:@usuario"
            )

    elif contacto.startswith("dir:"):
        if len(contacto[4:]) < 5:
            raise serializers.ValidationError(
                "Dirección demasiado corta"
            )

    elif contacto.startswith("web:"):
        if not contacto[4:].startswith("http"):
            raise serializers.ValidationError(
                "URL inválida"
            )

    else:
        raise serializers.ValidationError(
            "Formato inválido. Use wp:, ig:, dir: o web:"
        )

    return contacto


# API 1: /insumos (CRUD)
class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'


# API 2 y 3: /pedidos
class OrdenSerializer(serializers.ModelSerializer):

    contacto = serializers.CharField()

    class Meta:
        model = Orden
        fields = '__all__'

    def validate_contacto(self, value):
        return validar_contacto(value)


class OrdenItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenItem
        fields = '__all__'

