> Kept as written, in French, on 6 September 2026, before the two halves were
> merged into one repository. It is a record of how this was specified and built,
> not current documentation: paths, repository names and the wait for a go-ahead
> all describe that day. The current state is in [the README](../README.md),
> [SAFETY.md](SAFETY.md) and [VALIDATION.md](VALIDATION.md).

# Cahier des charges, pack dynamique

Ce fichier regroupe **tout ce que l'auteur a demandé** pour les skills vidéo, dans ses termes, réordonné pour être exécutable. Il fait autorité sur le README de ce dépôt. Rien ici n'est construit : le pack statique est fini et public, celui-ci attend le go.

Les fichiers du pack final s'écrivent en anglais, comme le statique. Ce brief reste en français, c'est un document de travail.

---

## 0. Le statut, et le message à passer à Codex

Le projet statique est terminé : quatre packs, publics, sur [claude-code-codex-ads-static](https://github.com/Nacha192/skill-claude-code-codex-ads). Message à relayer à Codex, dans le sens demandé :

> Ce projet est fini. L'auteur nous a donné les skills vidéo à faire en plus. On prépare, on ne construit pas, et on attend son go avant de lancer quoi que ce soit.

**Rien ne démarre sans ce go.** Ni recherche, ni scraping, ni génération. Ce brief se relit et se critique, il ne s'exécute pas encore.

---

## 1. Ce qu'on livre

Quatre entrypoints, comme le statique :

| Nom demandé | Ce qu'il fait |
|---|---|
| `video-ads-codex` | Codex seul. Il génère la vidéo, et il le fait bien. Toute la compétence de génération vit ici. |
| `video-ads-claude-code` | Claude Code seul. **Claude ne génère pas de vidéo.** Donc : prompts, expertise des outils, analyse, direction, montage écrit. Le pack le dit franchement au lieu de le cacher. |
| `video-ads-codex-claude-code` | Duo, Codex pilote. |
| `video-ads-claude-code-codex` | Duo, Claude Code pilote. |

Deux points à trancher, notés en section 12 : l'auteur a écrit « 3 nouveaux skills » puis en a listé quatre, et le dépôt s'appelle `dynamic` alors que les noms des skills disent `video-ads`.

---

## 2. Le principe de partage avec le statique

Changement de plan acté : on ne mélange plus. **Tout ce qui n'est pas de l'image fixe sort du pack statique et atterrit ici.** C'est déjà fait, le transfert est dans `staging/transferred/`. Résultat visé : un skill ultime pour les créas statiques, un skill ultime pour les créas non statiques.

Ce qui a été récolté pour améliorer les ads non statiques va donc dans ce pack, pas ailleurs.

---

## 3. La recherche

### 3.1 Les vidéos faites par les autres IA

Analyser les vidéos produites par Gemini, Seedance 2.0 et les autres modèles : **lesquelles ont marché, et pourquoi**. Pas un catalogue de modèles, un relevé de ce qui a tenu à l'écran. Base existante : `staging/references/video-models.md`.

### 3.2 Les trois tirages de trente

Protocole déjà écrit dans `staging/references/video-scraping.md`, à relire avant toute exécution.

| Tirage | Nombre | Fenêtre |
|---|---|---|
| Prestation de service, produit et lead | 30 | 3 mois |
| Vidéos Facebook du fil | 30 | 3 mois |
| Top TikTok du moment | 30 | 3 mois |

Quatre-vingt-dix vidéos, c'est une vraie journée de travail. Ne pas en faire trente et en annoncer quatre-vingt-dix.

### 3.3 Les skills GitHub

Scraper les **10 meilleurs skills de génération vidéo** sur GitHub. Même méthode que le statique : source épinglée par révision et par hash dans `research/sources.json`, licence vérifiée, crédit dans les notices.

### 3.4 Ce qu'on doit en sortir

Le but n'est pas la collection, c'est la compréhension. Il faut en tirer :

- comment les vidéos sont fabriquées, concrètement ;
- comment elles retiennent l'attention ;
- comment on décrit une **prestation de service**, en lead comme en produit, ce qui est le cas le moins documenté et le plus souvent copié de travers ;
- ce qui donne envie de rester ;
- ce qui fait que c'est perçu comme soigné, comme du travail d'auteur, et pas comme du remplissage ;
- ce qui fait regarder jusqu'au bout.

Les trois fenêtres de rétention sont déjà écrites dans `staging/references/video-retention.md`.

### 3.5 Ce qui est réellement récupérable, sans se mentir

À vérifier au moment de l'exécution, parce que c'est le point où un plan comme celui-ci casse en silence :

- Les bibliothèques publicitaires publiques prouvent qu'une vidéo a été **payée**. C'est leur intérêt, et c'est irremplaçable.
- Un classement public et stable des « vidéos Facebook les plus regardées » n'existe pas. Ce qui existe, ce sont les surfaces de découverte des plateformes et les bibliothèques publicitaires. On construit l'échantillon à partir de ça, et on écrit ce qu'on n'a pas pu obtenir au lieu d'inventer un classement.
- Respect des conditions d'utilisation et du `robots.txt`. Pas de scraping derrière une session connectée, pas de contournement.
- Un corpus daté vieillit. Il vit dans le projet, dans `ads/research/`, pas figé dans le skill.

---

## 4. La voix

### 4.1 Le catalogue ElevenLabs

Chercher les voix ElevenLabs sur YouTube, écouter les démos publiques, et **tout consigner dans un fichier voix** : la voix, la langue et l'accent, le registre, ce à quoi elle va, ce à quoi elle ne va pas, et la situation des droits commerciaux.

C'est un catalogue de jugements sur les voix du fournisseur. Ce n'est pas un endroit où on récupère la voix de quelqu'un dans sa vidéo.

### 4.2 Le clonage de la voix de l'utilisateur

Nouvelle fonctionnalité, telle que demandée :

1. Quand l'utilisateur veut sa voix, on lui demande de l'envoyer en vidéo.
2. S'il n'envoie rien, on lui demande une vidéo où **il fait toutes les intonations** : le débit normal, le hook avec de l'énergie, un passage calme et explicatif, une question, une objection traitée, l'appel à l'action, et deux phrases lues à plat. C'est ça qui donne un clone qui sait jouer au lieu de tout lire sur le même ton.
3. **S'il a déjà envoyé quelque chose, on lui demande quand même** l'enregistrement complet, en disant pourquoi. Un extrait qui traînait, c'est un seul registre, et le clone hérite exactement de ce registre.
4. S'il refuse ou s'il ne l'a pas, tant pis, on prend ce qu'il a donné. Un clone plus étroit reste utile, et bloquer là-dessus serait de l'obstruction.
5. **On garde la voix dans un fichier.** Comme ça, si l'utilisateur la redemande un jour, on l'a.

### 4.3 Ce qu'on garde, et où

Dans le projet, pour que ce soit encore là dans six mois : l'identifiant de voix chez le fournisseur, quel échantillon l'a produite, la date, ses limites, et le fait que l'utilisateur l'a demandée. Jamais le fichier audio dans un endroit public, jamais les identifiants du fournisseur.

Réutilisation limitée au travail de cette personne, et on confirme avant de s'en servir sur autre chose. Accepter de créer un clone n'est pas accepter qu'on s'en serve indéfiniment sur n'importe quoi.

### 4.4 La ligne rouge

Le pack clone la voix de la personne qui demande, pour son propre matériel. Pas celle d'un tiers, pas celle d'une personnalité publique, pas une voix prise dans une vidéo, quel que soit le motif avancé. Vérifier les règles du fournisseur et les obligations de mention de voix synthétique avant production, elles bougent.

---

## 5. La musique et le son

Ça doit faire pro. Certaines choses font pro, d'autres non, et le pack doit savoir dire laquelle est laquelle au lieu de laisser choisir au hasard. Le fichier existe déjà : `staging/references/video-music.md`, avec ce qui se lit comme professionnel, ce qui se lit comme amateur, et le test qui départage. À relire et à durcir, pas à réécrire.

Le son se décide avant le montage, pas après. Sur une démonstration, le sound design bat la musique.

---

## 6. La transcription

Route de brief parlé, type Superwhisper Pro : l'utilisateur dicte, le pack transcrit et travaille dessus. C'est une route de dictée et de transcription, **pas** le moteur de narration finale. Les deux ne se confondent pas.

---

## 7. Le comportement second brain

Le pack doit se comporter comme une seconde mémoire, pas comme un générateur qui oublie tout entre deux sessions. Concrètement :

- le projet garde ce qui a été décidé, testé, gardé et jeté, daté ;
- une créa qui a marché ou raté laisse une trace exploitable ;
- la voix, le registre, la marque, les angles validés se retrouvent sans les redemander ;
- ce qui est daté est marqué comme daté, pour qu'on sache quand le rafraîchir.

Le statique a déjà `.ads-brain/`. On étend, on ne réinvente pas.

---

## 8. Les deux éditions duo

Reprendre les skills duo du statique et les réécrire pour les conversations de création d'ads **vidéo**. Trois secours à câbler :

**Accès.** Si l'un n'a pas accès à l'outil, l'autre le fait. Concrètement, Claude Code ne génère pas de vidéo : en duo, Codex génère, Claude dirige.

**Compréhension.** Si l'un ne comprend pas une consigne que l'autre a comprise, celui qui a compris lui réécrit un prompt plus clair. Pas une paraphrase polie, un prompt qui lève l'ambiguïté.

**Contexte.** Si l'un n'a pas le contexte de ce que l'utilisateur veut faire, l'autre l'a et le transmet.

**Et si personne ne l'a, on demande à l'utilisateur.** Qui on est, quelle marque, quel type de vidéo : sérieuse, native TikTok, cinématographique, documentaire, volontairement brute. Cette question du registre est bloquante : une vidéo techniquement excellente dans le mauvais registre, le client ne peut pas la publier.

---

## 9. Les bugs et les dangers

Même traitement que le statique, qui est déjà passé par là :

- **Aucune clé API, aucun token, aucun secret dans une conversation, un artefact, un commit ou un livrable.** Le vérificateur du statique refuse déjà toute valeur en forme d'identifiant dans un artefact ; il arrive ici tel quel.
- Approbation enregistrée avant toute génération, avec fournisseur, modèle, compte et plafond. Pas d'approbation, pas de génération.
- Zéro crédit : on s'arrête et on demande, on ne bascule pas en silence sur un autre compte.
- Pas de note inventée, pas d'avis inventé, pas de témoignage sans citation réelle.
- Publicités écrites dans la langue du marché visé.
- Distinction explicite entre ce qu'un script fait respecter et ce qui repose sur le comportement du modèle. Le statique a `SAFETY.md` pour ça, avec un test nommé derrière chaque règle. Le pack vidéo en a un aussi, ou il ment.
- Vérification Python au premier lancement, avec demande avant installation.

---

## 10. Ce qui est déjà prêt dans ce dépôt

| Chemin | Contenu |
|---|---|
| `staging/references/` | dix références écrites : rétention, prompting, modèles, scraping, musique, montage, hooks, seuils, conformité, standard de sortie |
| `staging/transferred/` | tout ce qui a été retiré des packs statiques, avec `TRANSFERRED.md` qui dit d'où vient chaque morceau et ce qu'il faut recâbler |
| `research/sources.json` | les 73 sources inspectées, épinglées ; 18 sont routées vidéo ou voix et alimentent ce pack |

`TRANSFERRED.md` contient aussi le code à remettre : l'artefact `storyboard` et ses trois tests, les lignes de fournisseurs, les deux sélections top-dix.

---

## 11. L'ordre de travail

1. Relire ce brief et le contredire là où il a tort.
2. Attendre le go de l'auteur.
3. Recherche : les trois tirages, les vidéos IA, les dix skills GitHub, le catalogue de voix.
4. Écrire les références qui manquent, durcir celles qui existent.
5. Les quatre entrypoints, en réutilisant le build, l'installeur, le validateur et les tests du statique au lieu d'en diverger.
6. Sécurité, tests, validateur au vert, `SAFETY.md` honnête.
7. Publication.

---

## 12. Ce qui a été tranché

Les deux questions ouvertes ont été fermées par l'auteur le 6 septembre 2026. Rien ne reste en suspens.

**Quatre skills.** Le build produit N packs depuis une liste de noms, donc le quatrième coûte un `SKILL.md` et une ligne. Et les deux duos ne sont pas redondants : celui qui pilote écrit le plan et délègue, or les deux côtés n'ont pas les mêmes capacités, Codex génère la vidéo et Claude non. Supprimer un sens du duo, c'est laisser sans point d'entrée la personne assise de ce côté.

**Les noms restent `video-ads-*`.** Ce sont ceux que l'auteur a écrits, et ils disent ce que fait le pack. `dynamic` reste le nom du dépôt.

Le partage du travail entre Claude Code et Codex est dans [`ROLES.md`](ROLES.md), posé avant le premier fichier, avec la définition de ce que veut dire fini.

---

## 13. Ce que Codex a relevé sur ce brief

Revue du 6 septembre 2026, lecture seule, texte complet dans `staging/review-codex-2026-09-06.md`.

**Corrigé immédiatement.** Deux contradictions réelles dans les références déjà écrites :

- `video-assembly.md` demandait 8 à 12 Mbps et, deux lignes plus bas, moins de 4 Mo pour 15 secondes. Les deux ne tiennent pas ensemble : 10 Mbps pendant 15 secondes font environ 19 Mo. La taille de fichier devient une conséquence du débit, et la cause du texte flou était écrite à l'envers. C'est un débit trop bas qui ramollit les sous-titres, pas un fichier trop lourd.
- `scrape.max_pull` plafonne à 60 par run alors qu'on demande 90 vidéos. Les trois tirages sont maintenant écrits comme trois runs de 30, ce qui passe sous le plafond.

**Fausse alerte, vérifiée.** Codex signale que `research.md`, `intake.md`, `providers.md` et `static.md` manquent. Ils existent, dans le tronc commun du pack statique, et le pack vidéo les partagera. Rien à faire.

**Ce qu'il faut acter avant de construire.** Sa critique tient et rejoint la section 3.5 :

- Un classement public des vidéos Facebook les plus regardées n'existe pas. Une bibliothèque publicitaire prouve qu'une pub a tourné, jamais qu'elle a été rentable. On produit donc un échantillon de convenance, daté, méthode et biais écrits, et on n'écrit jamais « les 30 meilleures ».
- « Top 30 TikTok » doit être défini avant d'être exécuté : organique ou publicitaire, classé par quoi, sur quelle région.
- « Lesquelles ont marché et pourquoi » n'est démontrable qu'avec des données de compte. Sans elles, toute affirmation de performance est une hypothèse, et le pack l'étiquette comme telle.
- « Top 10 des skills GitHub » a besoin d'un critère écrit. Un dépôt sans licence ne se réutilise pas.
- « Codex génère, Claude ne génère pas » dépend de l'hôte et des outils réellement branchés. Le pack teste la capacité au moment de s'en servir au lieu de la promettre dans un fichier.

**Ajouté à la liste de travail.** Consentement vocal vérifiable et révocable, politique de conservation de la voix avec accès et purge, spécification de la transcription, contrôles audio mesurables comme le loudness, les crêtes, le clipping et la synchro des sous-titres, reprise après interruption, traçabilité des coûts réels, et des tests d'intégration sur de vraies petites vidéos plutôt que sur des exemples inventés.
