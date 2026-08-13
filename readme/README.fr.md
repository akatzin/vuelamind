# vuelamind

*Un cadre pour auditer et documenter un domaine complexe avec un assistant IA, sans que la documentation ne se détache du réel.*

[← English](../README.md)

## Le problème

Un assistant IA oublie : sa fenêtre de contexte se remplit et le début se dissout, si bien que chaque session naît orpheline — sans règles, sans histoire, sans cicatrices.

Et une documentation jamais confrontée au réel **ment avec assurance**. Six mois plus tard, la moitié de ce qu'affirment vos notes est faux, et rien n'indique quelle moitié.

vuelamind casse les deux à la fois — non par une application, mais par une discipline écrite : **on n'affirme rien qui n'ait été vérifié**, et chaque affirmation conserve sa provenance : **mesuré**, **inféré** ou **rapporté**.

## Ce que vous obtenez

Un vault en texte brut et un cycle en quatre actes : **naître** une fois ; **reprendre** au début de chaque session — en mesurant l'état actuel plutôt qu'en se fiant au souvenir ; et **réconcilier** à la clôture.

Dedans : une file de travail classée par gravité réelle, un registre de décisions qui note *ce qui me ferait changer d'avis*, et **un livre d'erreurs de 38 leçons, chacune payée par une vraie bévue**. C'est cette dernière partie qui vaut : la structure se refait en une après-midi, les cicatrices non.

## Pour commencer

1. Collez l'intégralité de `MARCO_Inicial.md` dans un contexte neuf de votre assistant.
2. Dites : **« initialise ce cadre »**.
3. Répondez à l'entretien — une vingtaine de minutes, avec pauses possibles.

Ni serveur, ni outils, ni compte. Un assistant et deux dossiers locaux.

**La question zéro porte sur la langue de travail**, et tout le reste sort dans la vôtre.

## Prérequis

Un assistant, deux dossiers locaux et **un shell de type Unix** — macOS ou Linux.

**Windows n’est pas pris en charge nativement.** Les scripts générés par le cadre supposent `sh`/`bash` et des chemins POSIX. La voie connue consiste à exécuter votre assistant **dans un conteneur Linux** (Docker, par exemple) et à y travailler : tout ce dont le cadre a besoin vit dans le conteneur, et le système hôte cesse d’importer.

Cette voie est **inférée, non testée** : elle devrait fonctionner, mais personne ne l’a encore réellement exécutée. Si vous le faites, cela mérite un correctif.

Le **noyau**, lui, fonctionne partout, Windows compris : l’entretien, les gabarits, les règles et le livre d’erreurs sont du texte brut. Vous renonceriez seulement à la machinerie optionnelle — moins commode, tout aussi valable.

## Comment il s'améliore

Par **correctifs** : des leçons avec cas réel, date et méthode de vérification, proposées en pull request. Le seul critère d'admission est l'épreuve de généricité — *réécrivez votre leçon sans aucun nom propre : survit-elle ?* — et **écarter avec une raison vaut mieux qu'adopter par politesse**.

## Licence

Usage personnel, éducatif, communautaire et de recherche : **libre**. Usage en entreprise : **licence payante**. Et une condition non négociable : ce cadre **ne doit pas servir à remplacer le travail de personnes employées**. Détails dans `LICENSE.md` — c'est du *source-available*, pas de l'open source au sens de l'OSI, et la licence le dit franchement.
