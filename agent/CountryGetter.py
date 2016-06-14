from geoip import geolite2
import ipgetter


class CountryGetter(object):
    """
    This class enables you to get your own country code by your IP address
    """

    @staticmethod
    def get_country():
        """
        Returns country code of the IP address that belongs to the machine this method is called on
        """
        myip = ipgetter.myip()
        match = geolite2.lookup(myip)
        return match.country
