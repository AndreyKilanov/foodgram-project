from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', )
    list_filter = ('id', 'email', 'username',)
    list_editable = ('email', 'username', 'first_name', 'last_name', )
    list_max_show_all = 15
    empty_value_display = '-пусто-'
