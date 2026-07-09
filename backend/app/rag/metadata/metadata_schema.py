from dataclasses import dataclass, field


@dataclass
class MetadataSchema:

    #
    # Metadata fields discovered
    #

    fields: set[str] = field(default_factory=set)

    #
    # All discovered values
    #

    values: dict[str, set[str]] = field(default_factory=dict)

    def has_field(

        self,

        field_name: str,

    ) -> bool:

        return field_name in self.fields

    def allowed_values(

        self,

        field_name: str,

    ) -> set[str]:

        return self.values.get(

            field_name,

            set(),

        )