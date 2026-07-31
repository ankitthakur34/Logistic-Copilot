from app.rag.loader.markdown_loader import (
    MarkdownLoader,
)

from app.rag.chunking.parent_child_chunker import (
    ParentChildChunker,
)

from app.rag.ingestion.ingest_pipeline import (
    IngestionPipeline,
)

from app.rag.llm.groq_llm import (
    GroqLLM,
)

from app.rag.evaluation.synthetic.question_answer_generator import (
    QuestionAnswerGenerator,
)

from app.rag.evaluation.synthetic.synthetic_dataset_generator import (
    SyntheticDatasetGenerator,
)


ingestion = IngestionPipeline(

    loader=MarkdownLoader(

        "data/rag"

    ),

    chunker=ParentChildChunker(),

).run()


generator = (

    SyntheticDatasetGenerator(

        qa_generator=(

            QuestionAnswerGenerator(

                llm=GroqLLM(),

            )

        )

    )

)


dataset = generator.generate(

    ingestion,

)

generator.save(

    dataset,

    "app/rag/evaluation/dataset/generated/generated_dataset.json",

)

print()

print("=" * 80)
print("GENERATED")
print("=" * 80)

for item in dataset[:10]:

    print()

    print(item)