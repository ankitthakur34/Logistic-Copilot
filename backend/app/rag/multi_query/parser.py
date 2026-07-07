class MultiQueryParser:

    @staticmethod
    def parse(
        text: str,
    ) -> list[str]:

        queries = []

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            if "." in line[:3]:

                line = line.split(".", 1)[1].strip()

            queries.append(line)

        return list(dict.fromkeys(queries))