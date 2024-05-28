from django.urls import path

from project.apps.factory.v1 import views


urlpatterns = [
    # Equipment
    path('create_equipment/', views.CreateEquipmentView.as_view(), name='create-equipment'),
    path('list_equipment/', views.ListEquipmentView.as_view(), name='list-equipment'),
    path('get_equipment/<int:pk>/', views.GetEquipmentView.as_view(), name='get-equipment'),
    path('delete_equipment/<int:pk>/', views.DeleteEquipmentView.as_view(), name='delete-equipment'),
    path('update-equipment/<int:pk>/', views.UpdateEquipmentView.as_view(), name='update-equipment'),

    # Emergency
    path('create_emergency/<int:equipment_id>/', views.CreateEmergencyView.as_view(), name='create-emergency'),
    path('get_emergency/<int:pk>/', views.GetEmergencyView.as_view(), name='get-emergency'),
    path('list_emergency/', views.ListEmergencyView.as_view(), name='list-emergency'),
    path('delete-emergency/<int:pk>/', views.DeleteEmergencyView.as_view(), name='delete-emergency'),
    path('update_emergency/<int:pk>/', views.UpdateEmergencyView.as_view(), name='update-emergency'),
    path('update-operator-emergency/<int:pk>/', views.UpdateOperatorEmergencyView.as_view(), name='update-operator-emergency'),
]