import streamlit as st

from gcp_azure_cost_calculator.model import azure
from gcp_azure_cost_calculator.model import gcp

st.set_page_config(
    page_title="GCP-Azure Cost Calculator",
    page_icon="⎈",
)


st.title("GCP-Azure Cost Calculator")

with st.sidebar:
    # ---------- Container-as-a-service ---------- #
    vcpu_request = st.number_input(
        label="cpu", min_value=1, max_value=8, step=1, value=2
    )
    memory_request = st.number_input(
        label="memory", min_value=1, max_value=8, step=1, value=2
    )
    execution_time_per_request_ms = st.number_input(
        label="execution time (ms)",
        min_value=100,
        max_value=300000,
        step=100,
        value=500,
    )
    requests_per_month = st.number_input(
        label="requests per month",
        min_value=1000,
        max_value=99999999999999,
        step=1000,
        value=100000000,
    )

# show results
gcp_caas = gcp.CloudRun(
    vcpu_request=vcpu_request,
    memory_request=memory_request,
    execution_time_per_request_ms=execution_time_per_request_ms,
    requests_per_month=requests_per_month,
).cost

azure_caas = azure.ContainerApps(
    vcpu_request=vcpu_request,
    memory_request=memory_request,
    execution_time_per_request_ms=execution_time_per_request_ms,
    requests_per_month=requests_per_month,
).cost

st.dataframe(
    [
        {"Service": "CaaS", "GCP": gcp_caas, "Azure": azure_caas},
        # {"Service": "Image Registry", "GCP": 5, "Azure": 6},
    ]
)
