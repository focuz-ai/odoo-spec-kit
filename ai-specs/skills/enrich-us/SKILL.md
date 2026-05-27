---
name: enrich-us
description: Analiza y enriquece historias de usuario (tickets) con detalles técnicos listos para desarrollo en Odoo 19.0, obligando a verificar contexto real y conectando con Jira MCP / Plane MCP.
author: Focuz AI
version: 1.0.0
---

# Skill: Enriquecimiento de Historias de Usuario (/enrich-us)

Esta skill guía al agente en el análisis de una solicitud de negocio o ticket para estructurarla con el nivel de detalle técnico que requiere el desarrollo autónomo en Odoo 19.0.

---

## Instrucciones de Ejecución

Analice y enriquezca la historia de usuario recibida como argumento: `$ARGUMENTS`. Siga estos pasos:

### 1. Origen del Ticket
- **Entrada Directa**: Si el usuario proporciona el texto del ticket en el chat, utilícelo.
- **Modo Jira / Plane**: Si se provee un ID de ticket o se solicita consultar la plataforma de gestión, intente cargar los detalles utilizando Jira MCP. Si no está configurado, utilice Plane MCP como alternativa.

### 2. Directiva de Búsqueda de Contexto Real (MANDATORIA)
- **Prohibido Adivinar**: El agente **NUNCA** debe adivinar nombres de campos, modelos
  de Odoo, estructuras XML o XML IDs de vistas nativas.
- **Investigación Activa**: Es obligatorio buscar y validar los elementos directamente
  en el código fuente del entorno de Odoo 19.0 o realizando consultas a la base de datos
  PostgreSQL activa para verificar la existencia real de los campos.
- **Rutas Locales Configurables**: Para ubicar el código de Odoo, use
  `config/local.paths.json` (no versionado), creado con
  `python scripts/setup_assistant.py init`:
  - `odoo_community_root` (obligatoria)
  - `odoo_enterprise_root` (opcional)

### 3. Validación de Completitud Técnica para Odoo
Asegúrese de mapear y enriquecer el ticket para que contenga:
- **Modelos y Campos**: Especificar los modelos nuevos a crear o los existentes a extender (`_inherit`). Indicar nombre del campo técnico, tipo (Monetary, Many2one, etc.), atributos (`string`, `tracking`, `check_company`, `precompute`).
- **Seguridad**: Identificar si requiere nuevos accesos en `ir.model.access.csv` o reglas de registro (`record rules`) en XML.
- **Vistas XML**: Listar las vistas (Form, Tree, Kanban, etc.) que se modificarán o crearán, incluyendo la ruta técnica de los campos y las expresiones XPath de herencia.
- **Wizards y Acciones**: Definir si se requiere un `TransientModel` para flujos paso a paso o acciones de servidor.
- **Estrategia de Verificación**: Especificar qué pruebas unitarias de backend (`TransactionCase`/`HttpCase`) o frontend (`HOOT`) se construirán para verificar la lógica de negocio.

### 4. Formato de Salida
Retorne la respuesta en markdown estructurado en dos secciones principales:
- `## Original`: El texto o requerimiento tal como fue provisto.
- `## Mejorado (Especificación Técnica Odoo)`: La especificación técnica completa y estructurada con todos los puntos del paso 3.

### 5. Actualización en la Plataforma (Opcional)
Si se encuentra en modo Jira/Plane, escriba la versión mejorada de regreso en el ticket correspondiente bajo las secciones `[original]` y `[enhanced]`.


