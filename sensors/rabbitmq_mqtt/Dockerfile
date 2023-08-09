FROM rabbitmq:3.12-management

RUN rabbitmq-plugins enable --offline rabbitmq_mqtt

COPY ./rabbitmq.conf /etc/rabbitmq/rabbitmq.conf
