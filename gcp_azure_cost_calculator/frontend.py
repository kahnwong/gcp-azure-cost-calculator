import streamlit as st

from gcp_azure_cost_calculator.model import azure
from gcp_azure_cost_calculator.model import gcp

st.set_page_config(
    page_title="GCP-Azure Cost Calculator",
    page_icon="⎈",
)


st.title("GCP-Azure Cost Calculator")
st.markdown(
    """
- Price is in USD
- GCP Gen AI model: PaLM 2 for Text
- Azure Gen AI model: GPT-3.5-Turbo-0125
"""
)

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

    # ---------- Container Registry ---------- #
    storage_gb = st.number_input(
        label="container storage (GB)", min_value=5, max_value=1000, step=2, value=5
    )

    # ---------- Gen AI ---------- #
    gen_ai_requests_per_month = st.number_input(
        label="Gen AI requests per month",
        min_value=1000,
        max_value=99999999999999,
        step=1000,
        value=20000,
    )

    avg_input_character = st.number_input(
        label="average input character",
        min_value=100,
        max_value=99999999999999,
        step=200,
        value=1000,
    )

    avg_output_character = st.number_input(
        label="average output character",
        min_value=100,
        max_value=99999999999999,
        step=200,
        value=2000,
    )

# show results

## CaaS
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

## Container Registry
gcp_cr = gcp.ArtifactRegistry(storage_gb=5).cost
azure_cr = azure.ContainerRegistry(storage_gb=5).cost

# Gen AI
gcp_gen_ai = gcp.GenAILanguage(
    requests_per_month=gen_ai_requests_per_month,
    avg_input_character=avg_input_character,
    avg_output_character=avg_output_character,
).cost

azure_gen_ai = azure.OpenAI(
    requests_per_month=gen_ai_requests_per_month,
    avg_input_character=avg_input_character,
    avg_output_character=avg_output_character,
).cost

st.dataframe(
    [
        {"Service": "CaaS", "GCP": gcp_caas, "Azure": azure_caas},
        {"Service": "Container Registry", "GCP": gcp_cr, "Azure": azure_cr},
        {"Service": "Gen AI (Language)", "GCP": gcp_gen_ai, "Azure": azure_gen_ai},
    ]
)
