from decimal import Decimal

from pydantic import BaseModel
from pydantic import computed_field

# """
# Ref: https://azure.microsoft.com/en-us/pricing/details/container-apps/#pricing
# Unit: USD
# Price: per month
# Region: asia-southeast1 # tier 2
# """


class ContainerApps(BaseModel):
    # cost
    vcpu_second: Decimal = Decimal(0.000034)
    memory_second: Decimal = Decimal(0.000004)
    request_million: Decimal = Decimal(0.40)

    # user's input
    vcpu_request: Decimal = Decimal(1.0)
    memory_request: Decimal = Decimal(1.0)
    execution_time_per_request_ms: Decimal = Decimal(50)
    requests_per_month: Decimal = Decimal(10000)

    @computed_field
    @property
    def execution_time_second(self) -> Decimal:
        return (
            self.execution_time_per_request_ms * self.requests_per_month / Decimal(1000)
        )

    @computed_field
    @property
    def cost_cpu(self) -> Decimal:
        return self.vcpu_request * self.vcpu_second * self.execution_time_second

    @computed_field
    @property
    def cost_memory(self) -> Decimal:
        return self.memory_request * self.memory_second * self.execution_time_second

    @computed_field
    @property
    def cost(self) -> Decimal:
        return self.cost_cpu + self.cost_memory


if __name__ == "__main__":
    # test
    container_apps = ContainerApps(
        vcpu_request=2,
        memory_request=2,
        execution_time_per_request_ms=500,
        requests_per_month=100000000,
    )
    print(f"Container Apps: {container_apps.cost}")
