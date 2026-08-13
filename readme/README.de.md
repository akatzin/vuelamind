# vuelamind

*Ein Rahmenwerk, um eine komplexe Domäne mit einem KI-Assistenten zu prüfen und zu dokumentieren, ohne dass die Dokumentation sich von der Wirklichkeit löst.*

[← English](../README.md)

## Das Problem

Ein KI-Assistent vergisst: Sein Kontextfenster füllt sich und der Anfang löst sich auf, also wird jede Sitzung als Waise geboren — ohne Regeln, ohne Geschichte, ohne Narben.

Und Dokumentation, die nie mit der Wirklichkeit abgeglichen wird, **lügt selbstbewusst**. Nach einem halben Jahr ist die Hälfte dessen, was deine Notizen behaupten, falsch — und nichts zeigt an, welche Hälfte.

vuelamind bricht beides zugleich — nicht mit einer App, sondern mit geschriebener Disziplin: **nichts wird behauptet, was nicht geprüft wurde**, und jede Aussage behält ihre Herkunft: **gemessen**, **erschlossen** oder **berichtet**.

## Was du bekommst

Ein Vault aus reinem Text und ein Zyklus aus vier Akten: einmal **geboren werden**; zu Beginn jeder Sitzung **wiederaufnehmen** — den aktuellen Zustand messen statt der Erinnerung trauen; und beim Abschluss **abgleichen**.

Darin: eine nach echter Schwere geordnete Arbeitswarteschlange, ein Entscheidungsregister, das festhält *was mich umstimmen würde*, und **ein Fehlerbuch mit 41 Lektionen, jede mit einem echten Fehler bezahlt**. Genau das ist das Wertvolle: die Struktur baust du an einem Nachmittag nach, die Narben nicht.

## Loslegen

1. Füge `MARCO_Inicial.md` vollständig in einen frischen Kontext deines Assistenten ein.
2. Sag: **„initialisiere dieses Rahmenwerk“**.
3. Beantworte das Interview — etwa zwanzig Minuten, Pausen möglich.

Kein Server, keine Werkzeuge, kein Konto. Ein Assistent und zwei lokale Ordner.

**Die nullte Frage lautet, in welcher Sprache du arbeiten willst** — alles Weitere entsteht in deiner.

## Voraussetzungen

Ein Assistent, zwei lokale Ordner und **eine Unix-artige Shell** — macOS oder Linux.

**Windows wird nativ nicht unterstützt.** Die Skripte, die das Rahmenwerk erzeugt, setzen `sh`/`bash` und POSIX-Pfade voraus. Der bekannte Weg ist, den Assistenten **in einem Linux-Container** (etwa Docker) laufen zu lassen und dort zu arbeiten: alles Nötige liegt im Container, das Wirtssystem spielt keine Rolle mehr.

Dieser Weg ist **erschlossen, nicht erprobt**: er sollte funktionieren, aber niemand hat ihn bislang tatsächlich gefahren. Wenn du es tust, ist das einen Patch wert.

Der **Kern** läuft überall, auch unter Windows: Interview, Vorlagen, Regeln und Fehlerbuch sind reiner Text. Du verzichtest nur auf die optionale Maschinerie — weniger bequem, ebenso gültig.

## Wie es besser wird

Durch **Patches**: Lektionen mit echtem Fall, Datum und Prüfweg, eingereicht als Pull Request. Das einzige Aufnahmekriterium ist die Allgemeinheitsprobe — *schreib deine Lektion ohne jeden Eigennamen neu: überlebt sie?* — und **mit Begründung verwerfen ist mehr wert als aus Höflichkeit übernehmen**.

## Lizenz

Private, edukative, gemeinschaftliche und Forschungsnutzung: **frei**. Unternehmensnutzung: **kostenpflichtige Lizenz**. Und eine nicht verhandelbare Bedingung: Dieses Rahmenwerk **darf nicht dazu verwendet werden, die Arbeit angestellter Menschen zu ersetzen**. Details in `LICENSE.md` — nach OSI-Definition ist es *source-available*, nicht Open Source, und die Lizenz sagt das offen.
