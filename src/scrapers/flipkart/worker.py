import asyncio
import logging
import concurrent.futures
from temporalio.client import Client
from temporalio.worker import Worker
from .workflow import FlipkartWorkflow
from .activities import FlipkartActivities
from .shared import TASK_QUEUE_NAME

async def main():
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect("localhost:7233", namespace="default")

    activities = FlipkartActivities()
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker = Worker(
            client,
            task_queue=TASK_QUEUE_NAME,
            workflows=[FlipkartWorkflow],
            activities=[activities.fetch_data_from_flipkart],
            activity_executor=activity_executor,
        )
        logging.info(f"Starting the worker....{client.identity}")
        await worker.run()

if __name__ == "__main__":
    asyncio.run(main())