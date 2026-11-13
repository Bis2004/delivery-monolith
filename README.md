# Delivery Platform — API de Delivery con Monolito Modular

API REST para administrar las operaciones principales de una plataforma de delivery: usuarios, restaurantes, productos, pedidos, pagos, repartidores y seguimiento de ubicaciones GPS.

El backend está desarrollado con **Python, FastAPI, SQLAlchemy y PostgreSQL**. El código se organiza como un **monolito modular**: todos los módulos se ejecutan dentro de una misma aplicación y comparten una base de datos, pero cada área del negocio mantiene sus propias capas y responsabilidades. La organización sigue principios de **Domain-Driven Design (DDD)**.

> **Estado del proyecto:** el repositorio contiene una implementación funcional de varias operaciones de backend y una estructura modular definida. No incluye una interfaz web o móvil. Tampoco debe considerarse listo para producción: hay aspectos de seguridad, autenticación, pagos reales, pruebas y configuración que requieren trabajo adicional. Las funcionalidades descritas más abajo corresponden al código incluido en este repositorio.

---

## 1. Objetivo del sistema

El sistema proporciona una API centralizada para gestionar el flujo básico de un servicio de entrega de comida:

1. Registrar usuarios y consultar sus datos.
2. Registrar restaurantes y administrar sus productos y disponibilidad.
3. Crear pedidos asociados a un cliente y a un restaurante.
4. Calcular los importes del pedido utilizando los precios guardados en el catálogo.
5. Controlar los cambios de estado del pedido.
6. Asignar repartidores y administrar su disponibilidad.
7. Guardar y consultar ubicaciones GPS de los repartidores.
8. Registrar pagos asociados a pedidos y confirmar pagos en efectivo.

El backend expone estos procesos mediante endpoints HTTP/JSON. La documentación interactiva de la API se genera automáticamente con FastAPI.

## 2. Tecnologías utilizadas

| Tecnología | Uso dentro del proyecto |
|---|---|
| Python 3.10 | Lenguaje y versión base de la imagen Docker. |
| FastAPI 0.110.0 | Creación de la API REST, rutas, dependencias y documentación OpenAPI. |
| Uvicorn 0.28.0 | Servidor ASGI que ejecuta la aplicación FastAPI. |
| SQLAlchemy 2.0.28 | Mapeo objeto-relacional (ORM), consultas y sesiones de base de datos. |
| PostgreSQL 15 | Motor de base de datos relacional. |
| psycopg2-binary 2.9.9 | Controlador de conexión entre Python y PostgreSQL. |
| Pydantic 2.6.4 | Validación de datos de entrada y definición de esquemas de respuesta. |
| email-validator 2.1.1 | Validación del formato de correo electrónico utilizado por Pydantic. |
| Docker | Construcción y ejecución de la aplicación en contenedores. |
| Docker Compose | Orquestación de la API y PostgreSQL. |

Las versiones indicadas corresponden al archivo `requirements.txt` del proyecto.

## 3. Arquitectura del sistema

### 3.1 Monolito modular

La aplicación se despliega como un único backend FastAPI. Los módulos no son microservicios separados: se ejecutan en el mismo proceso y trabajan con la misma base de datos PostgreSQL. La separación modular permite mantener diferenciadas las responsabilidades del negocio.

### 3.2 Organización por capas

Cada módulo de negocio puede contener las siguientes capas:

| Capa | Responsabilidad | Archivos habituales |
|---|---|---|
| `presentation/` | Recibe peticiones HTTP, define rutas, valida entradas y prepara respuestas JSON. | `router.py`, `schemas.py` |
| `application/` | Implementa casos de uso y coordina las operaciones del módulo. | `services.py`, `dtos.py` |
| `domain/` | Define entidades, reglas de negocio, excepciones y contratos de repositorio. | `models.py`, `exceptions.py`, `repositories.py` |
| `infrastructure/` | Implementa el acceso a PostgreSQL mediante SQLAlchemy y los adaptadores entre módulos. | `models_db.py`, `repository_impl.py`, `external_adapters.py` |

El flujo habitual de una petición es:

```text
Cliente HTTP
    |
    v
presentation/router.py
    |  Valida y recibe los datos
    v
application/services.py
    |  Ejecuta el caso de uso
    v
domain/
    |  Aplica las reglas del negocio y define contratos
    v
infrastructure/repository_impl.py
    |  Consulta o modifica la base de datos
    v
PostgreSQL
```

La respuesta vuelve desde el servicio al router y FastAPI la serializa como JSON de acuerdo con el esquema de respuesta.

### 3.3 Módulos de negocio

