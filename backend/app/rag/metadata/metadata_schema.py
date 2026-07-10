from dataclasses import dataclass


@dataclass
class MetadataSchema:

    #
    # All metadata fields
    #

    fields: set[str]

    #
    # field -> values
    #

    values: dict[str, set[str]]

    #
    # value -> fields
    #

    value_to_fields: dict[str, set[str]]

    #
    # lowercase value -> original value
    #

    normalized_values: dict[str, str]

    #
    # fields that can be used for filtering
    #

    queryable_fields: set[str]

    def has_field(

        self,

        field: str,

    ) -> bool:

        return field in self.fields

    def allowed_values(

        self,

        field: str,

    ) -> set[str]:

        return self.values.get(

            field,

            set(),

        )

    def candidate_fields(

        self,

        value: str,

    ) -> set[str]:

        return self.value_to_fields.get(

            value.lower(),

            set(),

        )

    def original_value(

        self,

        value: str,

    ) -> str:

        return self.normalized_values.get(

            value.lower(),

            value,

        )