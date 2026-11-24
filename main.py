"""Taller 6: formularios, rutas y registros en memoria con Flask."""
from decimal import Decimal, InvalidOperation
from itertools import count
import unicodedata

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)
registros = {}
identificadores = count(1)


def leer_numero(valor, etiqueta, minimo, maximo):
    """Valida un número finito dentro del intervalo permitido."""
    try:
        numero = Decimal(valor.strip().replace(',', '.'))
    except InvalidOperation:
        raise ValueError(f'{etiqueta}: ingresa un número válido.') from None
    if not numero.is_finite() or not minimo <= numero <= maximo:
        raise ValueError(f'{etiqueta}: debe estar entre {minimo} y {maximo}.')
    return numero


def evaluar_notas(datos):
    notas = [leer_numero(datos.get(f'nota{i}', ''), f'Nota {i}', 10, 70)
             for i in range(1, 4)]
    asistencia = leer_numero(datos.get('asistencia', ''), 'Asistencia', 0, 100)
    promedio = sum(notas) / Decimal(3)
    # Se compara el valor real, antes del redondeo para mostrar el resultado.
    estado = 'APROBADO' if sum(notas) >= 120 and asistencia >= 75 else 'REPROBADO'
    return {'promedio': f'{promedio:.2f}', 'estado': estado,
            'asistencia': str(asistencia)}


def comparar_nombres(datos):
    nombres = [unicodedata.normalize('NFC', datos.get(f'nombre{i}', '').strip())
               for i in range(1, 4)]
    for nombre in nombres:
        if not nombre or len(nombre) > 100:
            raise ValueError('Completa los tres nombres con un máximo de 100 caracteres cada uno.')
        if not all(c.isalpha() or c in " -’'" for c in nombre) or not any(c.isalpha() for c in nombre):
            raise ValueError('Los nombres deben contener letras; se permiten espacios, guiones y apóstrofos.')
    if len({nombre.casefold() for nombre in nombres}) != 3:
        raise ValueError('Debes ingresar tres nombres diferentes.')
    # len cuenta los caracteres del nombre, incluidos espacios internos.
    mayor = max(nombres, key=len)
    empatados = [nombre for nombre in nombres if len(nombre) == len(mayor)]
    return {'nombre': mayor, 'cantidad': len(mayor), 'empatados': empatados}


def formulario(ejercicio, registro_id=None):
    datos, resultado, error = {}, None, None
    if registro_id is not None:
        registro = registros.get(registro_id)
        if registro is None or registro['ejercicio'] != ejercicio:
            abort(404)
        datos, resultado = registro['datos'], registro['resultado']
    if request.method == 'POST':
        datos = request.form.to_dict()
        try:
            resultado = evaluar_notas(datos) if ejercicio == 1 else comparar_nombres(datos)
        except ValueError as problema:
            error = str(problema)
        else:
            nuevo_id = next(identificadores)
            registros[nuevo_id] = {'ejercicio': ejercicio, 'datos': datos,
                                  'resultado': resultado}
            return redirect(url_for(f'ejercicio{ejercicio}', registro_id=nuevo_id, _method='GET'), code=303)
    return render_template(f'ejercicio{ejercicio}.html', datos=datos,
                           resultado=resultado, error=error)


@app.get('/')
def index():
    return render_template('index.html')


@app.route('/ejercicio1', methods=['GET', 'POST'])
@app.get('/ejercicio1/<int:registro_id>')
def ejercicio1(registro_id=None):
    return formulario(1, registro_id)


@app.route('/ejercicio2', methods=['GET', 'POST'])
@app.get('/ejercicio2/<int:registro_id>')
def ejercicio2(registro_id=None):
    return formulario(2, registro_id)


@app.get('/historial')
def historial():
    return render_template('historial.html', registros=registros)


@app.post('/historial/<int:registro_id>/eliminar')
def eliminar(registro_id):
    if registro_id not in registros:
        abort(404)
    del registros[registro_id]
    return redirect(url_for('historial'), code=303)


@app.errorhandler(404)
def no_encontrado(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
