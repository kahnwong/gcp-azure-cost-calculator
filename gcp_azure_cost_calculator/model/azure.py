from decimal import Decimal

from gcp_azure_cost_calculator.model.gcp import ArtifactRegistry
from gcp_azure_cost_calculator.model.gcp import CloudRun

# """
# Ref: https://azure.microsoft.com/en-us/pricing/details/container-apps/#pricing
# Unit: USD
# Region: Southeast Asia
# """


class ContainerApps(CloudRun):
    # cost
    vcpu_second: Decimal = Decimal(0.000034)
    memory_second: Decimal = Decimal(0.000004)
    request_million: Decimal = Decimal(0.40)


class ContainerRegistry(ArtifactRegistry):
    # cost
    storage_per_gb_month: Decimal = Decimal(0.667)


if __name__ == "__main__":
    # test
    container_apps = ContainerApps(
        vcpu_request=2,
        memory_request=2,
        execution_time_per_request_ms=500,
        requests_per_month=100000000,
    )
    print(f"Container Apps: {container_apps.cost}")
