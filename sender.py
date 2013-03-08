__author__ = 'guglielmo'

import zmq


SERVER_HOST = '127.0.0.1'
MAILBIN_QUEUE_ADDR = "tcp://{0}:5558".format(SERVER_HOST)


def form_handler(email, service_uri, first_name='', last_name='', ip_address='', user_agent='', **extra):
    """
    Simulate the main form request handler.
    Send a fake message to the mailbin queue
    """
    context = zmq.Context()

    # socket to sending messages to save
    save_sender = context.socket(zmq.PUSH)

    try:
        save_sender.connect(MAILBIN_QUEUE_ADDR)
    except Exception, e:
        print "Error connecting: %s" % e

    data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        #'created_at': faker.dateTimeThisMonth().strftime('%Y%m%d'),
        'ip_address': ip_address,
        'user_agent': user_agent,
        'service_uri': service_uri
    }

    if extra:
        data.update(extra)

    # send message to receiver
    save_sender.send_json(data)
