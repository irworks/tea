def add_order_to_query(query, order_options, order_map):
    for order_option in order_options:
        if order_option not in order_map:
            continue
        order_field = order_map[order_option]
        order_value = order_options[order_option]
        if order_value:
            query = query.order_by(order_field.desc())
        else:
            query = query.order_by(order_field.asc())

    return query
