---
description: Guía de configuración del entorno de desarrollo para Odoo 16.0, incluyendo Python, PostgreSQL, archivo de configuración odoo.conf y comandos para ejecutar el servidor y las pruebas.
alwaysApply: true
---

# Guía de Setup y Desarrollo en Odoo 16.0 (Development Guide)

Esta guía describe los pasos necesarios para configurar el entorno de desarrollo local para Odoo 16.0 (Community o Enterprise) y ejecutar pruebas.

---

## 🚀 Instrucciones de Configuración

### Requisitos Previos
Asegúrese de tener instalados los siguientes componentes en su sistema:
- **Python 3.10** (versión recomendada para Odoo 16.0)
- **PostgreSQL 15 o superior**
- **Git**
- **Node.js** y **npm** (necesarios para la compilación de recursos SCSS y la ejecución de pruebas QUnit en el navegador)

---

### 1. Clonar los Repositorios de Odoo

Es recomendable tener una estructura donde residan Odoo Community, Enterprise (opcional) y sus módulos personalizados:

```bash
mkdir odoo16-env
cd odoo16-env
# Clonar Odoo Community (rama 16.0)
git clone https://github.com/odoo/odoo.git --depth 1 --branch 16.0 community
# Clonar Odoo Enterprise (si tiene acceso a la rama 16.0)
git clone https://github.com/odoo/enterprise.git --depth 1 --branch 16.0 enterprise
# Clonar su repositorio de módulos personalizados (ej. odoo-spec-kit)
git clone <url_su_repositorio> custom_addons
```

---

### 2. Entorno Virtual de Python y Dependencias

Cree y active un entorno virtual para aislar las librerías de Odoo:

```bash
cd community
# Crear entorno virtual
python -m venv venv

# Activar en Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Activar en Linux/macOS
source venv/bin/activate

# Instalar dependencias requeridas por Odoo
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3. Configuración de PostgreSQL

Odoo requiere un rol de PostgreSQL para conectarse a la base de datos. Cree un usuario con permisos de creación de base de datos (`CREATEDB`):

```bash
# Iniciar consola de PostgreSQL como administrador (ejemplo en Windows/Linux)
createuser -P -d -q -U postgres odoo
# Le pedirá definir una contraseña. Ejemplo: 'odoo_pwd'
```

---

### 4. Archivo de Configuración de Odoo (`odoo.conf`)

Cree un archivo de configuración para el servidor en la raíz del entorno virtual o de su proyecto. Ejemplo: `odoo.conf`

```ini
[options]
; Datos de conexión a la Base de Datos
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo_pwd

; Rutas de Addons (separe por comas, priorizando core, luego enterprise y custom)
addons_path = 
    D:/Projects/Odoo/o16-env/odoo/addons,
    D:/Projects/Odoo/o16-env/enterprise,
    D:/Projects/AI/odoo-specboot

; Configuración de desarrollo y rendimiento
admin_passwd = admin_master_password
port = 8069
log_level = info
dev_mode = reload,qweb,werkzeug
```

> [!TIP]
> Reemplace las rutas en `addons_path` con las rutas absolutas exactas de su máquina. Use barras diagonales (`/`) en Windows para evitar problemas de escape de caracteres en el archivo `.conf`.

---

## 🧪 Comandos de Ejecución y Pruebas

Una vez configurado, utilice los siguientes comandos en su terminal con el entorno virtual activo:

### Levantar el Servidor de Odoo:
```bash
# Ejecutar y forzar la instalación/actualización de su módulo
python odoo-bin -c odoo.conf -d bd_desarrollo -i mi_modulo_personalizado
```

### Ejecutar Pruebas Unitarias del Backend (Python):
Odoo incluye un comando específico para ejecutar pruebas habilitando el modo test:

```bash
# Correr tests de un módulo específico al instalarlo/actualizarlo
python odoo-bin -c odoo.conf -d bd_pruebas --test-enable --stop-after-init -i mi_modulo_personalizado
```

### Ejecutar Pruebas Filtrando por Tags:
```bash
# Ejecutar solo los tests de integración (post_install) de su módulo
python odoo-bin -c odoo.conf -d bd_pruebas --test-enable --stop-after-init --test-tags /mi_modulo_personalizado:post_install
```

### Ejecutar Pruebas Frontend en Navegador (Tours):
Para ejecutar tours interactivos que abren Chrome Headless, asegúrese de tener configurado Google Chrome en la máquina de ejecución:

```bash
# Ejecutar el tour de interfaz de usuario de su módulo
python odoo-bin -c odoo.conf -d bd_pruebas --test-enable --stop-after-init --test-tags /mi_modulo_personalizado:HttpCase
```
