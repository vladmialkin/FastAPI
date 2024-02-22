from connecting import channel, connection


def process_order(order):
    # Выполнение необходимых действий над заказом
    print("Processing order:", order)
    # Здесь можно добавить логику для подтверждения заказа, обновления статуса и подготовки к доставке


def consume_orders(ch, method, properties, body):
    # Обработчик для обработки полученных заказов
    order = body.decode('utf-8')
    process_order(order)

    # Подтверждение успешной обработки сообщения
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Указываем, что обработчик будет прослушивать очередь new_orders_queue
channel.basic_consume(queue='new_orders_queue', on_message_callback=consume_orders)

# Запуск обработчика
print("Waiting for new orders...")
channel.start_consuming()
