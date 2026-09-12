#!/bin/sh
# Instantánea del vault, para que el cierre pueda RELEER lo que la sesión escribió.
#
# EL HUECO QUE CIERRA. El ciclo comprueba el RADIO de un cambio —las vecinas de las notas
# tocadas— y el validador comprueba MECÁNICA —conteos, enlaces, huellas—. Nadie relee lo que
# la sesión ESCRIBIÓ. Un párrafo nuevo que afirma algo falso pasa los dos: cuadra, enlaza y
# no contradice a nadie. Es la única parte del cierre que nada comprueba.
#
# POR QUÉ NO ES GIT. Lo que hace falta es el diff de UNA sesión, no una historia. Meter un
# repositorio sube la barrera para quien no es técnico sin dar nada que este diff no dé, y
# el método sirve a casas que no tienen por qué aprender git para poder releerse. Un dominio
# que YA viva en git puede usar el suyo y saltarse esto.
#
#   instantanea_vault.sh diff     <vault>   al cerrar: qué se escribió desde el cierre anterior
#   instantanea_vault.sh renovar  <vault>   al TERMINAR el cierre, ya releído
#   instantanea_vault.sh tomar    <vault>   la primera vez, o si se perdió
#
# CUÁNDO SE TOMA, que es lo único que hay que entender: al TERMINAR cada cierre, no al
# empezar. Si se tomara al empezar el cierre, la copia ya traería dentro todo lo que la
# sesión escribió y el diff saldría vacío — es el error fácil, y da un verde que miente.
#
# Tomándola al terminar, el diff del cierre siguiente cubre TODO lo escrito desde el
# anterior. Y esa es además la unidad correcta: no «lo de esta sesión», sino **lo que nadie
# ha releído todavía** — que es lo que importa, porque una sesión que no cerró también
# escribió.

set -eu

ACCION="${1:-}"
VAULT="${2:-${VUELAMIND_VAULT:-}}"

[ -n "$ACCION" ] || { echo "uso: $0 diff|renovar|tomar|tirar <ruta-del-vault>" >&2; exit 1; }
[ -n "$VAULT" ] || { echo "falta la ruta del vault (o la variable VUELAMIND_VAULT)" >&2; exit 1; }
[ -d "$VAULT" ] || { echo "no existe el vault: $VAULT" >&2; exit 2; }

VAULT=$(cd "$VAULT" && pwd)
# una copia por vault, para que dos dominios en la misma máquina no se pisen
SELLO=$(printf '%s' "$VAULT" | cksum | cut -d' ' -f1)
COPIA="${TMPDIR:-/tmp}/vuelamind-instantanea-$SELLO"

notas() {
    # solo las notas; nada de directorios de herramientas del editor
    (cd "$VAULT" && find . -name '*.md' -not -path './.obsidian/*' -not -path './.git/*')
}

case "$ACCION" in
tomar|renovar)
    rm -rf "$COPIA"; mkdir -p "$COPIA"
    notas | while IFS= read -r f; do
        mkdir -p "$COPIA/$(dirname "$f")"
        cp "$VAULT/$f" "$COPIA/$f"
    done
    echo "instantánea $([ "$ACCION" = renovar ] && echo renovada || echo tomada): $(notas | wc -l | tr -d ' ') notas"
    echo "  el próximo cierre comparará contra esto"

    ;;
diff)
    [ -d "$COPIA" ] || {
        echo "NO HAY INSTANTÁNEA — este cierre NO puede releer lo que se escribió." >&2
        echo "  Se toma una vez:  $0 tomar $VAULT" >&2
        echo "  y se renueva al terminar cada cierre, ya releído." >&2
        echo "  Dilo en el reporte en vez de seguir como si se hubiera releído." >&2
        exit 3; }
    nuevas=$(notas | while IFS= read -r f; do [ -f "$COPIA/$f" ] || echo "$f"; done)
    if [ -n "$nuevas" ]; then
        echo "== NOTAS NUEVAS — nadie las ha releído, no tienen con qué compararse =="
        echo "$nuevas" | sed 's|^\./|  |'
        echo
    fi
    echo "== LO QUE CAMBIÓ EN LAS QUE YA EXISTÍAN =="
    notas | sort | while IFS= read -r f; do
        [ -f "$COPIA/$f" ] || continue
        diff -u "$COPIA/$f" "$VAULT/$f" >/dev/null 2>&1 && continue
        echo "--- $f"
        diff -u "$COPIA/$f" "$VAULT/$f" | tail -n +3
    done
    ;;
tirar)
    rm -rf "$COPIA"; echo "instantánea tirada"
    ;;
*)
    echo "uso: $0 diff|renovar|tomar|tirar <ruta-del-vault>" >&2; exit 1
    ;;
esac
