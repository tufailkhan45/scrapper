import requests
from bs4 import BeautifulSoup

productArray = []
brands = [
    {
        'name': 'testing-savyour',
        'url': "https://testing.savyour.com.pk/men.html",
    },
    {
        'name': 'elo',
        'url': "https://www.elo.shopping/collections/men?page={}"
    }
]
metaInfo = {
    'testing-savyour': {
        'main-class': 'product-item',
        'main-element': 'li',
        'name-class': 'product-item-link',
        'name-element': 'a',
        'image-class': 'product-image-photo',
        'img-attr': 'src',
        'image-element': 'img',
        'price-class': 'price',
        'price-element': 'span',
        'pagination': 0,
        'next-pagination-element': 'pagination__item--prev',
        'page-query-param': 'page'
    },
    'elo': {
        'main-class': 'grid__item',
        'main-element': 'li',
        'name-class': 'full-unstyled-link',
        'name-element': 'a',
        'image-class': 'motion-reduce',
        'image-element': 'img',
        'img-attr': 'srcset',
        'price-class': 'price-item--last',
        'price-element': 'span',
        'pagination': 1,
        'next-pagination-element': 'pagination__item--prev',
        'page-query-param': 'page'
    }
}

pageNumber = 1
for brand in brands:
    while True:
        url = brand['url'].format(pageNumber)
        print(url)
        page = requests.get(brand['url'])
        soup = BeautifulSoup(page.content, "html.parser")
        paginationElement = soup.find('a', metaInfo[brand['name']]['next-pagination-element'])

        if paginationElement is None:
            break
        products = soup.find_all(metaInfo[brand['name']]['main-element'], class_=metaInfo[brand['name']]['main-class'])

        for product in products:
            name = product.find(metaInfo[brand['name']]['name-element'], class_=metaInfo[brand['name']]['name-class'])
            image = product.find(metaInfo[brand['name']]['image-element'],
                                 class_=metaInfo[brand['name']]['image-class'])
            price = product.find(metaInfo[brand['name']]['price-element'],
                                 class_=metaInfo[brand['name']]['price-class'])
            productArray.append({
                'name': name.text.strip() if name else name,
                'image': image.get(metaInfo[brand['name']]['img-attr']) if image else image,
                'price': price.text.strip() if price else price,
            })
        pageNumber += 1

print('Total Products: ', len(productArray))
# for array in productArray:
#     print(array)
