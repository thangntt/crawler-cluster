from crawler.config_properties import ConfigProperties
import random
import logging


class ProxyHandler:
    __config_properties = ConfigProperties.get_config()
    __logger = logging.getLogger(__name__)
    __proxy_urls = None

    @staticmethod
    def random_proxy():
        try:
            if ProxyHandler.__proxy_urls is None:
                ProxyHandler.__proxy_urls = str(ProxyHandler.__config_properties.get('proxy', 'proxy_urls')).split(',')
            i = random.randint(0, len(ProxyHandler.__proxy_urls) - 1)
            return ProxyHandler.__proxy_urls[i].strip()
        except Exception as e:
            ProxyHandler.__logger.error(e)
        return None


    @staticmethod
    def contains(proxy_url):
        try:
            if ProxyHandler.__proxy_urls is None:
                ProxyHandler.__proxy_urls = str(
                    ProxyHandler.__config_properties.get('proxy', 'proxy_urls')).split(',')
            if proxy_url in ProxyHandler.__proxy_urls:
                return True
        except Exception as e:
            ProxyHandler.__logger.error(e)
        return False

