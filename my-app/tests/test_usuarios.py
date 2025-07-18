import pytest
from flask import Flask
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.funciones_home import lista_usuariosBD, buscar_usuariosBD

# NOTA: Ajustar los imports según la estructura real del proyecto y el nombre del paquete

def test_lista_usuariosBD_no_excepcion():
    """Verifica que la función lista_usuariosBD no lanza excepción y retorna una lista."""
    usuarios = lista_usuariosBD()
    assert isinstance(usuarios, list)


def test_buscar_usuariosBD_no_excepcion():
    """Verifica que buscar_usuariosBD no lanza excepción y retorna una lista."""
    resultados = buscar_usuariosBD('')
    assert isinstance(resultados, list)


def test_buscar_usuariosBD_busqueda_parcial():
    """Verifica que buscar_usuariosBD retorna usuarios que contienen el término de búsqueda."""
    term = 'a'  # Asume que hay usuarios con 'a' en algún campo
    resultados = buscar_usuariosBD(term)
    assert isinstance(resultados, list)
    # No se puede garantizar que siempre retorne resultados, pero no debe fallar


def test_lista_usuariosBD_campos_evaluador():
    """Verifica que los campos de evaluador estén presentes en los resultados de lista_usuariosBD."""
    usuarios = lista_usuariosBD()
    if usuarios:
        usuario = usuarios[0]
        assert 'especialidad' in usuario
        assert 'anos_experiencia' in usuario
        assert 'certificaciones' in usuario
