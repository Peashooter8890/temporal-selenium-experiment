import asyncio
from temporalio.client import Client
from .workflow import FlipkartWorkflow
from .config import TASK_QUEUE_NAME, WORKFLOW_ID

async def main():
    client = await Client.connect("localhost:7233", namespace="default")

    handle = await client.start_workflow(
        FlipkartWorkflow.scrape_flipkart,
        id=WORKFLOW_ID,
        task_queue=TASK_QUEUE_NAME,
    )

    result = await handle.result()
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
