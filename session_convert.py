from requests.cookies import create_cookie


def ListToSession(session, cookie_list):
    '''

    :param session:
    :param cookie_list:
    :return:
    '''
    for cookie in cookie_list:
        session.cookies.set_cookie(create_cookie(**cookie))
    return session

def SessionToList(session):
    '''
    session 转 dict
    :param session:
    :return: dict
    '''
    cookie_list = []
    for cookie in session.cookies:
        cookies_dict = {
            # 'version': cookie.version,
            'name':cookie.name,
            'value':cookie.value,
            # 'port':cookie.port,
            'domain': cookie.domain,
            'path': cookie.path,
            # 'secure': cookie.secure,
            # 'expires': cookie.expires,
            # 'discard': cookie.discard,
            # 'comment': cookie.comment,
            # 'comment_url': cookie.comment_url,
            # 'rfc2109': cookie.rfc2109,
        }
        cookie_list.append(cookies_dict)
    return cookie_list

