__author__ = 'radek hofman'
### this build web page with current results

import rad_config as rcf

def make_nuclide_combo(nuclides):
    """
    creates nuclide combo box
    :param nuclides:
    :return:
    """

    ret = """<select id="nuclide_combo">\n"""

    for nuc in nuclides:
        ret += """    <option value="%s">%s</option>\n""" % (nuc, nuc)

    ret += "</select>"

    return ret


if __name__ == "__main__":
    ST = rcf.SOURCE_TERM
    nuclides = ST["sources"][0][0]["inventory"].keys()
    nuclide_combo = make_nuclide_combo(nuclides)

    print nuclide_combo



