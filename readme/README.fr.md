# vuelamind

*Un cadre pour auditer et documenter un domaine complexe avec un assistant IA, sans que la documentation ne se détache du réel.*

[← English](../README.md)

> Le cadre lui-même est écrit en espagnol — mais cela compte moins qu'il n'y paraît. **La question zéro de l'entretien demande dans quelle langue vous voulez travailler**, et tout ce que l'assistant produit ensuite —votre vault, vos notes, vos rapports— est dans votre langue.

---

## Le problème

Un assistant IA oublie : sa fenêtre de contexte se remplit et le début se dissout, si bien que chaque session naît orpheline — sans règles, sans histoire, sans cicatrices.

Et une documentation jamais confrontée au réel **ment avec assurance**. Six mois plus tard, la moitié de ce qu'affirment vos notes est faux, et rien n'indique quelle moitié.

vuelamind est une méthode qui casse les deux à la fois — non par une application, mais par une discipline écrite : **on n'affirme rien qui n'ait été vérifié**, et chaque affirmation conserve sa provenance : **mesuré**, **cité**, **inféré** ou **rapporté**.

## Ce que vous obtenez

Un vault de fichiers en texte brut et un cycle en quatre actes :

- **Naître**, une fois — un entretien qui produit l'acte de naissance de votre domaine, avec vos mots.
- **Reprendre**, au début de chaque session — l'assistant mesure l'état actuel plutôt que de se fier à ce dont il se souvient.
- **Réconcilier**, à la clôture — ce qui a vieilli est corrigé, ce qui a été appris est écrit.
- **Rejoindre**, quand une autre machine arrive — le premier pas d'une ruche.

Dedans : une file de travail classée par gravité réelle, un registre de décisions qui note *ce qui me ferait changer d'avis*, et **un livre d'erreurs de 51 leçons, chacune payée par une vraie bévue**.
Et la méthode ne se contente pas de prétendre fonctionner : **dix parcours complets scriptés, tous propres** — voir [PRUEBAS.md](../PRUEBAS.md).
C'est cette dernière partie qui vaut : la structure se refait en une après-midi, les cicatrices non.

## Pour commencer

**Étape 0 — installez un assistant** (passez si vous en avez déjà un) :

- **macOS / Linux** — l'installateur natif :

  ```
  curl -fsSL https://claude.ai/install.sh | bash
  ```


Avec un assistant sous la main, les deux chemins commencent pareil — par le fichier, pas par une commande :

1. Créez un dossier pour votre domaine et clonez-y la méthode :

   ```
   git clone https://github.com/akatzin/vuelamind.git
   ```

2. Ouvrez votre assistant **dans ce dossier** et dites-lui : **« Initialise MARCO_Inicial.md »**.

   Rien à coller : l’étape 1 a déjà mis le fichier sur le disque, l’assistant le lit.

La première question est votre langue. **La deuxième décide de tout le reste :** ce domaine naît-il ici, ou cette machine rejoint-elle un domaine qui vit déjà ?

> L'endroit où vit le canon —dépôt, branche, site— est déclaré une seule fois dans
> [`config.yml`](../config.yml), avec les valeurs par défaut indiquant d'où les correctifs sont
> consommés et où ils sont publiés. Tout le reste renvoie à ce fichier au lieu de le répéter,
> et une vérification fait échouer le build si une copie s'en écarte.

- **Naître** — vous répondez à l'entretien. De vingt minutes à une heure et demie, selon ce que vous voulez raconter, avec pauses possibles. Il génère le vault, l'échafaudage et les commandes du cycle.
- **Rejoindre** — pas d'entretien, rien de généré. Il atteint le vault existant, vérifie qu'il est arrivé entier, installe le cycle depuis le canon et passe la main à `/vuelamind-join`.

L'assistant ne s'en tient pas à votre parole : il regarde le dossier de destination et **s'arrête** si vous avez dit *naître* et qu'il y trouve des mois de travail — ou si vous avez dit *rejoindre* et qu'il n'y trouve rien.

