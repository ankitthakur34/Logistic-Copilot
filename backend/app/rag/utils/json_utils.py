def flatten_json(

    data,
    parent_key="",
):

    items = {}

    for key, value in data.items():

        new_key = (

            f"{parent_key}.{key}"

            if parent_key

            else key

        )

        if isinstance(

            value,
            dict,

        ):

            items.update(

                flatten_json(

                    value,
                    new_key,

                )

            )

        else:

            items[new_key] = value

    return items