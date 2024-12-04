import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

def crawler(url, max_depth = 5,visited=None,offerts = None):
    try:
        if visited is None:
            visited = set()
        if offerts is None:
            offerts = set()
        def _crawl(current_url, depth):
            print(depth)
            if depth>max_depth:
                return
            visited.add(current_url)
            response = requests.get(current_url)
            soup = bs(response.text,'html.parser')
            for a_tag in soup.find_all('a', href = True):
                next_url = urljoin(url, a_tag['href'])
                if next_url not in visited:
                    if (next_url.startswith('http') and a_tag['href'].startswith('/d/oferta')):
                        offerts.add(next_url)
                        #print(f"URL: {next_url}, Title: {soup.title.string}")
                    elif next_url.startswith('http'):
                        # Jeśli URL wskazuje na kolejną stronę w wynikach wyszukiwania, nie zwiększaj głębokości
                        if 'page' in next_url:
                            _crawl(next_url, depth)  # Utrzymanie tej samej głębokości
                        else:
                            _crawl(next_url, depth + 1)  # Przejście na głębszy poziom
                        
                
        _crawl(url,0)
    except Exception as e:
        print(str(e))
    finally:    
        return offerts,visited
    