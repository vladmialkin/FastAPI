import pika


connect_params = pika.ConnectionParameters(
    host='rabbitmq',
    port=5672,
    virtual_host='/',
    credentials=pika.PlainCredentials(
        username='fast_api_user',
        password='fast_api_pass'
    )
)
connection = pika.BlockingConnection(connect_params)
channel = connection.channel()

channel.queue_declare(queue='new_orders_queue')
channel.queue_declare(queue='order_processing_queue')
channel.queue_declare(queue='sending_message_queue')