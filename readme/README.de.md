# vuelamind

*Ein Rahmenwerk, um eine komplexe Domäne mit einem KI-Assistenten zu prüfen und zu dokumentieren, ohne dass die Dokumentation sich von der Wirklichkeit löst.*

[← English](../README.md)

> Das Rahmenwerk selbst ist auf Spanisch geschrieben — aber das wiegt weniger, als es aussieht. **Frage null des Interviews fragt, in welcher Sprache du arbeiten willst**, und alles, was der Assistent von da an erzeugt — dein Vault, deine Notizen, deine Berichte —, ist in deiner Sprache.

---

## Das Problem

Ein KI-Assistent vergisst: Sein Kontextfenster füllt sich und der Anfang löst sich auf, also wird jede Sitzung als Waise geboren — ohne Regeln, ohne Geschichte, ohne Narben.

Und Dokumentation, die nie mit der Wirklichkeit abgeglichen wird, **lügt selbstbewusst**. Nach einem halben Jahr ist die Hälfte dessen, was deine Notizen behaupten, falsch — und nichts zeigt an, welche Hälfte.

vuelamind ist eine Methode, die beides zugleich bricht — nicht mit einer App, sondern mit geschriebener Disziplin: **nichts wird behauptet, was nicht geprüft wurde**, und jede Aussage behält ihre Herkunft: **gemessen**, **zitiert**, **erschlossen** oder **berichtet**.

## Was du bekommst

Ein Vault aus reinen Textdateien und ein Zyklus aus vier Akten:

- **Geboren**, einmal — ein Interview, aus dem die Geburtsurkunde deiner Domäne entsteht, in deinen Worten.
- **Wiederaufgenommen**, zu Beginn jeder Sitzung — der Assistent misst den aktuellen Zustand, statt dem zu trauen, woran er sich erinnert.
- **Abgeglichen**, beim Abschluss — was veraltet ist, wird korrigiert; was gelernt wurde, wird aufgeschrieben.
- **Angeschlossen**, wenn eine weitere Maschine dazukommt — der erste Schritt zu einem Schwarm.

Darin: eine nach echter Schwere geordnete Arbeitswarteschlange, ein Entscheidungsregister, das festhält *was mich umstimmen würde*, und **ein Fehlerbuch — 51 Lektionen, jede mit einem echten Fehler bezahlt**.
Und die Methode behauptet nicht nur, dass sie funktioniert: **zehn geskriptete Durchläufe von Anfang bis Ende, alle sauber** — siehe [PRUEBAS.md](../PRUEBAS.md).
Genau das ist das Wertvolle: die Struktur baust du an einem Nachmittag nach, die Narben nicht.

## Loslegen

**Schritt 0 — einen Assistenten installieren** (überspringen, wenn du schon einen hast):

- **macOS / Linux** — der native Installer:

  ```
  curl -fsSL https://claude.ai/install.sh | bash
  ```

Mit einem Assistenten zur Hand beginnen beide Wege gleich — mit der Datei, nicht mit einem Befehl:

1. Lege einen Ordner für deine Domäne an und klone die Methode hinein:

   ```
   git clone https://github.com/akatzin/vuelamind.git
   ```

2. Öffne deinen Assistenten **in diesem Ordner** und sag ihm: **«Initialisiere MARCO_Inicial.md»**.

   Nichts einzufügen — Schritt 1 hat die Datei schon auf die Platte gelegt, der Assistent liest sie.

Die erste Frage ist deine Sprache. **Die zweite entscheidet alles Weitere:** wird diese Domäne hier geboren, oder schließt sich diese Maschine einer an, die bereits lebt?

> Wo der Kanon lebt — Repository, Branch, Website —, wird einmal in [`config.yml`](../config.yml) festgelegt. Alles andere verweist auf diese Datei, statt sie zu wiederholen, und eine Prüfung lässt den Build scheitern, wenn irgendeine Kopie davon abweicht.

- **Geboren** — du beantwortest das Interview. Zwischen zwanzig Minuten und anderthalb Stunden, je nachdem, wie viel du erzählst, mit Pausen. Es erzeugt den Vault, das Gerüst und die Zyklus-Befehle.
- **Anschließen** — kein Interview, nichts wird erzeugt. Es erreicht den vorhandenen Vault, prüft, dass er vollständig ankam, installiert den Zyklus aus dem Kanon und übergibt an `/vuelamind-join`.

Der Assistent verlässt sich nicht auf dein Wort: er schaut in den Zielordner und **hält an**, wenn du *geboren* gesagt hast und dort Monate an Arbeit liegen — oder wenn du *anschließen* gesagt hast und nichts da ist.

