import floppyforms as forms

from questions.models import Question


class QuestionForm(forms.Form):
    key = forms.CharField(widget=forms.HiddenInput)


class MultiPolygonWidget(forms.gis.MultiPolygonWidget,
                         forms.gis.BaseOsmWidget):
    template_name = 'questions/widget.html'


class PreviousForm(forms.Form):
    previous = forms.gis.MultiPolygonField(widget=MultiPolygonWidget(
        attrs={'map_width': 400, 'map_height': 400},
    ))
