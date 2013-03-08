import web
from web import form


def csrf_token():
    from app import session
    if 'csrf_token' not in session:
        from uuid import uuid4
        session.csrf_token = uuid4().hex
    return session.csrf_token


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


validate_email = form.regexp(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                             "Inserisci un indirizzo email valido")

subscribe_form = form.Form(
    form.Textbox("first_name", maxlength="200", class_='span12', placeholder='Il tuo nome'),
    form.Textbox("last_name", maxlength="200", class_='span12', placeholder='Il tuo cognome'),
    form.Textbox("email", validate_email, placeholder='La tua Email')
)