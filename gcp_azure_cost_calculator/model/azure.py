from decimal import Decimal

from gcp_azure_cost_calculator.model.gcp import ArtifactRegistry
from gcp_azure_cost_calculator.model.gcp import CloudRun
from gcp_azure_cost_calculator.model.gcp import CloudStorage
from gcp_azure_cost_calculator.model.gcp import GenAILanguage

# """
# Price: USD
# Region: Southeast Asia
# """


class ContainerApps(CloudRun):
    """
    https://azure.microsoft.com/en-us/pricing/details/container-apps/#pricing
    """

    # cost
    vcpu_second: Decimal = Decimal(0.000034)
    memory_second: Decimal = Decimal(0.000004)
    request_million: Decimal = Decimal(0.40)


class ContainerRegistry(ArtifactRegistry):
    """
    https://azure.microsoft.com/en-us/pricing/details/container-registry/#pricing
    """

    # cost
    storage_per_gb_month: Decimal = Decimal(0.667)


class BlobStorage(CloudStorage):
    """
    https://azure.microsoft.com/en-us/pricing/details/storage/blobs/#pricing
    Standard
    """

    # cost
    storage_per_gb_month: Decimal = Decimal(0.02)


class OpenAI(GenAILanguage):
    """
    https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/#pricing
    GPT-3.5-Turbo-0125
    """

    # cost
    input_per_thousand_character: Decimal = Decimal(0.0005)
    output_per_thousand_character: Decimal = Decimal(0.0015)


if __name__ == "__main__":
    # test
    container_apps = ContainerApps(
        vcpu_request=2,
        memory_request=2,
        execution_time_per_request_ms=500,
        requests_per_month=100000000,
    )
    print(f"Container Apps: {container_apps.cost}")
