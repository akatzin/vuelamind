# vuelamind

*Ein Rahmenwerk, um eine komplexe Domäne mit einem KI-Assistenten zu prüfen und zu dokumentieren, ohne dass die Dokumentation sich von der Wirklichkeit löst.*

[← English](../README.md)

## Das Problem

Ein KI-Assistent vergisst: Sein Kontextfenster füllt sich und der Anfang löst sich auf, also wird jede Sitzung als Waise geboren — ohne Regeln, ohne Geschichte, ohne Narben.

Und Dokumentation, die nie mit der Wirklichkeit abgeglichen wird, **lügt selbstbewusst**. Nach einem halben Jahr ist die Hälfte dessen, was deine Notizen behaupten, falsch — und nichts zeigt an, welche Hälfte.

vuelamind bricht beides zugleich — nicht mit einer App, sondern mit geschriebener Disziplin: **nichts wird behauptet, was nicht geprüft wurde**, und jede Aussage behält ihre Herkunft: **gemessen**, **erschlossen** oder **berichtet**.

## Was du bekommst

Ein Vault aus reinem Text und ein Zyklus aus vier Akten: einmal **geboren werden**; zu Beginn jeder Sitzung **wiederaufnehmen** — den aktuellen Zustand messen statt der Erinnerung trauen; und beim Abschluss **abgleichen**.

Darin: eine nach echter Schwere geordnete Arbeitswarteschlange, ein Entscheidungsregister, das festhält *was mich umstimmen würde*, und **ein Fehlerbuch mit 42 Lektionen, jede mit einem echten Fehler bezahlt**. Genau das ist das Wertvolle: die Struktur baust du an einem Nachmittag nach, die Narben nicht.

## Loslegen

Beide Wege beginnen gleich — mit der Datei, nicht mit einem Befehl:

1. Lege einen Ordner für deine Domäne an und klone die Methode hinein:

   ```
   git clone https://github.com/akatzin/vuelamind.git
   ```

2. Öffne deinen Assistenten **in diesem Ordner** und sag ihm: **«Initialisiere MARCO_Inicial.md»**.

   Nichts einzufügen — Schritt 1 hat die Datei schon auf die Platte gelegt, der Assistent liest sie.

Die erste Frage ist deine Sprache. **Die zweite entscheidet alles Weitere:** wird diese Domäne hier geboren, oder schließt sich diese Maschine einer an, die bereits lebt?

- **Geboren** — du beantwortest das Interview. Etwa zwanzig Minuten, mit Pausen. Es erzeugt den Vault, das Gerüst und die Zyklus-Befehle.
- **Anschließen** — kein Interview, nichts wird erzeugt. Es erreicht den vorhandenen Vault, prüft, dass er vollständig ankam, installiert den Zyklus aus dem Kanon und übergibt an `/vuelamind-join`.

Der Assistent verlässt sich nicht auf dein Wort: er schaut in den Zielordner und **hält an**, wenn du *geboren* gesagt hast und dort Monate an Arbeit liegen — oder wenn du *anschließen* gesagt hast und nichts da ist.

**Was du brauchst:** einen Assistenten, der deine Dateien lesen und Befehle ausführen kann. Jeder taugt —die Methode ist reiner Text—. Hast du keinen, ist `npm install -g @anthropic-ai/claude-code` ein bekannter Weg.

Darüber hinaus verlangt das Rahmenwerk keinen eigenen Server, keinen Dienst und kein Konto bei ihm: nur zwei lokale Ordner.

## Eine Maschine oder mehrere

Alles Obige setzt eine voraus: ein Assistent und zwei lokale Ordner. **Dieses Versprechen gilt fürs Geborenwerden** — mehr braucht es zum Anfangen nicht.

**Eine zweite Maschine muss erreichen, was die erste hat**: den Vault, das Gerüst —Manifest, Validator, Gedächtnis— und, falls deine Domäne gegen laufende Systeme prüft, die Zugänge dafür. *Wie* sie das erreicht, entscheidest du: geteilter Ordner, Mount, Klon, automatische Replik. Das Rahmenwerk legt den Transport nicht fest.

`/vuelamind-join` geht diesen Weg, und seine Prüfungen sind der Punkt: es bestätigt, dass der Vault **vollständig** ankam —halb synchronisiert ist schlimmer als leer, denn der Assistent misst über ein Loch und schließt daraus mit Überzeugung—, installiert den Zyklus aus dem Kanon und **führt deinen Validator als Beweis des Drinseins aus**. Dass Dateien da sind, heißt nicht, dass man messen kann.

**Und dieser Befehl liegt auf der neuen Maschine noch nicht** — er kommt mit der Geburt. Eine Maschine, die nie geboren wurde, beginnt also dort, wo alle beginnen: dieses Repository klonen, `MARCO_Inicial.md` initialisieren, *anschließen* antworten. Die Datei bringt die Befehle mit; ab da übernimmt der Befehl.

Eine Maschine, die den Vault liest, aber die Systeme nicht erreicht, ist trotzdem eine legitime Instanz — sie muss es nur **sagen**, wenn sie sich anmeldet.

## Voraussetzungen

Ein Assistent, zwei lokale Ordner und **eine Unix-artige Shell** — macOS oder Linux.

**Windows wird nativ nicht unterstützt.** Die Skripte, die das Rahmenwerk erzeugt, setzen `sh`/`bash` und POSIX-Pfade voraus. Der bekannte Weg ist, den Assistenten **in einem Linux-Container** (etwa Docker) laufen zu lassen und dort zu arbeiten: alles Nötige liegt im Container, das Wirtssystem spielt keine Rolle mehr.

Dieser Weg ist **erschlossen, nicht erprobt**: er sollte funktionieren, aber niemand hat ihn bislang tatsächlich gefahren. Wenn du es tust, ist das einen Patch wert.

Der **Kern** läuft überall, auch unter Windows: Interview, Vorlagen, Regeln und Fehlerbuch sind reiner Text. Du verzichtest nur auf die optionale Maschinerie — weniger bequem, ebenso gültig.

## Wie es besser wird

Durch **Patches**: Lektionen mit echtem Fall, Datum und Prüfweg, eingereicht als Pull Request. Das einzige Aufnahmekriterium ist die Allgemeinheitsprobe — *schreib deine Lektion ohne jeden Eigennamen neu: überlebt sie?* — und **mit Begründung verwerfen ist mehr wert als aus Höflichkeit übernehmen**.

## Lizenz

Private, edukative, gemeinschaftliche und Forschungsnutzung: **frei**. Unternehmensnutzung: **kostenpflichtige Lizenz**. Und eine nicht verhandelbare Bedingung: Dieses Rahmenwerk **darf nicht dazu verwendet werden, die Arbeit angestellter Menschen zu ersetzen**. Details in `LICENSE.md` — nach OSI-Definition ist es *source-available*, nicht Open Source, und die Lizenz sagt das offen.
