def paginate(query, page):
    per_page = 50
    return query.paginate(page, per_page, error_out=False)


def pagination_meta(page_object):
    return {
        'page': page_object.page,
        'pages': page_object.pages,
        'per_page': page_object.per_page,
        'total': page_object.total,
    }
