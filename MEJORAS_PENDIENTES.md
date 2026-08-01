# Mejoras Pendientes — GIPIS

Ideas y funcionalidades a implementar en el futuro.

---

## 🔍 Búsqueda y filtrado de publicaciones

**Prioridad**: Media  
**Descripción**: En la sección de investigación, permitir a los visitantes buscar y filtrar publicaciones por:
- Año de publicación
- Autor/investigador
- Palabras clave
- Línea de investigación

**Notas**: Sería útil para visitantes académicos que buscan papers específicos. Se podría implementar con filtros dinámicos en el frontend (JavaScript) sin necesidad de consultas al backend, dado que el volumen de publicaciones es manejable.

---

## 🔄 Harvesting de novedades desde redes sociales

**Prioridad**: Alta  
**Descripción**: Alimentar automáticamente las tarjetas de Novedades con las publicaciones
del grupo en redes sociales.

**Estado (2026-07-31)**:
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

## 📄 Paginación de novedades

**Prioridad**: Media (crece con el tiempo)  
**Descripción**: Implementar paginación en la página de novedades para evitar que la página crezca indefinidamente.

**Notas**: Ya hay un `# TODO` en el código. Implementar después de que haya suficiente contenido para justificarlo (~20+ novedades). Flask-SQLAlchemy tiene `.paginate()` integrado.

---

## 📊 ORCID Integration — HECHO (2026-07-31)

**Implementado**: Los miembros pueden cargar su ORCID iD en el perfil (validado con
checksum, se muestra en su página pública) e importar sus trabajos públicos desde
"Mi Producción" con pantalla de revisión (mismo patrón que SIGEVA). Cliente de la API
pública en `app/orcid.py` (sin dependencias nuevas, `urllib`). Los trabajos importados
quedan con `source='orcid'` y se pueden compartir a la página de Investigación.
