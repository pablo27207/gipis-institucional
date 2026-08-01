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

## 🔄 Harvesting desde LinkedIn — DESCARTADO (2026-07-31)

**Decisión**: Se descartó la sincronización automática desde LinkedIn. La API oficial
(Community Management API) requiere una app aprobada por LinkedIn con proceso de revisión,
y el scraping va contra los términos de servicio. En su lugar se implementó la
**integración con ORCID** (ver abajo) y se ajustaron los textos de Novedades para no
prometer una sincronización que no existe (LinkedIn queda como link a la página del grupo).

Si en el futuro se quiere retomar: la alternativa razonable es carga semi-manual de
novedades con link al post original de LinkedIn.

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
