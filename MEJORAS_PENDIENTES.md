# Mejoras Pendientes — GIPIS

Ideas y funcionalidades a implementar en el futuro.

---

## 🔍 Búsqueda y filtrado de publicaciones — HECHO (2026-08-01)

**Implementado**: página `/investigacion/produccion` con toda la producción agrupada por
sección y filtros en el cliente (texto sobre título/autores, año y sección), más conteo
de citas vía OpenAlex y botón "Citar (BibTeX)" por ítem.

---

## 🔄 Harvesting de novedades desde redes sociales

**Prioridad**: Alta  
**Descripción**: Alimentar automáticamente las tarjetas de Novedades con las publicaciones
del grupo en redes sociales.

**Estado (2026-08-01)**: A la espera de datos de la página de Facebook — Pablo tiene que
consultar con Carlos quién es administrador de facebook.com/GIPISUNPSJB para poder crear
la app de Meta y generar el token. Mientras tanto ya se puede cargar novedades a mano
desde el panel admin (CRUD implementado). El modelo ya tiene `News.source` y la UI
muestra el badge de la red en las novedades harvesteadas.

**Instagram (pedirle también a Carlos)**: la misma app de Meta sirve para leer los posts
de instagram.com/gipis.unp **si la cuenta de Instagram está vinculada como cuenta
profesional a la página de Facebook**. Al hablar con Carlos, confirmar: (1) quién es
admin de la página de Facebook, (2) si la cuenta de Instagram está vinculada a esa
página y quién la administra. Con un solo token se harvestean las dos redes.

- **LinkedIn descartado como fuente**: la API de páginas de empresa (Community Management
  API) requiere una app aprobada por LinkedIn con proceso de revisión, y el scraping va
  contra sus términos de servicio. Los textos de Novedades que prometían "sincronización
  automática desde LinkedIn" se ajustaron; LinkedIn queda como link a la página del grupo.
- **Facebook es la alternativa viable**: el grupo tiene página (facebook.com/GIPISUNPSJB) y
  la Graph API permite a un administrador de la página leer sus propios posts
  (`/{page-id}/posts` con un Page Access Token de larga duración) sin pasar por App Review,
  usando una app propia en modo desarrollo. Requiere que un admin de la página genere el
  token. Los posts traen texto, fecha, imagen (`full_picture`) y link (`permalink_url`).

---

## 📈 Google Search Console (requiere acción de Pablo)

**Prioridad**: Alta, esfuerzo bajo  
**Descripción**: El sitio ya expone `sitemap.xml`, `robots.txt` y datos estructurados
schema.org (organización, personas, novedades). Falta darlo de alta en Search Console
para que Google lo indexe bien y reporte problemas:

1. Entrar a https://search.google.com/search-console con una cuenta de Google del grupo.
2. Agregar propiedad → "Prefijo de la URL" → `https://gipis.unp.edu.ar`.
3. Verificar con la opción "Etiqueta HTML": copiar el `content` de la meta etiqueta
   que da Google y pasárselo a Claude para agregarla al `<head>` del sitio (un deploy).
4. En "Sitemaps", enviar `https://gipis.unp.edu.ar/sitemap.xml`.

---

## 📶 Monitoreo de uptime (requiere acción de Pablo)

**Prioridad**: Media, esfuerzo bajo  
**Descripción**: Avisa por email si el sitio se cae. Pasos:

1. Crear cuenta gratuita en https://uptimerobot.com (50 monitores gratis).
2. Add New Monitor → tipo HTTP(s) → URL `https://gipis.unp.edu.ar` → intervalo 5 min.
3. Configurar alerta al email del grupo (gipis.unp@gmail.com).

---

## 📄 Paginación de novedades — HECHO (2026-08-01)

**Implementado**: 9 novedades por página con pager (Anterior/Siguiente y números),
usando `.paginate()` de Flask-SQLAlchemy.

---

## 📊 ORCID Integration — HECHO (2026-07-31)

**Implementado**: Los miembros pueden cargar su ORCID iD en el perfil (validado con
checksum, se muestra en su página pública) e importar sus trabajos públicos desde
"Mi Producción" con pantalla de revisión (mismo patrón que SIGEVA). Cliente de la API
pública en `app/orcid.py` (sin dependencias nuevas, `urllib`). Los trabajos importados
quedan con `source='orcid'` y se pueden compartir a la página de Investigación.
