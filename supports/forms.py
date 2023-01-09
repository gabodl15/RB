from django.forms import ModelForm
from .models import FeasibleOrNotFeasible

class FeasibleOrNotFeasibleForm(ModelForm):
    class Meta:
        model = FeasibleOrNotFeasible
        fields = '__all__'