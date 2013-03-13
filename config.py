# coding=utf-8

DEBUG = True

WEB_SERVICES = {
    "parlamento.openpolis.it": dict(
        title=u"Openparlamento",
        logo="/static/logo-openparlamento.png",
        arrow="/static/arrow-red.png",
        arrow_link="http://parlamento16.openpolis.it/",
        service_uri="http://parlamento17.openpolis.it/",
        description=u"""<strong>Open parlamento XVI legislatura (2008-2013)</strong><br>
            L’edizione della piattaforma web Open parlamento con tutti i lavori della XVI legislatura
            (2008-2013) è ancora disponibile e consultabile online. <br>
            I dati sono aggiornati a gennaio 2013 e provengono dalle fonti uffciali del Ministero
            dell’Interno, Camera e Senato.""",
        form_description=u"""Stiamo lavorando alla nuova edizione di Open parlamento,
            lasciaci la tua e-mail per sapere quando saremo online ed essere informato
            su tutte le iniziative di Openpolis.""",
        form_description_image="/static/logo-openparlamento-new.png",
    ),

    "indice.openpolis.it": dict(
        title=u"Indice di produttività parlamentare",
        logo="/static/logo-indice.png",
        arrow="/static/arrow-green.png",
        arrow_link="http://indice16.openpolis.it/",
        service_uri="http://indice17.openpolis.it/",
        description=u"""<strong>Indice di produttività parlamentare della XVI legislatura (2008-2013)</strong><br>
            Il sito che misura la quantità ed efficacia dell'attività dei parlamentari dall'inizio alla fine
            della XVI legislatura (2008-2013) è ancora disponibile e consultabile online.
            I dati sono aggiornati a gennaio 2013 e provengono dalle fonti ufficiali
            del Ministero dell'Interno, Camera e Senato.""",
        form_description=u"""Stiamo lavorando alla nuova edizione dell'Indice di produttività parlamentare,
            lasciaci la tua e-mail per sapere quando saremo online ed essere informato
            su tutte le iniziative di Openpolis.""",
        form_description_image="/static/logo-indice-new.png",
    ),
}


def get_config(host):
    if host in WEB_SERVICES:
        return WEB_SERVICES[host].copy()
    if ':' in host:
        host = host.split(':')[0]
        return get_config(host)
    raise KeyError("Service not found at {0}".format(host))
