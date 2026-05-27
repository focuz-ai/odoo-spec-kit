---
description: Define los pasos obligatorios y las reglas de ejecución del workflow OpenSpec adaptado para Odoo 17.0 (enrich-us, propose, apply, verify, code-review, archive, commit-odoo).
alwaysApply: true
---

# Pasos Obligatorios de Tareas en OpenSpec para Odoo (OpenSpec Tasks)

Al crear o actualizar el archivo de tareas (`task.md` o `tasks.md`) para cualquier cambio en el proyecto utilizando OpenSpec, el agente de IA **DEBE** seguir y estructurar las tareas de acuerdo con las siguientes directrices y secuencia obligatoria.

---

## 1. Secuencia de Ciclo de Vida de Tareas

Toda implementación técnica debe organizarse en base al siguiente flujo lógico secuencial:

```
Paso 0: Setup de Rama ➔ Fase de Codificación ➔ Paso N: Pruebas (/verify) ➔ Paso N+1: Auditoría (/code-review) ➔ Paso N+2: Documentación ➔ Paso N+3: Commit (/commit-odoo)
```

---

## 2. Definición Detallada de Pasos Obligatorios

Todas las tareas de desarrollo deben incluir estos pasos exactamente en el orden indicado:

### Paso 0: Creación de Rama de Característica (MANDATORIO - PRIMER PASO)
- **Acción**: Antes de realizar cualquier edición en los archivos del código fuente, el agente debe crear y cambiarse a una rama git dedicada.
- **Nomenclatura**: `feature/[id-ticket]` o `feature/[nombre-cambio]`.

### Paso N: Ejecución de Pruebas de Odoo (`verify`) (MANDATORIO)
- **Acción**: Ejecución del conjunto de pruebas backend (`TransactionCase`/`HttpCase`) o frontend (`QUnit`) mediante el comando oficial de pruebas de Odoo.
- **Comando de ejemplo**: `python odoo-bin -c odoo.conf -d bd_pruebas --test-enable --stop-after-init -i nombre_modulo`.
- **Responsabilidad de la IA**: El agente de IA **debe ejecutar el comando directamente en la consola** utilizando la herramienta `run_command`. Está prohibido delegar la ejecución de las pruebas al usuario.
- **Reporte de Verificación**: El agente debe documentar los resultados (pruebas pasadas, fallidas, tiempos) en un reporte guardado en la carpeta de especificaciones del cambio.

### Paso N+1: Revisión de Código y Cruce de Seguridad (`code-review`) (MANDATORIO)
- **Acción**: Ejecutar una revisión adversarial y una auditoría estática de seguridad antes de marcar la tarea como lista para integrar.
- **Cruce de Permisos Estático**: Validar que todos los modelos Python (`models.Model` y `TransientModel`) tengan sus accesos declarados en `security/ir.model.access.csv`.
- **Bucle de Autoreparación**: Si las pruebas en el paso anterior (`/verify`) o la auditoría estática detectan fallos, el agente debe activar un bucle de autoreparación autónomo de hasta 3 intentos para resolver los fallos de código y re-validar de forma automática.

### Paso N+2: Actualizar Documentación Técnica (MANDATORIO)
- **Acción**: Actualizar los archivos de documentación correspondientes en `docs/` (como `data-model.md` ante cambios de base de datos o `api-spec.md` para nuevos endpoints).

### Paso N+3: Creación de Commit Odoo-Style (`commit-odoo`) (MANDATORIO)
- **Acción**: Realizar el commit git siguiendo el formato oficial de Odoo descrito en `docs/git-guidelines.md`.

---

## 3. Ejemplo de Estructura de Tarea en `task.md`

```markdown
## 0. Setup: Crear Rama de Característica (MANDATORIO)
- [ ] 0.1 Crear y cambiarse a la rama `feature/localizacion-contable`
- [ ] 0.2 Confirmar estado limpio del working tree

## 1. Backend: Implementar Modelo de Factura Local
- [ ] 1.1 Crear modelo `factura.local` con campos requeridos y restricciones
- [ ] 1.2 Declarar accesos del modelo en `security/ir.model.access.csv`
- [ ] 1.3 Crear vista de formulario y árbol en `views/factura_local_views.xml`

## 8. Backend: Ejecutar Pruebas de Odoo (/verify) (MANDATORIO)
- [ ] 8.1 Ejecutar suite de pruebas unitarias locales con `odoo-bin --test-enable`
- [ ] 8.2 Verificar que el estado de base de datos se revierta tras las pruebas
- [ ] 8.3 Guardar reporte de resultados en la carpeta del cambio

## 9. Backend: Revisión de Código e Integridad de Seguridad (/code-review) (MANDATORIO)
- [ ] 9.1 Realizar cruce de seguridad estático entre modelos de Python y registros CSV de ACLs
- [ ] 9.2 Ejecutar bucle de autoreparación (máximo 3 intentos) si se reportan tracebacks o fallos
- [ ] 9.3 Validar adherencia a las Odoo Coding Guidelines

## 10. Documentación: Actualizar Estándares (MANDATORIO)
- [ ] 10.1 Actualizar `docs/data-model.md` con la definición del modelo de datos creado

## 11. Git: Crear Commit Odoo-Style (/commit-odoo) (MANDATORIO)
- [ ] 11.1 Crear commit con formato `[ADD] mi_modulo: agregar facturación local` y descripción larga
```

---

## 4. Reglas de Completitud

- El agente **NUNCA** debe marcar una tarea como completada (`[x]`) en `task.md` si no ha ejecutado los comandos de prueba y validación correspondientes en la consola.
- Los fallos o tracebacks en las pruebas deben ser atacados proactivamente mediante el bucle de autoreparación de `/code-review` antes de notificar al usuario.
