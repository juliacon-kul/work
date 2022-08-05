from django.contrib import admin
from app.models import Element

# Register your models here.
@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug':('company_name',)}
    pass

# @admin.register(Child)
# class DataAdmin(admin.ModelAdmin):
#     pass






