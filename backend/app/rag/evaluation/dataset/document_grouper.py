from collections import defaultdict


class DocumentGrouper:

    IGNORE_FIELDS = {

        "source",
        "path",
        "folder",
        "tags",
        "version",
        "title",
        "subject",
        "from",
        "to",
        "date",
        "document_type",
         "severity",
    "priority",
    "origin",
    "destination",
    "category",

    }

    def group(

        self,

        parents,

    ):

        ##################################################
        # metadata index
        ##################################################

        metadata_index = defaultdict(

            set,

        )

        for parent in parents:

            for field, value in parent.metadata.items():

                if value is None:

                    continue

                if field in self.IGNORE_FIELDS:

                    continue

                key = (

                    field,

                    str(value).lower(),

                )

                metadata_index[

                    key

                ].add(

                    parent.id,

                )

        ##################################################
        # graph
        ##################################################

        graph = defaultdict(

            set,

        )

        for doc_ids in metadata_index.values():

            doc_ids = list(

                doc_ids,

            )

            for i in range(

                len(doc_ids)

            ):

                for j in range(

                    i + 1,

                    len(doc_ids),

                ):

                    a = doc_ids[i]
                    b = doc_ids[j]

                    graph[a].add(b)
                    graph[b].add(a)

        ##################################################
        # lookup
        ##################################################

        parent_lookup = {

            p.id: p

            for p in parents

        }

        ##################################################
        # connected components
        ##################################################

        visited = set()

        groups = []

        for parent in parents:

            if parent.id in visited:

                continue

            stack = [

                parent.id,

            ]

            component = []

            while stack:

                node = stack.pop()

                if node in visited:

                    continue

                visited.add(

                    node,

                )

                component.append(

                    parent_lookup[node]

                )

                stack.extend(

                    graph[node]

                )

            groups.append(

                component,

            )

        return groups