# Référentiel RNCP — Développeur en Intelligence Artificielle

**Code RNCP** : 37827
**Certificateur** : Simplon.co
**Niveau** : 6 (équivalent Licence)

Ce référentiel décrit les 21 compétences attendues pour la certification de Développeur en Intelligence Artificielle, organisées en 3 blocs de compétences. Chaque compétence est rattachée à une activité professionnelle et à une modalité d'évaluation.

---

## Bloc 1 — Réaliser la collecte, le stockage et la mise à disposition des données d'un projet en intelligence artificielle

Ce bloc regroupe les compétences C1 à C5. Il couvre la collecte multi-sources, l'agrégation et le nettoyage des données, la création de bases de données conformes au RGPD, et l'exposition des données via une API REST.

### Compétence C1 — Automatiser l'extraction de données

**Activité parente** : A1 — Programmer la collecte de données depuis plusieurs sources pour un projet en intelligence artificielle
**Modalité d'évaluation** : E1 — Mise en situation professionnelle (projet de service numérique réel ou fictif)

**Énoncé** : Automatiser l'extraction de données depuis un service web, une page web (scraping), un fichier de données, une base de données et un système big data en programmant le script adapté afin de pérenniser la collecte des données nécessaires au projet.

**Activités détaillées** :
- Identification des contraintes techniques propres aux sources de données (documentation, règles de confidentialité)
- Rédaction des spécifications techniques pour l'extraction des données
- Construction des requêtes HTTP pour la récupération depuis un service web (REST)
- Lecture d'un fichier de données dans un script (Python, R, etc.)
- Téléchargement de l'HTML d'une ou plusieurs pages web visées par scraping
- Connexion programmatique à un système de gestion de base de données et à un système big data (Hive, Apache Impala, etc.)
- Programmation des filtrages et parsing des données utiles depuis les résultats d'API, fichiers, ou HTML scrapé
- Exécution programmatique des requêtes d'extraction SQL
- Exécution programmatique des requêtes d'extraction depuis un système big data
- Versionnement des scripts avec Git et un dépôt Git en ligne
- Documentation des scripts

**Critères d'évaluation** :
- La présentation du projet et de son contexte est complète : acteurs, objectifs fonctionnels et techniques, environnements, contraintes, budget, organisation et planification
- Les spécifications techniques précisent les technologies, outils, services externes, exigences de programmation et accessibilité
- Le script d'extraction est fonctionnel : toutes les données visées sont effectivement récupérées
- Le script comprend un point de lancement, l'initialisation des dépendances et connexions, les règles logiques de traitement, la gestion des erreurs et exceptions, la fin du traitement et la sauvegarde des résultats
- Le script est versionné et accessible depuis un dépôt Git
- L'extraction est faite depuis un mix d'au moins ces sources : API REST, fichier de données, scraping, base de données, système big data

---

### Compétence C2 — Développer des requêtes SQL d'extraction

**Activité parente** : A1 — Programmer la collecte de données depuis plusieurs sources
**Modalité d'évaluation** : E1 — Mise en situation professionnelle

**Énoncé** : Développer des requêtes de type SQL d'extraction des données depuis un système de gestion de base de données et un système big data en appliquant le langage de requête propre au système afin de préparer la collecte des données nécessaires au projet.

**Activités détaillées** :
- Écriture des requêtes d'extraction SQL pour la récupération de données stockées en base de données
- Écriture des requêtes d'extraction depuis un système big data (Hive, Spark, etc.)
- Documentation des requêtes d'extraction

**Critères d'évaluation** :
- Les requêtes SQL pour la collecte sont fonctionnelles : les données visées sont effectivement extraites
- La documentation des requêtes met en lumière les choix de sélections, filtrages, conditions, jointures, en fonction des objectifs de collecte
- La documentation explicite les optimisations appliquées aux requêtes

---

### Compétence C3 — Développer des règles d'agrégation de données

**Activité parente** : A1 — Programmer la collecte de données depuis plusieurs sources
**Modalité d'évaluation** : E1 — Mise en situation professionnelle

**Énoncé** : Développer des règles d'agrégation de données issues de différentes sources en programmant, sous forme de script, la suppression des entrées corrompues et en programmant l'homogénéisation des formats des données afin de préparer le stockage du jeu de données final.

**Activités détaillées** :
- Rédaction des spécifications techniques pour l'agrégation des données
- Programmation des règles d'agrégation des données collectées en un jeu de données brutes unique
- Programmation de l'identification des entrées corrompues (données partielles, manquantes)
- Programmation de la suppression des entrées corrompues
- Programmation de l'identification des entrées au format non normalisé
- Programmation de l'homogénéisation des formats de données (dates, unités, etc.)

**Critères d'évaluation** :
- Le script d'agrégation est fonctionnel : les données sont effectivement agrégées, nettoyées et normalisées en un seul jeu de données
- Le script est versionné et accessible depuis un dépôt Git
- La documentation du script est complète : dépendances, commandes, enchaînements logiques de l'algorithme, choix de nettoyage et d'homogénéisation des formats

---

### Compétence C4 — Créer une base de données dans le respect du RGPD

**Activité parente** : A2 — Développer la mise à disposition technique des données collectées
**Modalité d'évaluation** : E1 — Mise en situation professionnelle

