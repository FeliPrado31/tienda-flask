# 🛒 Tienda Flask - Proyecto Ecommerce

Bienvenido al proyecto **Tienda Flask**, una aplicación web simple para gestionar productos, pedidos y usuarios utilizando Flask. A continuación, se explica cómo configurar y ejecutar el proyecto.

---

## 📋 Requisitos previos

Antes de ejecutar la aplicación, asegúrate de tener instalado lo siguiente:

- **Python 3.12** o superior 🐍
- **MySQL Server** para la base de datos 🗄️
- **Pipenv** para manejar las dependencias (opcional) 📦

---

## 🚀 Instalación

Sigue estos pasos para configurar el proyecto:

### 1. Clonar el repositorio

```bash
git clone https://github.com/FeliPrado31/tienda-flask.git
cd tienda-flask
```

### 2. Configurar la base de datos

1. Crea una base de datos MySQL llamada `ecommerce`:
   ```sql
   CREATE DATABASE ecommerce;
   ```
2. Actualiza las credenciales de la base de datos en `app.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/ecommerce'
   ```
   Cambia `root:root` por tu usuario y contraseña de MySQL si es necesario.

### 3. Instalar dependencias

Usa `pipenv` o `pip` para instalar las dependencias:

#### Con Pipenv:
```bash
pipenv install
```

#### Con Pip:
```bash
pip install -r requirements.txt
```

Las dependencias principales son:
- **Flask**: Framework web.
- **Flask-SQLAlchemy**: ORM para interactuar con la base de datos.
- **PyMySQL**: Conector de MySQL para Python.
- **Flask-Login**: Manejo de autenticación.
- **Flask-Bcrypt**: Hashing de contraseñas.

---

## ▶️ Ejecutar la aplicación

1. Inicializa la base de datos:
   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
   ```

2. Ejecuta el servidor de desarrollo:
   ```bash
   flask run
   ```

3. Abre tu navegador y ve a [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 🧑‍💻 Funcionalidades

### Administrador 🛠️
- Crear, editar y eliminar productos.
- Ver todos los productos disponibles.

### Cliente 👤
- Crear nuevos pedidos.
- Ver el historial de pedidos.

---

## 📂 Estructura del proyecto

```
tienda-flask/
├── Pipfile                  # Dependencias del proyecto
├── app.py                   # Archivo principal de Flask
├── extensions.py            # Configuración de SQLAlchemy
├── models.py                # Definición de modelos de la base de datos
├── schema.sql               # Esquema de la base de datos
├── routes/                  # Rutas de la aplicación
│   ├── admin_routes.py      # Rutas para el administrador
│   ├── auth_routes.py       # Rutas para autenticación
│   └── cliente_routes.py    # Rutas para clientes
└── templates/               # Plantillas HTML
    ├── base.html            # Plantilla base
    ├── admin_dashboard.html # Panel del administrador
    ├── cliente_dashboard.html # Panel del cliente
    └── otros...             # Formularios y vistas adicionales
```

---

## 🔧 Pruebas y depuración

Para habilitar el modo de depuración, asegúrate de que `debug=True` esté configurado en `app.run()` en `app.py`. Esto te permitirá ver errores detallados durante el desarrollo [[5]].

---

## 🌟 Contribuciones

Si deseas contribuir al proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -m "Añadir nueva funcionalidad"`).
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un pull request.

---

## 📜 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---
