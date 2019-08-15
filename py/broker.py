import pika
import identify
import json

creds = pika.PlainCredentials("kelvin", "jerryboyis6")
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', credentials=creds))
channel = connection.channel()

channel.queue_declare(queue='simulations')
channel.queue_declare(queue='results')


def callback(ch, method, properties, body):
    requestParams = json.loads(body.decode('utf-8'))
    prefix = requestParams[0]
    storage_type = requestParams[1]

    results = {"hello": "hi"}

    print(prefix + " " +storage_type)

    # send a message back
    channel.basic_publish(exchange='',
                          routing_key='results',
                          body=json.dumps(results, ensure_ascii=False))

    # connection.close()


#  receive message and complete simulation
channel.basic_consume('simulations', callback, auto_ack=True)

channel.start_consuming()