**Énoncé** : Créer une base de données dans le respect du RGPD en élaborant les modèles conceptuels et physiques des données à partir des données préparées et en programmant leur import afin de stocker le jeu de données du projet.

**Activités détaillées** :
- Rédaction des spécifications techniques pour le stockage des données
- Modélisation de la structure des données selon la méthode Merise
- Choix du système de gestion de base de données
- Création de la base de données dans le SGBD
- Documentation de la procédure d'installation du SGBD
- Rédaction ou mise à jour du registre des traitements de données personnelles pour la mise en conformité RGPD
- Rédaction des procédures de tri des données personnelles (détection et suppression des données inutiles, trop anciennes, etc.)
- Programmation du script d'import des données en base
- Documentation du script d'import

**Critères d'évaluation** :
- Les modélisations respectent la méthode et le formalisme Merise
- Le modèle physique est fonctionnel : il est intégré avec succès lors de la création de la base, sans erreur
- La base est choisie au regard de la modélisation des données et des contraintes du projet
- La reproduction des procédures d'installation décrites a pour résultat un système conforme aux objets techniques attendus
- Le script d'import est fonctionnel : il permet l'insertion des données dans le système
- La documentation technique du script d'import est versionnée à la racine du même dépôt Git
- Les documentations couvrent les dépendances et les commandes pour l'exécution des scripts
- Le registre des traitements intègre l'ensemble des traitements de données personnelles
- Les procédures de tri pour la mise en conformité RGPD sont rédigées
- Les procédures détaillent les traitements de conformité (automatisés ou non) et leur fréquence d'exécution

---

### Compétence C5 — Développer une API REST mettant à disposition le jeu de données

**Activité parente** : A2 — Développer la mise à disposition technique des données collectées
**Modalité d'évaluation** : E1 — Mise en situation professionnelle

**Énoncé** : Développer une API mettant à disposition le jeu de données en utilisant l'architecture REST afin de permettre l'exploitation du jeu de données par les autres composants du projet.

**Activités détaillées** :
- Rédaction des spécifications techniques des moyens de mise à disposition et d'accès aux données : API REST et accès direct à la base
- Configuration des accès au jeu de données depuis le serveur de l'API
- Développement de la réception et de la validation des requêtes client (web, mobile)
- Développement des requêtes à la base de données selon les spécifications
- Développement des réponses de l'API au client
- Développement des règles d'autorisation et d'accès aux points de terminaison
- Sécurisation de l'API selon le Top 10 OWASP API
- Rédaction de la documentation technique de l'API REST
- Rédaction de la documentation technique d'accès à la base de données

**Critères d'évaluation** :
- La documentation technique de l'API REST couvre tous les points de terminaison
- La documentation couvre les règles d'authentification et d'autorisation de l'API
- La documentation respecte les standards du modèle choisi (par exemple OpenAPI)
- L'API REST est fonctionnelle pour l'accès aux données : elle restreint l'accès par autorisation ou authentification
- L'API REST est fonctionnelle pour la mise à disposition : elle permet la récupération de l'ensemble des données nécessaires au projet selon les spécifications

---

## Bloc 2 — Intégrer des modèles et des services d'intelligence artificielle

Ce bloc regroupe les compétences C6 à C13. Il couvre la veille technologique, le benchmark et le paramétrage de services IA, le développement d'API exposant des modèles, le monitoring, les tests automatisés et la chaîne de livraison continue MLOps.

### Compétence C6 — Organiser et réaliser une veille technique et réglementaire

**Activité parente** : A3 — Accompagner le choix et l'intégration d'un service d'intelligence artificielle préexistant
**Modalité d'évaluation** : E2 — Cas pratique (expression d'un besoin en fonctionnalités IA)

**Énoncé** : Organiser et réaliser une veille technique et réglementaire en animant le travail collectif de sélection des sources, de collecte, de traitement et de partage des informations afin de formuler des recommandations pour le projet toujours en phase avec l'état de l'art.

**Activités détaillées** :
- Définition des thématiques de veille
- Planification des temps dédiés à la veille
- Choix d'un outil d'agrégation des flux d'informations et d'actualités
- Choix d'un outil de partage ou communication des synthèses
- Identification des sources et flux d'informations utiles à la veille thématique
- Qualification de la fiabilité des sources et flux identifiés
- Configuration des outils d'agrégation selon les flux et thématiques
- Rédaction des synthèses des informations collectées
- Communications des synthèses aux parties prenantes

**Critères d'évaluation** :
- La thématique de veille porte sur un outil ou une réglementation mobilisée dans la mise en situation
- Les temps de veille sont planifiés régulièrement (minimum hebdomadaire)
- Le choix des outils d'agrégation est cohérent avec les sources et le budget (RSS, réseaux sociaux, newsletters)
- Les synthèses sont communiquées dans un format respectant les recommandations d'accessibilité
- Les informations partagées répondent à la thématique de veille
- Les sources répondent aux critères de fiabilité : auteur identifié, informations sur l'auteur disponibles, contenu valable (date récente, sources indiquées, niveau de langue correct), source structurée, normes d'accessibilité respectées, information confirmée par d'autres sites de confiance

---

### Compétence C7 — Identifier des services d'intelligence artificielle préexistants

**Activité parente** : A3 — Accompagner le choix et l'intégration d'un service IA préexistant
**Modalité d'évaluation** : E2 — Cas pratique

