from waitress import serve
import os
    
from glc.wsgi import application
    
if __name__ == '__main__':
    port = os.getenv('PORT', default=8000)
    serve(application, port=port)

threads = 8


