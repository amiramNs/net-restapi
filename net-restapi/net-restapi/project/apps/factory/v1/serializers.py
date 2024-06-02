from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from project.apps.factory.models import Emergency, Equipment


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return int(value.timestamp())


class EquipmentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(allow_null=False)
    expire = serializers.DateTimeField(allow_null=False)

    class Meta:
        model = Equipment
        fields = '__all__'
        read_only_fields = ('code_equip', 'state_code')


class ResponseEquipmentSerializer(serializers.ModelSerializer):
    created_at = TimestampField()
    expire = TimestampField()

    class Meta:
        model = Equipment
        fields = '__all__'



class OperatorEmergencySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(allow_null=False)

    class Meta:
        model = Emergency
        fields = '__all__'
        read_only_fields = ('reason_repairman', 'repair_date', 'repair_code', 'state_code')



class RepairmanEmergencySerializer(serializers.ModelSerializer):
    repair_date = serializers.DateTimeField(allow_null=False)

    class Meta:
        model = Emergency
        fields = '__all__'
        read_only_fields = ('state_code', 'created_at', 'reason_operator', 'repair_code')

    @extend_schema_field(field=OpenApiTypes.INT)
    def get_repair_date(self, obj):
        if obj.repair_date is not None:
            return int(obj.repair_date.timestamp())


class EmergencySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    repair_date = serializers.SerializerMethodField()
    state_code = ResponseEquipmentSerializer(read_only=True)

    class Meta:
        model = Emergency
        fields = '__all__'

    @extend_schema_field(field=OpenApiTypes.INT)
    def get_created_at(self, obj):
        return int(obj.created_at.timestamp())

    @extend_schema_field(field=OpenApiTypes.INT)
    def get_repair_date(self, obj):
        if obj.repair_date is not None:
            return int(obj.repair_date.timestamp())