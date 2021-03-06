from bs4 import BeautifulSoup
import requests
import os
import csv


def get_review_links(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tbody = soup.find('tbody', class_='lister-list')
    trs = tbody.find_all('tr')
    movies = list()
    for tr in trs:
        movie = dict()
        movie['name'] = tr.select('td')[1].a.text
        movie['review_link'] = 'https://www.imdb.com' + tr.select('td')[1].a.get('href') + 'reviews'
        movies.append(movie)
    return movies

def scrap_reviews(url: str):
    reviews_response = requests.get(url)
    print(reviews_response.status_code)
    reviews_soup = BeautifulSoup(reviews_response.content, 'html.parser')
    reviews_contents = reviews_soup.findAll('div', class_='review-container')
    reviews = list()
    for content in reviews_contents:
        review = dict()
        review['title'] = content.find('a').text.strip()
        review['content'] = content.find('div', class_='text').text.strip()
        reviews.append(review)
    return reviews

def main():
    url = 'https://www.imdb.com/chart/top/'
    movies = get_review_links(url)
    # create folder
    folder_path = os.path.join(os.getcwd(), 'reviews')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    for movie in movies:
        reviews = scrap_reviews(movie['review_link'])
        file_path = os.path.join(folder_path, movie['name'] + '.csv')
        # create file
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = reviews[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for review in reviews:
                writer.writerow(review)


if __name__ == '__main__':
    main()