| Módulo | Responsabilidad principal |
|---|---|
| `auth` | Registro y consulta de usuarios; maneja los datos básicos de identidad, rol y estado. |
| `restaurant` | Registro y administración de restaurantes y productos del menú. |
| `order` | Creación de pedidos, cálculo de totales, cambios de estado y asignación de repartidores. |
| `payment` | Registro de pagos vinculados a pedidos, estados de pago y confirmación manual de efectivo. |
| `tracking` | Registro de repartidores, disponibilidad e historial de posiciones GPS. |

## 4. Estructura de carpetas y archivos

```text
 delivery-monolith/
 ├── .gitignore
 ├── Dockerfile
 ├── docker-compose.yml
 ├── requirements.txt
 ├── init.sql
 ├── INFORME.md
 ├── DDD_modulo_Auth.ipynb
 ├── prueba.txt
 └── src/
     ├── main.py
     ├── core/
     │   ├── config.py
     │   ├── database.py
     │   └── types.py
     └── modules/
         ├── auth/
         │   ├── application/
         │   │   ├── dtos.py
         │   │   └── services.py
         │   ├── domain/
         │   │   ├── exceptions.py
         │   │   ├── models.py
         │   │   └── repositories.py
         │   ├── infrastructure/
         │   │   ├── external_adapters.py
         │   │   ├── models_db.py
         │   │   └── repository_impl.py
         │   └── presentation/
         │       ├── router.py
         │       └── schemas.py
         ├── restaurant/
         │   ├── application/
         │   │   ├── dtos.py
         │   │   └── services.py
         │   ├── domain/
         │   │   ├── exceptions.py
         │   │   ├── models.py
         │   │   └── repositories.py
         │   ├── infrastructure/
         │   │   ├── external_adapters.py
         │   │   ├── models_db.py
         │   │   └── repository_impl.py
         │   └── presentation/
         │       ├── router.py
         │       └── schemas.py
         ├── order/
         │   ├── application/
         │   │   ├── dtos.py
         │   │   └── services.py
         │   ├── domain/
         │   │   ├── exceptions.py
         │   │   ├── models.py
         │   │   └── repositories.py
         │   ├── infrastructure/
         │   │   ├── external_adapters.py
         │   │   ├── models_db.py
         │   │   └── repository_impl.py
         │   └── presentation/
         │       ├── router.py
         │       └── schemas.py
         ├── payment/
         │   ├── application/
         │   │   ├── dtos.py
         │   │   └── services.py
         │   ├── domain/
         │   │   ├── exceptions.py
         │   │   ├── models.py
         │   │   └── repositories.py
         │   ├── infrastructure/
         │   │   ├── external_adapters.py
         │   │   ├── models_db.py
         │   │   └── repository_impl.py
         │   └── presentation/
         │       ├── router.py
         │       └── schemas.py
         └── tracking/
             ├── application/
             │   ├── dtos.py
             │   └── services.py
             ├── domain/
             │   ├── exceptions.py
             │   ├── models.py
             │   └── repositories.py
             ├── infrastructure/
             │   ├── external_adapters.py
             │   ├── models_db.py
             │   └── repository_impl.py
             └── presentation/
                 ├── router.py
                 └── schemas.py
```

### 4.1 Archivos de la raíz

| Archivo | Función |
|---|---|
| `.gitignore` | Indica a Git qué elementos locales no deben agregarse al repositorio, como entornos virtuales, cachés de Python, archivos `.env`, datos locales de PostgreSQL y configuraciones de IDE. |
| `requirements.txt` | Lista las bibliotecas de Python y sus versiones utilizadas por el backend. |
| `Dockerfile` | Define cómo construir la imagen de la API: parte de Python 3.10, crea `/app`, instala las dependencias, copia el proyecto y ejecuta Uvicorn en el puerto 8000. El comando actual usa `--reload`, adecuado para desarrollo y no para producción. |
| `docker-compose.yml` | Define los servicios `postgres-db` y `delivery-app`, sus variables de entorno, puertos, volumen persistente, red interna y comprobación de disponibilidad de PostgreSQL. |
| `init.sql` | Crea el esquema `delivery`, las tablas relacionales, claves foráneas, restricciones e inserta los roles y estados iniciales. Docker lo ejecuta al inicializar por primera vez el volumen de PostgreSQL. |
| `INFORME.md` | Contiene un análisis técnico anterior de la arquitectura. Algunas partes ya no coinciden con el código actual —por ejemplo, afirma que los servicios y dominios estaban vacíos—, por lo que debe actualizarse antes de utilizarlo como documentación vigente. |
| `DDD_modulo_Auth.ipynb` | Notebook de trabajo que explica y ejemplifica la separación por capas del módulo de autenticación. Incluye ejemplos didácticos y versiones previas de código; no es necesario para ejecutar la API. |
| `prueba.txt` | Archivo de prueba sin relación funcional con el backend. Se recomienda eliminarlo o reemplazarlo por contenido pertinente antes de publicar el repositorio. |

