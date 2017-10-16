from urllib.request import urlopen

import esprima
import lxml.html


class AllGymsScaper:

    """
    A website scraper which parses the "Find your gym" page on `puregym.com`.
    """

    url = 'https://www.puregym.com/gyms/'

    def __init__(self):
        doc = lxml.html.parse(urlopen(self.url))
        root = doc.getroot()
        script_element = root.cssselect('script')[-1]

        tree = esprima.parseScript(script_element.text)
        dom_content_loaded = tree.body[0].expression.arguments[1]
        gym_list_object = dom_content_loaded.body.body[2] \
            .expression.arguments[0].arguments[1]

        self.data = self.esprima_to_python(gym_list_object)['allGyms']

    def esprima_to_python(self, node):
        if node.type == 'ObjectExpression':
            d = {}
            for p in node.properties:
                d[p.key.value] = self.esprima_to_python(p.value)
            return d
        elif node.type == 'ArrayExpression':
            d = []
            for p in node.elements:
                d.append(self.esprima_to_python(p))
            return d
        elif node.type == 'Literal':
            return node.value
        elif node.type == 'UnaryExpression' and node.operator == '-':
            return -self.esprima_to_python(node.argument)
        else:
            raise ValueError('Unknown node: {}'.format(obj))
