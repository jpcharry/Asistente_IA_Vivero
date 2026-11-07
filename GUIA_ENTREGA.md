# Guía breve para entregar — Semana 5

1. **Extraer** el ZIP completo en el escritorio y entrar a la carpeta `Charry_JuanPablo_S5_AsistenteIA_Vivero`.
2. **Verificar pruebas:** `python -m pip install -r requirements.txt` y luego `python -m pytest -v`. Deben aparecer 14 pruebas aprobadas (si el entorno cumple dependencias).
3. **Comprobar el historial:** `git log --oneline --reverse`. Deben verse 4 commits, incluidos los 3 exigidos.
4. **Leer la bitácora:** `bitacora_ia.md`, con cinco entradas, decisiones aceptada/ajustada/rechazada y reflexión.
5. **Si se usa GitHub:** crear desde la web un repositorio vacío llamado `asistente-ia-vivero-semana5` (sin README ni `.gitignore` nuevos); en PowerShell, dentro de esta carpeta, ejecutar:

```powershell
git remote add origin https://github.com/TU_USUARIO/asistente-ia-vivero-semana5.git
git branch -M main
git push -u origin main
```

El repositorio ya tiene `.git` e historial de commits. Sustituir `TU_USUARIO` con el nombre de usuario de GitHub. Si `origin` ya existe, verificar con `git remote -v` antes de cambiarlo.

6. **En Moodle:** pegar la URL de tu repositorio. Si se deja privado, dar acceso al docente. La actividad también permite entregar el ZIP con `.git` si no es posible usar repositorio en línea.

## Qué explicar si el docente pregunta

- *¿Qué implementaron?* La HU-03: sugerir la categoría mediante un proveedor configurable y registrar la sugerencia en un diccionario de incidencias.
- *¿Dónde está la IA?* En la interfaz `servicio_ia`; puede conectarse con el adaptador real `ProveedorOpenAI`, pero las pruebas usan dobles para ser repetibles y no requerir credenciales.
- *¿Qué pasa si se cae la IA?* No se borra el reporte ni se inventa una categoría; devuelve un mensaje de error.
- *¿Qué significa verde?* Que las pruebas automatizadas pasaron después de agregar implementación.
- *¿Qué se refactorizó?* Se cambió una cadena de condicionales por una tabla de categorías en un auxiliar; el comportamiento se mantuvo y las pruebas siguieron aprobadas.
- *¿Por qué no se modifica el inventario?* El asistente solo sugiere, el administrador debe revisar y aprobar según el alcance de semana 3.

## Pendiente fuera del alcance de este paquete

Este entorno no publica en tu cuenta de GitHub ni conoce tu usuario o las credenciales de un proveedor externo. Se entrega listo para subir, con pruebas e historial incluidos. El estudiante debe publicar o enviar el ZIP y revisar que la bitácora describa su participación real.
