from dataclasses import dataclass, field


@dataclass
class MetadataCatalog:

    allowed_fields: list[str] = field(default_factory=list)

    allowed_values: dict[str, set[str]] = field(default_factory=dict)