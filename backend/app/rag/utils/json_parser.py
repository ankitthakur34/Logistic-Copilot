import json


class JsonParser:

    @staticmethod
    def parse(text: str):

        #
        # Remove surrounding whitespace
        #

        text = text.strip()

        #
        # Remove ```json
        #

        if text.startswith("```json"):

            text = text[len("```json"):]

        #
        # Remove ```
        #

        elif text.startswith("```"):

            text = text[len("```"):]

        #
        # Remove ending ```
        #

        if text.endswith("```"):

            text = text[:-3]

        text = text.strip()

        return json.loads(text)