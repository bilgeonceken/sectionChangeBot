import time
import requests
from bs4 import BeautifulSoup as BS

username = "username" ## e1234567
password = "password"
get_url = "https://register.metu.edu.tr" ## Login page
post_url = "https://register.metu.edu.tr/main.php"

## Session class handles cookies automatically
session = requests.Session()
session.headers.update({
        "User-Agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Mobile Safari/537.36",
        "Upgrade-Insecure-Requests" : "1",
        "Host" : "register.metu.edu.tr",
        "DNT" : "1",
        "Connection" : "keep-alive",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language" : "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
    })
r = session.get(get_url)

## Get hidden fields that we need to send with the form
soup = BS(r.text, "lxml")
hidden_redir = soup.find("input",  {"name":"hidden_redir"})["value"]
hidden_form_id = soup.find("input",  {"name":"hidden_form_id"})["value"]

##construct form data
data = {"textUserCode":username,
        "textPassword":password,
        "selectProgType":"1",
        "submitLogin":"[ Login ]",
        "hidden_redir":hidden_redir,
        "hidden_form_id":hidden_form_id
        }
r = session.post(post_url, data=data,allow_redirects=True)

## Beginning of the endless grind
## May be generalized with some inspection and lil bit more beautiful soup
## Currently you only get 219, first section
counter = 0
while True:
    counter+=1
    print("Counter: "+str(counter))
    soup = BS(r.text, "lxml")

    hidden_redir = soup.find("input",  {"name":"hidden_redir"})["value"]
    hidden_form_id = soup.find("input",  {"name":"hidden_form_id"})["value"]

    data = {"radio_courseList":"2360219|2|1",
            "textChangeCourseSection":"1",
            "selectChangeCourseCategory":"1",
            "submitChangeSection":"[ Change Section ]",
            "textAddCourseCode":"",
            "textAddCourseSection":"",
            "textImgVerify":"",
            "selectAddCourseCategory":"1",
            "hidden_redir":hidden_redir,
            "hidden_form_id":hidden_form_id
            }
    r = session.post(post_url, data=data,allow_redirects=True)
    soup = BS(r.text, "lxml")
    mes = soup.find(color="red")
    print(mes.string) ## "Catagory is full Catagory is full Catagory is full"
    time.sleep(3) ## seconds
