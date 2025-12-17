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

    class Meta:
        model = Orden
        exclude = (
            'plataforma',
            'creado',
            'actualizado',
        )

    def validate(self, data):
        estado = data.get('estado')
        estado_pago = data.get('estado_pago')

        if estado == 'solicitado' and estado_pago != 'pendiente':
            raise serializers.ValidationError(
                "Un pedido solicitado no puede estar pagado."
            )

        if estado == 'completado' and estado_pago != 'pagado':
            raise serializers.ValidationError(
                "Un pedido completado debe estar pagado."
            )

        if estado == 'cancelado' and estado_pago == 'pagado':
            raise serializers.ValidationError(
                "Un pedido cancelado no puede estar pagado."
            )

        return data

    def update(self, instance, validated_data):
        estado = validated_data.get("estado", instance.estado)

        # Automatización extra (seguridad)
        if estado == "completado":
            validated_data["estado_pago"] = "pagado"

        return super().update(instance, validated_data)

    def create(self, validated_data):
        validated_data['plataforma'] = validated_data.get(
            'contacto_tipo', 'pagina web'
        )
        return super().create(validated_data)





class OrdenItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenItem
        fields = '__all__'

