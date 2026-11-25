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

## Marcador de casilla para Bedrock: prototipo adicional

`packs/DanusMochilas-Casilla-Bedrock-EXPERIMENTAL.mcpack` contiene una modificación visual pequeña del panel de inventario clásico basada en el panel común de Bedrock 1.26.60. Se comprobó que Geyser ofrece el pack a un cliente de protocolo simulado; **no se ha comprobado visualmente ni se ha demostrado que la interacción, las coordenadas o la interfaz táctil funcionen**. No instalar en producción ni combinar sin revisar otros packs de interfaz. El paquete no muestra la mochila en 3D ni cambia los objetos del jugador.

## Candidato para mano 3D y casilla amarilla

El pack de iconos en producción solo cambia el dibujo de los cuatro objetos. Este candidato conserva los iconos y añade cuatro modelos para la mano en primera y tercera persona. La casilla amarilla se entrega aparte para probar la interfaz clásica y táctil de Bedrock 1.26.60 por separado. El marco es decorativo: señala la primera casilla de la fila superior del inventario principal de Survival (índice 9 del backend), sin cambiar el botón, el desplazamiento ni el almacenamiento. La posición del marco debe confirmarse en ambos perfiles de interfaz.

Para probar en un proxy aislado:

1. Sustituye el pack de iconos anterior por `packs/DanusMochilas-Mano-3D-CANDIDATO.mcpack`. Conserva `custom_mappings/danus-iconos.json`. El pack nuevo usa el mismo UUID que el pack de iconos publicado y una versión superior, por lo que debe haber solo uno de los dos. Reinicia el proxy de pruebas y reconecta.
2. Añade `packs/DanusMochilas-Casilla-CANDIDATO.mcpack` por separado. Si el proxy ya tiene el prototipo de la casilla, sustitúyelo. Comprueba que no choque con otros archivos JSON de interfaz y que se pueda mover la mochila y otros objetos con ratón, táctil y mando. Comprueba otras pantallas de inventario y cofres.
3. Para probar la espalda, añade `packs/DanusMochilas-Espalda-CANDIDATO.mcpack` y `custom_mappings/danus-visual.json`. Si ya tienes el pack experimental de espalda, sustitúyelo, ya que los dos comparten UUID. El candidato alinea los cuatro modelos con el torso y orienta el bolsillo hacia afuera. Verifica que el backend reconozca la sesión por Floodgate y entonces configura `bedrock-visual.enabled: true` en el backend de prueba. Empieza con `bedrock-visual.show-with-equipment: false` y con el torso vacío. Pon la mochila en la primera casilla de la fila superior del inventario (fuera de la barra rápida) y comprueba la espalda en tercera persona y desde otra cuenta. Es el mismo equipamiento virtual que en el prototipo y no necesita entidades. Para armaduras, prueba la otra opción aparte. El aspecto con élitros sigue fuera de cobertura.
4. Comprueba los cuatro niveles, primera y tercera persona, inventario con mochila nueva y antigua, guardar y recuperar contenido, y la coexistencia de clientes Java. Guarda capturas. Si falla la interfaz, retira solo el pack de la casilla. Si falla el modelo de la mano, restaura el pack de iconos anterior. Si falla la espalda, desactiva el ajuste de backend y retira el pack y su mapeo.

Generación reproducible desde los assets originales: `python tools/build_visual_packs.py`.

El cliente automatizado puede comprobar qué pack anuncia Geyser y qué objetos traduce. La orientación, tamaño, posición y apariencia de los modelos y del marco requieren un cliente que renderice imágenes.

El recuadro junto al personaje es la mano secundaria. La mochila que aparece ahí es el objeto sostenido. Para ver el modelo de espalda deja las dos manos libres y coloca la mochila en la casilla 9, arriba a la izquierda del inventario principal. El indicador amarillo es independiente del estado de equipamiento.
