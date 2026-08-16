---
version: 1
origen: dominio de origen
estado: armonizado al master el 2026-08-16 · caso de ejecucion pendiente: el primer dominio que se adhiera lo pagara
---

# 2026-08-16 · Con canon versionado, el upgrade es adhesión — los upgraders solo migran contenido

## Qué corrige

El método heredó de su era pre-git la idea de que subir de versión es **migrar una copia**:
un upgrader con preflight que transforma la plantilla local. Con el canon versionado eso
quedó al revés: **la copia local del master es una conveniencia, no el sistema operativo del
dominio** — el sistema operativo son los comandos del ciclo (que se instalan del canon por
huella), el manifiesto, y las reglas ya absorbidas en el vault.

El modo de fallo del modelo viejo, medido: un dominio en v2.0 con un `MARCO_Inicial.v2.3.md`
huérfano al lado — una migración a medias, tirada en la carpeta, esperando que una sesión
futura la lea creyéndola vigente.

## La regla

> **El upgrade de MÁQUINA es re-instalar el ciclo desde el canon** (el paso 2 del acto de
> sumarse, por huella — sin ceremonia de join: la instancia fundadora no se re-declara ni
> hace primera sesión de lectura).
>
> **El upgrade de DOMINIO es adherirse al canon**, y su delta es enumerable y chico:
> el manifiesto gana las claves que le falten (`canon`, `aportar_a` — con los defaults
> asimétricos), la semilla del libro se refresca a la vigente, una fila en el registro
> (*"vN por adhesión al canon"*), y las copias locales del master **se archivan con fecha**
> — no se migran, no se quedan como trampas.
>
> **El upgrader queda para lo único que de verdad migra: CONTENIDO** — vaults cuya
> estructura cambió entre líneas base, no plantillas que el canon ya carga.

## Cómo verificar

**El que fallaba:** un dominio v2 sube a v3 sin tocar su copia del master — solo adhesión.
Su siguiente reconciliación corre con el motor v3 y el validador en verde. **El que DEBE
seguir fallando:** un vault cuya *estructura* requiere migración real (notas del ciclo
renombradas, marcas de procedencia viejas) no puede "adherirse" sin ese trabajo — la
adhesión no lo exime, y el preflight del upgrader debe seguir cazándolo.
