import requests
from bs4 import BeautifulSoup
import pprint
num_of_pages = 10

list_of_res = [requests.get('https://news.ycombinator.com/news')]
for i in range(2,num_of_pages+1):
    list_of_res.append(requests.get(f'https://news.ycombinator.com/news?p={i}'))

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k:k['votes'], reverse=True)

def get_page_as_list(res):
    soup = BeautifulSoup(res.text, 'html.parser')

    links = soup.select('.storylink')
    subtext = soup.select('.subtext')

    def create_custom_hn(links, subtext):
        hn = []
        for i, item in enumerate(links):
            title = item.getText()
            href = item.get('href', None)
            vote = subtext[i].select('.score')
            if len(vote):
                points = int(vote[0].getText().replace(' points', ''))
                if points > 99:
                    hn.append({'title': title, 'link': href, 'votes': points})
        return sort_stories_by_votes(hn)

    return(create_custom_hn(links, subtext))

pages = []
for res in list_of_res:
    pages = pages + get_page_as_list(res)

full = sort_stories_by_votes(pages)
pprint.pprint(full)