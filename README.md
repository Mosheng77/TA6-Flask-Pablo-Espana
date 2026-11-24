# Taller 6 Aplicación Flask

Autor: Pablo España Ramírez.

Aplicación individual para calcular el promedio y la aprobación de un estudiante,
y comparar la longitud de tres nombres. La interfaz reproduce los controles,
orden, botones azules y tarjetas de los ejemplos de TA_6.

## Inicio rápido en Windows

Instala Python 3, descomprime el proyecto y ejecuta INICIAR_WINDOWS.bat.
Abre http://127.0.0.1:5000. Para detenerlo, presiona Ctrl+C en la consola.
La primera ejecución requiere Internet para descargar Flask.

También puedes usar una terminal dentro de la carpeta:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

En Linux o macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

`pip` es el gestor de dependencias de Python; instala las bibliotecas declaradas
en requirements.txt. Flask es el framework que recibe las peticiones HTTP,
ejecuta las funciones Python y renderiza las plantillas HTML.
El entorno virtual aísla las dependencias del proyecto.

## Funcionamiento

1. El menú contiene dos botones, uno por ejercicio.
2. Ejercicio 1 recibe tres notas de 10 a 70 y asistencia de 0 a 100.
   Calcula (nota1 + nota2 + nota3) / 3. Se aprueba únicamente si el promedio
   real es al menos 40 Y la asistencia es al menos 75 %. El resultado se
   muestra con dos decimales; el redondeo no cambia la decisión.
3. Ejercicio 2 recibe tres nombres diferentes, muestra el de mayor longitud
   y su cantidad de caracteres. Se eliminan espacios externos y se normalizan
   tildes Unicode. Los espacios internos, guiones y apóstrofos cuentan como
   caracteres. En empate se muestra el primero y se informa cuáles empataron.
4. Historial permite consultar y eliminar registros mediante formularios.
   Es la cuarta página funcional para cubrir el indicador de cuatro páginas.
   No utiliza base de datos: al detener o reiniciar se pierde el historial.

Los datos se validan en HTML y nuevamente en Python. Los errores conservan los
campos ingresados. Las plantillas escapan el contenido antes de mostrarlo.

## Estructura y correspondencia con la pauta

- main.py: variables, funciones, validaciones, rutas GET/POST y diccionario en memoria.
- templates/base.html: plantilla base con bloques y carga del CSS.
- templates/index.html: menú de dos botones.
- templates/ejercicio1.html: formulario de notas y resultado.
- templates/ejercicio2.html: formulario de nombres y resultado.
- templates/historial.html: cuarta página funcional y eliminación de registros.
- templates/error.html: respuesta 404 personalizada.
- static/estilos.css: estilos compartidos.
- test_main.py: pruebas de resultados, límites, rutas y validaciones.

Rutas sin parámetros: /, /ejercicio1, /ejercicio2, /historial.
Los ejercicios aceptan GET para mostrar y POST para recibir datos.
Rutas con parámetros: /ejercicio1/<int:registro_id> y
/ejercicio2/<int:registro_id> consultan resultados por GET.
POST /historial/<int:registro_id>/eliminar elimina un registro.
Después de un POST válido se redirige con HTTP 303; actualizar el navegador
no vuelve a enviar el formulario. Un identificador inexistente o incorrecto
produce abort(404) y una página de error.

## Pruebas

```powershell
.venv\Scripts\python.exe -m unittest -v
```

## Publicar en GitHub y entregar

Este paquete NO contiene un enlace publicado. Ese paso requiere tu cuenta.
Crea en GitHub un repositorio vacío llamado TA6-Flask-Pablo-Espana.
En una terminal dentro de esta carpeta ejecuta, sustituyendo TU_USUARIO:

```bash
git init
git add .
git commit -m "Entrega taller 6 aplicacion Flask"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TA6-Flask-Pablo-Espana.git
git push -u origin main
```

Si Git solicita identidad, configura tu nombre y correo propios antes del commit.
Comprueba en GitHub que se ven main.py, templates y static y que el docente
puede acceder. Reemplaza ENLACE_GITHUB.txt por la URL real del repositorio.
Vuelve a comprimir la carpeta sin .venv, __pycache__ ni .git.
Entrega en Blackboard el ZIP del proyecto y ENLACE_GITHUB.txt por separado.
El enunciado advierte que un enlace sin el proyecto comprimido no es suficiente.

## Referencia

Documentación oficial de Flask: https://flask.palletsprojects.com/en/stable/quickstart/
