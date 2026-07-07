from app.rag.llm.groq_llm import GroqLLM

from app.rag.multi_query.llm_multi_query_generator import (
    LLMMultiQueryGenerator,
)

from app.rag.multi_query.multi_query_pipeline import (
    MultiQueryPipeline,
)

pipeline = MultiQueryPipeline(

    generator=LLMMultiQueryGenerator(

        llm=GroqLLM(),

    ),

)

queries = pipeline.run(

    "Why is shipment SHP0007 delayed?",

)

print(queries)

print("=" * 80)
print("GENERATED QUERIES")
print("=" * 80)

for idx, query in enumerate(

    queries,

    start=1,

):

    print()

    print(idx)

    print(query)