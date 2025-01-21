# simple_app.py

import os

def app(environ, start_response):
    path = environ.get('PATH_INFO', '')

    if path.startswith('/static/'):
        file_path = os.path.join(os.path.dirname(__file__), path.lstrip('/'))
        if os.path.exists(file_path) and os.path.isfile(file_path):
            if file_path.endswith('.css'):
                content_type = 'text/css'
            elif file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.png'):
                content_type = 'image/png'
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            else:
                content_type = 'application/octet-stream'

            with open(file_path, 'rb') as f:
                content = f.read()

            start_response('200 OK', [('Content-Type', content_type)])
            return [content]
        else:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b"File not found"]

    file_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    try:
        with open(file_path, 'rb') as f:
            content = f.read()

        start_response('200 OK', [('Content-Type', 'text/html')])
        return [content]
    except Exception as e:
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [f"Error: {str(e)}".encode()]
