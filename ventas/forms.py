from django.forms import ModelForm, Select
from .models import Inspection, Installation, InstallationFee

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

class UpdateInstallationForm(ModelForm):
    class Meta:
        model = Installation
        exclude = ('inspection','material', 'payment')

class InstallationFeeForm(ModelForm):
    class Meta:
        model = InstallationFee
        fields = ['installation', 'installation_fee', 'currency']