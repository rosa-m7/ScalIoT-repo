import sys
import os
import pytest

# Ajuste de path para importar el módulo de funciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../controllers')))
from funciones_home import (
    lista_ninosBD, guardar_ninoBD, actualizar_ninoBD, eliminar_ninoBD,
    buscar_ninoBD, obtener_nino_por_idBD,
    lista_condicionesBD, buscar_condicionBD, obtener_condicion_por_idBD,
    lista_nino_condicionesBD, insertar_nino_condicionBD, eliminar_nino_condicionBD, obtener_nino_condicionBD
)

def test_lista_ninosBD():
    ninos = lista_ninosBD()
    assert isinstance(ninos, list)
    if ninos:
        n = ninos[0]
        assert 'id_nino' in n
        assert 'nombre' in n
        assert 'apellido' in n
        assert 'codigo_nino' in n

def test_buscar_y_obtener_nino():
    ninos = lista_ninosBD()
    if ninos:
        nino = ninos[0]
        res = buscar_ninoBD(nino['nombre'])
        assert isinstance(res, list)
        por_id = obtener_nino_por_idBD(nino['id_nino'])
        assert por_id is not None
        assert por_id['id_nino'] == nino['id_nino']

def test_lista_condicionesBD():
    condiciones = lista_condicionesBD()
    assert isinstance(condiciones, list)
    if condiciones:
        c = condiciones[0]
        assert 'id_condicion' in c
        assert 'nombre_condicion' in c
        assert 'descripcion' in c

def test_buscar_y_obtener_condicion():
    condiciones = lista_condicionesBD()
    if condiciones:
        cond = condiciones[0]
        res = buscar_condicionBD(cond['nombre_condicion'])
        assert isinstance(res, list)
        por_id = obtener_condicion_por_idBD(cond['id_condicion'])
        assert por_id is not None
        assert por_id['id_condicion'] == cond['id_condicion']

def test_lista_nino_condicionesBD():
    # Esta prueba solo valida que la función retorna una lista
    resultado = lista_nino_condicionesBD() if callable(lista_nino_condicionesBD) else []
    assert isinstance(resultado, list)
    # Si hay datos, validar claves mínimas
    if resultado:
        rc = resultado[0]
        assert 'id_nino_condicion' in rc
        assert 'id_nino' in rc or 'nombre_nino' in rc
        assert 'id_condicion' in rc or 'nombre_condicion' in rc

def test_insertar_y_eliminar_nino_condicion():
    ninos = lista_ninosBD()
    condiciones = lista_condicionesBD()
    if ninos and condiciones:
        id_nino = ninos[0]['id_nino']
        id_condicion = condiciones[0]['id_condicion']
        # Insertar relación
        rowcount = insertar_nino_condicionBD(id_nino, id_condicion)
        assert rowcount == 1
        # Buscar la relación recién creada
        relaciones = lista_nino_condicionesBD(id_nino)
        assert any(r['id_condicion'] == id_condicion for r in relaciones)
        # Eliminar la relación
        id_nino_condicion = [r['id_nino_condicion'] for r in relaciones if r['id_condicion'] == id_condicion][0]
        eliminado = eliminar_nino_condicionBD(id_nino_condicion)
        assert eliminado == 1

def test_obtener_nino_condicionBD():
    ninos = lista_ninosBD()
    if ninos:
        relaciones = lista_nino_condicionesBD(ninos[0]['id_nino'])
        if relaciones:
            id_nino_condicion = relaciones[0]['id_nino_condicion']
            relacion = obtener_nino_condicionBD(id_nino_condicion)
            assert relacion is not None
            assert 'id_nino_condicion' in relacion
            assert 'id_nino' in relacion
            assert 'id_condicion' in relacion
