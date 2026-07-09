from dataclasses import dataclass, field


@dataclass
class MetadataResult:

    values: dict = field(
        default_factory=dict,
    )

    def get(

        self,

        key,

        default=None,

    ):

        return self.values.get(
            key,
            default,
        )

    def set(

        self,

        key,

        value,

    ):

        if value is None:
            return

        self.values[key] = value

    def to_dict(

        self,

    ):

        return dict(
            self.values,
        )

    def is_empty(

        self,

    ):

        return len(
            self.values,
        ) == 0