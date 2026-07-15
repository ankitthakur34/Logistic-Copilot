from collections import defaultdict

from app.database.db import db


class SchemaBuilder:

    def build(self):

        schema = []

        reverse_relations = defaultdict(list)

        #
        # Build reverse FK relations
        #

        for table in db.metadata.sorted_tables:

            for column in table.columns:

                for fk in column.foreign_keys:

                    target_table = fk.column.table.name

                    reverse_relations[
                        target_table
                    ].append(
                        (
                            table.name,
                            column.name,
                        )
                    )

        ###################################################
        # Build schema text
        ###################################################

        for table in db.metadata.sorted_tables:

            schema.append(
                "=" * 80
            )

            schema.append(
                f"TABLE: {table.name}"
            )

            schema.append("")

            schema.append(
                "Columns:"
            )

            for column in table.columns:
                line = f"- {column.name}"

                if hasattr(column.type, "enums"):

                    values = ", ".join(

                        column.type.enums

                    )

                    line += (

                    f" (ENUM: {values})"

                    )

                else:

                    line += (

                    f" ({column.type})"

                    )

                if column.primary_key:

                    line += (
                        " PRIMARY KEY"
                    )

                schema.append(
                    line
                )

            ###################################################
            # Relationships
            ###################################################

            relations = []

            #
            # outgoing fk
            #

            for column in table.columns:

                for fk in column.foreign_keys:

                    relations.append(
                        f"- {table.name}.{column.name}"
                        f" -> "
                        f"{fk.target_fullname}"
                    )

            #
            # incoming fk
            #

            for (
                child_table,
                child_column,
            ) in reverse_relations.get(
                table.name,
                [],
            ):

                relations.append(
                    f"- {table.name}.id"
                    f" <- "
                    f"{child_table}.{child_column}"
                )

            if relations:

                schema.append("")
                schema.append(
                    "Relationships:"
                )

                schema.extend(
                    relations
                )

            schema.append("")

        return "\n".join(schema)