### 4.2 Núcleo compartido: `src/core/`

| Archivo | Función |
|---|---|
| `src/core/config.py` | Archivo reservado para configuración centralizada. Actualmente está vacío; la conexión a la base de datos se configura directamente en `database.py`. |
| `src/core/database.py` | Lee `DATABASE_URL` desde las variables de entorno —o utiliza una URL local predeterminada—, crea el motor SQLAlchemy, configura el `search_path` de PostgreSQL para utilizar `delivery`, construye `SessionLocal`, declara la clase base `Base` y ofrece `get_db()` para abrir y cerrar una sesión por petición. |
| `src/core/types.py` | Define el tipo compartido `Dinero`, basado en `Decimal`, con un serializador para convertir los importes al formato numérico de las respuestas JSON. |

### 4.3 Punto de entrada: `src/main.py`

Es la raíz de composición de la aplicación. Importa los modelos ORM de los cinco módulos para registrarlos en los metadatos de SQLAlchemy, importa sus routers, ejecuta `Base.metadata.create_all()` para crear tablas faltantes e incorpora las rutas con el prefijo `/api/v1`. También define los endpoints generales `/` y `/health`.

### 4.4 Módulo `auth/`

Gestiona los datos básicos de los usuarios.

| Archivo | Función |
|---|---|
| `application/dtos.py` | Está vacío. En la implementación actual, `AuthService` recibe `UsuarioCreate`, definido en la capa `presentation`. |
| `application/services.py` | Contiene `AuthService`: registra usuarios, comprueba que el correo no exista, consulta un usuario por ID y lista usuarios. Coordina las operaciones con `IAuthRepository`. |
| `domain/exceptions.py` | Define las excepciones de dominio del módulo: error base, correo ya registrado y usuario no encontrado. |
| `domain/models.py` | Define la entidad pura `Usuario` con nombre, correo, contraseña, rol, estado e ID. Incluye `cambiar_password()`, que exige al menos seis caracteres. |
| `domain/repositories.py` | Declara el contrato abstracto `IAuthRepository` para buscar usuarios por ID o correo, guardar usuarios y listarlos. |
| `infrastructure/external_adapters.py` | Está vacío. No contiene adaptadores externos de autenticación en esta versión. |
| `infrastructure/models_db.py` | Define los modelos ORM `RolModel`, `EstadoModel`, `UsuarioModel`, `ContactoModel` y `DireccionModel`, además de sus relaciones SQLAlchemy. |
| `infrastructure/repository_impl.py` | Implementa `IAuthRepository` con SQLAlchemy. Convierte registros ORM a la entidad `Usuario`, consulta por ID/correo, guarda cambios y lista usuarios. |
| `presentation/router.py` | Expone el registro y las consultas de usuarios. Traduce excepciones del dominio a respuestas HTTP. |
| `presentation/schemas.py` | Define `UsuarioCreate` para recibir y validar datos, incluido `EmailStr`, y `UsuarioResponse` para devolver los campos públicos del usuario sin incluir la contraseña. |

**Operaciones actuales:** registro de usuario, listado y consulta por identificador. Aunque el módulo se llama `auth`, en el código incluido no hay endpoint de inicio de sesión, emisión de JWT/tokens ni protección de rutas mediante roles.

### 4.5 Módulo `restaurant/`

Administra los restaurantes y el catálogo de productos que cada restaurante ofrece.

| Archivo | Función |
|---|---|
| `application/dtos.py` | Define `RestauranteDTO` y `ProductoDTO`, que validan los datos de entrada, longitudes, horarios, estado, precio, disponibilidad y categoría. |
| `application/services.py` | Contiene `RestaurantService`. Implementa crear, listar, consultar, actualizar y eliminar restaurantes; también agregar, listar, consultar, actualizar y eliminar productos. Comprueba que el restaurante exista antes de gestionar su catálogo. |
| `domain/exceptions.py` | Define errores de dominio para recursos inexistentes, datos inválidos y operaciones no permitidas. |
| `domain/models.py` | Define las entidades `Restaurante` y `Producto`, valida nombre, estado, precio y categoría, y ofrece operaciones para abrir/cerrar restaurantes y cambiar disponibilidad de productos. |
| `domain/repositories.py` | Declara los contratos `IRestauranteRepository` e `IProductoRepository`, independientes de SQLAlchemy. |
| `infrastructure/external_adapters.py` | Está vacío. La integración de catálogo utilizada por pedidos está implementada en el adaptador del módulo `order`. |
| `infrastructure/models_db.py` | Define `RestauranteModel` y `ProductoModel`, con sus columnas y relación uno-a-muchos entre restaurante y productos. |
| `infrastructure/repository_impl.py` | Implementa los repositorios SQLAlchemy. Realiza consultas, inserciones, modificaciones y eliminaciones; traduce errores de integridad de la base de datos a errores de dominio. |
| `presentation/router.py` | Publica las rutas HTTP para restaurantes y productos y convierte excepciones del dominio en códigos HTTP. |
| `presentation/schemas.py` | Define `RestauranteResponse` y `ProductoResponse`, que especifican la estructura JSON devuelta por la API. El precio utiliza el tipo compartido `Dinero`. |

