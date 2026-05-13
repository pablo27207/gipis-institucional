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

## 🔄 Harvesting desde LinkedIn

**Prioridad**: Alta  
**Descripción**: Sincronizar automáticamente la información de los perfiles de miembros con sus datos en LinkedIn (publicaciones, experiencia, educación).

**Consideraciones**:
- La API oficial de LinkedIn tiene restricciones importantes (requiere app aprobada)
- Alternativas: scraping controlado, importación manual periódica, o integración con ORCID (más abierto para perfiles académicos)
- Evaluar ORCID como complemento/alternativa

---

## 📄 Paginación de novedades

**Prioridad**: Media (crece con el tiempo)  
**Descripción**: Implementar paginación en la página de novedades para evitar que la página crezca indefinidamente.

**Notas**: Ya hay un `# TODO` en el código. Implementar después de que haya suficiente contenido para justificarlo (~20+ novedades). Flask-SQLAlchemy tiene `.paginate()` integrado.

---

## 📊 ORCID Integration

**Prioridad**: Baja  
**Descripción**: Permitir a los miembros vincular su perfil ORCID para importar automáticamente sus publicaciones académicas. La API de ORCID es abierta y está diseñada para este tipo de integración.