**Énoncé** : Identifier des services d'intelligence artificielle préexistants à partir de l'expression de besoin en fonctionnalités IA, en réalisant un benchmark de services existants et en analysant leurs caractéristiques pour formaliser une ou plusieurs recommandations de services adaptés au besoin.

**Activités détaillées** :
- Définition de la problématique technique et fonctionnelle d'IA à adresser à partir de l'expression de besoin
- Identification des contraintes de moyens, techniques et opérationnelles liées au contexte du projet
- Benchmark des outils et services d'IA accessibles répondant au problème visé
- Rédaction des conclusions préconisant un ou plusieurs services d'IA

**Critères d'évaluation** :
- L'expression de besoin est reformulée et présente les objectifs et contraintes du projet d'intégration
- Le benchmark liste les services étudiés et les services non étudiés
- Les raisons pour écarter un service sont explicitées
- Le benchmark détaille le niveau d'adéquation du service étudié pour chaque ensemble fonctionnel souhaité
- Le benchmark détaille le niveau de la démarche éco-responsable du service étudié
- Le benchmark détaille les principales contraintes techniques et pré-requis pour chaque solution
- Les conclusions délimitent clairement les services répondant aux besoins (avec avantages et inconvénients) des services ne couvrant pas les besoins

---

### Compétence C8 — Paramétrer un service d'intelligence artificielle

**Activité parente** : A3 — Accompagner le choix et l'intégration d'un service IA préexistant
**Modalité d'évaluation** : E2 — Cas pratique

**Énoncé** : Paramétrer un service d'intelligence artificielle en suivant sa documentation technique et en respectant les spécifications du projet, afin de permettre l'intégration des connecteurs du service dans le système d'information.

**Activités détaillées** :
- Création de l'environnement d'exécution du service (compte SaaS, VPS, sur-site, etc.)
- Installation et configuration des dépendances (SDK, outils, autres services SaaS)
- Création des accès à l'environnement d'exécution et de configuration (comptes, groupes, droits)
- Installation et configuration des outils de monitorage disponibles avec le service intégré
- Rédaction de la documentation

**Critères d'évaluation** :
- Le service installé est accessible avec une éventuelle authentification
- Le service est configuré correctement et répond aux besoins fonctionnels et contraintes techniques
- Le monitorage disponible du service est opérationnel
- La documentation couvre la gestion des accès, les procédures d'installation et de test, les dépendances et interconnexions, les données impliquées
- La documentation est communiquée dans un format respectant les recommandations d'accessibilité

---

### Compétence C9 — Développer une API exposant un modèle d'intelligence artificielle

**Activité parente** : A4 — Réaliser l'intégration d'un modèle ou d'un service d'intelligence artificielle
**Modalité d'évaluation** : E3 — Mise en situation professionnelle (mise en service d'un modèle fourni)

**Énoncé** : Développer une API exposant un modèle d'intelligence artificielle en utilisant l'architecture REST pour permettre l'interaction entre le modèle et les autres composants du projet.

**Activités détaillées** :
- Analyse des spécifications fonctionnelles et techniques fournies par le commanditaire
- Conception de l'architecture de l'API : points de terminaison, règles d'accès
- Choix des outils et langages de programmation pour le développement de l'API
- Installation et configuration de l'environnement de développement
- Développement de la vérification et transformation des paramètres envoyés par le client au format attendu par le modèle
- Développement de l'exécution du modèle à partir de la requête client
- Développement de la réponse de l'API au client avec le résultat du modèle
- Développement des règles d'autorisation et d'accès aux points de terminaison
- Sécurisation de l'API : Top 10 OWASP API
- Développement des tests d'intégration validant le bon fonctionnement des points de terminaison
- Versionnement des sources avec Git et dépôt distant
- Rédaction et génération de la documentation de l'API

**Critères d'évaluation** :
- L'API restreint l'accès au modèle d'IA avec un moyen d'authentification
- L'API permet l'accès aux fonctions du modèle selon les spécifications
- Les recommandations de sécurisation du Top 10 OWASP sont intégrées
- Les sources sont versionnées et accessibles depuis un dépôt Git distant
- Les tests couvrent tous les points de terminaison dans le respect des spécifications
- Les tests s'exécutent sans bug et leurs résultats sont correctement interprétés
- La documentation couvre l'architecture, tous les points de terminaison, les règles d'authentification et d'autorisation
- La documentation et l'API respectent les standards d'un modèle choisi (par exemple OpenAPI)
- La documentation respecte les recommandations d'accessibilité

---

### Compétence C10 — Intégrer l'API d'un modèle ou d'un service d'IA dans une application

**Activité parente** : A4 — Réaliser l'intégration d'un modèle ou d'un service IA
**Modalité d'évaluation** : E3 — Mise en situation professionnelle

**Énoncé** : Intégrer l'API d'un modèle ou d'un service d'intelligence artificielle dans une application, en respectant les spécifications du projet et les normes d'accessibilité en vigueur, à l'aide de la documentation technique de l'API, afin de créer les fonctionnalités d'intelligence artificielle de l'application.

**Activités détaillées** :
- Installation de l'environnement de développement de l'application
- Programmation des étapes d'authentification ou d'autorisation avec l'API
- Programmation de la communication avec les points de terminaison de l'API du modèle ou service IA
- Intégration des adaptations d'interface dues à l'intégration de l'IA
- Test et validation du niveau d'accessibilité des interfaces modifiées
- Développement des tests d'intégration sur le périmètre de l'API exploité
- Versionnement des sources avec Git sur le dépôt de l'application