**Reglas relevantes:** un restaurante puede estar `Abierto` o `Cerrado`. Un producto tiene precio no negativo, categoría y bandera de disponibilidad. Un producto debe pertenecer a un restaurante.

### 4.6 Módulo `order/`

Gestiona el ciclo de vida de los pedidos y coordina información de usuarios, restaurantes, productos y repartidores.

| Archivo | Función |
|---|---|
| `application/dtos.py` | Define `ItemPedidoDTO`, `PedidoCrearDTO`, `CambiarEstadoDTO` y `AsignarRepartidorDTO`. Valida las cantidades y los datos necesarios para crear o modificar un pedido. El cliente no envía el precio ni el total: el sistema los obtiene del catálogo. |
| `application/services.py` | Contiene `OrderService`. Comprueba que el cliente y el restaurante existan, que el restaurante esté abierto, que los productos pertenezcan al restaurante y estén disponibles; construye los detalles, calcula el pedido, permite consultar/listar, cambiar estados, cancelar y asignar/liberar repartidores. |
| `domain/exceptions.py` | Define excepciones para pedidos inexistentes, referencias inválidas, transiciones de estado inválidas, cancelaciones no permitidas y repartidores no disponibles. |
| `domain/models.py` | Define `DetallePedido` y `Pedido`. Calcula subtotales y total, aplica la máquina de estados y valida la asignación de repartidores. También define `RestauranteInfo` y `ProductoInfo` como objetos de valor usados al consultar otros módulos. |
| `domain/repositories.py` | Declara `IPedidoRepository` y los puertos `ICatalogoGateway`, `IUsuarioGateway` e `IRepartidorGateway`, que permiten consultar otros módulos sin acoplar las reglas del pedido a sus tablas. |
| `infrastructure/external_adapters.py` | Implementa los adaptadores `CatalogoRestaurantAdapter`, `UsuarioAuthAdapter` y `RepartidorTrackingAdapter`. Conectan el módulo de pedidos con los servicios de restaurantes, usuarios y repartidores. |
| `infrastructure/models_db.py` | Define `PedidoModel` y `DetallePedidoModel`, sus columnas y relaciones ORM con los detalles y el pago del pedido. |
| `infrastructure/repository_impl.py` | Implementa `PedidoRepositorySqlAlchemy`. Lee y guarda pedidos, convierte los modelos ORM en entidades de dominio y persiste sus detalles. |
| `presentation/router.py` | Expone las rutas para crear, listar, consultar, cancelar, cambiar el estado y asignar repartidores a pedidos. |
| `presentation/schemas.py` | Define `DetallePedidoResponse` y `PedidoResponse`, estructuras que controlan la respuesta JSON de pedidos y sus importes. |

**Estados del pedido:**

```text
Pendiente ──> En_Preparacion ──> En_Camino ──> Entregado
     │
     └──────────────> Cancelado
```

Las transiciones están controladas por el dominio. Un pedido no puede pasar a `En_Camino` sin repartidor asignado. Cuando un pedido se entrega o cancela, el servicio intenta liberar al repartidor asociado. La cancelación queda limitada al estado permitido por las reglas del dominio.

### 4.7 Módulo `payment/`

Registra pagos y vincula cada pago con un pedido.

