from enum import Enum
from collections import namedtuple

from cached_property import cached_property

from .scraper import AllGymsScaper


class GymStatus(Enum):
    coming_soon = 1
    ready = 2
    opening_soon = 4


GymLocation = namedtuple('GymLocation',
                         ['latitude', 'longitude', 'address', 'postcode'])

GymPrice = namedtuple('GymPrice',
                      ['per_month', 'joining_fee', 'pay_as_you_go'])

Gym = namedtuple('Gym',
                 ['id', 'url', 'slug', 'name', 'location', 'price', 'status'])


class PureGym:

    @cached_property
    def gyms(self):
        scraper = AllGymsScaper()
        return [
            self.parse_gym_data(gym_data)
            for gym_data in scraper.data
        ]

    def parse_gym_data(self, gym_data):
        location = GymLocation(
            latitude=gym_data['latitude'],
            longitude=gym_data['longitude'],
            address=gym_data['streetAddress'],
            postcode=gym_data['postcode'],
        )

        price = GymPrice(
            per_month=gym_data['monthlyfee'],
            joining_fee=gym_data['joiningfee'],
            pay_as_you_go=gym_data['payAsYouGoFee'],
        )

        return Gym(
            id=gym_data['id'],
            url='https://www.puregym.com{0}'.format(gym_data['url']),
            slug=gym_data['urlName'],
            name=gym_data['name'],
            location=location,
            price=price,
            status=GymStatus(gym_data['status']),
        )
