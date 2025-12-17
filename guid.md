1️⃣ « Comment pouvez-vous affirmer qu’il existe un biais médiatique et pas seulement une différence de sujets ? »
🔍 Ce qu’ils testent

Confusion biais vs thématique

Ta capacité à nuancer

✅ Réponse idéale

Nous ne parlons pas d’un biais absolu, mais de cadrages médiatiques différenciés.
Pour éviter la confusion avec les thèmes, nous comparons :

des événements comparables (attaques, civils, bombardements),

les adjectifs, verbes et cooccurrences associés aux mêmes acteurs,

et des mesures normalisées comme le log-odds ratio.
Les différences observées ne portent donc pas seulement sur quoi est raconté, mais sur comment c’est formulé.

2️⃣ « Pourquoi utiliser TF-IDF alors que vous avez déjà les fréquences ? »
🔍 Ce qu’ils testent

Compréhension des méthodes

Pas d’utilisation “automatique”

✅ Réponse idéale

Les fréquences montrent ce qui est souvent mentionné, mais pas ce qui est distinctif.
TF-IDF permet d’identifier les termes qui caractérisent un corpus par rapport à l’ensemble, en réduisant l’impact des mots génériques.
C’est complémentaire aux fréquences brutes.

3️⃣ « Le Word2Vec ne reflète-t-il pas simplement les biais déjà présents dans les données ? »
🔥 QUESTION TRÈS PIÈGE
🔍 Ce qu’ils testent

Esprit critique

Limites méthodologiques

✅ Réponse idéale

Absolument. Word2Vec n’élimine pas les biais, il les révèle.
Notre objectif n’est pas de produire une représentation neutre, mais de montrer comment les associations sémantiques émergent dans chaque corpus.
Les différences entre les modèles Gaza et Ukraine reflètent donc précisément les cadres médiatiques dominants.

4️⃣ « Pourquoi séparer analyse lexicale et analyse sémantique ? »
🔍 Ce qu’ils testent

Méthodologie

Clarté scientifique

✅ Réponse idéale

L’analyse lexicale mesure des patrons statistiques du vocabulaire, tandis que l’analyse sémantique s’intéresse au sens et aux contextes d’usage.
Les séparer permet d’éviter toute confusion méthodologique et de rendre le pipeline plus lisible et reproductible.

5️⃣ « Comment avez-vous choisi les acteurs et les mots-clés analysés ? »
🔍 Ce qu’ils testent

Subjectivité potentielle

✅ Réponse idéale

Les acteurs ont été choisis en fonction de leur centralité médiatique dans chaque conflit.
Les mots-clés correspondent à :

des termes fréquents,

des notions centrales dans la littérature (violence, civils, diplomatie),

et des événements comparables.
Cette sélection est documentée et reste ajustable.

6️⃣ « Vos résultats seraient-ils les mêmes avec d’autres médias ou une autre période ? »
🔥 CLASSIQUE DE JURY
🔍 Ce qu’ils testent

Généralisation

Honnêteté scientifique

✅ Réponse idéale

Les résultats quantitatifs précis changeraient, mais la méthodologie resterait valide.
Notre objectif est de proposer un cadre d’analyse reproductible, pas de prétendre à une vérité universelle.
L’approche peut être appliquée à d’autres périodes ou sources.

7️⃣ « Pourquoi utiliser le log-odds ratio et pas une simple différence de fréquences ? »
🔍 Ce qu’ils testent

Statistiques

✅ Réponse idéale

Le log-odds ratio permet une comparaison normalisée, tenant compte de la taille des corpus et des termes rares.
Il est largement utilisé en linguistique computationnelle pour comparer des discours, ce qui en fait un choix méthodologiquement solide.

8️⃣ « Comment interprétez-vous les clusters sémantiques ? »
🔍 Ce qu’ils testent

Surinterprétation

✅ Réponse idéale

Les clusters ne sont pas interprétés isolément.
Ils sont analysés comme des groupes indicatifs de champs thématiques, que nous confrontons aux fréquences, aux cooccurrences et aux concordances.
L’interprétation reste qualitative et contextualisée.

9️⃣ « Pourquoi ne pas utiliser des modèles plus récents comme BERT ? »
🔥 QUESTION MODERNE
🔍 Ce qu’ils testent

Choix technologiques

✅ Réponse idéale

Les modèles contextualisés comme BERT sont puissants, mais moins interprétables et plus coûteux.
Notre objectif est l’analyse du discours, pas la prédiction.
Word2Vec et les méthodes statistiques offrent un meilleur compromis entre interprétabilité, transparence et ressources.

🔟 « Quelle est la principale limite de votre travail ? »
🔍 Ce qu’ils testent

Maturité scientifique

✅ Réponse idéale

La principale limite réside dans la dépendance aux sources médiatiques sélectionnées et à la langue analysée.
De plus, l’analyse automatique ne remplace pas une interprétation humaine.
Ces limites sont clairement discutées dans le rapport.