def _p_element(pub, ven_list):
    """ Search a correspondence for the current publication document in the venues list.
        If it founds ones the score is changed."""

    # if it has already found a match
    if len(pub['ven']):
        return pub

    pub['key'] = pub['pub']['key']

    # given a publication search if his key is related to some venue by the field 'crossref'

    for ven in ven_list:
        if not pub['pub']['crossref'] == '' and pub['pub']['crossref'].replace('\n', '') == ven['ven']['key']:
            pub['score'] = pub['pub']['o_score'] + ven['ven']['o_score']
            pub['ven'] = ven['ven']
            return pub
    return pub


def _v_element(ven, pub_list):
    """ Search a correspondence for the current venue document in the publications list.
        If it founds ones the score is changed.
        To give an higher relevance to the publications, the publication key is assigned to the object key
        (if there is a match) """

    # if it has already found a match
    if len(ven['pub']):
        return ven

    # given a venue search if his key is related to some publications by the field 'key'
    for pub in pub_list:

        if not pub['pub']['crossref'] == '' and pub['pub']['crossref'].replace('\n', '') == ven['ven']['key']:
            # if there is a match between a venue and a publication, the ven['key'] become the pub['key].
            # Thanx to this we can after eliminate duplicates data given by [(pubi, venuej), (venuej, pubi)]
            ven['key'] = pub['pub']['key']
            ven['score'] = ven['ven']['o_score'] + pub['pub']['o_score']
            ven['pub'] = pub['pub']
            return ven
    ven['key'] = ven['ven']['key']
    return ven


def threshold_rank(publications, venues):
    """ Implementation of Threshold alghorithm to merge the two indexes results and modify the resultant score.
        The function search for a correspondence between publications crossref attribute and the venue key, giving more
        relevance to the publications.
        """

    doc_limit = min(len(publications), len(venues))
    # cprint(doc_limit, 'lightgrey', start='doc_limit: ') # tracing

    list_results = list()
    ordered_list = list()

    for i in range(doc_limit):
        threshold = publications[i]['score'] + venues[i]['score']

        list_results.append(_p_element(publications[i], venues))
        list_results.append(_v_element(venues[i], publications))

        # using sorted and lambda to print list sorted by score.
        # the max score is check with current threshold.
        ordered_list = sorted(list_results, key=lambda s: s['score'], reverse=True)
        if ordered_list[0]['score'] > threshold:
            break

    # return the relevant documents list, filtering by object key.
    return list({x['key']: x for x in ordered_list}.values())
