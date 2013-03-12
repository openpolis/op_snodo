from web import form


validate_email = form.regexp(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                             "Inserisci un indirizzo email valido")

subscribe_form = form.Form(
    form.Textbox("first_name", maxlength="200", class_='span12', placeholder='Il tuo nome'),
    form.Textbox("last_name", maxlength="200", class_='span12', placeholder='Il tuo cognome'),
    form.Textbox("email", validate_email, placeholder='La tua Email')
)