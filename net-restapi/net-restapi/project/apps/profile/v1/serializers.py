from rest_framework.serializers import ModelSerializer, Serializer, CharField, IntegerField
from project.apps.profile.models import User


class LoginSerializer(Serializer):
    username = CharField(max_length=150)
    password = CharField(max_length=80)


class TokenSerializer(Serializer):
    access = CharField(max_length=400, required=False, allow_null=True, default=None)
    refresh = CharField(max_length=400, required=False, allow_null=True, default=None)
    token_id = IntegerField(read_only=True)


class LogoutSerializer(Serializer):
    refresh = CharField(max_length=400, required=True)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'job', 'password']


class ResponseUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'job']





# class CreatePurchaseSerializer(ModelSerializer):
#     expire = DateTimeField(allow_null=False)
#
#     class Meta:
#         model = Purchase
#         fields = '__all__'
#         read_only_fields = ('state_code', 'code_equip', 'create_at')
#
#
# class PurchaseSerializer(ModelSerializer):
#     create_at = SerializerMethodField()
#     expire = SerializerMethodField()
#
#     class Meta:
#         model = Purchase
#         fields = '__all__'
#
#     @extend_schema_field(field=OpenApiTypes.INT)
#     def get_created_at(self, obj):
#         return int(obj.created_at.timestamp())
#
#     @extend_schema_field(field=OpenApiTypes.INT)
#     def get_expire(self, obj):
#         if obj.repair_date is not None:
#             return int(obj.expire.timestamp())
