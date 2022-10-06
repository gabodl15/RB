# <center>Lancelot</center>
<hr>
Lancelot es un sistema para trabajar con routers mikrotik
<br>
<br>

### INSTALACION
<hr>
<p>En el directorio donde hemos clonado el repositorio realizamos la instlacion de los paquetes de django</p>
<code>pip install -r requirements.txt</code>
<p></p>

<p>routeros_api no maneja por defecto caracteres del español, hay que indicarle que los acepte.</p>
<p>En el archivo: <code>.env/lib/python3.9/site-packages/routeros_api/api_structure.py</code> le indicaremos ("utf-8","ignore").</p>

<pre>
def get_python_value(self, bytes):
        return bytes.decode("utf-8", "ignore")
</pre>

<p>Utilizo django-fernet-fields para encriptar y desencriptar datos sencibles. Como las claves que usará la api para conectarse con los routers.</p>
<p>En django 4.0 en adelante no existe force_text, hay que cambiarlo por force_str</p>

<p>En el archivo <code>/lib/YOUR-PYTHON-VERSION/site-packages/fernet_fields/fields.py</code> la linea:</p>
<code>from django.utils.encoding import force_bytes, force_text</code>
<p>a</p>
<code>from django.utils.encoding import force_bytes, force_str</code>
<p>Y</p>
<pre>
    def from_db_value(self, value, expression, connection, *args):
        if value is not None:
            value = bytes(value)
            return self.to_python(force_text(self.fernet.decrypt(value)))
</pre>

<p>a</p>
<pre>
    def from_db_value(self, value, expression, connection, *args):
        if value is not None:
            value = bytes(value)
            return self.to_python(force_str(self.fernet.decrypt(value)))
</pre>