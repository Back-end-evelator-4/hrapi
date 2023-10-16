from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserCompany, Candidate, UserExperience
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'email', 'first_name', 'last_name', 'type', 'is_superuser', 'is_staff', 'is_active', 'created_date')
    readonly_fields = ('last_login', 'modified_date', 'created_date')
    list_filter = ('created_date', 'type', 'is_superuser', 'is_staff', 'is_active')
    date_hierarchy = 'created_date'
    ordering = ('-id', )
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'bio', 'avatar')}),
        (_('Permissions'), {'fields': ('type', 'is_superuser', 'is_staff', 'is_active',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'modified_date', 'created_date')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2'), }),
    )
    search_fields = ('email', 'first_name', 'last_name')


@admin.register(UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company')
    search_fields = ('user__email', 'company__name')


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category')
    search_fields = ('user__email', 'category__name')
    filter_horizontal = ('skills', )


@admin.register(UserExperience)
class UserExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company', 'category', 'start_date', 'end_date', 'is_now_work', 'modified_date', 'created_date')
    search_fields = ('user__email', 'company__name', 'category__name')
    list_filter = ('is_now_work', 'category')
    date_hierarchy = 'created_date'


admin.site.register(User, UserAdmin)