| Archivo | Función |
|---|---|
| `application/dtos.py` | Define `PagoCrearDTO` y los valores permitidos para método y estado de pago. El cliente envía el ID del pedido y el método; el monto se calcula desde el pedido. |
| `application/services.py` | Contiene `PaymentService`. Verifica el pedido, impide pagar pedidos cancelados o registrar más de un pago por pedido, solicita el cobro al adaptador de pasarela, guarda el resultado y permite confirmar pagos en efectivo. |
| `domain/exceptions.py` | Define errores de pago inexistente, referencia inválida, pago duplicado, operación no permitida y pago rechazado. |
| `domain/models.py` | Define la entidad `Pago`, valida el monto, método y estado, y permite completar o marcar fallido un pago. También incluye `PedidoInfo` y `ResultadoPasarela` como objetos de valor. |
| `domain/repositories.py` | Declara `IPagoRepository`, `IPedidoGateway` e `IPasarelaPago`, que representan la persistencia de pagos, la consulta de pedidos y el contrato de una pasarela de cobro. |
| `infrastructure/external_adapters.py` | Implementa `PedidoOrderAdapter`, que consulta el módulo de pedidos, y `PasarelaPagoSimulada`, que simula la aprobación de pagos y genera identificadores ficticios de transacción. |
| `infrastructure/models_db.py` | Define `PagoModel` y su relación uno-a-uno con `PedidoModel`. La tabla limita a un pago por pedido. |
| `infrastructure/repository_impl.py` | Implementa las consultas y operaciones de persistencia de pagos mediante SQLAlchemy. Maneja las restricciones de unicidad. |
| `presentation/router.py` | Publica las rutas para procesar pagos, listarlos, consultarlos por ID o por pedido y confirmar pagos en efectivo. |
| `presentation/schemas.py` | Define `PagoResponse`, que establece los campos de salida del pago. El monto utiliza `Dinero`. |

**Métodos disponibles:** `Efectivo`, `Tarjeta` y `QR`. En la implementación actual, tarjeta y QR se aprueban mediante una pasarela simulada; el efectivo queda pendiente y puede confirmarse posteriormente. No existe integración con una entidad bancaria ni proveedor real.

### 4.8 Módulo `tracking/`

Administra los repartidores y almacena los puntos GPS que reportan.

| Archivo | Función |
|---|---|
| `application/dtos.py` | Define `RepartidorDTO`, `DisponibilidadDTO` y `UbicacionDTO`. Valida el tipo de vehículo, placa, disponibilidad y rangos geográficos de latitud/longitud. |
| `application/services.py` | Contiene `TrackingService`. Crea, consulta, actualiza y elimina repartidores; cambia su disponibilidad; registra ubicaciones con fecha y hora del servidor; y consulta el historial o la última ubicación. También expone operaciones internas para marcar repartidores ocupados o liberarlos desde `order`. |
| `domain/exceptions.py` | Define errores para repartidores inexistentes, ubicaciones no encontradas, datos inválidos y repartidores no disponibles. |
| `domain/models.py` | Define las entidades `Repartidor` y `UbicacionTracking`. Valida tipos de vehículo, placa obligatoria para moto/taxi y límites de coordenadas GPS. |
| `domain/repositories.py` | Declara `IRepartidorRepository` e `IUbicacionRepository`, contratos de persistencia para repartidores y ubicaciones. |
| `infrastructure/external_adapters.py` | Está vacío. La comunicación con tracking desde pedidos se implementa en `order/infrastructure/external_adapters.py`. |
| `infrastructure/models_db.py` | Define `RepartidorModel` y `UbicacionTrackingModel`, incluida la relación entre un repartidor y su historial de ubicaciones. |
| `infrastructure/repository_impl.py` | Implementa los repositorios SQLAlchemy para crear, consultar, modificar y eliminar repartidores, almacenar coordenadas y recuperar ubicaciones ordenadas de la más reciente a la más antigua. |
| `presentation/router.py` | Publica las rutas HTTP para administrar repartidores, cambiar su disponibilidad y registrar/consultar ubicaciones. |
| `presentation/schemas.py` | Define `RepartidorResponse` y `UbicacionResponse`, los formatos JSON de salida. |

**Tipos de vehículo admitidos:** `Bicicleta`, `Moto` y `Taxi`. Para moto y taxi se exige una placa. La API valida latitud entre -90 y 90 y longitud entre -180 y 180.

## 5. Base de datos

El proyecto utiliza PostgreSQL 15 y crea el esquema `delivery`. El script `init.sql` crea las siguientes tablas:

| Tabla | Propósito |
|---|---|
| `rol` | Catálogo de roles de usuario: cliente, repartidor y administrador. |
| `estado` | Catálogo de estados de cuenta: activo, inactivo, suspendido y eliminado. |
| `usuario` | Datos básicos de usuarios y referencias a rol y estado. |
| `contacto` | Teléfonos y domicilio de un usuario; relación uno-a-uno. |
| `direccion` | Direcciones guardadas de un usuario, con coordenadas, referencia y etiqueta. |
| `restaurante` | Información general, dirección, contacto, horarios y estado del restaurante. |
| `producto` | Productos del menú, descripción, precio, disponibilidad y categoría. |
| `repartidor` | Tipo de vehículo, placa, disponibilidad y posible relación con un usuario. |
| `ubicacion_tracking` | Historial de coordenadas GPS, fecha y hora por repartidor. |
| `pedido` | Cabecera del pedido, cliente, restaurante, repartidor, total, estado y fecha. |
| `detalle_pedido` | Productos, cantidades, precio unitario y subtotal de cada pedido. |
| `pago` | Monto, método, estado, identificador de transacción y pedido asociado. |

