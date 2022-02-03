# A list of ignored domains inside NSExceptionDomains.
def ignored_domains():
    return ['127.0.0.1', 'localhost', '%.localhost', '%.local']


# Returns a list of all ids from the domains table which include the ignored domains
def ignored_domain_ids(db):
    domains = ignored_domains()
    query = "SELECT id FROM domains WHERE"
    first = True

    for domain in domains:
        if not first:
            query += " OR"

        query += f" name LIKE '{domain}'"
        first = False

    rows = db.engine.execute(query)
    results = []
    for item in rows:
        results.append(item[0])

    return results
