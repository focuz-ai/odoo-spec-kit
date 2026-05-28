---
name: odoo-test-runner
description:
  Use esta skill cuando necesite ejecutar la suite de pruebas unitarias o de integración en Odoo, filtrando por módulo o
  etiqueta y extrayendo resultados detallados.
author: Focuz.io
version: 1.0.0
---

# Skill: Ejecución de Tests Odoo (/odoo-test-runner)

Esta skill proporciona los comandos y metodologías para lanzar y diagnosticar pruebas de Odoo.

---

## 1. Identificación del Entorno y Parámetros

Antes de ejecutar, el agente debe verificar:

- La ruta del ejecutable `odoo-bin` y el archivo de configuración `odoo.conf` (definidos en
  `docs/development-guide.md`).
- El nombre de la base de datos de pruebas (ej. `db_test`).
- El alcance de la prueba: ¿Todo el módulo, una clase específica, o un tour de interfaz?

---

## 2. Ejecución de Pruebas de Backend (Python)

Formular el comando utilizando los flags oficiales de Odoo:

- `--test-enable`: Habilita la carga y ejecución de tests.
- `--stop-after-init`: Detiene el servidor Odoo una vez finalizado el ciclo de pruebas (ideal para CI/CD y
  automatizaciones).
- `-i` / `-u`: Instala o actualiza el módulo antes de probar.
- `--test-tags`: Filtra la ejecución de los tests.

### Comandos de Ejemplo:

```bash
# Correr todos los tests de un módulo
python odoo-bin -c odoo.conf -d db_test --test-enable --stop-after-init -i mi_modulo

# Correr un método específico de una clase de pruebas
python odoo-bin -c odoo.conf -d db_test --test-enable --stop-after-init --test-tags /mi_modulo:MiClaseTest.test_metodo_calculo
```

---

## 3. Ejecución de Pruebas de Frontend (QUnit / Tours)

Para los tests interactivos de tours frontend en Python:

```bash
# Correr el test de caso HTTP (tours del navegador Chrome Headless)
python odoo-bin -c odoo.conf -d db_test --test-enable --stop-after-init --test-tags /mi_modulo:HttpCase
```

---

## 4. Interpretación de la Salida y Tracebacks

- **Éxito**: La consola finaliza con un log de cierre normal indicando que los módulos de test pasaron sin errores.
- **Fallo**: Odoo imprime un Traceback en Python indicando el tipo de error (`AssertionError`, `ValidationError`, etc.).
- **Acción del Agente**:
  - Extraer la sección del traceback correspondiente a los archivos de nuestro módulo, omitiendo llamadas del core de
    Odoo.
  - Pasar este traceback limpio al bucle de autoreparación de `/odoo-adversarial-review`.
