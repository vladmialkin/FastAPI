import json

from app.rabbitmq.connecting import channel, connection

try:
    while True:
        method_frame, properties, body = channel.basic_get(queue='new_orders_queue', auto_ack=True)

        if method_frame:
            print("Сообщение прочитано", body)
            # Добавьте вашу логику обработки сообщения здесь
            message = 'Пользватель, ваше сообщение отправлено'
            channel.basic_publish(exchange='', routing_key='sending_message_queue', body=message)
            print("Пользователь, ваше сообщение доставлено!")
        else:
            # Если очередь пуста, выход из цикла
            break
except Exception as e:
    print(e)
finally:
    # Закрытие соединения с RabbitMQ
    print("Соединение закрыто")
    connection.close()
