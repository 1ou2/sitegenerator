---
title: Sortie du Nvidia DGX Spark
date: 2025-10-16
tags: IA, hardware, DGX spark
abstract: Je me suis penché sur le DGX Spark, la nouvelle machine IA de Nvidia. Pas le plus rapide pour l’inférence, mais un bijou pour l’entraînement et le développement. Avec 128 Go de RAM, un environnement complet prêt à l’emploi et un silence bluffant, c’est une machine qui donne envie… si on peut se permettre ses 4 400 €.
---

Nvidia vient d’annoncer la sortie du DGX Spark, une petite bête présentée comme une alternative locale pour le développement en Intelligence artificielle. Annoncé en mars 2025, il a fallu attendre le 15 octobre 2025 pour voir les premiers retours d’utilisateurs.

De mon côté, j’avais fait une pré-réservation dès mars, et depuis je suis resté à l’affût de toute information. 
[![](nvidia-reservation.jpg)](nvidia-reservation.jpg)

Même si je ne l’ai pas encore entre les mains, j’ai lu et analysé beaucoup d’articles pour savoir ce qu’elle vaut vraiment et pour quel usage elle brille… ou déçoit.

# TLDR;

Le Nvidia DGX Spark n’est pas une machine grand public pour « juste utiliser » des modèles d’IA en local : pour de l’inférence pure, elle est souvent moins rapide et plus chère que des alternatives AMD, Mac ou Nvidia classiques.

En revanche, pour le développement et l’entraînement de modèles IA, c’est une machine taillée pour les pros : silencieuse, compacte, prête à l’emploi avec un environnement NVIDIA complet, idéale pour tester, fine-tuner et travailler localement sur de gros modèles.

En résumé : pas top pour l’inférence, excellente pour le développement IA.

# Utilisation pour de l’inférence

Le DGX Spark n’est pas forcément la machine la plus rapide pour de l’inférence “classique”, comme générer du texte avec un LLM standard. Mais réduire cette machine à ce seul usage serait injuste : elle brille dans des scénarios plus complexes.  
Pour analyser et comparer les performances, on va parler de deux métriques importantes : Token Generation (TG) et Prefill Prompt (PP).

## Token Generation (TG) – vitesse de génération

La métrique la plus souvent citée pour juger une machine en inférence est la vitesse de génération par token. Sur ce critère, le DGX Spark se situe derrière certaines machines desktop et cartes graphiques haut de gamme, car la vitesse de sa RAM limite la génération pour des modèles standards.

| Plateforme              | Vitesse mémoire (GB/s) |
| ----------------------- | ---------------------- |
| Apple M4                | 120 GB/s               |
| Apple M4 Pro            | 273 GB/s               |
| AMD Strix Halo          | 273 GB/s               |
| NVIDIA DGX Spark        | 273 GB/s               |
| Apple M4 Max            | 546 GB/s               |
| Mac Ultra (M3 Ultra)    | 819 GB/s               |
| NVIDIA GeForce RTX 3090 | 936 GB/s               |
| NVIDIA GeForce RTX 4090 | 1 008 GB/s             |
| NVIDIA GeForce RTX 5090 | 1 792 GB/s             |

Si c’est votre critère le plus important, il y a beaucoup plus rapide chez Apple !

## Prefill Prompt (PP) – performance sur prompts longs

Mais la génération ne se limite pas à un prompt court. Si vous utilisez des prompts très longs ou des contextes étendus, comme dans le RAG, l’analyse de gros blocs de code, ou des scénarios multi-LLM, une autre métrique devient cruciale : le Prefill Prompt (PP).

Ici, le DGX Spark est très performant. Son CPU puissant et sa grande RAM permettent de traiter des contextes longs sans ralentissement majeur. C’est d’ailleurs aujourd’hui le point faible des Mac pour des tâches d’inférence.

## Scénarios avancés et concurrence

La vraie force du DGX Spark se révèle lorsqu’on exploite sa mémoire massive de 128 Go et sa compatibilité CUDA : 

- Charger des modèles très lourds (LLM à plusieurs dizaines de milliards de paramètres).  
- Faire tourner plusieurs modèles simultanément, idéal pour des systèmes agentiques où plusieurs LLM communiquent entre eux.  
- Avoir un gros contexte.

Comparé à la concurrence :  