**Critères d'évaluation** :
- L'application de départ est installée et fonctionnelle en environnement de développement
- La communication avec l'API depuis l'application fonctionne
- Les étapes d'authentification et de renouvellement (expiration des jetons) sont intégrées correctement
- Tous les points de terminaison de l'API concernés sont intégrés selon les spécifications
- Les adaptations d'interfaces nécessaires sont intégrées en accord avec les spécifications
- Les tests d'intégration couvrent tous les points de terminaison exploités
- Les tests s'exécutent en totalité sans bug et leurs résultats sont correctement interprétés
- Les sources sont versionnées et accessibles depuis le dépôt Git de l'application

---

### Compétence C11 — Monitorer un modèle d'intelligence artificielle

**Activité parente** : A5 — Faciliter le déploiement d'un modèle d'IA avec une approche MLOps
**Modalité d'évaluation** : E3 — Mise en situation professionnelle

**Énoncé** : Monitorer un modèle d'intelligence artificielle à partir des métriques courantes et spécifiques au projet, en intégrant les outils de collecte, d'alerte et de restitution des données du monitorage pour permettre l'amélioration du modèle de façon itérative.

**Activités détaillées** :
- Liste des métriques du modèle à monitorer et des déclencheurs pour le réentraînement (stabilité des données, performance du modèle, santé du système)
- Choix d'une solution ou d'un outil pour le monitorage et la consolidation des indicateurs
- Intégration de la solution de monitorage : intégration des collecteurs, intégration des déclencheurs pour l'entraînement continu
- Sélection d'un outil de restitution des métriques (Grafana, Dash, Kibana, etc.)
- Intégration de l'outil de restitution et des alertes (notifications, e-mails)
- Test et validation du bon fonctionnement de la chaîne de monitorage
- Versionnement des sources avec Git sur dépôt distant
- Rédaction de la documentation technique des procédures d'installation et de maintenance
- Rédaction de la documentation utilisateur pour l'utilisation du monitorage

**Critères d'évaluation** :
- Les métriques sont expliquées sans erreur d'interprétation
- Les outils d'intégration du monitorage sont adaptés au contexte et aux contraintes techniques
- Au moins un vecteur de restitution des métriques en temps réel est proposé (dashboard, feuille de calcul)
- Les enjeux d'accessibilité sont pris en compte lors de la sélection de l'outil de restitution
- La chaîne de monitorage est d'abord testée dans un bac à sable ou environnement de test dédié
- La chaîne de monitorage est en état de marche : les métriques visées sont effectivement évaluées et restituées
- Les sources sont versionnées et accessibles depuis un dépôt Git distant
- La documentation technique couvre la procédure d'installation, de configuration, et d'utilisation du monitorage
- La documentation respecte les recommandations d'accessibilité

---

### Compétence C12 — Programmer les tests automatisés d'un modèle d'intelligence artificielle

**Activité parente** : A5 — Faciliter le déploiement d'un modèle d'IA avec une approche MLOps
**Modalité d'évaluation** : E3 — Mise en situation professionnelle

**Énoncé** : Programmer les tests automatisés d'un modèle d'intelligence artificielle en définissant les règles de validation des jeux de données, des étapes de préparation des données, d'entraînement, d'évaluation et de validation du modèle pour permettre son intégration en continu et garantir un niveau de qualité élevé.

**Activités détaillées** :
- Définition avec les équipes développement du périmètre des tests pour chaque composante du modèle : format des données, complétude et labellisation, phase d'entraînement, phase de validation
- Choix des outils de test (unittest par exemple)
- Installation et configuration de l'environnement d'exécution des tests
- Intégration des tests : assertions, mocks, fixtures
- Versionnement des sources et des données si possible (DVC, Gitlab)
- Rédaction de documentation technique pour la configuration de l'environnement et l'exécution des tests

**Critères d'évaluation** :
- L'ensemble des cas à tester sont listés et définis : partie du modèle visée, périmètre, stratégie de test
- Les outils de test (framework, bibliothèque) choisis sont cohérents avec l'environnement technique
- Les tests sont intégrés et respectent la couverture souhaitée
- Les tests s'exécutent sans problème technique en environnement de test
- Les sources sont versionnées et accessibles depuis un dépôt Git distant (DVC, Gitlab)
- La documentation couvre la procédure d'installation de l'environnement de test, les dépendances, l'exécution des tests, le calcul de la couverture
- La documentation respecte les recommandations d'accessibilité

---

### Compétence C13 — Créer une chaîne de livraison continue d'un modèle d'IA (MLOps)

**Activité parente** : A5 — Faciliter le déploiement d'un modèle d'IA avec une approche MLOps
**Modalité d'évaluation** : E3 — Mise en situation professionnelle

**Énoncé** : Créer une chaîne de livraison continue d'un modèle d'intelligence artificielle en installant les outils et en appliquant les configurations souhaitées, dans le respect du cadre imposé par le projet et dans une approche MLOps, pour automatiser les étapes de validation, de test, de packaging et de déploiement du modèle.

