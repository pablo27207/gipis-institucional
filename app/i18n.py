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
    'Congreso Científico': 'Scientific Conference',
    'Miembros del GIPIS presentaron avances significativos en el desarrollo de redes de sensores subacuáticos durante la última edición...':
        'GIPIS members presented significant advances in the development of underwater sensor networks during the latest edition...',
    'En el marco de las redes eléctricas, las investigaciones se enfocan en esquemas de modulación de multiplexación por división de frecuencia ortogonal (OFDM)...':
        'In the context of power grids, research focuses on orthogonal frequency-division multiplexing (OFDM) modulation schemes...',
    'Se ha firmado un convenio para la implementación de dispositivos programables FPGA en el monitoreo de campañas oceanográficas...':
        'An agreement has been signed for the implementation of FPGA programmable devices in the monitoring of oceanographic campaigns...',
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
    'Producción': 'Scientific Output',
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
    'Producción Científica': 'Scientific Output',
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
    'Novedades y noticias del GIPIS. Congresos, publicaciones, proyectos y actividades del grupo de investigación.':
        'News and updates from GIPIS. Conferences, publications, projects and activities of the research group.',
    'Publicado en Facebook': 'Posted on Facebook',
    'Participación en el Congreso Nacional de Procesamiento':
        'Participation in the National Congress on Signal Processing',
    'Miembros del GIPIS presentaron avances significativos en el desarrollo de redes de sensores subacuáticos...':
        'GIPIS members presented significant advances in the development of underwater sensor networks...',
    'Nuevas técnicas de sincronización para PLC': 'New synchronization techniques for PLC',
    'En el marco de las redes eléctricas, las investigaciones se enfocan en esquemas OFDM...':
        'Within the framework of power line networks, research focuses on OFDM schemes...',
    'Alianza Estratégica con Sector Productivo Local':
        'Strategic Partnership with the Local Productive Sector',
    'Se ha firmado un convenio para la implementación de dispositivos programables FPGA...':
        'An agreement has been signed for the implementation of FPGA programmable devices...',
    'Novedad del GIPIS, Grupo de Investigación en Procesamiento de la Información y Sensores.':
        'News from GIPIS, the Information Processing and Sensors Research Group.',
    'Detalle': 'Detail',
    'Volver a Novedades': 'Back to News',

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
}


def translate(text, lang):
    """Traducir una cadena; si no hay traducción, devolver el original."""
    if lang == 'en':
        return TRANSLATIONS.get(text, text)
    return text
