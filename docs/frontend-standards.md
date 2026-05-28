# Estándares de Desarrollo Frontend en Odoo (Frontend Standards)

## Tabla de Contenidos

1. [Stack Tecnológico](#stack-tecnológico)
2. [Estructura y Ciclo de Vida de Componentes OWL 2](#estructura-y-ciclo-de-vida-de-componentes-owl-2)
3. [Plantillas QWeb del Lado del Cliente](#plantillas-qweb-del-lado-del-cliente)
4. [Uso e Integración de Servicios del Core](#uso-e-integración-de-servicios-del-core)
5. [Registro de Assets en el Manifest](#registro-de-assets-en-el-manifest)
6. [Estilos SCSS y Diseño Responsivo](#estilos-scss-y-diseño-responsivo)
7. [Pruebas Frontend con QUnit y Web Test Helpers](#pruebas-frontend-con-qunit-y-web-test-helpers)
8. [Creación de Widgets de Campos Personalizados](#creación-de-widgets-de-campos-personalizados)
9. [Convenciones de Nombres y Estructura de Archivos](#convenciones-de-nombres-y-estructura-de-archivos)

---

## 1. Stack Tecnológico

El frontend del cliente web de Odoo está construido sobre las siguientes
tecnologías principales:

- **OWL 2 (Odoo Web Library)**: Framework moderno de componentes reactivos basado en
  clases y hooks de JavaScript, adaptado al DOM virtual.
- **QWeb (XML)**: Motor de plantillas XML utilizado tanto para renderizado en servidor
  como para renderizado dinámico en cliente (JS).
- **Bootstrap 5**: Framework CSS subyacente personalizado para la estructura y
  componentes UI nativos.
- **SCSS**: Preprocesador de CSS utilizado para extender y modificar el diseño visual de
  Odoo.
- **QUnit**: El framework de pruebas unitarias y de integración oficial de Odoo
  para JavaScript.

---

## 2. Estructura y Ciclo de Vida de Componentes OWL 2

Todos los componentes de OWL 2 se definen utilizando clases estándar de ES6 que heredan
de `Component` de `@odoo/owl`.

### Estructura Base de un Componente:

```javascript
import {Component, useState, onWillStart, onMounted, onWillUnmount} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class MiComponente extends Component {
  static template = "mi_modulo.MiComponente";
  static props = {
    mensaje: {type: String, optional: true},
    activo: Boolean,
    onCambio: Function,
  };
  static defaultProps = {
    mensaje: "Hola Mundo",
  };

  setup() {
    // Inicialización de estado reactivo
    this.state = useState({
      contador: 0,
      cargando: false,
    });

    // Inyección de servicios del core
    this.notification = useService("notification");

    // Ganchos del ciclo de vida (Hooks)
    onWillStart(async () => {
      this.state.cargando = true;
      await this._cargarDatosIniciales();
      this.state.cargando = false;
    });

    onMounted(() => {
      console.log("Componente montado en el DOM");
    });

    onWillUnmount(() => {
      console.log("Componente listo para ser destruido");
    });
  }

  async _cargarDatosIniciales() {
    // Simulación o llamada al servidor
  }

  incrementar() {
    this.state.contador++;
    this.props.onCambio(this.state.contador);
    this.notification.add(`Contador incrementado a ${this.state.contador}`, {
      type: "info",
    });
  }
}
```

### Reglas Clave:

- **`setup()`**: Es el único punto de entrada para registrar hooks, inicializar el
  estado reactivo (`useState`) y consumir servicios (`useService`). No debe usarse el
  constructor clásico de ES6.
- **Props de Entrada**: Validar siempre las propiedades del componente declarando
  `static props`. Use tipos precisos y marque propiedades opcionales explícitamente.

---

## 3. Plantillas QWeb del Lado del Cliente

Las vistas frontend se definen mediante plantillas XML de QWeb. Se procesan de manera
reactiva ante los cambios del estado del componente.

```xml
<?xml version="1.0" encoding="utf-8" ?>
<templates xml:space="preserve">
    <t t-name="mi_modulo.MiComponente">
    <div class="o_mi_modulo_componente p-3 border rounded shadow-sm">
      <h4 class="mb-2">
        <t t-esc="props.mensaje" />
      </h4>

      <p t-if="state.cargando" class="text-muted">
                <i class="fa fa-spin fa-spinner me-1" />Cargando datos...
            </p>

      <t t-else="">
        <div class="d-flex align-items-center gap-2">
          <span class="badge bg-primary fs-6">
            <t t-esc="state.contador" />
          </span>
          <button
            class="btn btn-sm btn-outline-primary"
            t-on-click="incrementar"
            t-att-disabled="props.activo ? '' : '1'"
          >
                        Incrementar
                    </button>
        </div>
      </t>

      <!-- Renderizado de contenido hijo opcional a través de Slots -->
      <div class="mt-3 border-top pt-2" t-if="slots and slots.default">
        <t t-slot="default" />
      </div>
    </div>
  </t>
</templates>
```

### Directivas Esenciales:

- **`t-esc` / `t-out`**: Para evaluar y escapar/renderizar variables de texto en el DOM
  (en Odoo 16+, `t-out` reemplaza en la mayoría de los casos a `t-raw` por seguridad
  contra inyección XSS).
- **`t-if` / `t-elif` / `t-else`**: Para renderizado condicional.
- **`t-foreach` + `t-as`**: Para bucles iterativos. Es obligatorio incluir un atributo
  `t-key` único en el nodo hijo para optimizar el reconciliador del DOM virtual de OWL.
- **`t-att-*`**: Enlace dinámico de atributos (ej. `t-att-class`, `t-att-disabled`).
- **`t-on-*`**: Suscripción reactiva a eventos del navegador o de OWL (ej. `t-on-click`,
  `t-on-change`).

---

## 4. Uso e Integración de Servicios del Core

Odoo expone una arquitectura basada en servicios del core mediante el hook
`useService("nombre_servicio")` dentro de `setup()`.

### Servicios más Utilizados:

| Servicio           | Propósito                                                  | Ejemplo de Uso                                                              |
| ------------------ | ---------------------------------------------------------- | --------------------------------------------------------------------------- |
| **`orm`**          | Realizar consultas CRUD rápidas a modelos de base de datos | `this.orm.searchRead("res.partner", [["is_company", "=", true]], ["name"])` |
| **`rpc`**          | Llamar a métodos de Python customizados del backend        | `this.rpc("/mi_modulo/mi_ruta_json", { params })`                           |
| **`notification`** | Mostrar toasts informativos de éxito, alerta o peligro     | `this.notification.add("Éxito", { type: "success" })`                       |
| **`dialog`**       | Renderizar ventanas modales flotantes                      | `this.dialog.add(ConfirmationDialog, { body: "Confirmar acción" })`         |
| **`action`**       | Desparar acciones de ventana (`ir.actions.act_window`)     | `this.action.doAction("account.action_move_out_invoice_type")`              |
| **`user`**         | Obtener metadatos y contexto del usuario activo            | `const isCompanyUser = this.user.hasGroup("base.group_user")`               |

```javascript
// Ejemplo de consulta ORM desde un componente
setup() {
    this.orm = useService("orm");
    onWillStart(async () => {
        this.partners = await this.orm.searchRead(
            "res.partner",
            [["is_company", "=", true]],
            ["name", "email"]
        );
    });
}
```

---

## 5. Registro de Assets en el Manifest

Odoo empaqueta todos los recursos de frontend (JS, CSS, SCSS, plantillas XML de QWeb)
utilizando "Bundles" definidos en el archivo `__manifest__.py`.

```python
# __manifest__.py
{
    'name': 'Mi Módulo Frontend',
    'version': '<ODOO_VERSION>.1.0.0',
    'depends': ['web'],
    'data': [
        # Archivos XML de backend tradicionales van aquí (vistas, security)
    ],
    'assets': {
        # Bundle principal del backend del cliente web (incluye JS, XML y SCSS)
        'web.assets_backend': [
            'mi_modulo/static/src/js/**/*.js',
            'mi_modulo/static/src/xml/**/*.xml',
            'mi_modulo/static/src/scss/**/*.scss',
        ],
        # Bundle de pruebas unitarias/integración
        'web.assets_tests': [
            'mi_modulo/static/tests/tours/**/*.js',
        ],
    },
}
```

> [!IMPORTANT] > **Registro en Odoo**: En Odoo+, las plantillas QWeb JS se
> registran directamente dentro del bundle principal (como `'web.assets_backend'`) y no
> bajo un bundle separado de QWeb. Además, todo recurso estático debe ser registrado en
> los assets del manifiesto y no importado mediante etiquetas de script/style en vistas
> XML.

---

## 6. Estilos SCSS y Diseño Responsivo

- **Espacio de Nombres Obligatorio**: Encapsule todos los estilos del módulo
  envolviéndolos en la clase contenedora de su componente utilizando el prefijo
  `.o_<modulo>_<nombre>` para evitar romper el diseño global del cliente web.
- **Variables de Odoo**: Reutilice las variables SCSS del backend de Odoo para colores
  de marca, márgenes y tipografías:
  - `$o-brand-odoo`: Color púrpura oficial de Odoo.
  - `$o-brand-primary`: Color primario activo.
  - `$o-view-background-color`: Fondo de la vista activa.
- **Evite `!important`**: El uso de `!important` debe evitarse siempre. Para
  sobreescribir estilos del core, incremente la especificidad CSS usando selectores más
  concretos.

```scss
// static/src/scss/mi_componente.scss
.o_mi_modulo_componente {
  background-color: $o-view-background-color;
  border: 1px solid rgba($o-brand-primary, 0.2);

  .o_contador_valor {
    font-family: $o-font-family-monospace;
    color: $o-brand-odoo;
    font-size: 1.5rem;
  }
}
```

---

## 7. Pruebas Frontend con QUnit y Web Test Helpers

Odoo utiliza **QUnit** como su motor de pruebas unitarias y de integración oficial
para JavaScript en el cliente web.

> [!IMPORTANT]
> **Prohibición de Herramientas E2E Externas**: Al igual que en el backend, queda terminantemente prohibido configurar o recomendar herramientas E2E de terceros (Playwright, Cypress, Selenium). El ecosistema de Odoo dicta que las pruebas de componentes puros se hacen con **QUnit**, y las simulaciones de flujo de usuario completo se hacen con **Odoo JS Tours**. No contamine el proyecto con dependencias E2E ajenas a Odoo.

### Conceptos Clave de QUnit:

- **`QUnit.module` / `QUnit.test`**: Para estructurar, agrupar y nombrar los casos de
  prueba.
- **`assert`**: Objeto que provee las aserciones de prueba (ej. `assert.strictEqual`,
  `assert.containsOnce`, `assert.ok`).
- **Helpers de Simulación**:
  - `makeTestEnv`: Inicializar un entorno de pruebas simulado del cliente web
    (`mock_env`).
  - `getFixture`: Obtener el contenedor DOM limpio de la suite para poder renderizar
    nuestro componente.
  - `mount`: Montar de forma asíncrona un componente OWL dentro de nuestro contenedor
    DOM de pruebas.
  - `nextTick`: Esperar de forma asíncrona al siguiente ciclo de renderizado del DOM de
    OWL después de cambiar el estado reactivo.
  - `click`: Helper para disparar un evento de click simulado sobre un selector DOM.
  - `patchWithCleanup`: Modificar temporalmente comportamientos de servicios o clases
    del core y restablecerlos automáticamente tras finalizar la prueba.

### Ejemplo de Test Unitario OWL con QUnit:

```javascript
// static/tests/mi_componente_tests.js
import {makeTestEnv} from "@web/../tests/helpers/mock_env";
import {getFixture, mount, nextTick, click} from "@web/../tests/helpers/utils";
import {MiComponente} from "../src/js/mi_componente";

let target;

QUnit.module("MiComponente OWL Tests", {
  beforeEach() {
    target = getFixture();
  },
});

QUnit.test("Debería renderizar el mensaje y reaccionar al click", async (assert) => {
  let contadorCambio = 0;

  const env = await makeTestEnv();
  await mount(MiComponente, target, {
    env,
    props: {
      mensaje: "Test Unitario",
      activo: true,
      onCambio: (val) => {
        contadorCambio = val;
      },
    },
  });

  // Verificar el renderizado inicial en el DOM
  assert.containsOnce(target, ".o_mi_modulo_componente");
  assert.strictEqual(
    target.querySelector(".o_mi_modulo_componente h4").textContent.trim(),
    "Test Unitario"
  );
  assert.strictEqual(target.querySelector(".badge").textContent.trim(), "0");

  // Simular click en el botón de incrementar usando el helper click
  await click(target, ".o_mi_modulo_componente button");
  await nextTick();

  // Verificar cambio de estado y llamada al callback prop
  assert.strictEqual(target.querySelector(".badge").textContent.trim(), "1");
  assert.strictEqual(contadorCambio, 1);
});
```

---

## 8. Creación de Widgets de Campos Personalizados

En Odoo, los widgets de campos del formulario se crean extendiendo de `Component`
de OWL 2, recibiendo propiedades estándar del formulario en `props` (como `value` para
el valor del campo y `update` para actualizarlo) y registrando la clase directamente en
el registry `fields`.

```javascript
// static/src/js/campos/mi_campo_color.js
import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
import {Component} from "@odoo/owl";

export class MiCampoColor extends Component {
  get colorClass() {
    return `bg-${this.props.value || "light"}`;
  }

  seleccionarColor(color) {
    // Actualizar el valor del campo llamando a la función update provista en las props
    this.props.update(color);
  }
}

MiCampoColor.template = "mi_modulo.MiCampoColor";
MiCampoColor.props = {
  ...standardFieldProps,
};
MiCampoColor.supportedTypes = ["char", "selection"];

// Registrar el widget para hacerlo utilizable en XML mediante widget="mi_campo_color"
registry.category("fields").add("mi_campo_color", MiCampoColor);
```

---

## 9. Convenciones de Nombres y Estructura de Archivos

- **JavaScript**: Utilice clases en `PascalCase` para componentes y nombres en
  `camelCase` para variables o servicios de negocio.
- **Archivos Estáticos**:
  - Un componente compuesto de JS + XML + SCSS debe compartir el mismo nombre base en
    minúsculas y snake_case (ej. `mi_tarjeta.js`, `mi_tarjeta.xml`, `mi_tarjeta.scss`).
  - Guarde siempre los widgets en `static/src/js/fields/` o `static/src/components/`.
- **Plantillas QWeb**: El `t-name` de la plantilla XML debe coincidir exactamente con el
  nombre de clase completo calificado (ej. `mi_modulo.MiComponente`).
