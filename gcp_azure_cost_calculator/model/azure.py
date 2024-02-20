from decimal import Decimal

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

    # user's input
    vcpu_request: Decimal = Decimal(1.0)
    memory_request: Decimal = Decimal(1.0)
    execution_time_per_request_ms: Decimal = Decimal(50)
    requests_per_month: Decimal = Decimal(10000)


if __name__ == "__main__":
    # test
    container_apps = ContainerApps(
        vcpu_request=2,
        memory_request=2,
        execution_time_per_request_ms=500,
        requests_per_month=100000000,
    )
    print(f"Container Apps: {container_apps.cost}")