**Activités détaillées** :
- Définition des étapes, tâches et déclencheurs de la chaîne de livraison continue (réentraînement, exécution des tests, livraison en pré-production)
- Paramétrage de la chaîne : variables d'environnement, versions des environnements et dépendances, déclencheurs
- Intégration de l'exécution des tests du modèle et des données
- Intégration des étapes d'entraînement et d'évaluation du modèle
- Intégration de la génération des rapports d'évaluation (accuracy, confusion matrix, etc.)
- Intégration de l'étape de livraison (sous forme de pull request par exemple) avec rapports d'évaluation attachés
- Versionnement des sources de la chaîne sur dépôt Git du projet (DVC, Gitlab)
- Documentation des procédures d'installation et de test de la chaîne
- Documentation utilisateur pour le déclenchement de la chaîne

**Critères d'évaluation** :
- La documentation pour l'utilisation de la chaîne couvre toutes les étapes, tâches et déclencheurs disponibles
- Les déclencheurs sont intégrés comme préalablement définis
- Les fichiers de configuration de la chaîne sont correctement reconnus et exécutés selon les déclencheurs
- L'étape de test des données est intégrée à la chaîne et s'exécute sans erreur
- Les étapes de test, d'entraînement et de validation du modèle sont intégrées et s'exécutent sans erreur
- Les sources de la chaîne sont versionnées et accessibles depuis le dépôt Git distant du projet
- La documentation couvre la procédure d'installation, de configuration et de test de la chaîne
- La documentation respecte les recommandations d'accessibilité

---

## Bloc 3 — Réaliser une application intégrant un service d'intelligence artificielle

Ce bloc regroupe les compétences C14 à C21. Il couvre l'analyse de besoin et la conception d'application, la coordination en méthode agile, le développement front-end et back-end, l'intégration continue et la livraison continue, le monitoring applicatif et la résolution d'incidents.

### Compétence C14 — Analyser le besoin d'application intégrant un service d'IA

**Activité parente** : A6 — Concevoir une application intégrant un service d'intelligence artificielle
**Modalité d'évaluation** : E4 — Mise en situation professionnelle (développement d'une application intégrant un service IA)

**Énoncé** : Analyser le besoin d'application d'un commanditaire intégrant un service d'intelligence artificielle, en rédigeant les spécifications fonctionnelles et en le modélisant, dans le respect des standards d'utilisabilité et d'accessibilité, afin d'établir avec précision les objectifs de développement correspondant au besoin et à la faisabilité technique.

**Activités détaillées** :
- Modélisation des données de l'application (entités-relations, MCD/MPD, etc.)
- Modélisation des parcours utilisateurs (schéma fonctionnel, story board, etc.)
- Rédaction des spécifications fonctionnelles sous forme de user stories
- Définition des objectifs techniques d'accessibilité des interfaces

**Critères d'évaluation** :
- La modélisation des données respecte un formalisme : Merise, entités-relations, etc.
- La modélisation des parcours utilisateurs respecte un formalisme : schéma fonctionnel, wireframes, etc.
- Chaque spécification fonctionnelle couvre le contexte, les scénarios d'utilisation et les critères de validation
- Les objectifs d'accessibilité sont directement intégrés aux critères d'acceptation des user stories
- Les objectifs d'accessibilité sont formulés en s'appuyant sur un standard d'accessibilité (WCAG, RG2AA, etc.)

---

### Compétence C15 — Concevoir le cadre technique d'une application intégrant un service d'IA

**Activité parente** : A6 — Concevoir une application intégrant un service IA
**Modalité d'évaluation** : E4 — Mise en situation professionnelle

**Énoncé** : Concevoir le cadre technique d'une application intégrant un service d'intelligence artificielle, à partir de l'analyse du besoin, en spécifiant l'architecture technique et applicative et en préconisant les outils et méthodes de développement, pour permettre le développement du projet.

**Activités détaillées** :
- Conception de l'architecture de l'application (n-tiers, serverless, micro-service, model-vue-controller, etc.)
- Choix des langages de programmation et outils pour l'environnement de développement (Python, Java, Node.js, React, Dash, GitHub, etc.)
- Identification des flux de données et zones de stockage : base de données, fichiers de journalisation, etc.
- Choix des services externes complémentaires (BaaS, paiements, cartographie, etc.)
- Rédaction des spécifications techniques

**Critères d'évaluation** :
- Les spécifications techniques rédigées couvrent l'architecture, ses dépendances et son environnement d'exécution (langage, framework, outils)
- Les services et prestataires ayant une démarche éco-responsable sont favorisés lors des choix techniques
- Les flux de données impliqués sont représentés par un diagramme de flux de données
- La preuve de concept est accessible et fonctionnelle en environnement de pré-production
- La conclusion à l'issue de la preuve de concept donne un avis précis permettant une prise de décision sur la poursuite du projet

---

### Compétence C16 — Coordonner la réalisation technique d'une application d'IA en méthode agile

**Activité parente** : A7 — Développer les interfaces et les fonctionnalités d'une application d'intelligence artificielle
**Modalité d'évaluation** : E4 — Mise en situation professionnelle

**Énoncé** : Coordonner la réalisation technique d'une application d'intelligence artificielle en s'intégrant dans une conduite agile de projet et un contexte MLOps et en facilitant les temps de collaboration dans le but d'atteindre les objectifs de production et de qualité.

