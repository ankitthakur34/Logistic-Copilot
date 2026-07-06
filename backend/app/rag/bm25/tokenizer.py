import re


class Tokenizer:

    @staticmethod
    def tokenize(
        text: str,
    ) -> list[str]:
        """
        Normalize text for BM25.

        - lowercase
        - keep letters and digits
        - preserve IDs like SHP0007
        """

        text = text.lower()

        tokens = re.findall(
            r"[a-z0-9]+",
            text,
        )

        return tokens