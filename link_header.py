def parse(header):
    """Parses HTTP Link headers"""

    if not header:
        return dict()

    results = dict()

    links = header.split(",")

    for link in links:
        pair = link.split(";")

        # malformatted
        if len(pair) != 2:
            continue

        # parse out data
        url = pair[0].strip(" <>")
        rel = pair[1].strip().split('"')
        # malformatted
        if len(rel) != 3:
            continue
        rel = rel[1]

        results[rel] = url

    return results
