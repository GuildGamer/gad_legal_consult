from waitress import serve
    
from glc.wsgi import application
    
if __name__ == '__main__':
    serve(application)

threads = 8