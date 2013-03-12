import web
import sender
import config
import utils


urls = (
    '/', 'home',
    '/subscription', 'subscribe'
)

app = web.application(urls, globals())
web.config.debug = config.DEBUG
# Session/debug tweak from http://webpy.org/cookbook/session_with_reloader
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'))
    web.config._session = session
else:
    session = web.config._session


def csrf_token():
    if 'csrf_token' not in session:
        from uuid import uuid4
        session.csrf_token = uuid4().hex
    return session.csrf_token

render = web.template.render('templates/', globals={'csrf_token': csrf_token})


def csrf_protected(f):
    """Usage:
       @csrf_protected
       def POST(self):
           ..."""
    def decorated(*args, **kwargs):
        inp = web.input()
        if not (('csrf_token' in inp) and inp.csrf_token == session.pop('csrf_token', None)):
            raise web.HTTPError(
                "400 Bad request",
                {'content-type': 'text/html'},
                'Cross-site request forgery (CSRF) attempt (or stale browser form). <a href="/">Back to the form</a>.')

        return f(*args, **kwargs)
    return decorated


class home:
    def GET(self):
        form = utils.subscribe_form()
        result = session.get('success', False)
        try:
            configuration = config.get_config(web.ctx.host)
        except KeyError:
            return render.switch(config.WEB_SERVICES.keys())
        if result:
            del session.success

        return render.index(configuration, form, result)


class subscribe:
    @csrf_protected
    def POST(self):
        form = utils.subscribe_form()
        configuration = config.get_config(web.ctx.host)

        if not form.validates():
            return render.index(configuration, form, False)
        else:
            session.success = True

            # prepare user data
            user_data = form.d
            email = user_data.pop('email')

            user_data['ip_address'] = web.ctx.ip
            if not user_data['ip_address'] or user_data['ip_address'] == '127.0.0.1':
                user_data['ip_address'] = web.ctx.env.get('HTTP_X_FORWARDED_FOR', web.ctx.ip)
            user_data['user_agent'] = web.ctx.env.get('HTTP_USER_AGENT', '')

            # send to zmq
            sender.form_handler(email, configuration['service_uri'], **user_data)

            raise web.seeother('/')


if __name__ == "__main__":
    app.run()

application = app.wsgifunc()