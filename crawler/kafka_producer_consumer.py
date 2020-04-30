from confluent_kafka import Producer, Consumer, KafkaException
import logging
from crawler.protobuf_message_handler import ProtobufMessageHandler
from crawler.config_properties import ConfigProperties
import ast


class KafkaProducer:

    __protobuf_message_handler = ProtobufMessageHandler()
    __logger = logging.getLogger(__name__)
    __config_properties = ConfigProperties.get_config()

    def __init__(self):
        config_producer_string = self.__config_properties.get('kafka', 'config_producer')
        config_producer = ast.literal_eval(config_producer_string)
        self.producer = Producer(config_producer)

    def ack(self, err, msg):
        if err is not None:
            self.__logger.error("Failed to deliver message: {0}: {1}".format(msg.value(), err.str()))
        else:
            self.__logger.debug("Message produced: {0}".format(msg.value()))
            pass

    def send_message(self, topic, message, callback=None):
        try:
            self.producer.poll(0)
            message_serialize = self.__protobuf_message_handler.serialize(message)
            if callback is None:
                self.producer.produce(topic, message_serialize, callback=self.ack)
            else:
                self.producer.produce(topic, message_serialize, callback=callback)
            self.producer.flush(0.1)
        except KafkaException as e:
            raise e


class KafkaConsumer:
    __protobuf_message_handler = ProtobufMessageHandler()
    __config_properties = ConfigProperties.get_config()

    def __init__(self, group_id, topic):
        config_consumer_string = self.__config_properties.get('kafka', 'config_consumer')
        config_consumer = ast.literal_eval(config_consumer_string)
        config_consumer['group.id'] = group_id
        self.consumer = Consumer(config_consumer)
        self.consumer.subscribe(topic)

    def receive_message(self, payload, callback_error=None, callback_success=None):
        try:
            while True:
                msg = self.consumer.poll(0.0)
                if msg is None:
                    continue
                elif not msg.error():
                    logging.info('topic: {}, partition: {}, offset: {}'.format(msg.topic(), msg.partition(), msg.offset()))
                    message_deserialize = self.__protobuf_message_handler.deserialize(msg.value(), payload)
                    callback_success(message_deserialize)
                elif msg.error() is not None:
                    logging.error(msg.error().str())
                    if callback_error:
                        callback_error()
                else:
                    logging.error(msg.error().str())
                    if callback_error:
                        callback_error()
        except KafkaException as kafkaException:
            logging.error(kafkaException)
            raise kafkaException
        finally:
            self.consumer.close()
