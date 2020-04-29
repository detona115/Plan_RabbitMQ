# -*- encoding: utf-8 -*-

import pika
from pika.exceptions import AMQPConnectionError, AMQPError
import json
import logging
import time

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%H:%M:%S', level=logging.INFO)

if __name__ == '__main__':

    # conectando com o server Rabbit
    logging.info('Conectando com o servidor Rabbit')
    time.sleep(0.5)
    try:
        conn = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = conn.channel()

        # declarando o pipeline já existente
        channel.queue_declare(queue='plan_pipeline')
    except AMQPConnectionError:
        logging.error('Não foi possível conectar com o servidor RabbitMQ')
        exit(1)
    except AMQPError:
        logging.error('Ocorreu um erro ao declarar o pipeline')
        exit(1)

    # criando o loop que vai capturar as mensagens do server
    def callback(ch, method, properties, body):
        logging.info(' [x] Recebido %s' %body.decode())

        # isolando a o numero de processo para nomear o arquivo
        num_proc = json.loads(body.decode())

        # escrevendo os dados recebidos em novo arquivo
        with open(f'/code/procs/Processo_{num_proc["nuprocesso"]}.json', 'w') as file:
            file.write(body.decode())

    # chamando o loop
    channel.basic_consume(queue='plan_pipeline', on_message_callback=callback, auto_ack=True)

    logging.info(' [*] Esperando novas mensagens. Aperta CTRL+C para sair')

    channel.start_consuming()