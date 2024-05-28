from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.forms import ModelForm, ModelMultipleChoiceField

from project.apps.profile.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'job')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    ordering = ('id',)


class GroupAdminForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    users = ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        instance = super(GroupAdminForm, self).save()
        self.save_m2m()
        return instance


class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ['permissions']
    list_display = ('name',)


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Permission)
admin.site.register(User, CustomUserAdmin)
