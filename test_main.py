"""Pruebas funcionales del taller con el cliente de Flask."""
import unittest
from main import app, registros


class AplicacionTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        registros.clear()
        self.cliente = app.test_client()

    def notas(self, n1='40', n2='40', n3='40', asistencia='75'):
        return self.cliente.post('/ejercicio1', data={
            'nota1': n1, 'nota2': n2, 'nota3': n3,
            'asistencia': asistencia}, follow_redirects=True)

    def nombres(self, a='Felipe', b='Juan', c='Gustavo'):
        return self.cliente.post('/ejercicio2', data={
            'nombre1': a, 'nombre2': b, 'nombre3': c}, follow_redirects=True)

    def test_paginas_y_css(self):
        for ruta in ['/', '/ejercicio1', '/ejercicio2', '/historial', '/static/estilos.css']:
            with self.subTest(ruta=ruta):
                with self.cliente.get(ruta) as respuesta:
                    self.assertEqual(respuesta.status_code, 200)

    def test_ejemplo_notas(self):
        respuesta = self.notas('55', '65', '45', '86')
        self.assertIn(b'55.00', respuesta.data)
        self.assertIn(b'<strong>APROBADO</strong>', respuesta.data)

    def test_limite_aprobacion(self):
        self.assertIn(b'<strong>APROBADO</strong>', self.notas().data)

    def test_asistencia_insuficiente(self):
        self.assertIn(b'REPROBADO', self.notas('70', '70', '70', '74.99').data)

    def test_promedio_insuficiente_sin_redondear(self):
        self.assertIn(b'REPROBADO', self.notas('39.999', '40', '40').data)

    def test_notas_invalidas(self):
        for invalido in ['9', '71', '', 'hola', 'NaN', 'Infinity']:
            with self.subTest(valor=invalido):
                registros.clear()
                respuesta = self.notas(invalido)
                self.assertIn(b'role="alert"', respuesta.data)
                self.assertFalse(registros)

    def test_asistencia_invalida(self):
        for valor in ['-1', '101']:
            self.assertIn(b'role="alert"', self.notas(asistencia=valor).data)

    def test_extremos_validos(self):
        self.assertIn(b'REPROBADO', self.notas('10', '10', '10', '0').data)
        self.assertIn(b'<strong>APROBADO</strong>', self.notas('70', '70', '70', '100').data)

    def test_ejemplo_nombres(self):
        respuesta = self.nombres()
        self.assertIn(b'caracteres es: Gustavo', respuesta.data)
        self.assertIn(b'7 caracteres', respuesta.data)

    def test_nombres_vacios_repetidos_y_no_validos(self):
        for datos in [('', 'Ana', 'Juan'), ('Ana', 'ana', 'Juan'), ('123', 'Ana', 'Juan')]:
            self.assertIn(b'role="alert"', self.nombres(*datos).data)

    def test_empate_y_tildes(self):
        respuesta = self.nombres('Jose\u0301', 'Luis', 'Ana').get_data(as_text=True)
        self.assertIn('caracteres es: José', respuesta)
        self.assertIn('4 caracteres', respuesta)
        self.assertIn('Empate entre José, Luis', respuesta)

    def test_redireccion_consulta_y_eliminacion(self):
        respuesta = self.cliente.post('/ejercicio2', data={
            'nombre1': 'Felipe', 'nombre2': 'Juan', 'nombre3': 'Gustavo'})
        self.assertEqual(respuesta.status_code, 303)
        self.assertEqual(len(registros), 1)
        self.cliente.get(respuesta.location)
        self.cliente.get(respuesta.location)
        self.assertEqual(len(registros), 1)
        identificador = next(iter(registros))
        self.assertEqual(self.cliente.get(f'/ejercicio1/{identificador}').status_code, 404)
        self.assertIn(b'Registro', self.cliente.get('/historial').data)
        self.assertEqual(self.cliente.post(f'/historial/{identificador}/eliminar').status_code, 303)
        self.assertFalse(registros)
        self.assertEqual(self.cliente.get(respuesta.location).status_code, 404)

    def test_rutas_invalidas(self):
        self.assertEqual(self.cliente.get('/ejercicio1/99999').status_code, 404)
        self.assertEqual(self.cliente.get('/inexistente').status_code, 404)
        self.assertEqual(self.cliente.get('/historial/1/eliminar').status_code, 405)


if __name__ == '__main__':
    unittest.main()
