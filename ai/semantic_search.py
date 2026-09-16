import re

import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class SemanticSearch:

    def __init__(self, window=2):

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        self.window = window
        self.index = None
        self.messages = None
        self.ai_results = None

        self.searchable_indices = []
        self.searchable_texts = []

    def _is_searchable(self, message):
        """
        Decide whether an individual message contains
        enough information to be useful for search.
        """

        if not isinstance(message, str):
            return False

        message = message.strip()

        if not message:
            return False

        noise_messages = {
            "<media omitted>",
            "you deleted this message",
            "this message was deleted",
        }

        if message.lower() in noise_messages:
            return False

        if len(message.split()) < 3:
            return False

        return True

    def _normalize_text(self, text):
        """
        Normalize text for keyword matching.
        """

        text = str(text).lower()

        text = re.sub(
            r"https?://\S+|www\.\S+",
            " ",
            text
        )

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def _get_keywords(self, text):
        """
        Extract useful keywords from text.
        """

        stop_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "do",
            "did",
            "does",
            "what",
            "when",
            "where",
            "who",
            "how",
            "why",
            "which",
            "about",
            "with",
            "for",
            "from",
            "to",
            "of",
            "in",
            "on",
            "and",
            "or",
            "me",
            "we",
            "i",
            "you",
            "my",
            "our",
            "it",
            "need",
        }

        words = self._normalize_text(
            text
        ).split()

        return [
            word
            for word in words
            if word not in stop_words
            and len(word) >= 3
        ]

    def _keyword_score(self, query, message):
        """
        Calculate keyword overlap between query
        and message.
        """

        query_keywords = set(
            self._get_keywords(query)
        )

        if not query_keywords:
            return 0.0

        message_keywords = set(
            self._get_keywords(message)
        )

        if not message_keywords:
            return 0.0

        matches = (
            query_keywords
            & message_keywords
        )

        return len(matches) / len(
            query_keywords
        )

    def build_index(self, df, ai_results=None):
        """
        Build the semantic search index.

        ai_results is optional and should contain
        validated AI extraction results.
        """

        self.messages = df.copy()

        if ai_results is not None:
            self.ai_results = ai_results.copy()
        else:
            self.ai_results = None

        self.searchable_indices = []
        self.searchable_texts = []

        for index, row in self.messages.iterrows():

            message = str(
                row["message"]
            ).strip()

            if not self._is_searchable(
                message
            ):
                continue

            self.searchable_indices.append(
                index
            )

            self.searchable_texts.append(
                message
            )

        if not self.searchable_texts:
            raise ValueError(
                "No searchable messages were found."
            )

        embeddings = self.model.encode(
            self.searchable_texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        embeddings = embeddings.astype(
            "float32"
        )

        faiss.normalize_L2(
            embeddings
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(
            embeddings
        )

    def _get_context(self, index):
        """
        Retrieve the original conversation around
        a matched message.
        """

        start = max(
            0,
            index - self.window
        )

        end = min(
            len(self.messages),
            index + self.window + 1
        )

        context = []

        for i in range(start, end):

            row = self.messages.iloc[i]

            context.append({
                "message_id": int(
                    row["message_id"]
                ),
                "date": row["date"],
                "user": row["user"],
                "message": row["message"]
            })

        return context

    def _find_ai_result(self, message_id):
        """
        Find the AI-extracted information associated
        with a message.
        """

        if self.ai_results is None:
            return None

        if self.ai_results.empty:
            return None

        matches = self.ai_results[
            self.ai_results["message_id"]
            == message_id
        ]

        if matches.empty:
            return None

        row = matches.iloc[0]

        return {
            "type": row.get("type"),
            "task": row.get("task"),
            "deadline": row.get("deadline"),
            "priority": row.get("priority"),
            "confidence": row.get("confidence"),
            "evidence": row.get("evidence"),
            "is_important": row.get(
                "is_important"
            ),
        }

    def _ai_relevance_score(self, query, ai_result):
        """
        Estimate how relevant an AI-extracted result
        is to the user's query.
        """

        if ai_result is None:
            return 0.0

        searchable_parts = []

        for field in [
            "type",
            "task",
            "deadline",
            "evidence",
        ]:

            value = ai_result.get(field)

            if (
                value is not None
                and not pd.isna(value)
            ):
                searchable_parts.append(
                    str(value)
                )

        if not searchable_parts:
            return 0.0

        ai_text = " ".join(
            searchable_parts
        )

        return self._keyword_score(
            query,
            ai_text
        )

    def search(self, query, top_k=5):
        """
        Hybrid search using:

        1. Semantic similarity
        2. Keyword overlap
        3. AI-extracted information

        Results are ranked using a combined score.
        """

        if self.index is None:
            raise RuntimeError(
                "Search index has not been built yet."
            )

        if (
            not isinstance(query, str)
            or not query.strip()
        ):
            return []

        candidate_k = min(
            top_k * 5,
            len(self.searchable_indices)
        )

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        query_embedding = query_embedding.astype(
            "float32"
        )

        faiss.normalize_L2(
            query_embedding
        )

        semantic_scores, indices = (
            self.index.search(
                query_embedding,
                candidate_k
            )
        )

        ranked_results = []

        for semantic_score, vector_index in zip(
            semantic_scores[0],
            indices[0]
        ):

            if vector_index == -1:
                continue

            original_index = (
                self.searchable_indices[
                    vector_index
                ]
            )

            message = self.searchable_texts[
                vector_index
            ]

            keyword_score = (
                self._keyword_score(
                    query,
                    message
                )
            )

            message_id = int(
                self.messages.iloc[
                    original_index
                ]["message_id"]
            )

            ai_result = self._find_ai_result(
                message_id
            )

            ai_score = (
                self._ai_relevance_score(
                    query,
                    ai_result
                )
            )

            combined_score = (
                0.60 * float(semantic_score)
                +
                0.25 * keyword_score
                +
                0.15 * ai_score
            )

            row = self.messages.iloc[
                original_index
            ]

            ranked_results.append({
                "message_id": message_id,
                "date": row["date"],
                "user": row["user"],
                "message": row["message"],
                "semantic_score": float(
                    semantic_score
                ),
                "keyword_score": float(
                    keyword_score
                ),
                "ai_score": float(
                    ai_score
                ),
                "score": combined_score,
                "context": self._get_context(
                    original_index
                ),
                "ai_result": ai_result,
            })

        ranked_results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return ranked_results[:top_k]