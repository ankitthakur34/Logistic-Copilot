class ContextFormatter:

    def format(
        self,
        retrieval_result,
    ) -> str:

        sections = []

        for parent in retrieval_result.parents:

            metadata = parent.metadata

            header = []

            if metadata.get("document_type"):
                header.append(
                    f"DOCUMENT TYPE  : {metadata['document_type']}"
                )

            if metadata.get("shipment"):
                header.append(
                    f"SHIPMENT       : {metadata['shipment']}"
                )

            if metadata.get("customer"):
                header.append(
                    f"CUSTOMER       : {metadata['customer']}"
                )

            if metadata.get("email_id"):
                header.append(
                    f"EMAIL ID       : {metadata['email_id']}"
                )

            if metadata.get("priority"):
                header.append(
                    f"PRIORITY       : {metadata['priority']}"
                )

            if metadata.get("date"):
                header.append(
                    f"DATE           : {metadata['date']}"
                )

            if metadata.get("folder"):
                header.append(
                    f"FOLDER         : {metadata['folder']}"
                )

            if metadata.get("source"):
                header.append(
                    f"SOURCE         : {metadata['source']}"
                )

            section = "\n".join(
                [
                    "=" * 60,
                    *header,
                    "=" * 60,
                    parent.content,
                ]
            )

            sections.append(section)

        return "\n\n".join(sections)