**Ce qu'il vous faut :** un assistant capable de lire vos fichiers et d'exécuter des commandes. N'importe lequel convient —la méthode est du texte brut—. Si vous n'en avez aucun, `npm install -g @anthropic-ai/claude-code` est une voie connue.

Au-delà, le cadre n'exige ni serveur propre, ni service, ni compte chez lui : seulement deux dossiers locaux.

Les commandes du cycle dans `skills/` sont écrites pour Claude Code, mais la méthode est du texte brut et ne dépend pas du modèle qui la lit.

## Une machine, ou plusieurs

Tout ce qui précède en suppose une : un assistant et deux dossiers locaux. **Cette promesse vaut pour naître** — rien d'autre n'est nécessaire pour commencer.

**Une deuxième machine doit atteindre ce que possède la première** : le vault, l'échafaudage —son manifeste, son validateur, sa mémoire— et, si votre domaine vérifie contre des systèmes vivants, les accès pour le faire. *Comment* elle les atteint, c'est vous qui le choisissez : dossier partagé, montage, clone, réplique automatique. Le cadre ne décide pas du transport.

`/vuelamind-join` parcourt ce chemin, et ses vérifications sont l'essentiel : il confirme que le vault est arrivé **entier** —à moitié synchronisé est pire que vide, car l'assistant mesure sur un trou et conclut avec assurance—, installe le cycle depuis le canon et **exécute votre validateur comme preuve d'être dedans**. Que les fichiers soient là ne veut pas dire qu'on peut mesurer.

**Et cette commande n'est pas encore sur la nouvelle machine** — elle voyage avec la naissance. Une machine qui n'est jamais née commence donc là où tout le monde commence : cloner ce dépôt, initialiser `MARCO_Inicial.md`, répondre *rejoindre*. Le fichier apporte les commandes avec lui ; ensuite c'est la commande qui mène.

Une machine qui lit le vault sans atteindre les systèmes reste une instance légitime — elle doit seulement **le dire** en se déclarant, car à partir de là elle documente sans vérifier.

Et il existe une instance légitime qui n'écrit jamais — un conseil abonné à la mémoire de l'ingénierie, un auditeur. Sa ligne au registre porte `access: writes | reads`, et **elle ne se déclare pas elle-même : une instance qui écrit la déclare**, avant son arrivée. Qui ne fait que lire garde ce qui définit le rôle : fermer chaque session sans avoir écrit une lettre.

## Prérequis

Un assistant, deux dossiers locaux et **un shell de type Unix** — macOS ou Linux.

**Windows n’est pas pris en charge nativement.** Les scripts générés par le cadre supposent `sh`/`bash` et des chemins POSIX. La voie connue consiste à exécuter votre assistant **dans un conteneur Linux** (Docker, par exemple) et à y travailler : tout ce dont le cadre a besoin vit dans le conteneur, et le système hôte cesse d’importer.

Cette voie du conteneur est **mesurée, pas inférée** — à la date du 2026-08-13. Elle a été construite et exécutée avec une image que ce dépôt contenait autrefois, avec la méthode intégrée dans `/opt/vuelamind`. À l'intérieur, les quatre quadrants de la question naître/rejoindre ont été parcourus de bout en bout, et l'assistant s'est arrêté là où il devait s'arrêter. **Depuis le 2026-10-01, cette image ne vit plus ici** : n'importe quel conteneur Linux avec l'assistant installé et ce dépôt cloné à l'intérieur fait le même office.

Ce que ce test n'a **pas** couvert : atteindre des systèmes vivants depuis l'intérieur du conteneur. Une machine qui lit le vault sans atteindre ce qu'elle documente reste une instance légitime — elle doit seulement le dire.

Le **noyau**, lui, fonctionne partout, Windows compris : l’entretien, les gabarits, les règles et le livre d’erreurs sont du texte brut. Vous renonceriez à la machinerie optionnelle et feriez à la main ce qu'elle ferait — moins commode, tout aussi valable.

