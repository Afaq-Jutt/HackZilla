from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models

# Create your views here.

def home(request):
    return render(request, 'Base.html')           #For rendering the Basic page of website.


# BASE_CRAGLIST_URL='https://newyork.craigslist.org/search/bbb?query=python&sort=rel'
BASE_CRAGLIST_URL='https://newyork.craigslist.org/search/?query={}'
BASE_IMAGE_URL='https://images.craigslist.org/{}_300x300.jpg'

response=requests.get(BASE_CRAGLIST_URL)
def new_search(request):
    search=request.POST.get('search')
    models.Search.objects.create(search=search)
    finalurl=BASE_CRAGLIST_URL.format(quote_plus(search))
    # print(finalurl)
    Response=requests.get(finalurl)
    data=Response.text
    # print(data)
    soup=BeautifulSoup(data, features='html.parser')

    post_listning=soup.find_all('li',{'class':'result-row'})

    Final_Posting=[]

    for post in post_listning:
        post_title=post.find(class_='result-title').text
        post_url=post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price=post.find(class_='result-price').text
        else:
            post_price='N/A'
        if post.find(class_='result-image').get('data-ids'):
            post_image_id=post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]  #Here, we are sipliting the images data ids with split function.In First split(',')[0],we are spliting all images first data id with (',') and [0] means images first data id.In second split(',')[0] we are spliting the all images first data id with (:) and in second case,[1] means give us the second element of image data id. ex:-  1:BBob_93758f_0923(This is the image data id). 1=first element and BBob_93758f_0923=Second element.
            post_image_url=BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url='data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIAHUArwMBIgACEQEDEQH/xAAcAAABBAMBAAAAAAAAAAAAAAAGAwQFBwABAgj/xAA4EAACAQMDAwIEAwUJAQEAAAABAgMABBEFEiEGMUETUSJhcZEUMoEHFSNCsUNSU2KhwdHw8eEz/8QAGgEAAgMBAQAAAAAAAAAAAAAAAgMAAQQFBv/EACcRAAICAgIBAwMFAAAAAAAAAAABAhEDIRIxBCJBUQUTMhRhobHR/9oADAMBAAIRAxEAPwCqRXS1yK6FMKO81hNardCWbXNdDPua1itioQ0Sfc1sFv7x+9axXQX2qEs5Jf8AvH71gLk/mb70rHBLM6xxIzs3ACjOatTozoS2tI47rWolnue6wnlE+vuaGUlEKMXLoq61sr68bbZ211cH2hiZ/wCgqct+gerriISx6RcKrdt5VT9ic1fdtLFaRCOCOOJR2WNQo/0rcmoN7kYoHlQX25FDXnQXV1jbtNLp0jIvf0nDn7ChqR7mF2jlMiOpwyuuCP0NeljqMn8jk0N9T6BpnUiE30IjucYW5iUBx9fcfWrU0yuLRRYupx/aGt/jZwPz1I9RdOX2gXJS5QvAx/hXCj4X/wCD8qhTTOKAtij3Mj/mOaVsmOTTXFL2jj1MVJLWi09k7p7HBFSqkEAFQfrUTYAo2alE3SYKCsOVbOhh6NSTCLIVcUxgiR3Z5RknzTm+BQZNcKVaIKO9VBUiTtugUCn2rrGKsebpaFdu0DBqI1/poWlv60Y4x48VrWVN0YHBpAiBWwK6x3p7pNmby7SL3NMbpWAtsabTjtWYq17Toy2NupdATisl6ItmB2rik/eXwM+2yp66VVz8ROPl5o01vpE2cZlj8eKDWG1ivtRwmpASi49lgfsvsNOuLmS6UTG5gGfiXgfQg/1qw2kZWBoG/ZtazXOhXChniiedcyKcEgc4H9KPvT3y4xhFFYc1uWjf46SjbEi5C73PFJrIJV3DkeOahestdh0mJYmRncjeqp5Apn0p1nBqFy1neWjWr8BAw4Oe3I48f+1I4pNBSnFBI7uP5v8ASuoLiHd/FAOPmKy+UISYz28ChPXr2S3jiaNny83p4Xt2zzQc5J0WoRkgqnitb+JoRHHJC4w0bDINVP1t0XcaTPJeWcSixbkKG5Q+30o7ivXgVSD8Xn5UrdXZv7CeGU7sqe4rRjz7M2TDRRTGtWxxMM0tcpsmkUZwGOM0h2YGt3aMy0EtpIoxk0+iu/SYBcUPQSHA5p2j8ZJ7Vlnj2a4ZNEjqspkQ4Pioe2u3Dtk9qcXU4aPv4qIV9shPvV44emiZJ+qy3tLvP3jMoTJJ70+6ttDHokhPgV1+zjT09H1nHJPepjryANo8yoMnb2FBCPuJk/YoRELdqIujbVn1VTjtzTOw02aVcrCx+gox6L0yWK/ZniKjHcimylaEq1INJLg26RqR3FO7aQyJkiktQtNyoT/LWW0oUbSQKzXs1VaGvUUQexfA/lNVT0901ddQ6m8ao0VvC4NxMRjaufn5q1epJY/3c+5sDb3AzVddRXOodMaDpdpaTlYtQSS5nbGHbkBQfltI/WnQ+ELkrey0NIj0rS7KOxsGURRDCjduJPkk+9SRKshIHeqB6c1q6S8t447h2Dv2B7fpV26ZcI0Qy3PGfrQOLjKmNTTjaIbqbQItbELMXWWEkZQ4OD/5UXpf7PFhlzLfTNF5U4zjvjPjsPtRo+1G3jya7aUenngVFJxtFv1EZdwm1jwHLoBjk80L3EyX9wUaMFLZw/qdsHnipjWr31SLdGwCeSO+B3qKMX8IKoGB3H+9YW05aNsLUdjSe5K+oxP5Rk/0x/32pSyuDk71P+Yim20yBkJ2qp+I4zk/70u4/CRKcbiTgD3zRX8FONgb1Toxs7p54kJt5TuVxyBnxmhRxyatS/uEhtpo5SroF+JW7EGqwuyhncwj4Ccge1dLx8nJHPz4+DFbNs4FO3bA21G20mx6ezHsw7UyS2BF6MkyIsc0z7d6lI3jMOHGTio6VfiJHapFlyR6c6d0xbOxRVGOKeXunrcxlXAII5zT20XEKge1KsOKTGOgb2D+ndO2sDNsjAzUrFpkEXKoop3GKVHarUSrIy9tFaI8VA/gDvOB5osmXK02W3Gc0EsabDjNohG0j1kwwz9aEP2ndPS6ha2rIh328ZAPsP8Aoq044wBSd7aR3ULRyAEMMcjNTg1tFqe9nnCy0+TT5496su7lXI71aOjTH0VLOzZx5+3FZqPRRhlZ7FigJ5XOVP6Gk7fSZLXACxKV9l7fpnFLlPdyH0mqiEMW113e/wBjTK9YIj4YCmyQTp8bXLO2exPH2pO5VZsq+0HztNLnNOPRcIUwbyxv5ixJf8q+wB7n9ak4o1dduByM8+9Nr60khuIWtwSp3B8fpilFnkUEbGHvxWS2pGzTjoYrtVQG4ZWJOfesmGdjSHJUHAHnINJ3izQRzXVyvpQKpdixwT9KH36gllklkhjwu3ai+cn/AIFNx4Zyf7FqSapdiOvyGeHEJ/hsdrH3x4oUltWBNGuvWx0rStOhkX4imWP+Y96GprhCO1dLH6NI52fjKbaIj0WVsmnMb5XBrcrqc8Ugrc07sQtHchrTPmtsu4VwE296rRZ6rs7omIc+KWe6wKZWjLsHApdiuOwrOih1DPlaVWamUTA0suKKyC7zDFaSQU3kIxXCtUslD8SgVy8wFNg4pKWQAHmqbJRueUMdoqAv4/UVsd6kFlDzMAfFM7g5Y1kz7Rs8bTK01uTU9J122ubd3NtK4jkXuFJIGTSN91Bf2Gr3VpcBRNDKUZc4z9Pfijy9so7pcED37UI6rpjXmv3l9dab+JjYDEfq7A7gAcnvjipikmql7G68fK5e/wDYvZdY2su71R6bIMBT5qWm6g0yK2WSW4jG75+R4oR1DSdWvZVeSwWFFGI44VRUUfL/AO1K/uw3fSkOlzadsv4Zy6XGAMqe+SPrimRULLn4+NRjLl3/AAC/UWuXGt3QEKlIF/LHnufdvlUr0b09LdTR3EwIgjbdlh+dvl8qnNE6MiiIe9Kvj+zAwKL44EgRVRQoAwAKfGXLSEZc2PBHjh7+f8Kz/ahOWuYLZcYRc8UBMre9FXXd6t11BMAP/wA/g70O8Gmp0cqhqUNclCKdkCuSoq+RYgCQKU3hhzS6RK4pJ7Vs8c1LVl06PSluSFpVnPzpC3bilWbikWQUjlx37Un++LUTel6i7/bNcNkowXviq5nS6stYkllBLFyc/KtXi4Y5W7ZzvqHly8aKcVdlmy3yBc5qJuupLS1bErgUxS+WW3XLDOKFtZt5bic7CMGtX6XH7nOl9Tz64oM06usZOFlX71uXXIJB8LjmgKHR5uCzjj2rcu62lUM2MexpcvExvpjI/U88X6olgaVN6krtnIx3pW5IGSWAqJ6cud8L8+KeTHccZri5vS+J6nxnzipDW4lYMNnK/KkhcDeokUYY0rMNq8VD3V4MjA7NS0h8mEs00EaEZG7HApkk2WLeB4qHicvJvlY8896k4wGHw8CilKgIRTJJH+EbmAFI310sNtI+eVFcxFhjd2pnrLD8K4/vVpxS1Zmyxp0VTqdlLcXcs57uxNRklrLEeQftR49uvOQPtTeSyjcciqWdg/bAbDA8itE+9FlzpMbA4HNRN3o7LkqKaskWC4NETuYHg1sXDjxXUtpLGeQcUiQR+YEU2kwLZ6PgIA70sW9qGbXU2XAZqk4dSibGWrOFRJg8UN9VWxaIzRj64qZN7GV4NRep3f8ACdcZyKPHPhK0I8jCsuNxZX7X80bELKRXDalP/iE1u9snM7lQQM0yNpNnzW39TE5K+n5EOn1W528SkCo+a/dpQXctzXUlnOR2Ncw6ZKxHwHNBkzprRp8fwZKVzDPpPV/UmSIDvxRbJw1AvTNjLb3aORtGaOrn8wINcrN2eg8fqhtftth+tDJbOB7tRJecwvnwKBbu+eOUrGpJDe1HCFoqcqCPyoqVgwEFCVtqTMV9QEdqK4DuRfpSsq2M8fpjst8A57VDatOXcJ7CpQkhCaFr65H4lyzYAOK0QjUDPk3I24pIpkcms9UOMgitAZ80PAXyEHKg470kyk+KeekveuJDGvdh/WpxJyIya1VxyoqOuNNjJ4H+lTUkmeEUn602eOQ9+KNNop0wlQc04UkdqysoGMFI5Xz3pWQ7hz5rKyrQEhs0SE8qDWxbxf4a/asrKohv8NDn8gpRYIh2QCtVlQJCgUKeB2qSkbMamt1lKydD8PYlIchgR4oXuoI9zHaM5rKynQ/FC5fkxpDCjXMakfzCjFAFQDHisrKDL2huHpiN3KVgcj2quJ55pLmQGQ4LGsrK0w/FGWT9THUDsqfmJxXQvpMlVAGKysqxaFUkeQ4ZjSj4j8Z+tarKohtZDtrl+a3WUIR//9k='

        Final_Posting.append((post_title,post_url,post_price,post_image_url))

    # print(post_listning)

    # print(post_title)
    # print(post_url)
    # print(post_price)

    Stuff_for_Frontend={
        'search':search,
        'Final_Posting':Final_Posting,
    }
    return render(request, 'my_app/new_search.html', Stuff_for_Frontend)