Las claves foráneas mantienen las relaciones entre usuarios, restaurantes, productos, repartidores, pedidos y pagos. El script define reglas de integridad como precios no negativos, cantidades positivas, estados permitidos y un pago por pedido.

**Importante:** `contacto`, `direccion`, `rol` y `estado` están definidos en el SQL y en los modelos ORM de autenticación, pero no todos cuentan con endpoints de administración propios en la API actual.

## 6. Endpoints de la API

Todos los endpoints de negocio utilizan el prefijo `/api/v1`. Los endpoints marcados como `health` sirven para comprobar el estado de cada módulo.

### Sistema

| Método | Ruta | Función |
|---|---|---|
| GET | `/` | Devuelve un mensaje general y los módulos activos. |
| GET | `/health` | Comprueba que el servicio principal responde. |

### Auth — `/api/v1/auth`

| Método | Ruta | Función |
|---|---|---|
| POST | `/register` | Registra un usuario. |
| GET | `/users` | Lista usuarios. |
| GET | `/users/{usuario_id}` | Consulta un usuario por ID. |

### Restaurants — `/api/v1/restaurants`

| Método | Ruta | Función |
|---|---|---|
| GET | `/health` | Estado del módulo. |
| POST | `/` | Crea un restaurante. |
| GET | `/` | Lista restaurantes; admite filtro `estado`. |
| GET | `/{restaurant_id}` | Consulta un restaurante. |
| PUT | `/{restaurant_id}` | Actualiza un restaurante. |
| DELETE | `/{restaurant_id}` | Elimina un restaurante, si las restricciones lo permiten. |
| POST | `/{restaurant_id}/productos` | Agrega un producto al restaurante. |
| GET | `/{restaurant_id}/productos` | Lista productos; admite `solo_disponibles`. |
| GET | `/productos/{producto_id}` | Consulta un producto. |
| PUT | `/productos/{producto_id}` | Actualiza un producto. |
| DELETE | `/productos/{producto_id}` | Elimina un producto, si no está referenciado por pedidos. |

### Orders — `/api/v1/orders`

| Método | Ruta | Función |
|---|---|---|
| GET | `/health` | Estado del módulo. |
| POST | `/` | Crea un pedido con uno o más productos. |
| GET | `/` | Lista pedidos; admite filtros `usuario_id` y `estado`. |
| GET | `/{pedido_id}` | Consulta un pedido y sus detalles. |
| PATCH | `/{pedido_id}/estado` | Cambia el estado respetando las transiciones permitidas. |
| POST | `/{pedido_id}/cancelar` | Solicita cancelar un pedido. |
| PATCH | `/{pedido_id}/repartidor` | Asigna un repartidor disponible. |

### Payments — `/api/v1/payments`

| Método | Ruta | Función |
|---|---|---|
| GET | `/health` | Estado del módulo. |
| POST | `/` | Procesa y registra un pago para un pedido. |
| GET | `/` | Lista pagos; admite filtro `estado`. |
| GET | `/pedido/{pedido_id}` | Consulta el pago asociado a un pedido. |
| GET | `/{pago_id}` | Consulta un pago por ID. |
| PATCH | `/{pago_id}/confirmar` | Confirma manualmente un pago en efectivo. |

### Tracking — `/api/v1/tracking`

| Método | Ruta | Función |
|---|---|---|
| GET | `/health` | Estado del módulo. |
| POST | `/repartidores` | Registra un repartidor. |
| GET | `/repartidores` | Lista repartidores; admite filtro `disponible`. |
| GET | `/repartidores/{repartidor_id}` | Consulta un repartidor. |
| PUT | `/repartidores/{repartidor_id}` | Actualiza los datos de un repartidor. |
| PATCH | `/repartidores/{repartidor_id}/disponibilidad` | Cambia su disponibilidad. |
| DELETE | `/repartidores/{repartidor_id}` | Elimina un repartidor según las relaciones existentes. |
| POST | `/repartidores/{repartidor_id}/ubicaciones` | Registra una nueva posición GPS. |
| GET | `/repartidores/{repartidor_id}/ubicaciones` | Consulta el historial GPS; `limite` admite de 1 a 500 registros. |
| GET | `/repartidores/{repartidor_id}/ubicacion-actual` | Devuelve la última posición registrada. |

