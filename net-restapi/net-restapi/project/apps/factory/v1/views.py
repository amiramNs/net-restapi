import uuid
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response

from project.apps.factory.models import Equipment, Emergency
from project.apps.factory.v1 import serializers
from project.permissions import IsUserAdmin, IsUserOperator, IsRepairMan


@extend_schema(
    tags=['equipment'],
    request=serializers.EquipmentSerializer,
    responses={200: OpenApiResponse(response=serializers.ResponseEquipmentSerializer, description='SUCCESS'),
               401: OpenApiResponse(description='UNAUTHORIZED'),
               403: OpenApiResponse(description='FORBIDDEN'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="create equipment.",
)
class CreateEquipmentView(CreateAPIView):
    serializer_class = serializers.EquipmentSerializer
    response_serializer = serializers.ResponseEquipmentSerializer
    # permission_classes = (IsUserAdmin,)

    def create(self, request, *args, **kwargs):
        code_equip = uuid.uuid4()
        state_code = uuid.uuid4()
        serializer = self.serializer_class(data=request.data, context={'code_equip': code_equip, 'state_code': state_code})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(code_equip=code_equip, state_code=state_code)
        return Response(data=self.response_serializer(obj).data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['equipment'],
    responses={200: OpenApiResponse(response=serializers.ResponseEquipmentSerializer, description='SUCCESS'),
               401: OpenApiResponse(description='UNAUTHORIZED'),
               403: OpenApiResponse(description='FORBIDDEN'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="list equipment.",
)
class ListEquipmentView(ListAPIView):
    permission_classes = ()
    serializer_class = serializers.ResponseEquipmentSerializer
    queryset = Equipment.objects.all().order_by('-id')


@extend_schema(
    tags=['equipment'],
    responses={200: OpenApiResponse(response=serializers.ResponseEquipmentSerializer, description='SUCCESS'),
               401: OpenApiResponse(description='UNAUTHORIZED'),
               403: OpenApiResponse(description='FORBIDDEN'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="get equipment.",
)
class GetEquipmentView(RetrieveAPIView):
    permission_classes = ()
    serializer_class = serializers.ResponseEquipmentSerializer

    def get_object(self):
        try:
            return Equipment.objects.get(id=self.kwargs['pk'])
        except Equipment.DoesNotExist:
            raise NotFound('Equipment Notfound!')


@extend_schema(
    tags=['equipment'],
    responses={200: OpenApiResponse(description='SUCCESS'),
               403: OpenApiResponse(description='FORBIDDEN'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="delete equipment.",
)
class DeleteEquipmentView(DestroyAPIView):
    permission_classes = (IsUserAdmin,)
    serializer_class = serializers.ResponseEquipmentSerializer

    def get_object(self):
        try:
            return Equipment.objects.get(id=self.kwargs['pk'])
        except Equipment.DoesNotExist:
            raise NotFound('Equipment Notfound!')

    def destroy(self, request, *args, **kwargs):
        super().destroy(request ,*args, **kwargs)
        return Response(status=status.HTTP_200_OK)


@extend_schema(
    tags=['equipment'],
    request=serializers.EquipmentSerializer,
    responses={200: OpenApiResponse(response=serializers.EquipmentSerializer, description='SUCCESS'),
               401: OpenApiResponse(description='UNAUTHORIZED'),
               403: OpenApiResponse(description='FORBIDDEN'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="update equipment.",
)
@extend_schema(methods=['PUT'], exclude=True)
class UpdateEquipmentView(UpdateAPIView):
    serializer_class = serializers.EquipmentSerializer
    permission_classes = (IsUserAdmin,)

    def get_object(self):
        try:
            return Equipment.objects.get(id=self.kwargs[self.lookup_field])
        except Equipment.DoesNotExist:
            raise NotFound('Equipment Notfound!')


@extend_schema(
    tags=['emergency'],
    request=serializers.OperatorEmergencySerializer,
    responses={200: OpenApiResponse(response=serializers.EmergencySerializer, description='SUCCESS'),
               401: OpenApiResponse(description='UNAUTHORIZED'),
               403: OpenApiResponse(description='FORBIDDEN'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="create emergency.",
)
class CreateEmergencyView(CreateAPIView):
    permission_classes = (IsUserAdmin | IsUserOperator,)
    serializer_class = serializers.OperatorEmergencySerializer
    response_serializer = serializers.EmergencySerializer
    lookup_field = 'equipment_id'

    def create(self, request, *args, **kwargs):
        repair_code = uuid.uuid4()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(state_code=self.get_object(), repair_code=repair_code)
        return Response(data=self.response_serializer(obj).data, status=status.HTTP_200_OK)

    def get_object(self):
        try:
            return Equipment.objects.get(id=self.kwargs[self.lookup_field])
        except Equipment.DoesNotExist:
            raise NotFound('Equipment Notfound!')


@extend_schema(
    tags=['emergency'],
    responses={200: OpenApiResponse(response=serializers.EmergencySerializer, description='SUCCESS'),
               401: OpenApiResponse(description='UNAUTHORIZED'),
               403: OpenApiResponse(description='FORBIDDEN'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="create emergency.",
)
class GetEmergencyView(RetrieveAPIView):
    permission_classes = ()
    serializer_class = serializers.EmergencySerializer

    def get_object(self):
        try:
            return Emergency.objects.get(id=self.kwargs[self.lookup_field])
        except Emergency.DoesNotExist:
            raise NotFound('Emergency Notfound!')


@extend_schema(
    tags=['emergency'],
    responses={200: OpenApiResponse(response=serializers.EmergencySerializer, description='SUCCESS'),
               401: OpenApiResponse(description='UNAUTHORIZED'),
               403: OpenApiResponse(description='FORBIDDEN'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="list emergency.",
)
class ListEmergencyView(ListAPIView):
    permission_classes = ()
    serializer_class = serializers.EmergencySerializer
    queryset = Emergency.objects.all().order_by('-id')


@extend_schema(
    tags=['emergency'],
    responses={200: OpenApiResponse(description='SUCCESS'),
               403: OpenApiResponse(description='FORBIDDEN'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="delete emergency.",
)
class DeleteEmergencyView(DestroyAPIView):
    permission_classes = (IsUserAdmin,)

    def get_object(self):
        try:
            return Emergency.objects.get(id=self.kwargs[self.lookup_field])
        except Emergency.DoesNotExist:
            raise NotFound('Emergency Notfound!')

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)


@extend_schema(
    tags=['emergency'],
    request=serializers.RepairmanEmergencySerializer,
    responses={200: OpenApiResponse(response=serializers.EmergencySerializer, description='SUCCESS'),
               401: OpenApiResponse(description='UNAUTHORIZED'),
               403: OpenApiResponse(description='FORBIDDEN'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="update emergency.",
)
@extend_schema(methods=['PUT'], exclude=True)
class UpdateEmergencyView(UpdateAPIView):
    permission_classes = (IsUserAdmin | IsRepairMan,)
    serializer_class = serializers.RepairmanEmergencySerializer
    response_serializer = serializers.EmergencySerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response(data=self.response_serializer(obj).data, status=status.HTTP_200_OK)

    def get_object(self):
        try:
            return Emergency.objects.get(id=self.kwargs[self.lookup_field])
        except Emergency.DoesNotExist:
            raise NotFound('Emergency Notfound!')


@extend_schema(
    tags=['emergency'],
    request=serializers.OperatorEmergencySerializer,
    responses={200: OpenApiResponse(response=serializers.EmergencySerializer, description='SUCCESS'),
               401: OpenApiResponse(description='UNAUTHORIZED'),
               403: OpenApiResponse(description='FORBIDDEN'),
               404: OpenApiResponse(description='NOT FOUND')},
    description="update operator emergency.",
)
class UpdateOperatorEmergencyView(UpdateEmergencyView):
    permission_classes = (IsUserAdmin | IsUserOperator,)
    serializer_class = serializers.OperatorEmergencySerializer
    response_serializer = serializers.EmergencySerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response(data=self.response_serializer(obj).data, status=status.HTTP_200_OK)

    def get_object(self):
        try:
            return Emergency.objects.get(id=self.kwargs[self.lookup_field])
        except Emergency.DoesNotExist:
            raise NotFound('Emergency Notfound!')
