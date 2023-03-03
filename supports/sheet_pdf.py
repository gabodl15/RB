from .models import WirelessInstallationSheet, WirelessInspectionSheet, WirelessSupportSheet
from .models import FiberInspectionSheet, FiberInstallationSheet, FiberSupportSheet
from .models import Support
from pypdf import PdfReader, PdfWriter
import io, os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
from datetime import datetime, date

class Pdf:

    def __init__(self, obj, client, support):
        self.client = client
        self.last_name = self.client.last_name if self.client.last_name is not None else ''
        self.obj = obj
        self.support = support

    def print_sheet(self):
        pass

    def _type_(self):
        if self.support == 'installations':
            _type = self.obj.inspect.inspect.inspection_type
        if self.support == 'inspections':
            _type = self.obj.inspect.inspection_type
        return _type

    def _check_for_existing_sheet(self, _sheet):
        return True if hasattr(self.obj, _sheet) else False

    def create_sheet(self):
        self.packet = io.BytesIO()
        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        self.can = canvas.Canvas(self.packet, pagesize=letter)
        self.today = date.today()
        self.media = settings.MEDIA_ROOT
        
        if self.support == 'installations':
            _type = self._type_()
            if _type == 'WA':
                check = self._check_for_existing_sheet('wirelessinstallationsheet')
                if check:
                    return self.obj.wirelessinstallationsheet.sheet
                
                record = WirelessInstallationSheet.objects.last()
                self.order = (record.order + 1) if record is not None else 1
                destination_sheet = f'clients/{self.client}-{self.client.id}/{self.support}/{self.order}.pdf'
                wis = WirelessInstallationSheet(
                    client = self.client,
                    installation = self.obj,
                    sheet = destination_sheet,
                    order = self.order
                )
                wis.save()
                base = self.wireless_installation()

            else:
                check = self._check_for_existing_sheet('fiberinstallationsheet')
                if check:
                    return self.obj.fiberinstallationsheet.sheet

                record = FiberInstallationSheet.objects.last()
                self.order = (record.order + 1) if record is not None else 1
                destination_sheet = f'clients/{self.client}-{self.client.id}/{self.support}/{self.order}.pdf'
                fis = FiberInstallationSheet(
                    client = self.client,
                    installation= self.obj,
                    sheet = destination_sheet,
                    order = self.order
                )
                fis.save()
                base = self.fiber_optic_intallation()

        if self.support == 'inspections':
            _type = self._type_()
            if _type == 'WA':
                check = self._check_for_existing_sheet('wirelessinspectionsheet')
                if check:
                    return self.obj.wirelessinspectionsheet.sheet
                
                record = WirelessInspectionSheet.objects.last()
                self.order = (record.order + 1) if record is not None else 1
                destination_sheet = f'clients/{self.client}-{self.client.id}/{self.support}/{self.order}.pdf'
                wis = WirelessInspectionSheet(
                    client = self.client,
                    inspection = self.obj,
                    sheet = destination_sheet,
                    order = self.order
                )
                wis.save()
                base = self.wireless_inspection()

            else:
                check = self._check_for_existing_sheet('fiberinspectionsheet')
                if check:
                    return self.obj.fiberinspectionsheet.sheet

                record = FiberInspectionSheet.objects.last()
                self.order = (record.order + 1) if record is not None else 1
                destination_sheet = f'clients/{self.client}-{self.client.id}/{self.support}/{self.order}.pdf'
                fis = FiberInspectionSheet(
                    client = self.client,
                    inspection= self.obj,
                    sheet = destination_sheet,
                    order = self.order
                )
                fis.save()
                base = self.fiber_optic_inspection()

        if self.support == 'support':
            
            check = self._check_for_existing_sheet('wirelesssupportsheet')
            if check:
                return self.obj.wirelesssupportsheet.sheet
            
            record = Support.objects.last()
            self.order = (record.order + 1) if record is not None else 1
            destination_sheet = f'clients/{self.client}-{self.client.id}/{self.support}/{self.order}.pdf'
            
            wss = WirelessSupportSheet(
                client = self.client,
                support = self.obj.profile,
                sheet = destination_sheet,
                order = self.order
            )
            wss.save()
            
            base = self.wireless_support()


    
        # SETIAMOS EL TIPO DE INSTALACION
        
        # GUARDAR LOS CAMBIOS
        self.can.save()

        #move to the beginning of the StringIO buffer
        self.packet.seek(0)

        # create a new PDF with Reportlab
        new_pdf = PdfReader(self.packet)
        _base = self.media + base
        # read your existing PDF
        existing_pdf = PdfReader(open(_base, "rb"))
        output = PdfWriter()
        
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)

        # finally, write "output" to a real file
        new_dir = self.media + f"/clients/{self.client}-{self.client.id}/{self.support}/"
        if not os.path.exists(new_dir):
            try:
                os.makedirs(new_dir)
            except:
                return 'No Se puede crear el archivo'
        destination = new_dir + f"{self.order}.pdf"
        output_stream = open(destination, "wb")
        output.write(output_stream)
        output_stream.close()
        
        sheet = f'clients/{self.client}-{self.client.id}/{self.support}/{self.order}.pdf'
        return sheet

    """ LA EDICION DE CADA HOJA, POR SEPARADO."""

    def fiber_optic_inspection(self):
        base = '/formatos/INSPECCION_FIBRA_OPTICA.pdf'
        # COLOCANDO NUMERO DE CONTROL
        self.control_number = str(self.order).rjust(5, '0')
        self.can.drawString(526, 776, f"{self.control_number}")

        # FECHA CUANDO SE IMPRIME
        self.can.drawString(500, 745, f"{self.today}")

        # NOMBRE Y APRELLIDO
        self.can.drawString(109, 609, f"{self.client} {self.last_name}")

        # DOCUMENTO
        self.can.drawString(341, 609, f"{self.client.dni}")

        # TELEFONO
        self.can.setFont('Vera', 10)
        self.can.drawString(415, 609, f"{self.client.phone}")

        # DIRECCION
        self.can.drawString(70, 592, f"{self.obj.inspect.address}"  )

        # RETORNAMOS        
        return base

    def fiber_optic_intallation(self):
        base = '/formatos/ORDEN_DE_SERVICIO_FIBRA_OPTICA.pdf'

        # COLOCANDO NUMERO DE CONTROL
        self.control_number = str(self.order).rjust(5, '0')
        self.can.drawString(526, 766, f"{self.control_number}")

        # FECHA CUANDO SE IMPRIME
        self.can.drawString(500, 722, f"{self.today}")

        # NOMBRE Y APRELLIDO
        self.can.drawString(115, 639, f"{self.client} {self.last_name}")

        # TELEFONO
        self.can.setFont('Vera', 10)
        self.can.drawString(473, 639.5, f"{self.client.phone}")

        # DOCUMENTO
        self.can.drawString(378, 639.5, f"{self.client.dni}")

        # DIRECCION
        self.can.drawString(70, 614, f"{self.obj.inspect.inspect.address}"  )

        # RETORNAMOS        
        return base

    def wireless_inspection(self):
        base = '/formatos/INSPECCION_INALAMBRICO.pdf'

        # COLOCANDO NUMERO DE CONTROL
        self.control_number = str(self.order).rjust(5, '0')
        self.can.drawString(526, 776, f"{self.control_number}")

        # FECHA CUANDO SE IMPRIME
        self.can.drawString(500, 745, f"{self.today}")

        # NOMBRE Y APRELLIDO
        self.can.drawString(109, 609, f"{self.client} {self.last_name}")

        # DOCUMENTO
        self.can.drawString(345, 609, f"{self.client.dni}")

        # TELEFONO
        self.can.setFont('Vera', 10)
        self.can.drawString(465, 609, f"{self.client.phone}")

        # DIRECCION
        self.can.drawString(70, 585, f"{self.obj.inspect.address}"  )

        # RETORNAMOS        
        return base

    def wireless_installation(self):
        base = '/formatos/ORDEN_DE_SERVICIO_INALAMBRICO.pdf'

        # COLOCANDO NUMERO DE CONTROL
        self.control_number = str(self.order).rjust(5, '0')
        self.can.drawString(526, 766, f"{self.control_number}")

        # FECHA CUANDO SE IMPRIME
        self.can.drawString(500, 722, f"{self.today}")

        # MARCANDO CASILLA DE FIBRA
        self.can.drawString(465, 674, 'XXX')

        # NOMBRE Y APRELLIDO
        self.can.drawString(115, 639, f"{self.client} {self.last_name}")

        # TELEFONO
        self.can.setFont('Vera', 10)
        self.can.drawString(473, 639.5, f"{self.client.phone}")

        # DOCUMENTO
        self.can.drawString(378, 639.5, f"{self.client.dni}")

        # DIRECCION
        self.can.drawString(70, 614, f"{self.obj.inspect.inspect.address}")

        # RETORNAMOS
        return base

    def fiber_optic_support(self):
        base = '/formatos/VISITA_TECNICA.pdf'
        
         # COLOCANDO NUMERO DE CONTROL
        self.control_number = str(self.order).rjust(5, '0')
        self.can.drawString(526, 779, f"{self.control_number}")

        # FECHA CUANDO SE IMPRIME
        self.can.drawString(500, 748, f"{self.today}")

        # MARCANDO CASILLA DE FIBRA
        self.can.drawString(462, 687, 'XXX')

        # NOMBRE Y APRELLIDO
        self.can.drawString(110, 653, f"{self.client} {self.last_name}")

        # TELEFONO
        self.can.setFont('Vera', 10)
        self.can.drawString(473, 653, f"{self.client.phone}")

        # DOCUMENTO
        self.can.drawString(370, 653, f"{self.client.dni}")

        # DIRECCION
        self.can.drawString(68, 630, f"{self.obj.client.address}")

        return base

    def wireless_support(self):
        base = '/formatos/VISITA_TECNICA.pdf'

        # COLOCANDO NUMERO DE CONTROL
        self.control_number = str(self.order).rjust(5, '0')
        self.can.drawString(526, 779, f"{self.control_number}")

        # FECHA CUANDO SE IMPRIME
        self.can.drawString(500, 748, f"{self.today}")

        # MARCANDO CASILLA DE FIBRA
        self.can.drawString(462, 687, 'XXX')

        # NOMBRE Y APRELLIDO
        self.can.drawString(110, 653, f"{self.client} {self.last_name}")

        # TELEFONO
        self.can.setFont('Vera', 10)
        self.can.drawString(473, 653, f"{self.client.phone}")

        # DOCUMENTO
        self.can.drawString(370, 653, f"{self.client.dni}")

        # DIRECCION
        self.can.drawString(68, 630, f"{self.obj.client.address}")

        return base