En total, el código actual declara **37 rutas HTTP en los cinco módulos**. A estas se suman los dos endpoints generales (`/` y `/health`) definidos en `src/main.py`, para un total de **39 rutas HTTP**.

## 7. Flujo general de un pedido

1. El cliente se registra mediante el módulo `auth`.
2. El restaurante se registra y carga sus productos mediante `restaurant`.
3. El cliente solicita un pedido indicando su ID, el restaurante y los productos/cantidades.
4. `OrderService` comprueba que el usuario exista, que el restaurante esté abierto y que cada producto pertenezca al restaurante y esté disponible.
5. El backend obtiene los precios desde la base de datos, calcula los subtotales y el total, y guarda el pedido con estado `Pendiente`.
6. El pedido puede pasar a preparación. Un repartidor registrado en `tracking` puede ser asignado si está disponible.
7. Al asignarlo, el sistema marca al repartidor como ocupado. Cuando el pedido se entrega o cancela, el servicio intenta liberarlo.
8. El módulo `payment` consulta el total del pedido y registra el pago según el método seleccionado.
9. El repartidor puede reportar coordenadas GPS. El módulo `tracking` conserva el historial y permite consultar la última ubicación.

Este flujo representa la lógica del backend disponible. No implica que el repositorio incluya una aplicación de cliente, notificaciones, un mapa visual o seguimiento en tiempo real mediante WebSockets.

## 8. Instalación y ejecución con Docker

### Requisitos

- Docker instalado.
- Docker Compose disponible como `docker compose`.

### Pasos

Desde la carpeta raíz del proyecto, donde se encuentran `Dockerfile` y `docker-compose.yml`, ejecutar:

```bash
docker compose up --build -d
```

Este comando construye la imagen del backend, crea el contenedor de PostgreSQL, espera a que la base de datos esté saludable y luego inicia la API.

Comprobar el estado de los contenedores:

```bash
docker compose ps
```

Ver los registros de la API:

```bash
docker compose logs -f delivery-app
```

Ver los registros de PostgreSQL:

```bash
docker compose logs -f postgres-db
```

Detener los contenedores sin borrar los datos persistidos:

```bash
docker compose down
```

> **Advertencia:** `docker compose down -v` también elimina el volumen de PostgreSQL y, por tanto, los datos guardados en ese volumen. No utilizarlo si se desea conservar la base de datos.

### Puertos y conexión local

| Servicio | Dirección |
|---|---|
| API | `http://localhost:8000` |
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |
| PostgreSQL | `localhost:5432` |

La configuración actual de Compose crea la base `delivery_db` y utiliza el usuario `delivery_user`. Las credenciales incluidas en `docker-compose.yml` son valores de desarrollo de ejemplo; deben cambiarse y trasladarse a variables de entorno antes de cualquier despliegue compartido o público.

## 9. Ejecución local sin Docker

### Requisitos

- Python 3.10 o una versión compatible.
- PostgreSQL 15 (o una versión compatible).
- Base de datos creada y esquema/tablas inicializados mediante `init.sql`.

### Crear y activar un entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Configurar la conexión

La aplicación utiliza la variable `DATABASE_URL`. En PowerShell, por ejemplo:

```powershell
$env:DATABASE_URL = "postgresql://delivery_user:delivery_password@localhost:5432/delivery_db"
```

En Linux/macOS:

```bash
export DATABASE_URL="postgresql://delivery_user:delivery_password@localhost:5432/delivery_db"
```

La base de datos debe existir y debe tener inicializadas las tablas del archivo `init.sql`. Si se utiliza `psql`, el script puede ejecutarse con:

```bash
psql -U delivery_user -d delivery_db -f init.sql
```

### Iniciar la API

```bash
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

Luego abrir `http://localhost:8000/docs` para probar los endpoints.

## 10. Validaciones y reglas de negocio implementadas

