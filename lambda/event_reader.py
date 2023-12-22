from abc import ABC, abstractmethod


class IEventReader(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_object(self, event, key=str):
        pass


class EventReader(IEventReader):
    def __init__(self):

    def get_object(self, event, key=str):
        bucket = event["bucket"]
        bucket_object = bucket[key]
        return {"bucket_name": bucket, "bucket_object": bucket_object}





