from django.forms import ModelForm, Select
from .models import Inspection

class InspectionForm(ModelForm):
    class Meta:
        model = Inspection
        exclude = ('created', 'updated', 'inspection')

class UpdateInspectionForm(ModelForm):
    class Meta:
        model = Inspection
        fields = ['client', 'inspection', 'comment']
        widgets = {
            'inspection': Select(attrs={'onchange':'checkValue(this.value)'})
        }