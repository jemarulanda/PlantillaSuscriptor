'''Module RabbitMQ'''
import pika
import util
from pika import exceptions
import ssl

class RabbitMQ:
    @classmethod
    def __init__(cls, **kwargs):
        '''Method init'''
        keys = util.DICT2KEYS(kwargs, 'host', 'virtualhost', 'port', 'username', 'password', 'queue')
        cls.host, cls.virtualhost, cls.port, cls.username, cls.password, cls.queue = keys

    @classmethod
    def connect(cls):
        '''Connect to RabbitMQ'''
        try:
            cxt = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_options = pika.SSLOptions(
                context=cxt,
                server_hostname=cls.host)
            credentials = pika.PlainCredentials(cls.username, cls.password)
            parameters = pika.ConnectionParameters(
                cls.host,
                cls.port,
                cls.virtualhost,
                credentials,
                ssl_options=ssl_options)
            cls.connection = pika.BlockingConnection(parameters)
            cls.channel = cls.connection.channel()
            #cls.channel.queue_declare(queue=cls.queue)
            print('connection_established_rabbit')
            return True
        except exceptions.AMQPConnectionError as error:
            print('connection_established_not_rabbit', str(error))
            return False

    @classmethod
    def disconnect(cls):
        '''Disconnect'''
        cls.connection.close()
