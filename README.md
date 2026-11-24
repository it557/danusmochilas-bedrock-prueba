# DanusMochilas Bedrock — prueba experimental

**No es una version de produccion.** Este repositorio permite preparar una prueba coordinada de Bedrock en una instalacion aislada. Los modelos 3D no se han probado en un cliente Bedrock real; el recurso de Java, el inventario real, las armaduras y el almacenamiento deben permanecer intactos.

## Archivos

- `packs/DanusMochilas-3D-EXPERIMENTAL.mcpack`: 4 geometrías y variantes de seis pecheras.
- `custom_mappings/danus-visual.json`: 28 mapeos de pecheras visuales.
- `packs/DanusMochilas-iconos-EXPERIMENTAL.mcpack` y `custom_mappings/danus-iconos.json`: iconos de objetos de los cuatro niveles.

Para Velocity 4.3.1 + Geyser-Velocity 2.12.1 build 1306. Los archivos del proxy **no bastan por sí solos**: el backend debe ejecutar una versión específica de DanusMochilas con soporte Bedrock y disponer de identificación Floodgate en el backend. El plugin del backend y la configuración no están publicados en este repositorio. No activar hasta que quien administra el survival haya confirmado la versión y el estado de la integración.

## Para el administrador del proxy

1. Preparar una instancia aislada, identificar versiones y respaldar los packs, mappings y configuración existentes. No copiar secretos a este repositorio.
2. Confirmar que Floodgate está correctamente configurado en el proxy y que el backend puede identificar a esos jugadores. Comprobar que custom content está activado, y revisar las políticas de descarga de packs y si existen mapeos que entren en conflicto.
3. Solo en la instancia de prueba, añadir los dos `.mcpack` a `plugins/Geyser-Velocity/packs/` y los dos JSON a `plugins/Geyser-Velocity/custom_mappings/`, sin sustituir archivos existentes. Reiniciar el proxy de prueba y revisar los mensajes de carga. Los packs Bedrock se negocian al conectar; los jugadores deben reconectar.
4. Coordinar con el administrador del backend antes de habilitar `bedrock-visual.enabled` o `bedrock-visual.show-with-equipment`: faltan verificación de aceptación del pack y pruebas de coexistencia. Las dos opciones son experimentales y están desactivadas por defecto en el prototipo.
5. Probar con un cliente Bedrock real los cuatro niveles con torso vacío y las pecheras; revisar tercera persona, otros observadores, texturas, animaciones, inventario, almacenamiento, daño, encantamientos y tintes, y repetir con clientes Java. Probar también rechazar o no cargar el pack. Si falla, desactivar las opciones y restaurar la configuración de prueba.

## Límites y resultados

En un laboratorio con cliente automatizado de protocolo Bedrock 1.26.60, Geyser registró 28 variantes y se observaron sus identificadores; se comprobó el tipo del equipo real en 32 combinaciones. Floodgate se simuló; el cliente no renderiza imágenes. Esto **no demuestra** compatibilidad visual o de jugabilidad completa. `min_engine_version` es provisional, no una versión mínima verificada.

Los élitros conservan su comportamiento normal pero actualmente no muestran la mochila: Geyser utiliza el identificador vanilla para conservar el vuelo. La pechera de cobre tampoco está cubierta. No se crean entidades de seguimiento.

Referencias: [mapeos de Geyser](https://geysermc.org/wiki/geyser/custom-items/), [packs de Geyser](https://geysermc.org/wiki/geyser/packs/), [modelos attachable de Bedrock](https://learn.microsoft.com/en-us/minecraft/creator/documents/attachables?view=minecraft-bedrock-stable), [GliderUtils de Geyser](https://github.com/GeyserMC/Geyser/blob/cb04ea8afe63e76b7c8219810faa47534bf7f2fc/core/src/main/java/org/geysermc/geyser/util/GliderUtils.java).
