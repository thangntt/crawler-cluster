import zlib
import logging


class ProtobufMessageHandler:

    @staticmethod
    def serialize(protobuf_message):
        return zlib.compress(protobuf_message.SerializeToString(), -1)

    @staticmethod
    def deserialize(protobuf_message, payload):
        return payload.FromString(zlib.decompress(protobuf_message))
