# Prueba técnica Akila

Solución reproducible para los ejercicios de triaje de correos y dashboard de ventas.

## Ejecución

El script usa Python 3.10+ y la biblioteca estándar. Si los CSV no están en la carpeta, los descarga automáticamente desde el repositorio oficial de la prueba.

    python solution.py

Genera:

- seguimiento_correos.csv con las columnas Fecha, Cliente, Tipo, Urgencia, Acción y Responsable.
- dashboard.html con indicadores ejecutivos, tipos vendidos y ventas por semana.

Abrir después dashboard.html en el navegador.

## Resultados validados

- 457 apartamentos.
- 271 vendidos.
- 186 disponibles.
- 5 tipos de producto.
- Las semanas comienzan el lunes.

## Decisiones de automatización

La IA puede proponer extracción, clasificación, resumen y responsable. Se mantienen bajo revisión humana las reclamaciones, devoluciones, instrucciones bancarias, cambios de obra, compromisos legales y mensajes ambiguos. El script detecta duplicados y notificaciones automáticas.

## Limitaciones

La solución es una demostración local. En producción añadiría conexión segura al buzón/CRM, autenticación, auditoría, métricas de precisión, monitoreo y aprobación humana para acciones sensibles.

Fuente de datos: https://github.com/akiladesarrollo/tech_interview
