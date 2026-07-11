# Comprendre `evaluate_ragas.py`

## Objectif

`evaluate_ragas.py` sert à évaluer un pipeline RAG NBA.

Il fait deux choses distinctes :

1. Générer une réponse avec le RAG.
2. Évaluer cette réponse avec RAGAS.

Ces deux phases utilisent Mistral, mais pas de la même manière.

---

## Vue d'ensemble du pipeline

```text
YAML d'évaluation
        ↓
Question
        ↓
Recherche FAISS
        ↓
Contextes récupérés
        ↓
RagAgent
        ↓
Réponse LLM structurée
        ↓
Dataset RAGAS
        ↓
Métriques RAGAS
        ↓
CSV + rapport Markdown
```

---

## Phase 1 — Chargement des cas YAML

Le script charge les cas depuis `eval_cases/nba_eval_cases.yaml`.

Chaque cas contient notamment :

- `question`
- `reference_answer`
- `expected_sources`
- `category`
- `source_type`

Ces éléments servent ensuite à comparer la réponse générée par le RAG avec la réponse attendue.

---

## Phase 2 — Recherche des contextes

Pour chaque question, le script appelle :

```python
vector_store.search(question, k=SEARCH_K)
```

Cette étape fait un appel Mistral embeddings.

```text
Question
    ↓
Mistral embeddings
    ↓
Vecteur de question
    ↓
Recherche FAISS
    ↓
Top-k chunks
```

Objet produit :

```python
RetrievedContext
```

Il contient :

- le texte du chunk ;
- le score FAISS ;
- la source ;
- les métadonnées.

---

## Phase 3 — Génération de la réponse avec `RagAgent`

Le `RagAgent` reçoit :

- la question ;
- les contextes récupérés par FAISS.

Il appelle Mistral via Pydantic AI pour générer une réponse structurée.

Objet produit :

```python
RagAnswer
```

Il contient :

- `answer`
- `used_sources`
- `insufficient_context`
- `confidence`
- `contexts`
- `model`

Ici, Pydantic AI sert à forcer une sortie propre et structurée.

```text
Question + contextes
        ↓
Pydantic AI Agent
        ↓
Mistral chat/completions
        ↓
StructuredRagOutput
        ↓
RagAnswer
```

Pour une question, cette phase fait généralement :

```text
1 appel embeddings
1 appel chat/completions
```

---

## Phase 4 — Construction du dataset RAGAS

Une fois la réponse générée, le script construit un dataset RAGAS.

Format logique :

```python
{
    "user_input": question,
    "response": rag_answer.answer,
    "retrieved_contexts": [ctx.text for ctx in contexts],
    "reference": reference_answer,
}
```

Important : RAGAS ne génère pas une nouvelle réponse utilisateur.

Il évalue la réponse déjà produite par `RagAgent`.

---

## Phase 5 — Évaluation RAGAS

RAGAS calcule 4 métriques :

```python
faithfulness
answer_relevancy
context_precision
context_recall
```

Ces métriques utilisent :

```python
MistralRagasLLM
MistralRagasEmbeddings
```

Ces classes ne passent pas par le `RagAgent`.

Elles appellent directement le SDK Mistral :

```python
self.client.chat.complete(...)
self.client.embeddings.create(...)
```

---

## Pourquoi RAGAS fait beaucoup d'appels API

Une métrique RAGAS ne correspond pas forcément à un seul appel API.

Sur un run avec 1 question et 4 métriques, on peut observer environ :

```text
Phase RAG classique : 2 appels API
Phase RAGAS         : ~13 appels API
Total visible       : ~15 appels API
```

Donc :

```text
1 question × 4 métriques ≠ 4 appels API
```

Certaines métriques font plusieurs appels LLM ou embeddings.

---

## Pourquoi certaines métriques RAGAS font plusieurs appels

Dans le rapport, on voit 4 métriques :

```python
faithfulness
answer_relevancy
context_precision
context_recall
```

Mais une métrique RAGAS n'est pas toujours un calcul simple.

Certaines métriques demandent au LLM juge de faire plusieurs sous-tâches, par exemple :

- extraire des affirmations depuis la réponse ;
- vérifier si ces affirmations sont supportées par les contextes ;
- comparer la question et la réponse ;
- juger si chaque contexte récupéré est utile ;
- comparer les contextes avec la réponse attendue ;
- calculer une similarité via embeddings.

