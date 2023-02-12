import redis
from fastapi import FastAPI
from pydantic import BaseModel
import re


app = FastAPI()

SITE_URL = 'https://shorty.ly/'
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$" )

r = redis.Redis(host='redis', port=6379, db=0)

class SaveRequest(BaseModel):
    user_email: str
    url: str

@app.post('/shorten_url')
def save_url(save_request: SaveRequest):
    if not EMAIL_REGEX.match(save_request.user_email):
        return {'status': 'Invalid Email'}

    hash_url = hash(save_request.url+save_request.user_email)

    status = 'ALREADY EXISTS'
    if not r.exists(hash_url):
        url_data = {
            'user': save_request.user_email,
            'url': save_request.url,
            'view_count': 0
        }
        r.hset(hash_url, mapping=url_data)
        r.incrby(save_request.user_email, 1)
        status = 'OK'

    return {
        'status': status,
        'short_url': SITE_URL + str(hash_url)
    } 


@app.get('/decode/{hash_url}')
def get_urls(hash_url):
    url = r.hget(hash_url, 'url')
    if url is None:
        return {'status': 'Not Found'}
    r.hincrby(hash_url, 'view_count', 1)
    return {'status': 'OK', 'url': url}


@app.get('/view_counts/{hash_url}')
def get_view_counts(hash_url):        
    counts = r.hget(hash_url, 'view_count')
    if counts is None:
        return {'status': 'Not Found'}
    return {'status': 'OK', 'view_counts': counts}


@app.get('/user_count/{user_email}')
def get_user_counts(user_email):        
    counts = r.get(user_email)
    if counts is None:
        return {'status': 'Not Found'}
    return {'status': 'OK', 'counts': counts}


@app.delete('/{hash_url}')
def delete_url(hash_url):
    url_data = r.hgetall(hash_url)
    if not url_data:
        return {'status': 'Not Found'}

    user = url_data[b'user']
    r.delete(hash_url)
    r.decrby(user, 1)
    return {'status': 'OK'}