- Nvidia desktop (3090, 4090, 5090) : plus rapide pour un LLM unique, mais moins pratique pour des modèles massifs ou multiples.  
- Mac : excellente vitesse sur un LLM classique, mais limité par la RAM et l’absence de CUDA pour l’entraînement.  
- AMD Strix Halo : bon rapport qualité/prix pour de l’inférence simple, mais moins adapté aux scénarios avancés. Exemple avec un [Framework desktop AMD](https://frame.work/fr/fr/products/desktop-diy-amd-aimax300/configuration/new) pour un prix simulé à 2 754 € : AMD MAX+ 395, 128 Go de RAM LPDDR5x, 4 To de disque SSD.

En résumé, le DGX Spark n’est pas un champion pour l’inférence classique, mais pour des scénarios avancés ou multi-modèles, c’est une machine extrêmement capable. Son véritable frein reste le prix : autour de 4 400 €, il faut être prêt à payer pour cette flexibilité et cette puissance locale.

# L’entraînement et le développement IA

Si le DGX Spark n’est pas forcément le meilleur choix pour de l’inférence classique, c’est sur l’entraînement et le développement que cette machine révèle toute sa valeur. Pour les développeurs IA, c’est un véritable petit laboratoire local.

## Points forts hardware

Le DGX Spark a été conçu pour être à la fois compact et silencieux. On peut le laisser tourner pendant des heures sans bruit ni surchauffe. Sa mémoire massive de 128 Go et son stockage rapide permettent de charger de très gros modèles et de gérer plusieurs projets simultanément, un vrai avantage par rapport à un desktop classique.

## Environnement logiciel prêt à l’emploi

La machine est fournie avec une version customisée d’Ubuntu, prête pour le développement IA : Docker, les bons drivers NVIDIA, CUDA… tout est déjà configuré. Plus besoin de passer des heures à installer et tester les bons outils.

Côté logiciels, vous bénéficiez de l’écosystème NVIDIA complet, parfaitement intégré avec Pytorch. Vous pouvez entraîner, fine-tuner ou expérimenter vos modèles locaux comme sur un serveur cloud, mais en restant chez vous. Les tutoriels officiels et guides fournis par Nvidia sont d’excellente qualité et facilitent la prise en main : [build.nvidia.com/spark](https://build.nvidia.com/spark)

## Capacités pour l’entraînement et le fine-tuning

Grâce à sa puissance, vous pouvez :

- Entraîner des modèles lourds localement, sans dépendre du cloud.  
- Fine-tuner des LLM sur vos propres données.  
- Faire tourner plusieurs modèles simultanément pour des projets complexes ou des systèmes multi-LLM.

La grande mémoire et le CPU performant permettent de travailler sur des contextes très larges, idéal pour les projets de RAG ou les analyses complexes.

## Usage distant et serveur local

Vous pouvez également accéder à la machine à distance via Nvidia SYNC, ce qui permet de l’utiliser comme serveur local. Cela facilite le travail collaboratif ou l’accès aux modèles depuis plusieurs machines sur le même réseau.

## Conclusion

En résumé, le DGX Spark est une machine pensée pour les développeurs IA et les chercheurs. Compacte, silencieuse et prête à l’emploi, elle offre une expérience proche d’un environnement cloud, mais en local, avec la liberté de tester, entraîner et fine-tuner des modèles de manière flexible et sécurisée. Si votre objectif est le développement IA sérieux, c’est un excellent choix.
PS: ne pas craquer, ne pas craquer, ...

# Mon avis

Le Nvidia DGX Spark n’est pas une machine “grand public” pour de l’inférence simple : pour générer du texte avec un LLM classique, elle est souvent moins rapide et plus chère que des alternatives AMD, Mac ou Nvidia desktop.

Mais réduire le DGX Spark à ce seul usage serait passer à côté de sa vraie valeur. Pour l’entraînement et le développement IA, c’est une machine exceptionnelle : silencieuse, compacte, prête à l’emploi avec un environnement NVIDIA complet, capable de gérer de très gros modèles ou plusieurs modèles simultanément grâce à ses 128 Go de RAM.

En résumé :

- Pour de l’inférence simple : le rapport qualité/prix est moyen.  
- Pour des scénarios avancés (multi-LLM, contextes longs, fine-tuning local) : c’est un outil puissant et flexible.

Si vous êtes développeur, chercheur ou étudiant sérieux en IA et que vous voulez un laboratoire IA local, cette machine fait vraiment envie. Si votre usage se limite à “tester des modèles” ou générer du texte ponctuellement, il existe des alternatives plus rapides et surtout moins coûteuses.

Bref, c’est cher mais ça fait envie !

# Références

- [Tests de performance fait sur llama.cpp](https://github.com/ggml-org/llama.cpp/discussions/16578)  
- [Avis d’un possesseur heureux – continue.dev](https://blog.continue.dev/my-new-developer-workstation-nvidia-dgx-spark/)  
- [Analyse en profondeur du hardware et des performances – StorageReview](https://www.storagereview.com/review/nvidia-dgx-spark-review-the-ai-appliance-bringing-datacenter-capabilities-to-desktops)
