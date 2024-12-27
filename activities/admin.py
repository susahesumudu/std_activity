from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Activity, GradingRubric

@admin.register(GradingRubric)
class GradingRubricAdmin(admin.ModelAdmin):
    list_display = ['criteria', 'weight']


admin.site.register(Activity)