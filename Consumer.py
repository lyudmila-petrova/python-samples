import pika

from app.config.queue_enum import Queue
from app.lib.queue.util import get_rabbit_connection_params
from app.lib.queue.command_processing import execute_lis_command


class Consumer:
    def __init__(self, queue: Queue, connection_params=None):
        self.connection_params = connection_params or get_rabbit_connection_params()
        self.queue_name = queue.value

    def start(self):
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=True)
        channel.basic_qos(prefetch_count=1)  # not to give more than one message to a worker at a time
        channel.basic_consume(self.__callback,
                              queue=self.queue_name)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    @staticmethod
    def __callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        execute_lis_command(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # delete message from queue
