from django.contrib import admin

from foods_container.models import Container

class ContainerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Container, ContainerAdmin)
