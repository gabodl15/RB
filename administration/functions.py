from pypdf import PdfReader, PdfWriter
import io, os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
from datetime import datetime, date

class Pdf:

    def __init__(self, obj, client):
        self.client = client
        self.last_name = self.client.last_name if self.client.last_name is not None else ''
        self.obj = obj

    def solvency(self, _from, _to, _code):
        self.packet = io.BytesIO()
        self.can = canvas.Canvas(self.packet, pagesize=letter)
        self.today = date.today()
        created = self.obj.created
        self.media = settings.MEDIA_ROOT
        base = '/formatos/SOLVENCIA.pdf'

        # FECHA CUANDO SE IMPRIME
        self.can.drawString(423, 730, f"{self.today}")
        
        # NOMBRE Y APELLIDO
        self.can.drawString(185, 710, f"{self.client} {self.last_name}")

        # MES A PAGAR
        self.can.drawString(244, 653, f"{_from}")

        # SOLVENTE
        self.can.drawString(330, 608, "SOLVENTE")

        # MES A PAGAR
        self.can.drawString(185, 560, f"{_to}")

        # CODIGO
        self.can.drawString(405, 542, f"{_code}")

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
        new_dir = self.media + f"/clients/{self.client}-{self.client.id}/administration/"
        if not os.path.exists(new_dir):
            try:
                os.makedirs(new_dir)
            except:
                return 'No Se puede crear el archivo'
        destination = new_dir + f"SOLVENCIA-{self.obj.id}-{self.obj.created}.pdf"
        output_stream = open(destination, "wb")
        output.write(output_stream)
        output_stream.close()
        
    def print_solvency(self):
        sheet = f'clients/{self.client}-{self.client.id}/administration/SOLVENCIA-{self.obj.id}-{self.created}.pdf'
        return sheet
        