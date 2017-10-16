from urllib.request import urlopen

import esprima
import lxml.html

from .gym import Gym

class PureGym:

    def __init__(self):
        pass

    @property
    def gyms(self):
        gyms = []

        for gym in self.find_gyms():
            gyms.append(Gym(gym['id']))

        return gyms

    def find_gyms(self):
        url = 'https://www.puregym.com/gyms/'
        doc = lxml.html.parse(urlopen(url))
        script = doc.getroot().cssselect('script')[-1]

        tree = esprima.parseScript(script.text)
        dom_content_loaded = tree.body[0].expression.arguments[1]
        gym_list_object = dom_content_loaded.body.body[2].expression.arguments[0].arguments[1]

        return self.esprima_to_python(gym_list_object)['allGyms']

    def esprima_to_python(self, obj):
        if obj.type == 'ObjectExpression':
            d = {}
            for p in obj.properties:
                d[p.key.value] = self.esprima_to_python(p.value)
            return d
        elif obj.type == 'ArrayExpression':
            d = []
            for p in obj.elements:
                d.append(self.esprima_to_python(p))
            return d
        elif obj.type == 'Literal':
            return obj.value