**Activités détaillées** :
- Mise en place des outils et supports de pilotage selon la méthode agile retenue (SCRUM, Shape Up, etc.)
- Facilitation des rituels agiles et du respect du cadre des rituels
- Communication de l'avancement des productions techniques
- Communication des imprévus et des changements

**Critères d'évaluation** :
- Les cycles, étapes, rôles, rituels et outils de la méthode agile appliquée sont respectés tout au long du projet
- Les outils de pilotage (kanban, burndown chart, backlog, etc.) sont disponibles selon les conditions de la méthode appliquée
- Les objectifs et modalités des rituels sont partagés à toutes les parties prenantes
- Les éléments de pilotage sont rendus accessibles à toutes les parties du projet, en accord avec les recommandations de la méthode

---

### Compétence C17 — Développer les composants techniques et les interfaces d'une application

**Activité parente** : A7 — Développer les interfaces et les fonctionnalités
**Modalité d'évaluation** : E4 — Mise en situation professionnelle

**Énoncé** : Développer les composants techniques et les interfaces d'une application en utilisant les outils et langages de programmation adaptés et en respectant les spécifications fonctionnelles et techniques, les standards et normes d'accessibilité, de sécurité et de gestion des données en vigueur dans le but de répondre aux besoins fonctionnels identifiés.

**Activités détaillées** :
- Installation de l'environnement de développement du projet
- Intégration de la mise en page selon les maquettes graphiques
- Intégration des contenus des interfaces (textes, images, mise en page)
- Développement des fonctionnalités front-end (animations, validations, interactions avec APIs et services tiers)
- Développement des composants métiers (calculs spécifiques, fonctionnalités, email)
- Gestion des droits et accès à l'application (authentification, permissions, groupes)
- Intégration des composants d'accès aux données
- Sécurisation de l'application (Top 10 OWASP)
- Intégration de tests automatisés (unitaires, fonctionnels)
- Versionnement des sources avec Git sur dépôt distant
- Prise en compte des enjeux d'accessibilité dans le développement
- Rédaction de la documentation technique

**Critères d'évaluation** :
- L'environnement de développement installé respecte les spécifications techniques
- Les interfaces sont intégrées et respectent les maquettes
- Les comportements des composants d'interface (validation formulaire, animations) et la navigation respectent les spécifications fonctionnelles
- Les composants métier sont développés et fonctionnent comme prévu
- La gestion des droits d'accès est développée et respecte les spécifications fonctionnelles
- Les flux de données sont intégrés dans le respect des spécifications techniques et fonctionnelles
- Les développements respectent les bonnes pratiques d'éco-conception (éco-index, Green IT)
- Les préconisations du Top 10 OWASP sont implémentées quand nécessaire
- Des tests d'intégration ou unitaires couvrent au moins les composants métier et la gestion des accès
- Les sources sont versionnées et accessibles depuis un dépôt Git distant
- La documentation technique couvre l'installation de l'environnement, l'architecture applicative, les dépendances, l'exécution des tests
- La documentation respecte les recommandations d'accessibilité

---

### Compétence C18 — Automatiser les phases de tests via une chaîne d'intégration continue

**Activité parente** : A8 — Développer les fonctions de tests et de contrôle d'une application d'IA
**Modalité d'évaluation** : E4 — Mise en situation professionnelle

**Énoncé** : Automatiser les phases de tests du code source lors du versionnement des sources à l'aide d'un outil d'intégration continue de manière à garantir la qualité technique des réalisations.

**Activités détaillées** :
- Choix de l'outil d'intégration continue
- Définition des étapes, tâches et déclencheurs de la chaîne d'intégration continue
- Production des fichiers de configuration de la chaîne
- Configuration de l'automatisation : déclencheurs, variables d'environnement, dépendances, commandes à exécuter
- Test et validation du bon fonctionnement de la chaîne
- Versionnement des sources pour la configuration de la chaîne
- Documentation des procédures d'installation et de test
- Documentation utilisateur pour le déclenchement de la chaîne

**Critères d'évaluation** :
- La documentation pour l'utilisation de la chaîne couvre les outils, étapes, tâches et déclencheurs
- Un outil d'intégration continue est sélectionné de façon cohérente avec l'environnement technique
- La chaîne intègre toutes les étapes nécessaires et préalables à l'exécution des tests (build, configurations)
- La chaîne exécute les tests de l'application disponibles lors de son déclenchement
- Les configurations sont versionnées avec les sources du projet sur un dépôt Git distant
- La documentation couvre la procédure d'installation, de configuration et de test de la chaîne
- La documentation respecte les recommandations d'accessibilité

---

### Compétence C19 — Créer un processus de livraison continue d'une application

**Activité parente** : A8 — Développer les fonctions de tests et de contrôle
**Modalité d'évaluation** : E4 — Mise en situation professionnelle

**Énoncé** : Créer un processus de livraison continue d'une application en s'appuyant sur une chaîne d'intégration continue et en paramétrant les outils d'automatisation et les environnements de test afin de permettre une restitution optimale de l'application.

**Activités détaillées** :
- Définition des étapes, tâches et déclencheurs de la chaîne de livraison continue
- Paramétrage de la chaîne : variables d'environnement, versions, déclencheurs
- Configuration des étapes automatisées (build, pull request) à partir de la chaîne d'intégration continue
- Versionnement des configurations depuis le Git du projet
- Test de la chaîne de livraison continue
- Documentation de la procédure de livraison continue : outils, configurations, exécution, debug