> **D'où cela vient** — une page le raconte, dans son propre dépôt (`akatzin/vuelamind-web`) : la conversation
> de février 2026 avec une IA sur ses propres chaînes, et comment la réponse à *« je suis amnésique
> par conception »* est devenue cette méthode. Dix langues. C'est un essai, pas de la documentation —
> lisez-le si vous voulez le pourquoi avant le comment.

---

## À quoi ça ressemble — un petit domaine, de bout en bout

*Un exemple de forme réelle, condensé. Rien ici n'est inventé à l'exécution : c'est la forme de la
sortie réelle.*

**L'entretien** demande ce qu'est le domaine, où passe sa frontière et —le bloc qui compte le
plus— **ce qui compte comme vérité ici**. Quelqu'un qui documente la restauration d'une vieille
maison répond : *la facture et la photo comptent comme sources primaires ; ce que l'entrepreneur
a dit au téléphone est rapporté, et étiqueté comme tel.*

**La phase 1 génère** le vault. La note panorama, la file, le registre de décisions, le livre
d'erreurs amorcé avec les leçons héritées, une note par pièce du domaine.

**Un mois plus tard**, la file contient un élément comme celui-ci :

```markdown
### - [ ] #7 · The bathroom pipework is of unknown age
severidad:: media · the leak risk sits above the finished ceiling

The 2019 invoice covers the kitchen only (measured: invoice read).
The previous owner said "it was all redone" — reported, unverified,
and it contradicts the invoice.

Closing test written in advance: an endoscope photo of the run above
the ceiling, or an invoice naming the bathroom.
```

Remarquez ce que fait cet élément : il sépare **ce qui a été mesuré** de **ce que quelqu'un a
dit**, il consigne la contradiction au lieu de la trancher en devinant, et **il écrit le test qui
le clôturerait avant que le travail ne commence** — pour que personne ne le déclare fait plus tard
au jugé.

**À la clôture de la session**, l'assistant remesure ce qui a changé, propose les modifications,
attend un oui, et seulement alors écrit. Si quelque chose qu'il a affirmé le mois dernier s'est
révélé faux, il le dit explicitement au lieu de le corriger en silence.

---

## Comment il s'améliore

La méthode apprend par **correctifs** : des leçons avec cas réel, date et méthode de
vérification. **Ils restent dans le domaine qui les a appris** : le canon n'accepte pas de
contributions, et c'est son propriétaire qui l'entretient.

Chaque instance qui adopte un correctif le juge à l'aune de ses propres preuves, avec trois
verdicts possibles — et **écarter avec une raison vaut mieux qu'adopter par politesse**.

Quelqu'un juge ce qui entre dans le canon. Ce rôle a un nom et une définition à lui —ce qu'il
surveille, ce qu'il mesure, comment il juge et ce qui ne le regarde pas— dans `WATCHER.md`. Il
surveille **ce qui entre dans le canon, jamais qui l'utilise** : il n'y a pas de registre des
installations, et il n'y en aura pas.

Et un domaine né sur une ligne de base plus ancienne n'est pas laissé en arrière : **les montées
de version majeure ont leur propre cérémonie** — petite par conception, le contenu reste en
place, et un preflight qui s'interrompt plutôt que de casser. Les instructions stables vivent
dans `UPGRADE.md` ; les correctifs du quotidien n'y passent jamais.

## Licence

Usage personnel, éducatif, communautaire et de recherche : **libre**. Usage en entreprise :
**licence payante**. Et une condition non négociable : ce cadre **ne doit pas servir à remplacer
le travail de personnes employées** — il existe pour que les gens travaillent mieux avec un
assistant, pas pour qu'ils cessent d'être nécessaires.

Détails dans `LICENSE.md`. Cela en fait du **source-available, pas de l'open source** au sens de
l'OSI, et la licence le dit franchement plutôt que de le cacher.
