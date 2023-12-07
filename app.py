import streamlit as sp
import pickle
import re
from urllib.parse import urlparse
from tld import get_tld
import numpy as np


rf = pickle.load(open('model.pkl','rb'))
sp.title("URL Detection")
url = sp.text_area("Enter URL")


def find_ip_add(url):
  match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
  if match:
    return 1
  else:
    return 0


def check_hostname(url):
    hostname = urlparse(url).hostname
    hostname = str(hostname)
    match = re.search(hostname,url)
    if match:
        return 1
    else:
        return 0


def count_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')

def count_domain(url):
   urldir = urlparse(url).path
   return urldir.count('//')

def count_len(url):
    return len(str(url))

def count_host_name(url):
    return len(urlparse(url).netloc)

def shortening_service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return 1
    else:
        return 0
    
def supicious_words(url):
    match = re.search('paypal|login|singin|bank|account|update|credit|free|lucky|service|customercare|bonus|ebayisapi|webscr',url.lower())

    if match:
        return 1
    else:
        return 0

def special_char(url):
    count = 0
    for i in url:
       if (i.isdigit() == False) and (i.isalpha() == False):
           count+=1
    return count       


def count_digit(url):
    count = 0

    for i in url:
        if(i.isdigit()):
            count+=1
    return count

def count_letter(url):
    count = 0

    for i in url:
        if(i.isalpha()):
            count+=1

    return count


def fd_length(url):
    urlpath = urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0
    
def tld_len(tld):
    try:
      return len(tld)
    except:
      return 0

    

# main function
def main(url):
    status = []
    status.append(find_ip_add(url))
    status.append(check_hostname(url))
    status.append(url.count('.'))
    status.append(url.count('www'))
    status.append(url.count('@'))
    status.append(count_dir(url))
    status.append(count_domain(url))
    status.append(url.count('http'))
    status.append(url.count('https'))
    status.append(url.count('?'))
    status.append(url.count('%'))
    status.append(url.count('-'))
    status.append(url.count('='))
    status.append(url.count('+'))
    status.append(count_len(url))
    status.append(count_host_name(url))
    status.append(shortening_service(url))
    status.append(supicious_words(url))
    status.append(special_char(url))
    status.append(count_digit(url))
    status.append(count_letter(url))
    status.append(fd_length(url))
    tld = get_tld(url,fail_silently=True)
    status.append(tld_len(tld))

    return status

# predict function
def prediction(url):
    features = main(url)
    features = np.array(features).reshape((1,-1))
    pred = rf.predict(features)

    if int(pred[0]) == 0:
        return "Safe"
    
    elif int(pred[0]) == 1.0:
        return "Defacement"
    
    elif int(pred[0]) == 2.0:
        return "Phishing"
    
    elif int(pred[0]) == 3.0:
        return "Malware"


if sp.button("predict"):
     sp.header(prediction(url))
 