Donc une seule métrique visible dans la barre de progression peut déclencher plusieurs appels Mistral.

Exemple logique :

```text
Métrique faithfulness
        ↓
Appel LLM 1 : extraire les claims de la réponse
        ↓
Appel LLM 2 : vérifier les claims avec les contextes
        ↓
Score final
```

Autre exemple :

```text
Métrique answer_relevancy
        ↓
Appel LLM : générer ou reformuler des questions candidates
        ↓
Appels embeddings : comparer question originale et questions générées
        ↓
Score final
```

Et pour les métriques liées aux contextes :

```text
Métrique context_precision / context_recall
        ↓
Appels LLM : juger quels contextes sont utiles ou couverts
        ↓
Agrégation des jugements
        ↓
Score final
```

C'est pour cela qu'un run affiché comme :

```text
1 question × 4 métriques = 4 jobs RAGAS
```

peut produire beaucoup plus que 4 appels API.

Dans le run isolé sur Q04, on observe environ :

```text
Phase RAG classique : 2 appels API
Phase RAGAS         : ~13 appels API
Total visible       : ~15 appels API
```

Les 2 appels de la phase RAG sont :

```text
1 appel embeddings pour encoder la question
1 appel chat/completions pour générer la réponse RagAgent
```

Les ~13 appels RAGAS viennent des sous-tâches internes des métriques.

Donc la barre de progression RAGAS compte des jobs de métriques, pas des appels API.

## Pourquoi un run complet est beaucoup plus long

Avec 10 questions et 4 métriques :

```text
10 questions × 4 métriques = 40 jobs RAGAS
```

Mais en appels API réels, cela peut devenir beaucoup plus important.

Approximation :

```text
~13 appels RAGAS par question × 10 questions ≈ 130 appels API RAGAS
+ 10 appels embeddings pour les questions
+ 10 appels chat pour les réponses RagAgent
≈ 150 appels API Mistral
```

C'est pour cela que la phase RAGAS est beaucoup plus lente que la génération des réponses.

---

## Rôle de chaque outil

### FAISS

Stocke et recherche les embeddings des chunks.

Il sert à retrouver les contextes les plus proches de la question.

---

### Mistral

Mistral est utilisé à plusieurs endroits :

1. Embedding de la question pour FAISS.
2. Génération de la réponse par `RagAgent`.
3. Jugement RAGAS via `MistralRagasLLM`.
4. Embeddings RAGAS via `MistralRagasEmbeddings`.

---

### Pydantic AI

Pydantic AI est utilisé dans `RagAgent`.

Son rôle est de forcer une sortie structurée :

```python
StructuredRagOutput
```

Avec :

- réponse concise ;
- sources utilisées ;
- confiance ;
- indication de contexte insuffisant.

---

### RAGAS

RAGAS évalue la qualité du RAG.

Il ne remplace pas le jugement métier.

Il vérifie surtout :

- si la réponse est fidèle aux contextes ;
- si elle répond à la question ;
- si les contextes retrouvés sont pertinents ;
- si les contextes couvrent la réponse attendue.

---

## Attention aux scores `n/a`

Un score `n/a` peut apparaître même sans erreur Python visible.

Ca peut venir de :

- rate limit Mistral ;
- timeout ;
- sortie juge non exploitable ;
- métrique RAGAS qui retourne `NaN` sans lever d'exception.

`raise_exceptions=True` ne capture pas forcément ce cas, car il ne s'agit pas toujours d'une exception.

---

## Pourquoi un run isolé passe mieux qu'un run complet

Sur une seule question :

```text
peu d'appels API
moins de pression sur Mistral
moins de risque de rate limit
moins de sorties juge invalides
```

Sur 10 questions :

```text
beaucoup d'appels API
enchaînement rapide malgré max_workers=1
risque de 429
risque de NaN
```

`max_workers=1` évite le parallélisme, mais ne force pas une pause entre les appels.

Pour limiter les erreurs, il faut ajouter un rate limiter dans les wrappers Mistral utilisés par RAGAS.

---

## Résumé court

```text
RagAgent produit les réponses.
RAGAS juge les réponses.
Mistral est utilisé dans les deux phases.
Pydantic AI structure la réponse du RagAgent.
RAGAS utilise ses propres wrappers Mistral.
La phase RAGAS est coûteuse car chaque métrique peut faire plusieurs appels API.
Les erreurs 429 et les n/a viennent surtout du volume d'appels RAGAS.
```
