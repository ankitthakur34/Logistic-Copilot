from app.rag.bm25.tokenizer import Tokenizer


text = """
Shipment SHP0007 delayed due to reefer failure.
Container ABC-123 arrived at Rotterdam Port.
"""

tokens = Tokenizer.tokenize(text)

print(tokens)