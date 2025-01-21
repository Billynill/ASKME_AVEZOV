def application(environ, start_response):
    # Заголовки для ответа
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=UTF-8')]
    start_response(status, headers)

    # Получаем GET и POST параметры
    get_params = environ.get('QUERY_STRING', '')
    post_params = environ.get('wsgi.input', '').read()

    # Формируем тело ответа
    response_body = f"GET Parameters: {get_params}\nPOST Parameters: {post_params.decode()}"
    return [response_body.encode()]
