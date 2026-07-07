from sentence_transformers import CrossEncoder

from app.rag.reranker.base_reranker import BaseReranker


class CrossEncoderReranker(BaseReranker):

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ):

        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        question: str,
        children,
        top_k: int = 5,
    ):

        if not children:
            return []

        sentence_pairs = [

            (
                question,
                child.content,
            )

            for child in children

        ]

        scores = self.model.predict(sentence_pairs)

        ranked = sorted(

            zip(children, scores),

            key=lambda x: x[1],

            reverse=True,

        )

        reranked_children = []

        for child, score in ranked[:top_k]:

            child.score = float(score)

            reranked_children.append(child)

        return reranked_children