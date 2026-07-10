from rapidfuzz import process

class MetadataMatcher:

    @staticmethod
    def match(

        value: str,

        candidates,

        threshold: int = 80,

    ):

        if not candidates:

            return None

        result = process.extractOne(

            value,

            candidates,

        )

        if result is None:

            return None

        matched_value, score, _ = result

        if score < threshold:

            return None

        return matched_value