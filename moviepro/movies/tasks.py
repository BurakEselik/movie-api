import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from celery import shared_task

@shared_task()
def get_imdb_rating(name: str, instance=None, **kwargs):
    """
    ...

    Basic Usage: get_imdb_rating('spiderman') or give exact=True as a kwarg
    """
    url = "https://www.imdb.com"
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    def get_first_movie() -> str:
        """
        Searchs and gets the link of the first movie from the imdb
        """
        payload = {"s": "tt", "q": str(name), "ref_": "nv_sr_sm"}
        if 'exact' in kwargs:
            if isinstance(kwargs['exact'], bool) and kwargs['exact'] == True:
                payload["exact"] = 'true'
        response = requests.get(url=url + '/find/', params=payload, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        first_movie_link = soup.find("div", {'class': 'sc-17bafbdb-2 ffAEHI'}).ul.li.a
        return first_movie_link.get('href')
    
    def get_rating(href: str):
        """
        Scraps movie page and gets the imdb rating based on href
        """
        payload = {"ref_": "fn_tt_tt_1"}
        response = requests.get(url=url + href, params=payload, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        rating = soup.find("span", {"class": "sc-bde20123-1 iZlgcd"}).get_text()
        return rating

    def main():
        fm_href = get_first_movie()
        rating = get_rating(fm_href)
        return Decimal(rating)

    if instance is not None:
        from .models import Movie
        instance = Movie.objects.get(pk=instance)
        instance.imdb = main()
        instance.save()