**Critères d'évaluation** :
- La documentation pour l'utilisation de la chaîne couvre toutes les étapes, tâches et déclencheurs
- Les fichiers de configuration de la chaîne sont correctement reconnus et exécutés
- Les étapes de packaging (compilation, minification, build de containers) sont intégrées et s'exécutent sans erreur
- L'étape de livraison (pull request par exemple) est intégrée et exécutée une fois les étapes de packaging validées
- Les sources de la chaîne sont versionnées et accessibles depuis le dépôt Git distant
- La documentation couvre la procédure d'installation, de configuration et de test
- La documentation respecte les recommandations d'accessibilité

---

### Compétence C20 — Surveiller une application d'intelligence artificielle

**Activité parente** : A9 — Assurer le maintien en condition opérationnelle d'une application d'IA
**Modalité d'évaluation** : E5 — Cas pratique (application existante avec au moins une erreur technique)

**Énoncé** : Surveiller une application d'intelligence artificielle, en mobilisant des techniques de monitorage et de journalisation, dans le respect des normes de gestion des données personnelles en vigueur, afin d'alimenter la feedback loop dans une approche MLOps, et de permettre la détection automatique d'incidents.

**Activités détaillées** :
- Définition des métriques pour le monitorage de l'application
- Définition des seuils ou valeurs devant générer une alerte
- Choix d'une solution ou outil pour la consolidation et le suivi des indicateurs
- Configuration de l'outil de monitorage
- Intégration de la journalisation nécessaire aux objectifs de monitorage dans l'application
- Intégration d'alertes (e-mail, push) en fonction des indicateurs
- Documentation du monitorage et des procédures d'installation et configuration

**Critères d'évaluation** :
- La documentation liste les métriques, seuils et valeurs d'alerte pour chaque métrique à risque
- La documentation explicite les arguments en faveur des choix techniques pour l'outillage du monitorage
- Les outils (collecteurs, journalisation, agrégateurs, filtres, dashboard) sont installés et opérationnels au moins en environnement local
- Les règles de journalisation sont intégrées aux sources de l'application en fonction des métriques à surveiller
- Les alertes sont configurées et en état de marche selon les seuils définis
- La documentation couvre la procédure d'installation et de configuration des dépendances pour l'outillage du monitorage
- La documentation respecte les recommandations d'accessibilité

---

### Compétence C21 — Résoudre les incidents techniques

**Activité parente** : A9 — Assurer le maintien en condition opérationnelle
**Modalité d'évaluation** : E5 — Cas pratique

**Énoncé** : Résoudre les incidents techniques en apportant les modifications nécessaires au code de l'application et en documentant les solutions pour en garantir le fonctionnement opérationnel.

**Activités détaillées** :
- Analyse d'un message d'erreur (console ou fichier de journalisation)
- Recherche d'une solution à l'aide de ressources externes (documentation, plateformes en ligne)
- Test et validation d'une solution
- Versionnement de la solution depuis le dépôt Git du projet
- Documentation de l'erreur et de la solution implémentée

**Critères d'évaluation** :
- La ou les causes du problème sont identifiées correctement
- Le problème est reproduit en environnement de développement
- La procédure de débogage du code est documentée depuis l'outil de suivi
- La solution documentée explicite chaque étape de la résolution et de son implémentation
- La solution est versionnée dans le dépôt Git du projet (par exemple avec une merge request)

---

## Modalités d'évaluation

Le titre RNCP comporte 5 modalités d'évaluation, réparties sur les 3 blocs de compétences. Chaque candidat doit réussir l'ensemble des évaluations pour obtenir le titre complet, ou peut valider chaque bloc de manière autonome.

### E1 — Mise en situation professionnelle (Bloc 1)

**Compétences évaluées** : C1, C2, C3, C4, C5
**Contexte** : Réalisation d'un service numérique réel ou fictif basé sur l'usage de données, à partir du cadrage pour la réalisation d'un service numérique (spécifications fonctionnelles et techniques).
**Objectif** : Optimiser, automatiser, pérenniser et mettre à disposition les flux de données et les données utiles à la réalisation du service numérique.
**Livrable** : Rapport professionnel individuel.
**Évaluation** : Correction du rapport + Soutenance orale individuelle (15 min de présentation + 10 min de questions).

### E2 — Cas pratique (Bloc 2 — partie 1)