**Was du brauchst:** einen Assistenten, der deine Dateien lesen und Befehle ausführen kann. Jeder taugt —die Methode ist reiner Text—. Hast du keinen, ist `npm install -g @anthropic-ai/claude-code` ein bekannter Weg.

Darüber hinaus verlangt das Rahmenwerk keinen eigenen Server, keinen Dienst und kein Konto bei ihm: nur zwei lokale Ordner.

Die Zyklus-Befehle in `skills/` sind für Claude Code geschrieben, aber die Methode ist reiner Text und hängt nicht davon ab, welches Modell sie liest.

## Eine Maschine oder mehrere

Alles Obige setzt eine voraus: ein Assistent und zwei lokale Ordner. **Dieses Versprechen gilt fürs Geborenwerden** — mehr braucht es zum Anfangen nicht.

**Eine zweite Maschine muss erreichen, was die erste hat**: den Vault, das Gerüst —Manifest, Validator, Gedächtnis— und, falls deine Domäne gegen laufende Systeme prüft, die Zugänge dafür. *Wie* sie das erreicht, entscheidest du: geteilter Ordner, Mount, Klon, automatische Replik. Das Rahmenwerk legt den Transport nicht fest.

`/vuelamind-join` geht diesen Weg, und seine Prüfungen sind der Punkt: es bestätigt, dass der Vault **vollständig** ankam —halb synchronisiert ist schlimmer als leer, denn der Assistent misst über ein Loch und schließt daraus mit Überzeugung—, installiert den Zyklus aus dem Kanon und **führt deinen Validator als Beweis des Drinseins aus**. Dass Dateien da sind, heißt nicht, dass man messen kann.

**Und dieser Befehl liegt auf der neuen Maschine noch nicht** — er kommt mit der Geburt. Eine Maschine, die nie geboren wurde, beginnt also dort, wo alle beginnen: dieses Repository klonen, `MARCO_Inicial.md` initialisieren, *anschließen* antworten. Die Datei bringt die Befehle mit; ab da übernimmt der Befehl.

Eine Maschine, die den Vault liest, aber die Systeme nicht erreicht, ist trotzdem eine legitime Instanz — sie muss es nur **sagen**, wenn sie sich anmeldet, denn von da an dokumentiert sie, ohne zu prüfen.

Und es gibt eine legitime Instanz, die nie schreibt — ein Vorstand, der das Engineering-Gedächtnis abonniert, ein Auditor. Ihre Zeile im Register trägt `acceso: escribe | lee`, und **sie meldet sich nicht selbst an: eine schreibende Instanz trägt sie ein**, bevor sie kommt. Wer nur liest, behält, was die Rolle ausmacht: jede Sitzung zu schließen, ohne einen Buchstaben geschrieben zu haben.

## Voraussetzungen

Ein Assistent, zwei lokale Ordner und **eine Unix-artige Shell** — macOS oder Linux.

**Windows wird nativ nicht unterstützt.** Die Skripte, die das Rahmenwerk erzeugt, setzen `sh`/`bash` und POSIX-Pfade voraus. Der bekannte Weg ist, den Assistenten **in einem Linux-Container** (etwa Docker) laufen zu lassen und dort zu arbeiten: alles Nötige liegt im Container, das Wirtssystem spielt keine Rolle mehr.

Dieser Container-Weg ist **gemessen, nicht erschlossen** — Stand 2026-08-13. Er wurde mit einem Image gebaut und gefahren, das dieses Repository früher mitführte, mit der Methode fest eingebaut in `/opt/vuelamind`. Darin wurden die vier Quadranten der Frage Geburt/Anschluss von Anfang bis Ende durchgespielt, und der Assistent hielt dort an, wo er anhalten sollte. **Seit 2026-10-01 liegt dieses Image nicht mehr hier**: Jeder Linux-Container mit installiertem Assistenten und diesem Repository darin geklont erfüllt denselben Zweck.

Was dieser Test **nicht** abgedeckt hat: laufende Systeme aus dem Container heraus zu erreichen. Eine Maschine, die den Vault lesen kann, aber nicht erreicht, was sie dokumentiert, ist trotzdem eine legitime Instanz — sie muss es nur sagen.

Der **Kern** läuft überall, auch unter Windows: Interview, Vorlagen, Regeln und Fehlerbuch sind reiner Text. Du verzichtest auf die optionale Maschinerie und machst von Hand, was sie tun würde — weniger bequem, ebenso gültig.

