from app.rag.llm.groq_llm import (
    GroqLLM,
)

from app.rag.decomposition.llm_query_decomposer import (
    LLMQueryDecomposer,
)


decomposer = LLMQueryDecomposer(

    llm=GroqLLM(),

)


questions = [

    "High priority emails for Samsung India and incidents at Rotterdam",

    "Why is SHP0007 delayed?",

    "Show incidents and emails related to Apple",

    "Any update on vessel Maersk Horizon and shipment SHP0001",

    "Show Rotterdam weather issue and Samsung emails",

    "Tell me about SHP0007, EMAIL-001 and MV Maersk Horizon",

    "Why is shipment SHP0007 delayed and what is the revised ETA?"

]


for question in questions:

    print()
    print("=" * 100)
    print("QUESTION")
    print("=" * 100)

    print(question)

    print()

    queries = decomposer.decompose(
        question,
    )

    print("-" * 100)
    print("DECOMPOSED")
    print("-" * 100)

    for i, query in enumerate(
        queries,
        start=1,
    ):

        print(
            f"{i}. {query}"
        )

    print()