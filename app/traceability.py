''''''
import uuid
import asyncio
import util
import ssl
import json
import pika
from pika import exceptions
import sys
from azure.cosmosdb.table.tableservice import TableService

class Traceability(object):
    '''class main traceability'''
    #traceability
    @classmethod
    def __init__(cls, **kwargs):
        '''method init'''
        keys = util.DICT2KEYS(kwargs, 'partitionKey', 'nameTable', 'host', 
        'port', 'username', 'password', 'virtualHost', 'exchange', 'routingKey', 'connectionString')
        cls.partitionKey, cls.nameTable, cls.host, cls.port, cls.username, cls.password, cls.virtual_host, cls.exchange, cls.routing_key, connection_string=keys
        cls.table_service = TableService(connection_string=connection_string)

    @classmethod
    def connect(cls):
        """ Crea una conexión con RabbitMQ """
        try:
            cxt = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_options = pika.SSLOptions(
                context=cxt,
                server_hostname=cls.host)
            credentials = pika.PlainCredentials(cls.username, cls.password)
            parameters = pika.ConnectionParameters(
                cls.host,
                cls.port,
                cls.virtual_host,
                credentials,
                ssl_options=ssl_options)
            cls.connection = pika.BlockingConnection(parameters)
            cls.channel = cls.connection.channel()
            print('connection_established')
            return True
        except exceptions.AMQPConnectionError as error:
            print('connection_not_established', error)
            return False

    @classmethod
    def disconnect(cls):
        """ Cierra conexión con RabbitMQ """
        cls.connection.close()
        print('connection_closed')

    @classmethod
    def send_json(cls, mensaje):
        """ Envia un mensaje JSON a un tópico de RabbitMQ """
        try:
            cls.channel.basic_publish(
                exchange=cls.exchange,
                routing_key=cls.routing_key,
                body=json.dumps(mensaje))
            print('message_send')
        except (exceptions.ConnectionClosed, exceptions.ChannelClosed, exceptions.ChannelWrongStateError):
            if not cls.connect():
                print('connection_lost')
                print('pending_message')

    @classmethod #async
    def save(cls, business_key, transaction_id, operation, componentName, types, message, status, description):
        '''insert traceability table azure'''
        print('insert traceability table azure')
        registry = {
            'PartitionKey': cls.partitionKey,
            'RowKey': str(uuid.uuid4()),
            'BusinesKey': business_key,
            'idTransaction': transaction_id,
            'operation': operation,
            'componentName': componentName,
            'type': types,
            'message': message,
            'status':status,
            'description':description
        }
        print(registry)
        cls.connect()
        cls.send_json(registry)
        cls.disconnect()
        cls.table_service.insert_entity(cls.nameTable, registry)

    @classmethod
    def main(cls):
        '''Method main'''