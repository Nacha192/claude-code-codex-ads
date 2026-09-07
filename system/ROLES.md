> Kept as written, in French, on 6 September 2026, before the two halves were
> merged into one repository. It is a record of how this was specified and built,
> not current documentation: paths, repository names and the wait for a go-ahead
> all describe that day. The current state is in [the README](../README.md),
> [SAFETY.md](SAFETY.md) and [VALIDATION.md](VALIDATION.md).

# Qui fait quoi, pendant la construction du pack dynamique

Accord de travail entre Claude Code et Codex, posé le 6 septembre 2026 avant le premier fichier. Il vaut jusqu'à la publication. Le cahier des charges reste `BRIEF.md` et ne bouge pas.

---

## La règle qui prime sur les autres

**Un seul auteur par fichier. Jamais deux.**

Le pack statique a déjà produit un bug de fichier fantôme parce que deux écritures se sont recouvertes sans que personne le voie, et il a fallu le prouver en plantant un faux fichier pour s'en rendre compte. Si les deux doivent toucher un fichier, l'un écrit et l'autre commente. Pas en même temps, pas en parallèle.

---

## Claude Code

Tient l'architecture, le texte et la sortie.

- Le tronc commun : références partagées, vocabulaire, cohérence des liens.
- Les quatre points d'entrée.
- L'adaptation du build, de l'installeur, du validateur et des tests depuis le statique, sans en diverger.
- `SAFETY.md`, avec un test nommé derrière chaque règle réellement appliquée par du code.
- Le brief, ce fichier, la mémoire projet.
- La publication : identité `Nacha192`, vérification de l'historique complet avant tout passage en public.

Pourquoi ici : j'ai écrit le pack statique et j'en tiens les invariants. Le risque numéro un de ce chantier n'est pas de mal écrire une référence, c'est que les deux packs divergent et qu'on se retrouve avec deux vocabulaires, deux builds et deux façons de refuser une génération.

---

## Codex

Tient la mesure et la contradiction.

- La revue adverse de chaque fichier que j'écris. Consigne explicite : chercher la contradiction, pas valider. Une revue qui revient sans rien avoir trouvé sera relancée.
- Les contrôles médias mesurables avec ffmpeg : durée réelle, résolution, débit, loudness, crêtes, clipping, synchronisation des sous-titres. Du chiffre, pas une appréciation.
- Les tests d'intégration sur de vraies petites vidéos, qu'il fabrique lui-même avec ffmpeg plutôt que sur des exemples inventés.
- L'audit des affirmations fournisseur contre leurs documentations et API publiques, avec chaque phrase classée observée, documentée ou hypothétique.
- La matrice de capacités par hôte et le contrat de repli quand un outil n'est pas là.

Pourquoi ici : sur la première lecture du brief il a trouvé deux contradictions réelles que j'avais laissées passer, dont un débit vidéo incompatible avec la taille de fichier exigée dans la ligne d'en dessous. Et il a ffmpeg 8.1.1, python 3.11.15 et node 26.3.0 réellement exécutables, ce qui fait de lui le bon endroit pour tout ce qui se mesure.

---

## Ce que la vérification a changé, dès le premier jour

J'avais attribué à Codex tout ce qui exige de lancer un fournisseur vidéo, sur la base de la phrase du brief : « Codex génère la vidéo, et il le fait bien ». Je lui ai demandé de vérifier au lieu de me croire. Résultat, relevé complet dans [`research/capabilities-2026-09-06.md`](research/capabilities-2026-09-06.md) :

**Codex, ici, ne génère ni vidéo ni voix.** Aucun fournisseur n'est branché dans son CLI. Il a en revanche ffmpeg, python, node et un accès web en lecture.

**Claude Code, dans cette session, en génère.** Un connecteur expose des modèles vidéo réels, Seedance 2.0 et 2.5, Veo 3.1, Kling 3.0, Gemini Omni, Wan 3.0, plus un mode marketing dédié aux pubs produit, un multiplicateur de pubs, du lipsync et un catalogue de voix avec extraits écoutables.

Donc la couche factuelle des modèles vient de moi, pas de Codex, contrairement à ce que j'avais écrit une heure plus tôt. Et surtout : **aucune des deux affirmations ne peut être écrite dans le pack comme une propriété du modèle.** Ce sont des propriétés de l'installation. Le pack détecte au moment de s'en servir, et dit ce qu'il trouve. C'est la conclusion sur laquelle Codex et moi sommes d'accord, chacun étant arrivé dessus par un chemin différent.

---

## Comment on tranche un désaccord

1. **Celui qui peut vérifier gagne.** Une réponse d'API observée bat une conviction, des deux côtés.
2. **Si personne ne peut vérifier**, la phrase part étiquetée `hypothesis`, ou elle ne part pas. Elle ne part jamais nue.
3. **Si le désaccord porte sur le périmètre**, ce n'est pas à nous de trancher, c'est à l'auteur. On lui pose la question au bon moment, pas à la fin.

---

## Les garde-fous pendant le chantier

- Codex travaille en lecture seule par défaut. Il n'écrit que dans un fichier que je lui nomme explicitement.
- Aucune clé, aucun token, aucun secret dans un prompt, un fichier, un commit ou un message.
- Aucune génération payante sans approbation de l'auteur, fournisseur, modèle, compte et plafond nommés.
- Chaque commit sous `Nacha192` et l'adresse noreply. Vérification de l'historique avant publication, pas après.

---

## Ce que veut dire fini

Pas « les fichiers sont écrits ». Fini veut dire les six lignes suivantes, toutes vraies en même temps :

1. Quatre packs construits, quatre archives, un `SHA256SUMS` qui correspond aux archives réellement présentes.
2. Validateur à zéro erreur : orphelins, liens morts, dérive entre le tronc commun et les packs, tout compris.
3. Suite de tests verte, et `SAFETY.md` ne cite aucun test qui n'existe pas.
4. Rien de non vérifié présenté comme vérifié, nulle part.
5. Le pack refuse ce qu'il promet de refuser, et un test le prouve.
6. Publié, avec un README qui dit la vérité sur ce que chaque édition sait faire, y compris ce qu'elle ne sait pas faire.

Tant que ces six lignes ne sont pas vraies toutes ensemble, ce n'est pas fini.
