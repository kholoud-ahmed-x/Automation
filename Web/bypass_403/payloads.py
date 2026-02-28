HTTP_METHODS = ['GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH']

# Since we are concatinating the url with '/', i removed the trailing and leading slashes from the list as they are gonna be appended below
PATH_NORM = ['','.', '../../', '..', '%2e', '%2e%2e', '%00', '%20', '..;', '.;', '%2e%2e%2f', '%2e%2e', '/;/']

CONTENT_TYPES = [
    'application/json',
    'application/xml',
    'text/xml',
    'application/x-www-form-urlencoded',
    'multipart/form-data',
    'text/html',
    'text/plain'
]

PROXIES = {
    "http":"127.0.0.1:8080",
    "https":"127.0.0.1:8080"
}
