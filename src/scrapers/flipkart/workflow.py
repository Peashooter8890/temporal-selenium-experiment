from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from .activities import FlipkartActivities
    from .config import SEARCH_INSTRUCTIONS
    
@workflow.defn
class FlipkartWorkflow:
    @workflow.run
    async def scrape_flipkart(self) -> str:
        workflow.logger.info('scrape_flipkart workflow invoked.')
        for instruction in SEARCH_INSTRUCTIONS:
            try:
                await workflow.execute_activity_method(
                    FlipkartActivities.fetch_data_from_flipkart,
                    instruction,
                    start_to_close_timeout=timedelta(seconds=45),
                    retry_policy=RetryPolicy(
                        backoff_coefficient=2.0,
                        maximum_attempts=3,
                        initial_interval=timedelta(seconds=1)
                    ),
                )
            except Exception as e:
                workflow.logger.error(f"Error executing fetch_data_from_flipkart activity: {e}")
                raise
            try:
                await workflow.execute_activity_method(
                    FlipkartActivities.submit_data_to_database,
                    instruction,
                    start_to_close_timeout=timedelta(seconds=45),
                    retry_policy=RetryPolicy(
                        backoff_coefficient=2.0,
                        maximum_attempts=3,
                        initial_interval=timedelta(seconds=1)
                    ),
                )
            except Exception as e:
                workflow.logger.error(f"Error executing submit_data_to_database activity: {e}")
                raise
        return 'Flipkart scraping completed.'