'''Modulo table azure - parametros'''
import json
from azure.cosmosdb.table.tableservice import TableService

class Parameter(object):
    '''Clase principal'''
    @classmethod
    def __init__(cls, account_name, account_key):
        '''Metodo init'''
        cls.table_service = TableService(
            account_name=account_name,
            account_key=account_key
        )

    @classmethod
    def create_array_email(cls, data):
        emails = []
        result = data.split(',')
        for email in result:
            emails.append({'email':email.strip()})
        return emails

    @classmethod
    def get_parameters(cls):
        '''Obtiene parametros de la tabla'''
        tasks = cls.table_service.query_entities('parameters')
        config = {}
        for task in tasks:
            if task.PartitionKey in config:
                if  task.PartitionKey == 'sendGrid' and task.RowKey == 'toEmail':
                    config[task.PartitionKey][task.RowKey] = cls.create_array_email(task.Value)
                else:
                    config[task.PartitionKey][task.RowKey] = task.Value
            else:
                config[task.PartitionKey] = {}
                config[task.PartitionKey][task.RowKey] = task.Value
        print(f'JSON de configuracion:\n {config}')
        return config
