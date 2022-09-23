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
