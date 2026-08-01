"""
Traducción de la interfaz pública (ES → EN).

El español es el idioma canónico: los templates usan _('texto en español')
y acá se busca la versión en inglés. Si una cadena no está en el
diccionario, se muestra el español tal cual (fallback seguro), así que
agregar textos nuevos nunca rompe nada.

Los nombres de categorías y secciones que vienen de la base también
pasan por _(), por eso figuran acá ('Publicaciones', 'Investigadores', etc.).
"""

LANGUAGES = ('es', 'en')

TRANSLATIONS = {
    # --- Navegación / base ---
    'Inicio': 'Home',
    'Nuestro Equipo': 'Our Team',
    'Investigación': 'Research',
    'Cooperación': 'Cooperation',
    'Novedades': 'News',
    'Contacto': 'Contact',
    'Ingresar': 'Sign in',
    'Grupo': 'Team',
    'Mi Perfil': 'My Profile',
    'Institución': 'Institution',
    'Facultad de Ingeniería': 'Faculty of Engineering',
    'Grupo de Investigación en Procesamiento de la Información y Sensores':
        'Information Processing and Sensors Research Group',
    'Liderando la innovación en el procesamiento de señales y sistemas sensoriales desde la Patagonia para el mundo.':
        'Leading innovation in signal processing and sensor systems from Patagonia to the world.',
    'KM4 Ciudad Universitaria, Comodoro Rivadavia, Chubut':
        'KM4 University Campus, Comodoro Rivadavia, Chubut, Argentina',
    '© 2026 GIPIS | Facultad de Ingeniería | Universidad Nacional de la Patagonia San Juan Bosco':
        '© 2026 GIPIS | Faculty of Engineering | National University of Patagonia San Juan Bosco',

    # --- Home ---
    'GIPIS: Grupo de Investigación en Procesamiento de la Información y Sensores. Investigación de vanguardia en señales digitales, redes de sensores y telecomunicaciones. FI-UNPSJB, Comodoro Rivadavia.':
        'GIPIS: Information Processing and Sensors Research Group. Cutting-edge research in digital signals, sensor networks and telecommunications. FI-UNPSJB, Comodoro Rivadavia.',
    'Universidad Nacional de la Patagonia San Juan Bosco':
        'National University of Patagonia San Juan Bosco',
    'GIPIS: Procesamiento de la Información y Sensores':
        'GIPIS: Information Processing and Sensors',
    'Investigación de vanguardia para la transformación digital y el desarrollo tecnológico regional.':
        'Cutting-edge research for digital transformation and regional technological development.',
    'Explorar Proyectos': 'Explore Projects',
    'Sobre el Grupo': 'About the Group',
    'Fortaleciendo el Sistema Científico-Tecnológico':
        'Strengthening the Scientific and Technological System',
    'Este grupo busca fortalecer la vinculación entre el sistema científico-tecnológico y la estructura productiva en el ámbito de la informática y las telecomunicaciones para afrontar los nuevos desafíos que se proponen con la transformación digital.':
        'This group seeks to strengthen the links between the scientific-technological system and the productive sector in the fields of computer science and telecommunications, in order to meet the new challenges posed by digital transformation.',
    'Nuestras líneas de investigación se centran en el procesamiento digital de señales utilizando sistemas sensoriales desplegados en espacios inteligentes, redes eléctricas y entornos subacuáticos para percibir el estado del entorno y las entidades con las cuales se interactúa.':
        'Our research lines focus on digital signal processing using sensor systems deployed in smart spaces, power grids and underwater environments to perceive the state of the surroundings and the entities they interact with.',
    'Análisis de Datos': 'Data Analysis',
    'Telecomunicaciones': 'Telecommunications',
    'Sensores': 'Sensors',
    'Facultad de Ingeniería UNPSJB': 'Faculty of Engineering, UNPSJB',
    'Novedades Recientes': 'Recent News',
    'Ver todas las noticias': 'View all news',
    'Procesamiento de la Información y Sensores':
        'Information Processing and Sensors',
    'Investigación aplicada en electrónica, sensores y sistemas de información desde la Facultad de Ingeniería de la UNPSJB.':
        'Applied research in electronics, sensors and information systems at the UNPSJB Faculty of Engineering.',
    'Conocé el grupo': 'Meet the group',
    'Nuestra Misión': 'Our Mission',
    'Últimas Novedades': 'Latest News',
    'Ver todas': 'View all',
    'Leer más': 'Read more',
    'Conocé más': 'Learn more',
    'Líneas de Investigación': 'Research Lines',
    'Ver equipo': 'View team',

    # --- Equipo ---
    'Un equipo multidisciplinario de investigadores, docentes y becarios.':
        'A multidisciplinary team of researchers, faculty and fellows.',
    'Conocé al equipo multidisciplinario de investigadores, docentes y becarios del GIPIS. Facultad de Ingeniería, UNPSJB.':
        'Meet the multidisciplinary team of researchers, faculty members and fellows at GIPIS. Faculty of Engineering, UNPSJB.',
    'Contamos con un equipo multidisciplinario de investigadores, docentes y becarios comprometidos con la excelencia académica y la innovación tecnológica en el procesamiento de señales y sistemas sensoriales.':
        'We have a multidisciplinary team of researchers, faculty members and fellows committed to academic excellence and technological innovation in signal processing and sensor systems.',
    'Dirección e Investigación Senior': 'Leadership and Senior Research',
    'Director': 'Director',
    'Datos próximamente disponibles.': 'Information coming soon.',
    'Equipo': 'Team',
    'Miembro del GIPIS, Grupo de Investigación en Procesamiento de la Información y Sensores, UNPSJB.':
        'Member of GIPIS, the Information Processing and Sensors Research Group, UNPSJB.',
    'Ver perfil': 'View profile',
    'Miembro del grupo': 'Group member',
    # Categorías (vienen de la base)
    'Investigadores': 'Researchers',
    'Investigadores Formados': 'Senior Researchers',
    'Investigadores en Formación': 'Researchers in Training',
    'Becarios': 'Fellows',
    'Becarios y Tesistas': 'Fellows and Thesis Students',
    'Colaboradores': 'Collaborators',
    'Personal de Apoyo': 'Support Staff',

    # --- Perfil de miembro ---
    'Publicaciones': 'Publications',
    'Proyectos': 'Projects',
    'Tesis y becarios dirigidos': 'Supervised theses and fellows',
    'Descargar contacto': 'Download contact',
    'Volver al equipo': 'Back to team',
    'Email personal': 'Personal email',
    'Email institucional': 'Institutional email',
    'Teléfono': 'Phone',

    # --- Investigación ---
    'Desarrollamos investigación aplicada en múltiples áreas del procesamiento de señales y sistemas sensoriales.':
        'We carry out applied research across multiple areas of signal processing and sensor systems.',
    'Ver más': 'See more',
    'Ver todos': 'View all',
    'Volver a investigación': 'Back to research',
    # Secciones (vienen de la base)
    'Proyectos de Investigación': 'Research Projects',
    'Transferencias': 'Technology Transfer',
    'Reportes internos': 'Internal Reports',
    'Tesis de maestría': "Master's Theses",
    'Tesis doctorales': 'Doctoral Theses',

    # --- Investigación / Líneas ---
    'Líneas de investigación del GIPIS: procesamiento digital de señales, redes de sensores, telecomunicaciones, sistemas sensoriales y espacios inteligentes.':
        'GIPIS research lines: digital signal processing, sensor networks, telecommunications, sensory systems, and smart environments.',
    'Nuestras actividades de investigación se centran en el desarrollo de soluciones innovadoras mediante el procesamiento de información y el uso avanzado de sensores en diversos entornos.':
        'Our research activities focus on developing innovative solutions through information processing and the advanced use of sensors in a variety of environments.',
    'Saber más': 'Learn more',
    'Procesamiento Digital de Señales': 'Digital Signal Processing',
    'Desarrollo de algoritmos avanzados para el análisis y mejora de señales en diversos contextos, con aplicaciones en biometría y reconocimiento de patrones.':
        'Development of advanced algorithms for signal analysis and enhancement in diverse contexts, with applications in biometrics and pattern recognition.',
    'Redes PLC y Comunicaciones': 'PLC Networks and Communications',
    'Investigación en Power Line Communications (PLC) para la optimización de la transmisión de datos sobre infraestructuras eléctricas existentes.':
        'Research on Power Line Communications (PLC) for optimizing data transmission over existing electrical infrastructure.',
    'Espacios Inteligentes': 'Smart Environments',
    'Implementación de sistemas de sensores interactivos y eficientes en contextos urbanos e inteligentes.':
        'Implementation of interactive, efficient sensor systems in urban and smart contexts.',
    'Sensores Subacuáticos': 'Underwater Sensors',
    'Despliegue y procesamiento de redes de sensores para el monitoreo de entornos marinos y campañas oceanográficas en la Patagonia.':
        'Deployment and processing of sensor networks for monitoring marine environments and oceanographic campaigns in Patagonia.',
    'Sistemas Embebidos y FPGA': 'Embedded Systems and FPGA',
    'Diseño de hardware dedicado para el procesamiento de alta velocidad mediante dispositivos programables para aplicaciones críticas.':
        'Design of dedicated hardware for high-speed processing using programmable devices for critical applications.',
    'Optimización y monitoreo de redes eléctricas inteligentes para mejorar la eficiencia energética y la integración de renovables.':
        'Optimization and monitoring of smart power grids to improve energy efficiency and the integration of renewables.',
    'I+D+i Activo': 'Active R&D&i',
    'Proyectos Activos': 'Active Projects',
    'Los proyectos activos se mostrarán próximamente.': 'Active projects will be published soon.',
    'Línea de investigación del GIPIS.': 'GIPIS research line.',
    'Descripción': 'Description',
    'Esta línea de investigación se enfoca en el desarrollo de soluciones innovadoras mediante técnicas avanzadas de procesamiento de señales y sistemas sensoriales. Nuestro enfoque multidisciplinario permite abordar problemas complejos en diversos contextos.':
        'This research line focuses on developing innovative solutions through advanced signal processing techniques and sensory systems. Our multidisciplinary approach enables us to tackle complex problems in diverse contexts.',
    'Objetivos': 'Objectives',
    'Desarrollar algoritmos y técnicas innovadoras para el procesamiento de señales en tiempo real.':
        'Develop innovative algorithms and techniques for real-time signal processing.',
    'Implementar prototipos funcionales para validar los resultados teóricos.':
        'Implement functional prototypes to validate theoretical results.',
    'Formar recursos humanos especializados en el área.':
        'Train specialized human resources in the field.',
    'Transferir conocimientos y tecnologías al sector productivo.':
        'Transfer knowledge and technologies to the productive sector.',
    'Metodologías': 'Methodologies',
    'Modelado matemático y simulación': 'Mathematical modeling and simulation',
    'Prototipado rápido': 'Rapid prototyping',
    'Validación experimental': 'Experimental validation',
    'Transferencia tecnológica': 'Technology transfer',
    'Tecnologías': 'Technologies',
    'Aplicaciones': 'Applications',
    'Industria': 'Industry',
    'Automatización y control': 'Automation and control',
    'Oceanografía': 'Oceanography',
    'Monitoreo marino': 'Marine monitoring',
    'Energía': 'Energy',
    'Redes inteligentes': 'Smart grids',
    'Volver a Líneas de Investigación': 'Back to Research Lines',

    # --- Cooperación ---
    'Cooperación científica e industrial del GIPIS. Vínculos con el sector productivo, convenios de investigación y transferencia tecnológica desde la Patagonia.':
        'Scientific and industrial cooperation at GIPIS. Ties with the productive sector, research agreements, and technology transfer from Patagonia.',
    'Campus Universitario': 'University Campus',
    'Cooperación Científica e Industrial': 'Scientific and Industrial Cooperation',
    'Desarrollamos vinculaciones estratégicas con instituciones académicas, centros de investigación y el sector productivo.':
        'We build strategic partnerships with academic institutions, research centers and industry.',
    'Redes Académicas': 'Academic Networks',
    'Convenios de colaboración con universidades nacionales e internacionales para intercambio científico.':
        'Collaboration agreements with national and international universities for scientific exchange.',
    'Transferencia Industrial': 'Industrial Transfer',
    'Soluciones profesionales y asesoría técnica para empresas del sector energético y telecomunicaciones.':
        'Professional solutions and technical consulting for companies in the energy and telecommunications sectors.',
    'Proyectos Conjuntos': 'Joint Projects',
    'Planificación y ejecución de proyectos I+D+i con financiamiento público, privado e institucional.':
        'Planning and execution of R&D&i projects with public, private and institutional funding.',
    'Red de Colaboración': 'Collaboration Network',
    'Colaboramos con prestigiosas organizaciones para potenciar el desarrollo tecnológico regional y nacional.':
        'We collaborate with prestigious organizations to boost regional and national technological development.',
    'Oportunidades de Cooperación': 'Cooperation Opportunities',
    '¿Su institución o empresa está interesada en colaborar con nosotros? Buscamos constantemente nuevos socios para proyectos de investigación, tesis doctorales y consultoría tecnológica.':
        'Is your institution or company interested in collaborating with us? We are always looking for new partners for research projects, doctoral theses and technology consulting.',
    'Becas de postgrado conjuntas': 'Joint postgraduate scholarships',
    'Prácticas profesionales': 'Professional internships',
    'I+D para el sector industrial': 'R&D for industry',
    'Proyectos internacionales': 'International projects',
    'Iniciar una Propuesta': 'Start a Proposal',
    'Contactar': 'Contact us',

    # --- Novedades ---
    'Enterate de las últimas actividades, logros y anuncios del grupo.':
        'Stay up to date with the latest activities, achievements and announcements of the group.',
    'Volver a novedades': 'Back to news',
    'No hay novedades publicadas por el momento.': 'There are no news posted at the moment.',
    'No hay novedades aún.': 'No news yet.',
    'Novedades y noticias del GIPIS. Congresos, publicaciones, proyectos y actividades del grupo de investigación.':
        'News and updates from GIPIS. Conferences, publications, projects and activities of the research group.',
    'Publicado en Facebook': 'Posted on Facebook',
    'Novedad del GIPIS, Grupo de Investigación en Procesamiento de la Información y Sensores.':
        'News from GIPIS, the Information Processing and Sensors Research Group.',
    'Detalle': 'Detail',
    'Volver a Novedades': 'Back to News',
    'Anterior': 'Previous',
    'Siguiente': 'Next',
    'Paginación': 'Pagination',

    # --- Producción científica ---
    'Producción Científica': 'Scientific Production',
    'Producción': 'Production',
    'Producción científica del GIPIS: publicaciones, proyectos y tesis del grupo de investigación.':
        'Scientific production of GIPIS: publications, projects and theses of the research group.',
    'Publicaciones, proyectos y tesis del grupo. Usá los filtros para encontrar trabajos específicos.':
        'Publications, projects and theses of the group. Use the filters to find specific works.',
    'Buscar por título o autor…': 'Search by title or author…',
    'Todos los años': 'All years',
    'Todas las secciones': 'All sections',
    'Limpiar filtros': 'Clear filters',
    'No se encontraron resultados con esos filtros.': 'No results were found with those filters.',
    'La producción del grupo se mostrará próximamente.': "The group's production will be published soon.",
    'Ver toda la producción': 'View all production',
    'Citar (BibTeX)': 'Cite (BibTeX)',
    'citas': 'citations',
    '¡Copiado!': 'Copied!',
    'Software y Repositorios': 'Software & Repositories',
    'Ver en GitHub': 'View on GitHub',

    # --- Contacto ---
    'Estamos interesados en establecer nuevas colaboraciones y responder tus consultas.':
        'We are interested in establishing new collaborations and answering your inquiries.',
    'Envianos tu consulta': 'Send us your inquiry',
    'Nombre completo': 'Full name',
    'Correo electrónico': 'Email address',
    'Asunto': 'Subject',
    'Mensaje': 'Message',
    'Enviar mensaje': 'Send message',
    'Información de contacto': 'Contact information',
    'Dirección': 'Address',
    'Seguinos en redes': 'Follow us',
    'Escribinos y te responderemos a la brevedad.':
        'Write to us and we will get back to you shortly.',
    'Contactá al GIPIS. Consultas académicas, propuestas de cooperación científica o información sobre líneas de investigación. Ciudad Universitaria, Comodoro Rivadavia.':
        'Contact GIPIS. Academic inquiries, scientific cooperation proposals or information about research lines. Ciudad Universitaria, Comodoro Rivadavia.',
    'Contáctenos': 'Contact Us',
    'Estamos a su disposición para consultas académicas, propuestas de cooperación científica o información sobre nuestras líneas de investigación.':
        'We are at your disposal for academic inquiries, scientific cooperation proposals or information about our research lines.',
    'Nombre Completo': 'Full Name',
    'Ej: Dr. Juan Pérez': 'E.g.: Dr. John Smith',
    'Correo Electrónico': 'Email Address',
    'nombre@institucion.edu': 'name@institution.edu',
    'Ej: Consulta sobre Redes de Sensores': 'E.g.: Inquiry about Sensor Networks',
    'Escriba su consulta aquí...': 'Write your inquiry here...',
    'Enviar Mensaje': 'Send Message',
    'Dirección Postal': 'Postal Address',
    'Ver en Google Maps': 'View on Google Maps',

    # --- Panel de miembros y administración ---
    # Login / recuperación de contraseña
    'Bienvenido': 'Welcome',
    'Ingresá con tu cuenta de miembro': 'Sign in with your member account',
    'Contraseña': 'Password',
    '¿Olvidaste tu contraseña?': 'Forgot your password?',
    'Volver al inicio': 'Back to home',
    '¿No tenés cuenta? Contactá al administrador del grupo.':
        "Don't have an account? Contact the group administrator.",
    'Recuperar contraseña': 'Reset your password',
    'Ingresá tu email y te enviamos un enlace para restablecerla.':
        'Enter your email and we will send you a link to reset it.',
    'Enviar enlace': 'Send link',
    'Volver al ingreso': 'Back to sign in',
    'Nueva contraseña': 'New password',
    'Hola': 'Hello',
    'definí tu nueva contraseña.': 'set your new password.',
    'Mínimo 8 caracteres': 'At least 8 characters',
    'Repetir contraseña': 'Repeat password',
    'Guardar contraseña': 'Save password',
    # Dashboard
    'Acá podés administrar tu información.': 'Here you can manage your information.',
    'Cerrar sesión': 'Sign out',
    'Ver perfil público': 'View public profile',
    'Administración': 'Administration',
    'Miembros': 'Members',
    'Información actual': 'Current information',
    'Público': 'Public',
    'Privado': 'Private',
    'Con este email iniciás sesión': 'You sign in with this email',
    'Título/Grado': 'Degree',
    'Cargo/Posición': 'Position',
    'Biografía': 'Biography',
    'Sin biografía': 'No biography',
    'Editar mi perfil': 'Edit my profile',
    'Mi Producción': 'My Production',
    # Editar perfil
    'Editar Perfil': 'Edit Profile',
    'Volver al dashboard': 'Back to dashboard',
    'Foto de perfil': 'Profile photo',
    'Hacé click o arrastrá una imagen': 'Click or drag an image',
    'PNG, JPG o WebP • Máximo 10 MB': 'PNG, JPG or WebP • 10 MB max',
    'Eliminar foto actual': 'Remove current photo',
    'Información básica': 'Basic information',
    'Nombre completo *': 'Full name *',
    'Título / Grado académico': 'Degree / Academic title',
    'Ej: Dr. en Ingeniería': 'E.g.: PhD in Engineering',
    'Cargo / Posición': 'Position',
    'Ej: Investigador Principal': 'E.g.: Principal Investigator',
    'Contanos sobre tu trayectoria, áreas de interés, etc.':
        'Tell us about your background, areas of interest, etc.',
    'Biografía en inglés (opcional)': 'Biography in English (optional)',
    'Si la dejás vacía, los visitantes en inglés ven tu biografía en español.':
        'If you leave it empty, English-language visitors will see your Spanish biography.',
    'LinkedIn (URL completa)': 'LinkedIn (full URL)',
    'Tu identificador de': 'Your identifier from',
    'Se muestra en tu perfil público y permite importar tus publicaciones desde "Mi Producción".':
        'It is shown on your public profile and lets you import your publications from "My Production".',
    'Emails de contacto': 'Contact emails',
    'Podés elegir qué emails se muestran en tu perfil público y con cuáles podés iniciar sesión (tu email de acceso original':
        'You can choose which emails are shown on your public profile and which ones you can sign in with (your original sign-in email',
    'siempre funciona).': 'always works).',
    'Mostrar en perfil público': 'Show on public profile',
    'Permitir iniciar sesión con este email': 'Allow signing in with this email',
    'Teléfono de contacto': 'Contact phone',
    'Cambiar contraseña': 'Change password',
    '(opcional)': '(optional)',
    'Dejá en blanco para no cambiarla': 'Leave blank to keep it unchanged',
    'Mínimo 6 caracteres. Hacé click en el ojo para ver la contraseña.':
        'At least 6 characters. Click the eye icon to reveal the password.',
    'La imagen no puede superar los 10 MB.': 'The image cannot exceed 10 MB.',
    'Guardar cambios': 'Save changes',
    'Cancelar': 'Cancel',
    # Mi Producción
    'Tus publicaciones, proyectos y direcciones. Lo que compartas aparece también en la página de Investigación del sitio.':
        "Your publications, projects and supervisions. Whatever you share also appears on the site's Research page.",
    'Volver al panel': 'Back to dashboard',
    'Importar desde SIGEVA': 'Import from SIGEVA',
    'Subí el PDF de tu CV exportado de SIGEVA (Banco de datos → Imprimir CV). Vas a poder revisar y elegir qué importar antes de guardar.':
        'Upload the PDF of your CV exported from SIGEVA (Data bank → Print CV). You will be able to review and choose what to import before saving.',
    'Analizar PDF': 'Analyze PDF',
    'Importar desde ORCID': 'Import from ORCID',
    'Vamos a buscar los trabajos públicos de tu registro':
        'We will look up the public works from your record',
    'Vas a poder revisar y elegir qué importar antes de guardar.':
        'You will be able to review and choose what to import before saving.',
    'Buscar mis publicaciones': 'Find my publications',
    'Ingresá tu ORCID iD (o la URL de tu perfil en orcid.org) para buscar tus trabajos públicos. Se guarda en tu perfil para la próxima vez.':
        'Enter your ORCID iD (or your orcid.org profile URL) to look up your public works. It is saved to your profile for next time.',
    'Buscar publicaciones': 'Find publications',
    'Descubrir publicaciones (OpenAlex)': 'Discover publications (OpenAlex)',
    'OpenAlex indexa publicaciones de toda la literatura académica, incluso las que no cargaste en ORCID. Buscamos por tu ORCID iD y te mostramos lo que encuentre, con su cantidad de citas. Ojo: puede traer atribuciones erróneas — revisá antes de importar.':
        'OpenAlex indexes publications from across the academic literature, including ones you did not add to ORCID. We search by your ORCID iD and show you what it finds, with citation counts. Note: it may include incorrect attributions — review before importing.',
    'Buscar en OpenAlex': 'Search OpenAlex',
    'Cargá tu ORCID iD (en la tarjeta de arriba o en tu perfil) y vas a poder descubrir publicaciones tuyas indexadas en OpenAlex, con su cantidad de citas.':
        'Add your ORCID iD (in the card above or in your profile) and you will be able to discover your publications indexed in OpenAlex, with citation counts.',
    'Agregar trabajo a mano': 'Add a work manually',
    '¿Tenés el DOI? Completá los campos automáticamente':
        'Have the DOI? Fill in the fields automatically',
    '10.1109/5.771073 o https://doi.org/…': '10.1109/5.771073 or https://doi.org/…',
    'Buscar DOI': 'Look up DOI',
    'Título *': 'Title *',
    'Tipo': 'Type',
    'Año': 'Year',
    'Autores': 'Authors',
    'Agregar': 'Add',
    'En el sitio': 'On the site',
    'Quitar de la página de Investigación': 'Remove from the Research page',
    'Compartir al sitio': 'Share to the site',
    'Guardar': 'Save',
    '¿Eliminar este trabajo de tu producción?': 'Delete this work from your production?',
    'Eliminar': 'Delete',
    'Todavía no cargaste ningún trabajo. Importá tu CV de SIGEVA o agregá uno a mano.':
        'You have not added any works yet. Import your SIGEVA CV or add one manually.',
    'Ingresá un DOI.': 'Enter a DOI.',
    'Consultando…': 'Looking up…',
    'Datos cargados. Revisalos antes de agregar.': 'Data loaded. Review it before adding.',
    'No se pudo consultar el DOI.': 'Could not look up the DOI.',
    # Revisión de importaciones
    'Revisar importación': 'Review import',
    'Destildá lo que no tenga relevancia para el grupo y confirmá. Después vas a poder editar cada trabajo y elegir cuáles compartir en la página de Investigación.':
        'Uncheck anything not relevant to the group and confirm. Afterwards you will be able to edit each work and choose which ones to share on the Research page.',
    'Ya está en tu producción': 'Already in your production',
    'Importar seleccionados': 'Import selected',
    'Esto es lo que encontramos en tu CV de SIGEVA.': 'This is what we found in your SIGEVA CV.',
    'Datos de perfil': 'Profile data',
    'Reemplaza tu valor actual:': 'Replaces your current value:',
    'Biografía (resumen de experticia):': 'Biography (expertise summary):',
    'Reemplaza tu biografía actual.': 'Replaces your current biography.',
    # Admin: miembros
    'Administrar Miembros': 'Manage Members',
    'Alta de nuevos integrantes y gestión de roles.': 'Add new members and manage roles.',
    'Nuevo integrante': 'New member',
    'Contraseña inicial *': 'Initial password *',
    'El integrante puede cambiarla desde su perfil.': 'The member can change it from their profile.',
    'Categoría *': 'Category *',
    '— Elegir categoría —': '— Choose a category —',
    'Determina en qué bloque aparece en la página del grupo.':
        'Determines which block they appear in on the team page.',
    'Ej: Ing. Electrónico': 'E.g.: Electronic Engineer',
    'Ej: Investigador': 'E.g.: Researcher',
    'Rol': 'Role',
    'Miembro': 'Member',
    'Administrador': 'Administrator',
    'Crear integrante': 'Create member',
    'Integrantes': 'Members',
    'Nombre': 'Name',
    'Categoría': 'Category',
    'Estado': 'Status',
    'Acciones': 'Actions',
    '⚠ Sin categoría': '⚠ No category',
    'Activo': 'Active',
    'Inactivo': 'Inactive',
    'Quitar admin': 'Remove admin',
    'Hacer admin': 'Make admin',
    'Desactivar': 'Deactivate',
    'Activar': 'Activate',
    '¿Generar una contraseña temporal para': 'Generate a temporary password for',
    'La actual dejará de funcionar.': 'The current one will stop working.',
    'Restablecer contraseña': 'Reset password',
    '(vos)': '(you)',
    # Admin: investigación
    'Administrar Investigación': 'Manage Research',
    'Secciones e ítems (publicaciones, proyectos, tesis, etc.) que se muestran en la página de Investigación.':
        'Sections and items (publications, projects, theses, etc.) shown on the Research page.',
    'Agregar ítem': 'Add item',
    'Sección *': 'Section *',
    'Resumen / detalle': 'Summary / detail',
    'Nueva sección': 'New section',
    'Ej: Patentes': 'E.g.: Patents',
    'Crear sección': 'Create section',
    'ítems': 'items',
    'Resumen': 'Summary',
    '¿Eliminar este ítem del sitio?': 'Delete this item from the site?',
    'Sin ítems.': 'No items.',
    # Admin: red de colaboración
    'Organizaciones que se muestran en la página de Cooperación.':
        'Organizations shown on the Cooperation page.',
    'Agregar organización': 'Add organization',
    'Nombre de la organización *': 'Organization name *',
    'Sitio web (opcional)': 'Website (optional)',
    '(opcional, PNG/JPG/WebP/SVG, idealmente con fondo transparente)':
        '(optional, PNG/JPG/WebP/SVG, ideally with a transparent background)',
    'Orden': 'Order',
    'Sitio web': 'Website',
    'Quitar logo': 'Remove logo',
    '¿Quitar': 'Remove',
    'de la Red de Colaboración?': 'from the Collaboration Network?',
    'No hay organizaciones cargadas.': 'No organizations added yet.',
    # Admin: novedades
    'Cargá y administrá las novedades que se muestran en el sitio y en la portada.':
        'Add and manage the news shown on the site and on the home page.',
    'Publicar novedad': 'Publish news',
    'Congresos, Proyectos, Publicaciones…': 'Conferences, Projects, Publications…',
    'Fecha': 'Date',
    '(se muestra en las tarjetas)': '(shown on the cards)',
    'Contenido': 'Content',
    '(texto de la novedad; separá párrafos con una línea en blanco)':
        '(news text; separate paragraphs with a blank line)',
    'Imagen': 'Image',
    '(opcional, PNG/JPG/WebP)': '(optional, PNG/JPG/WebP)',
    'Traducción al inglés (opcional)': 'English translation (optional)',
    'Si se completa, los visitantes que usen el sitio en inglés verán esta versión; si no, se muestra el texto en español.':
        'If provided, visitors using the site in English will see this version; otherwise the Spanish text is shown.',
    'Publicar': 'Publish',
    'Sin fecha': 'No date',
    'Ver en el sitio': 'View on the site',
    'Quitar imagen actual': 'Remove current image',
    '¿Eliminar la novedad': 'Delete the news item',
    'Todavía no hay novedades cargadas.': 'No news added yet.',
    # Botones admin en páginas públicas
    'Gestionar novedades': 'Manage news',
    'Gestionar red de colaboración': 'Manage collaboration network',
    'Gestionar miembros': 'Manage members',
    'Gestionar investigación': 'Manage research',
}


MONTHS = {
    'es': ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
           'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July',
           'August', 'September', 'October', 'November', 'December'],
}


def format_date(dt, lang='es', short=False):
    """Formatear fecha según el idioma de la interfaz ('1 de agosto de 2026',
    'August 1, 2026'; short: '1 ago, 2026' / 'Aug 1, 2026')."""
    if not dt:
        return ''
    month = MONTHS.get(lang, MONTHS['es'])[dt.month - 1]
    if lang == 'en':
        return f'{month[:3]} {dt.day}, {dt.year}' if short else f'{month} {dt.day}, {dt.year}'
    return f'{dt.day} {month[:3]}, {dt.year}' if short else f'{dt.day} de {month} de {dt.year}'


def translate(text, lang):
    """Traducir una cadena; si no hay traducción, devolver el original."""
    if lang == 'en':
        return TRANSLATIONS.get(text, text)
    return text
