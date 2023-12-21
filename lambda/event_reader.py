from abc import ABC, abstractmethod


class Reader(ABC):
    @abstractmethod
    def __init__(self, event):
        pass

    @abstractmethod
    def get_object(self, key=str):
        pass


class EventReader(Reader):
    def __init__(self, event):
        self.event = event

    def get_object(self, key=str):
        bucket = self.event["bucket"]
        bucket_object = bucket[key]
        return {"bucket_name": bucket, "bucket_object": bucket_object}