- El correo electrónico de un usuario no puede repetirse.
- Los restaurantes admiten los estados `Abierto` y `Cerrado`.
- Un producto debe estar asociado a un restaurante y su precio no puede ser negativo.
- Un pedido debe tener al menos un producto y cada cantidad debe ser positiva.
- Los precios y el total del pedido se calculan en el backend; no se confía en importes enviados por el cliente.
- No se puede crear un pedido para un restaurante cerrado.
- Los productos del pedido deben pertenecer al restaurante seleccionado y estar disponibles.
- Los estados del pedido siguen transiciones definidas en el dominio.
- Para pasar un pedido a `En_Camino` debe existir un repartidor asignado.
- Un repartidor ocupado no puede asignarse nuevamente a otro pedido mediante el flujo del servicio.
- Los tipos de vehículo están limitados a bicicleta, moto y taxi; moto y taxi requieren placa.
- Las coordenadas GPS se validan dentro de los rangos geográficos permitidos.
- No se puede registrar un pago para un pedido inexistente o cancelado.
- El sistema comprueba que no exista ya un pago asociado al pedido.
- El monto del pago se toma del total almacenado en el pedido, no de un monto enviado por el cliente.
- La confirmación manual está reservada para pagos en efectivo.

## 11. Estado actual, limitaciones y tareas pendientes

La estructura y buena parte de las reglas centrales están implementadas, pero deben completarse varios aspectos antes de utilizar el sistema en un entorno real:

1. **Seguridad de usuarios:** `AuthService` guarda actualmente la contraseña recibida sin aplicar un hash. Debe implementarse hashing seguro (por ejemplo, Argon2 o bcrypt), inicio de sesión, emisión/validación de tokens y controles de autorización por rol. Las rutas actuales no están protegidas por autenticación.
2. **Credenciales y configuración:** las credenciales de PostgreSQL están escritas como valores de desarrollo en `docker-compose.yml` y también hay una URL predeterminada en `database.py`. Deben gestionarse mediante variables de entorno y un archivo de ejemplo sin secretos reales.
3. **Pagos reales:** `PasarelaPagoSimulada` aprueba las operaciones de manera ficticia. Para cobrar de verdad debe integrarse un proveedor autorizado y verificarse sus respuestas de forma segura.
4. **Transacciones y concurrencia:** las operaciones que coordinan pedido, disponibilidad del repartidor y pago deben revisarse para garantizar consistencia cuando varias peticiones ocurren simultáneamente.
5. **Migraciones:** `Base.metadata.create_all()` crea tablas faltantes, pero no reemplaza un sistema de migraciones para modificar estructuras ya existentes. Se recomienda incorporar Alembic.
6. **Pruebas automatizadas:** no se encontraron archivos de pruebas en el ZIP. Se recomienda crear pruebas unitarias para el dominio y servicios, y pruebas de integración para API y PostgreSQL.
7. **Configuración centralizada:** `src/core/config.py` está vacío. Se recomienda centralizar la lectura y validación de variables de entorno.
8. **Módulos de usuario:** las tablas `contacto` y `direccion` están modeladas en infraestructura, pero no tienen servicios y endpoints completos en esta versión.
9. **Interfaz de usuario:** el repositorio contiene el backend/API, no una aplicación web, Android, iOS ni panel administrativo.
10. **Seguimiento visual y tiempo real:** se almacenan coordenadas mediante peticiones HTTP, pero no se incluye mapa, transmisión en tiempo real ni conexión automática con el dispositivo del repartidor.
11. **Ejecución de producción:** el `Dockerfile` utiliza `uvicorn --reload`; debe sustituirse por una configuración de producción y complementarse con HTTPS, logs, monitoreo, copias de seguridad y políticas de secretos.
12. **Documentación heredada:** `INFORME.md` contiene observaciones de una versión anterior y debe revisarse para que no contradiga el código actual.

## 12. Buenas prácticas para contribuir

- Mantener cada regla del negocio en la capa `domain` o en el caso de uso correspondiente, evitando poner reglas complejas directamente en los routers.
- Definir contratos en `domain/repositories.py` y sus implementaciones en `infrastructure/repository_impl.py`.
- Validar los datos externos con Pydantic y volver a comprobar las invariantes importantes dentro del dominio.
- Obtener los precios y totales desde la base de datos, nunca confiar en valores monetarios enviados por el cliente.
- No guardar contraseñas en texto plano ni publicar credenciales, claves API o archivos `.env`.
- Agregar pruebas al introducir nuevas reglas o endpoints.
- Documentar nuevas variables de entorno y cambios de esquema.

## 13. Resumen

Delivery Platform es un backend de delivery construido con FastAPI y PostgreSQL bajo una arquitectura de monolito modular. Sus módulos permiten gestionar usuarios, restaurantes, productos, pedidos, pagos simulados y repartidores con historial GPS. La separación por capas facilita mantener y ampliar el código, mientras que Docker Compose simplifica el entorno local de ejecución.

El repositorio constituye una base de desarrollo para continuar construyendo una plataforma de delivery. Para un uso real se deben completar especialmente la seguridad de autenticación, el proveedor de pagos, las migraciones, las pruebas automatizadas, la configuración segura y la interfaz de usuario.
