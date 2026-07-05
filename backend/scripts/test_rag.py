from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.ingestion.ingest_pipeline import IngestionPipeline

from app.rag.embeddings.sentence_transformer_embedding import (
    SentenceTransformerEmbedding,
)

from app.rag.vector_store.chroma_vector_store import (
    ChromaVectorStore,
)

from app.rag.retrieval.chroma_retriever import (
    ChromaRetriever,
)

from app.rag.retrieval.retrieval_pipeline import (
    RetrievalPipeline,
)

from app.rag.context.default_context_builder import (
    DefaultContextBuilder,
)

from app.rag.prompts.cargo_prompt_builder import (
    CargoPromptBuilder,
)

from app.rag.llm.groq_llm import (
    GroqLLM,
)

from app.rag.service.rag_service import (
    RAGService,
)


rag = RAGService(

    ingestion_pipeline=IngestionPipeline(
        loader=MarkdownLoader("data/rag"),
        chunker=ParentChildChunker(),
    ),

    retrieval_pipeline=RetrievalPipeline(
        embedding_model=SentenceTransformerEmbedding(),
        retriever=ChromaRetriever(
            vector_store=ChromaVectorStore(),
        ),
    ),

    context_builder=DefaultContextBuilder(),

    prompt_builder=CargoPromptBuilder(),

    llm=GroqLLM(),

)


questions = [

    "what to do for bill of lading",

    "why SHP0007 is delayed",

]


for question in questions:

    print()
    print("=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(question)

    response = rag.ask(question)

    print()
    print("=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(response.answer)

    print()
    print("=" * 80)
    print("MODEL")
    print("=" * 80)
    print(response.model)

    print()
    print("=" * 80)
    print("TOKEN USAGE")
    print("=" * 80)
    print(response.usage)

    print()
    print("=" * 80)
    print("SOURCES")
    print("=" * 80)

    if response.context.sources:

        for source in response.context.sources:

            print(f"- {source}")

    else:

        print("No sources")

    # print()
    # print("=" * 80)
    # print("SYSTEM PROMPT")
    # print("=" * 80)

    # print(response.prompt.system_prompt)

    # print()
    # print("=" * 80)
    # print("USER PROMPT")
    # print("=" * 80)

    # print(response.prompt.user_prompt)

    # print()
    # print("=" * 80)
    # print("FULL PROMPT")
    # print("=" * 80)

    # print(response.prompt.full_prompt)

    print()
    print("=" * 80)
    print("END")
    print("=" * 80)