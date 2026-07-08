from copy import deepcopy
from collections import defaultdict

from app.rag.context_compression.base_context_compressor import (
    BaseContextCompressor,
)

from app.rag.schema.retrieval_result import (
    RetrievalResult,
)


class ChildContextCompressor(BaseContextCompressor):

    def compress(
        self,
        retrieval: RetrievalResult,
    ) -> RetrievalResult:

        compressed = deepcopy(retrieval)

        grouped = defaultdict(list)

        for child in compressed.children:

            grouped[child.parent_id].append(child)

        for children in grouped.values():

            children.sort(

        key=lambda child: child.child_index

    )    

        for parent in compressed.parents:

            if parent.id not in grouped:
                continue

            parent.content = "\n\n".join(

                child.content

                for child in grouped[parent.id]

            )

        return compressed