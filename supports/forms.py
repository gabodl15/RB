from django.forms import ModelForm, Select
from .models import FeasibleOrNotFeasible, Material

class FeasibleOrNotFeasibleForm(ModelForm):
    class Meta:
        model = FeasibleOrNotFeasible
        fields = '__all__'

class MaterialFiberForm(ModelForm):
    class Meta:
        model = Material
        exclude = ['pipe', 'wire', 'base', 'anchor', 'welding']
        labels = {
            'cabling': 'Cantidad de Cable',
            'intallation_location': 'Lugar de Instalación',
            'tensors': 'Tensores',
            'cable_routin': 'Ruta del cableado',
            'support_post': 'Poste de Sujeción',
            'nap_code': 'Codigo Nap',
            'comment': 'comentario'
        }
        
class MaterialWirelessForm(ModelForm):
    class Meta:
        model = Material
        exclude = ['tensors', 'support_post', 'nap_code',]
        labels = {
            'pipe': 'Metros de Tubo',
            'wire': 'Vientos',
            'base': 'Base (Piso o Pared)',
            'anchor': 'Anclajes',
            'welding': 'Trabajo de Soldadura',
            'cabling': 'Cantidad de Cable',
            'intallation_location': 'Lugar de Instalación',
            'cable_routin': 'Ruta del cableado',
            'comment': 'comentario'
        }