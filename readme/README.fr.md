# vuelamind

*Un cadre pour auditer et documenter un domaine complexe avec un assistant IA, sans que la documentation ne se détache du réel.*

[← English](../README.md)

## Le problème

Un assistant IA oublie : sa fenêtre de contexte se remplit et le début se dissout, si bien que chaque session naît orpheline — sans règles, sans histoire, sans cicatrices.

Et une documentation jamais confrontée au réel **ment avec assurance**. Six mois plus tard, la moitié de ce qu'affirment vos notes est faux, et rien n'indique quelle moitié.

vuelamind casse les deux à la fois — non par une application, mais par une discipline écrite : **on n'affirme rien qui n'ait été vérifié**, et chaque affirmation conserve sa provenance : **mesuré**, **cité**, **inféré** ou **rapporté**.

## Ce que vous obtenez

Un vault en texte brut et un cycle en quatre actes : **naître** une fois ; **reprendre** au début de chaque session — en mesurant l'état actuel plutôt qu'en se fiant au souvenir ; et **réconcilier** à la clôture.

Dedans : une file de travail classée par gravité réelle, un registre de décisions qui note *ce qui me ferait changer d'avis*, et **un livre d'erreurs de 51 leçons, chacune payée par une vraie bévue**. C'est cette dernière partie qui vaut : la structure se refait en une après-midi, les cicatrices non.

## Pour commencer

Les deux chemins commencent pareil — par le fichier, pas par une commande :

1. Créez un dossier pour votre domaine et clonez-y la méthode :

   ```
   git clone https://github.com/akatzin/vuelamind.git
   ```

2. Ouvrez votre assistant **dans ce dossier** et dites-lui : **« Initialise MARCO_Inicial.md »**.

   Rien à coller : l’étape 1 a déjà mis le fichier sur le disque, l’assistant le lit.

La première question est votre langue. **La deuxième décide de tout le reste :** ce domaine naît-il ici, ou cette machine rejoint-elle un domaine qui vit déjà ?

- **Naître** — vous répondez à l'entretien. Une vingtaine de minutes, avec pauses possibles. Il génère le vault, l'échafaudage et les commandes du cycle.
- **Rejoindre** — pas d'entretien, rien de généré. Il atteint le vault existant, vérifie qu'il est arrivé entier, installe le cycle depuis le canon et passe la main à `/vuelamind-join`.

L'assistant ne s'en tient pas à votre parole : il regarde le dossier de destination et **s'arrête** si vous avez dit *naître* et qu'il y trouve des mois de travail — ou si vous avez dit *rejoindre* et qu'il n'y trouve rien.

**Ce qu'il vous faut :** un assistant capable de lire vos fichiers et d'exécuter des commandes. N'importe lequel convient —la méthode est du texte brut—. Si vous n'en avez aucun, `npm install -g @anthropic-ai/claude-code` est une voie connue.

Au-delà, le cadre n'exige ni serveur propre, ni service, ni compte chez lui : seulement deux dossiers locaux.

## Une machine, ou plusieurs

Tout ce qui précède en suppose une : un assistant et deux dossiers locaux. **Cette promesse vaut pour naître** — rien d'autre n'est nécessaire pour commencer.

**Une deuxième machine doit atteindre ce que possède la première** : le vault, l'échafaudage —son manifeste, son validateur, sa mémoire— et, si votre domaine vérifie contre des systèmes vivants, les accès pour le faire. *Comment* elle les atteint, c'est vous qui le choisissez : dossier partagé, montage, clone, réplique automatique. Le cadre ne décide pas du transport.

`/vuelamind-join` parcourt ce chemin, et ses vérifications sont l'essentiel : il confirme que le vault est arrivé **entier** —à moitié synchronisé est pire que vide, car l'assistant mesure sur un trou et conclut avec assurance—, installe le cycle depuis le canon et **exécute votre validateur comme preuve d'être dedans**. Que les fichiers soient là ne veut pas dire qu'on peut mesurer.

**Et cette commande n'est pas encore sur la nouvelle machine** — elle voyage avec la naissance. Une machine qui n'est jamais née commence donc là où tout le monde commence : cloner ce dépôt, initialiser `MARCO_Inicial.md`, répondre *rejoindre*. Le fichier apporte les commandes avec lui ; ensuite c'est la commande qui mène.

Une machine qui lit le vault sans atteindre les systèmes reste une instance légitime — elle doit seulement **le dire** en se déclarant.

Et il existe une instance légitime qui n'écrit jamais — un conseil abonné à la mémoire de l'ingénierie, un auditeur. Sa ligne au registre porte `accès : écrit | lit`, et **elle ne se déclare pas elle-même : une instance qui écrit la déclare**, avant son arrivée. Qui ne fait que lire garde ce qui définit le rôle : fermer chaque session sans avoir écrit une lettre.

## Prérequis

Un assistant, deux dossiers locaux et **un shell de type Unix** — macOS ou Linux.

**Windows n’est pas pris en charge nativement.** Les scripts générés par le cadre supposent `sh`/`bash` et des chemins POSIX. La voie connue consiste à exécuter votre assistant **dans un conteneur Linux** (Docker, par exemple) et à y travailler : tout ce dont le cadre a besoin vit dans le conteneur, et le système hôte cesse d’importer.

Cette voie est **inférée, non testée** : elle devrait fonctionner, mais personne ne l’a encore réellement exécutée. Si vous le faites, cela mérite un correctif.

Le **noyau**, lui, fonctionne partout, Windows compris : l’entretien, les gabarits, les règles et le livre d’erreurs sont du texte brut. Vous renonceriez seulement à la machinerie optionnelle — moins commode, tout aussi valable.

## Comment il s'améliore

Par **correctifs** : des leçons avec cas réel, date et méthode de vérification, proposées en pull request. Le seul critère d'admission est l'épreuve de généricité — *réécrivez votre leçon sans aucun nom propre : survit-elle ?* — et **écarter avec une raison vaut mieux qu'adopter par politesse**.

## Licence

Usage personnel, éducatif, communautaire et de recherche : **libre**. Usage en entreprise : **licence payante**. Et une condition non négociable : ce cadre **ne doit pas servir à remplacer le travail de personnes employées**. Détails dans `LICENSE.md` — c'est du *source-available*, pas de l'open source au sens de l'OSI, et la licence le dit franchement.
