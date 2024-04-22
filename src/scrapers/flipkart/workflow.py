from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from .activities import FlipkartActivities
    
@workflow.defn
class FlipkartWorkflow:
    @workflow.run
    async def scrape_flipkart(self) -> str:
        workflow.logger.info(f"scrape_flipkart workflow invoked.")
        product_data = {
            "name": "gionee", 
            "type": "smartphones"
        }
        try:
            await workflow.execute_activity_method(
                FlipkartActivities.fetch_data_from_flipkart,
                product_data,
                start_to_close_timeout=timedelta(seconds=45),
                retry_policy=RetryPolicy(
                    backoff_coefficient=2.0,
                    maximum_attempts=3,
                    initial_interval=timedelta(seconds=1)
                ),
            )
        except Exception as e:
            workflow.logger.error(f"Error executing fetch_from_flipkart_and_plot_data activity: {e}")
            return 'Flipkart scraping failed.'
        return "Flipkart scraping completed."