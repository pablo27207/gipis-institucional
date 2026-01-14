# 🔬 GIPIS Institucional

Sitio web institucional del **Grupo de Investigación en Procesamiento de la Información y Sensores (GIPIS)** de la Facultad de Ingeniería, Universidad Nacional de la Patagonia San Juan Bosco.

![GIPIS](Gipis.jpg)

## 🚀 Tecnologías

- **Backend:** Flask + SQLAlchemy + Flask-Login
- **Frontend:** Tailwind CSS (CDN) + XHTML 1.0 Strict
- **Base de Datos:** SQLite
- **Despliegue:** Docker + Traefik (reverse proxy + SSL automático)

## 📁 Estructura

```
├── app/
│   ├── __init__.py        # Factory de la app
│   ├── models.py          # Modelos SQLAlchemy
│   ├── routes/            # Blueprints (main, auth)
│   ├── templates/         # Templates Jinja2/XHTML
│   └── static/            # CSS, imágenes
├── scripts/
│   ├── migrate_json.py    # Migrar datos desde database.json
│   └── set_passwords.py   # Establecer contraseñas iniciales
├── docker-compose.yml     # Producción (con SSL)
├── docker-compose.local.yml # Desarrollo local
├── Dockerfile
└── .env.example           # Variables de entorno ejemplo
```

## 🏃 Desarrollo Local

### Opción 1: Python directo
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos
python scripts/migrate_json.py
python scripts/set_passwords.py

# Ejecutar
python run.py
```

### Opción 2: Docker
```bash
docker compose -f docker-compose.local.yml up -d --build
```

Acceder a: http://localhost

## 🌐 Despliegue en Producción

### 1. Requisitos del servidor
- Docker y Docker Compose instalados
- Puertos 80 y 443 abiertos
- Dominio apuntando a la IP del servidor

### 2. Configurar
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/gipis-institucional.git
cd gipis-institucional

# Configurar variables
cp .env.example .env
nano .env
```

Editar `.env`:
```
DOMAIN=gipis.unp.edu.ar
ACME_EMAIL=admin@unp.edu.ar
SECRET_KEY=tu-clave-secreta-de-32-caracteres
```

### 3. Desplegar
```bash
docker compose up -d --build
```

¡Listo! Traefik genera automáticamente el certificado SSL.

### 4. Verificar
```bash
docker compose logs -f
```

## 👥 Login de Miembros

Los miembros del grupo pueden acceder con su email institucional.

- **URL:** `/auth/login`
- **Contraseña inicial:** `gipis2024`

Cada miembro puede editar su perfil (nombre, cargo, bio, LinkedIn).

## 📖 Más Información

Ver [DEPLOY.md](DEPLOY.md) para guía completa de despliegue y arquitectura.

---

**GIPIS - FI UNPSJB** | Comodoro Rivadavia, Chubut, Argentina
