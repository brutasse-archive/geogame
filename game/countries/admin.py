import floppyforms as forms

from django.contrib import admin

from countries.models import Country


class MultiPolygonWidget(forms.gis.MultiPolygonWidget,
                         forms.gis.BaseOsmWidget):
    pass


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        widgets = {
            'mpoly': MultiPolygonWidget,
        }


class CountryAdmin(admin.ModelAdmin):
    form = CountryForm
    list_display = ['name', 'region', 'subregion']
    list_filter = ['region', 'subregion']
    search_fields = ['name']


admin.site.register(Country, CountryAdmin)
