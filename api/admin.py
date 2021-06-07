from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class AccountAdmin(UserAdmin):
	list_display = ('email','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('email',)
	readonly_fields=('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	ordering = ('email',)


admin.site.register(Account, AccountAdmin)
admin.site.register(ChangePassword)