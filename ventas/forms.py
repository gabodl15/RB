from django.forms import ModelForm
from .models import Inspection

class InspectionForm(ModelForm):
    class Meta:
        model = Inspection
        exclude = ('created', 'updated', 'inspection')
        