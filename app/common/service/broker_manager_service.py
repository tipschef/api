import os
from dataclasses import dataclass, field

from google.cloud import pubsub_v1


@dataclass
class BrokerManagerService:
    env: str
    topic_name: str = field(init=False)
    publisher_client: pubsub_v1.PublisherClient = field(init=False)

    def __post_init__(self) -> None:
        self.publisher_client = pubsub_v1.PublisherClient()
        self.topic_name = 'projects/{project_id}/topics/{topic}'.format(
            project_id=os.getenv('PROJECT_ID'),
            topic=f'topic-queue-{self.env}-gcf-generate-book',
        )

    def publish(self, message: str):
        future = (self.publisher_client.publish(self.topic_name, message.encode('utf-8')))
        future.result()


def get_broker_manager_service() -> BrokerManagerService:
    return BrokerManagerService(os.getenv('PROJECT_ENV'))
