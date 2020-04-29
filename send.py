# -*- encoding: utf-8 -*-

import pika
from pika.exceptions import AMQPConnectionError, AMQPError
import re
import json
import csv
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

        # criando o pipeline a ser usado
        channel.queue_declare(queue='plan_pipeline')
    except AMQPConnectionError:
        logging.error('Não foi possível conectar com o servidor RabbitMQ')
        exit(1)
    except AMQPError:
        logging.error('Ocorreu um erro ao criar o pipeline')
        exit(1)

    # lendo o arquivo csv
    logging.info('Lendo o arquivo CSV')
    time.sleep(0.5)
    with open('inputvagapython.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # recuperando os header do csv
        i = csv_file.readline()

        # criar o pattern para formatar o header
        pattern = re.compile(r"\"(.+?)\"")
        headers = pattern.findall(i)

        # recuperando as linhas de dados sem os headers
        linhas = [dados for dados in csv_reader if dados != ['nuprocesso;"deassunto";"devara";"dtcoleta";"declasse"']]

        # criar os patterns para formatar as linhas de dados
        pattern_subs_pontovir = re.compile(r";;")
        pattern_subs_quotes = re.compile(r'""|^\s')
        pattern_alter_pontovir = re.compile(r';')
        pattern_add_proc = re.compile(r'^" "')
        pattern_split = re.compile(r",")

        # variavel que servir para nomear processos sem numeros
        num = 0

        # criando o dicionario junto com as headers e formatando cada linha
        for linha in linhas:
            val = pattern_subs_quotes.sub('" "', linha[0])
            val = pattern_subs_pontovir.sub(';" ";', val)
            val = pattern_alter_pontovir.sub(',', val)
            val = pattern_add_proc.sub(f'Sem_numero_{num},', val)
            val = pattern_split.split(val)
            num = num + 1

            # criando um dicionario para cada linha percorrida
            result = dict([(k, v) for k, v in zip(headers, val)])

            # convertendo o dicionario recem criado em json
            result_json = json.dumps(result, ensure_ascii=False)

            # enviando o json criado para o server Rabbit
            channel.basic_publish(exchange='', routing_key='plan_pipeline', body=result_json)

    time.sleep(1)
    logging.info(' [x] Dados enviados com sucesso!')
    conn.close()