# Issues Directory Structure

Este directorio contiene documentación y pruebas para issues resueltos de pylink-square.

## Estructura

```
issues/
├── 151/                    # Issue #151: USB JLink selection by Serial Number
│   ├── README.md           # Documentación completa del issue y solución
│   ├── ISSUE_151_SOLUTION.md  # Análisis detallado de la solución
│   ├── TEST_RESULTS_ISSUE_151.md  # Resultados de las pruebas
│   ├── test_issue_151.py   # Tests funcionales básicos
│   ├── test_issue_151_integration.py  # Tests de integración
│   └── test_issue_151_edge_cases.py   # Tests de edge cases
└── README.md               # Este archivo
```

## Cómo Usar

Cada issue tiene su propio directorio con:
- **README.md**: Documentación completa del problema, solución, y cómo usar
- **Archivos de prueba**: Scripts de Python que validan la solución
- **Documentación adicional**: Análisis detallado si es necesario

### Ejecutar Tests de un Issue

```bash
cd issues/151
python3 test_issue_151.py
python3 test_issue_151_integration.py
python3 test_issue_151_edge_cases.py
```

## Issues Resueltos

### Issue #151 - USB JLink selection by Serial Number ✅

**Estado**: Resuelto  
**Fecha**: 2025-01-XX  
**Archivos modificados**: `pylink/jlink.py`  
**Tests**: 28/28 pasando

**Resumen**: El `serial_no` pasado a `JLink.__init__()` ahora se usa automáticamente cuando `open()` se llama sin parámetros.

Ver detalles completos en [issues/151/README.md](151/README.md)

---

## Convenciones

- Cada issue tiene su propio directorio numerado (ej: `151/`)
- El README.md del issue contiene toda la información relevante
- Los tests deben poder ejecutarse independientemente desde el directorio del issue
- Todos los archivos relacionados con un issue están en su directorio

