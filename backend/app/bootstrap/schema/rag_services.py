from dataclasses import dataclass

from app.rag.generation.answer_pipeline import AnswerPipeline


@dataclass
class RAGServices:

    pipeline: AnswerPipeline

    ingestion: object