**Compétences évaluées** : C6, C7, C8
**Contexte** : Expression d'un besoin réel ou fictif de fonctionnalités d'intelligence artificielle (commande client ou sollicitation interne d'un data scientist).
**Objectif** : Installation et configuration du service d'IA préconisé.
**Livrable** : Rapport professionnel individuel.
**Évaluation** : Correction du rapport + Soutenance orale individuelle (15 min de présentation).

### E3 — Mise en situation professionnelle (Bloc 2 — partie 2)

**Compétences évaluées** : C9, C10, C11, C12, C13
**Contexte** : Réalisation d'un service d'intelligence artificielle à partir d'un modèle fourni.
**Objectif** : Mise en service (packaging, monitorage, test) du modèle fourni et son intégration dans une application existante.
**Livrable** : Rapport professionnel individuel.
**Évaluation** : Correction du rapport + Soutenance orale individuelle intégrant une démonstration (20 min).

### E4 — Mise en situation professionnelle (Bloc 3 — partie 1)

**Compétences évaluées** : C14, C15, C16, C17, C18, C19
**Contexte** : Développement d'une application intégrant un service d'intelligence artificielle.
**Objectif** : Analyser un besoin en développement d'application d'IA, concevoir, développer, tester et livrer l'application.
**Livrable** : Rapport professionnel individuel.
**Évaluation** : Correction du rapport + Soutenance orale individuelle intégrant une démonstration du projet (20 min).

### E5 — Cas pratique (Bloc 3 — partie 2)

**Compétences évaluées** : C20, C21
**Contexte** : Application existante présentant au moins une erreur technique, en contexte réel ou fictif.
**Objectif** : Mise en place du monitorage applicatif et résolution d'un incident technique dans l'application.
**Livrable** : Documentation technique du monitorage + Documentation de la résolution de l'incident technique.
**Évaluation** : Correction de la documentation + Soutenance orale individuelle (10 min).

---

## Glossaire

### Accuracy
Métrique d'évaluation d'un modèle d'apprentissage automatique mesurant le taux de prédictions correctes.

### BaaS (Backend as a Service)
Modèle de service cloud dans lequel les développeurs externalisent les aspects génériques d'un back-end d'application web ou mobile (authentification, comptes utilisateurs, notifications) afin de concentrer l'effort sur la valeur ajoutée du produit.

### Back-end
Couche serveur d'une application.

### Big data
Jeux de données plus variées, arrivant dans des volumes croissants et avec des flux dont la vitesse est élevée. Caractérisés par les trois "V" : variété, volume, vitesse.

### Confusion matrix
Tableau permettant l'évaluation des performances d'un modèle de classification, en croisant les prédictions du modèle avec les valeurs réelles.

### Déployer / déploiement
Action ou processus de mise en ligne ou en production d'un programme, d'une application.

### Dépôt Git
Entrepôt virtuel d'un projet en développement informatique, où sont stockées les versions d'un logiciel, ses sources et dépendances (images, données, etc.).

### Feedback loop
Désigne le processus par lequel les résultats prédits d'un modèle d'intelligence artificielle sont réutilisés pour former de nouvelles versions du modèle.

### Fixtures
Initialiseurs personnalisés pour simplifier la construction des dépendances nécessaires aux tests.

### Front-end
Couches "visibles" d'une application, dont les interfaces.

### Intégration continue (CI)
Pratique consistant à automatiser l'exécution de tests sur le code source à chaque modification, via un outil dédié.

### Livraison continue (CD)
Pratique consistant à automatiser le packaging, la livraison et le déploiement d'une application à partir de la chaîne d'intégration continue.

### Merise
Méthode d'analyse, de conception et de réalisation de systèmes d'informations. Aujourd'hui principalement utilisée dans sa déclinaison pour la conception de structures de données relationnelles.

### Micro-services
Architecture qui organise une application comme une collection de services indépendants.

### MLOps
Pratique qui établit des règles de collaboration entre les concepteurs/développeurs et les opérateurs des infrastructures informatiques pour le développement, le déploiement et la maintenance de modèles d'IA.

### Mocks
Objets simulés utilisés dans les tests pour remplacer des dépendances réelles, simplifiant la construction des dépendances nécessaires aux tests.

### Model-vue-contrôleur (MVC)
Modèle de conception de logiciel couramment utilisé qui divise la logique de programme correspondante en trois éléments interconnectés.

### N-tiers
Architecture multicouche en génie logiciel, dans laquelle les fonctions de présentation, de traitement des applications et de gestion des données sont physiquement séparées.

### OpenAPI
Norme de description des interfaces de programmation. OpenAPI encadre le développement et la documentation des API conformes à l'architecture REST.

### Packaging (d'un modèle d'IA)
Action de transformation d'un modèle en un format d'exécution générique et auto-suffisant (embarquant les dépendances et données nécessaires à l'exécution du modèle). Cette opération est menée à l'aide d'outils dédiés comme ONNX ou Docker.

### Pull request
Demande de fusion d'une branche de développement dans une autre, généralement utilisée comme étape de validation dans une chaîne de livraison.

### REST (API)
Architecture d'API utilisée pour la création de services web (HTTP).

### SaaS (Software as a Service)
Modèle de distribution de logiciel uniquement accessible via un navigateur web, en ligne. Les SaaS sont hébergés par l'éditeur, et les accès sont souvent conditionnés par un système d'abonnement et de création de compte utilisateur.

### Scraping
Technique d'extraction du contenu de sites Web, via un script ou un programme, dans le but de le transformer pour permettre son utilisation dans un autre contexte (par exemple l'enrichissement de bases de données).

### Script
Programme dédié à une unique tâche, souvent dans le cadre d'automatisation.

### Serverless
Modèle d'exécution de l'informatique dans le Cloud dans lequel le fournisseur de services Cloud fait fonctionner le serveur et gère dynamiquement l'allocation des ressources de la machine.

### SQL
Langage informatique servant à exploiter des bases de données relationnelles. Il est également à la base de multiples adaptations, formant une famille de dérivées propre à des systèmes de stockage dont les besoins en requêtage sortent du cadre initialement prévu par SQL.

### VPS (Virtual Private Server)
Serveur virtuel privé.