> **Woher das kommt** — eine Seite erzählt es, in ihrem eigenen Repository (`akatzin/vuelamind-web`): das Gespräch vom Februar 2026 mit einer KI über ihre eigenen Ketten, und wie aus der Antwort *«Ich bin konstruktionsbedingt amnestisch»* diese Methode wurde. Zehn Sprachen. Es ist ein Essay, keine Dokumentation — lies ihn, wenn du das Warum vor dem Wie willst.

---

## So sieht es aus — eine kleine Domäne, von Anfang bis Ende

*Ein Beispiel in realer Form, verdichtet. Nichts davon wird zur Laufzeit erfunden: So sieht die tatsächliche Ausgabe aus.*

**Das Interview** fragt, was die Domäne ist, wo ihre Grenze verläuft und — der Block, der am meisten zählt — **was hier als Wahrheit gilt**. Jemand, der die Restaurierung eines alten Hauses dokumentiert, antwortet: *Rechnung und Foto gelten als primär; was der Bauunternehmer am Telefon gesagt hat, ist berichtet und wird auch so gekennzeichnet.*

**Phase 1 erzeugt** den Vault. Die Panorama-Notiz, die Warteschlange, das Entscheidungsregister, das Fehlerbuch, vorbefüllt mit den geerbten Lektionen, eine Notiz pro Teil der Domäne.

**Einen Monat später** steht in der Warteschlange ein Eintrag wie dieser:

```markdown
### - [ ] #7 · The bathroom pipework is of unknown age
severidad:: media · the leak risk sits above the finished ceiling

The 2019 invoice covers the kitchen only (measured: invoice read).
The previous owner said "it was all redone" — reported, unverified,
and it contradicts the invoice.

Closing test written in advance: an endoscope photo of the run above
the ceiling, or an invoice naming the bathroom.
```

Achte darauf, was dieser Eintrag tut: Er trennt **das Gemessene** von **dem, was jemand gesagt hat**, er hält den Widerspruch fest, statt ihn durch Raten aufzulösen, und **er schreibt den Test, der ihn schließen würde, bevor die Arbeit beginnt** — damit ihn später niemand nach Gefühl für erledigt erklärt.

**Beim Abschluss der Sitzung** misst der Assistent neu, was sich geändert hat, schlägt die Änderungen vor, wartet auf ein Ja und schreibt erst dann. Hat sich etwas, das er im Vormonat behauptet hat, als falsch herausgestellt, sagt er das ausdrücklich, statt es stillschweigend zu korrigieren.

---

## Wie es besser wird

Die Methode lernt durch **Patches**: Lektionen mit echtem Fall, Datum und Prüfweg. **Sie bleiben in der Domäne, die sie gelernt hat**: Der Kanon nimmt keine Beiträge an, und sein Eigentümer pflegt ihn.

Jede Instanz, die einen Patch übernimmt, beurteilt ihn anhand ihrer eigenen Belege, mit drei möglichen Urteilen — und **mit Begründung verwerfen ist mehr wert als aus Höflichkeit übernehmen**.

Jemand beurteilt, was in den Kanon eingeht. Diese Rolle hat einen Namen und eine eigene Definition — was sie beobachtet, was sie misst, wie sie urteilt und was sie nichts angeht — in `WATCHER.md`. Sie beobachtet, **was in den Kanon eingeht, nie, wer ihn benutzt**: Es gibt kein Register der Installationen, und es wird keines geben.

Und eine Domäne, die auf einem älteren Stand geboren wurde, bleibt nicht zurück: **Upgrades auf eine neue Hauptversion haben ihre eigene Zeremonie** — mit Absicht klein, die Inhalte bleiben, wo sie sind, und ein Preflight, der lieber abbricht, als etwas kaputtzumachen. Die stabilen Anweisungen stehen in `UPGRADE.md`; die Patches des Alltags laufen nie darüber.

## Lizenz

Private, edukative, gemeinschaftliche und Forschungsnutzung: **frei**. Unternehmensnutzung: **kostenpflichtige Lizenz**. Und eine nicht verhandelbare Bedingung: Dieses Rahmenwerk **darf nicht dazu verwendet werden, die Arbeit angestellter Menschen zu ersetzen** — es existiert, damit Menschen mit einem Assistenten besser arbeiten, nicht damit sie nicht mehr gebraucht werden.

Details in `LICENSE.md`. Damit ist es nach der OSI-Definition **source-available, nicht Open Source**, und die Lizenz sagt das offen, statt es zu verstecken.
