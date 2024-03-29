from decimal import Decimal

from pydantic import BaseModel
from pydantic import computed_field

# """
# Price: USD
# Region: asia-southeast1
# """


class CloudRun(BaseModel):
    """
    https://cloud.google.com/run/pricing
    Tier 2
    """

    # cost
    vcpu_second: Decimal = Decimal(0.00003360)
    memory_second: Decimal = Decimal(0.00000350)
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
    def cost(self) -> float:
        return round(float(self.cost_cpu + self.cost_memory), 2)


class ArtifactRegistry(BaseModel):
    """
    https://cloud.google.com/artifact-registry/pricing
    """

    # cost
    storage_per_gb_month: Decimal = Decimal(0.10)

    # user's input
    storage_gb: Decimal = Decimal(1)

    @computed_field
    @property
    def cost(self) -> float:
        return round(float(self.storage_per_gb_month * self.storage_gb), 2)


class CloudStorage(BaseModel):
    """
    https://cloud.google.com/storage/pricing
    Standard
    """

    # cost
    storage_per_gb_month: Decimal = Decimal(0.020)

    # user's input
    storage_gb: Decimal = Decimal(1)

    @computed_field
    @property
    def cost(self) -> float:
        return round(float(self.storage_per_gb_month * self.storage_gb), 2)


class GenAILanguage(BaseModel):
    """
    https://cloud.google.com/vertex-ai/docs/generative-ai/pricing
    PaLM 2 for Text
    """

    # cost
    input_per_thousand_character: Decimal = Decimal(0.00025)
    output_per_thousand_character: Decimal = Decimal(0.0005)

    # user's input
    requests_per_month: Decimal = Decimal(20000)
    avg_input_character: Decimal = Decimal(1000)
    avg_output_character: Decimal = Decimal(2000)

    @computed_field
    @property
    def cost_per_request(self) -> Decimal:
        return (
            self.input_per_thousand_character * self.avg_input_character / Decimal(1000)
        ) + (
            self.output_per_thousand_character
            * self.avg_output_character
            / Decimal(1000)
        )

    @computed_field
    @property
    def cost(self) -> float:
        return round(float(self.cost_per_request * self.requests_per_month), 2)


if __name__ == "__main__":
    # test
    cloud_run = CloudRun(
        vcpu_request=2,
        memory_request=2,
        execution_time_per_request_ms=500,
        requests_per_month=100000000,
    )
    print(f"Cloud Run: {cloud_run.cost}")
