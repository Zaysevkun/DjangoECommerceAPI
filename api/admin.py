from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from api.models import User, Product, Order, ProductsInOrder


# Redefine Django Admin for it to represent our custom user
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'role', 'mailing_address')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'full_name', 'role', 'mailing_address')
    search_fields = ('email', 'full_name', 'role')
    ordering = ('email',)


admin.site.register(Product)


class OrderInline(admin.TabularInline):
    model = ProductsInOrder
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderInline,)


admin.site.register(Order, OrderAdmin)
