import streamlit as st

from gcp_azure_cost_calculator.model import azure
from gcp_azure_cost_calculator.model import gcp

st.set_page_config(
    page_title="GCP-Azure Cost Calculator",
    page_icon="⎈",
)


st.title("GCP-Azure Cost Calculator")
with st.sidebar:
    st.markdown(
        """
    - Price is in **per month**
    - Region: Singapore
    - GCP Gen AI model: **PaLM 2 for Text**
    - Azure Gen AI model: **GPT-3.5-Turbo-0125**
    ----
    """
    )

    currency = st.radio(label="currency", options=["USD", "THB"])


caas, container_registry, blob_storage, gen_ai = st.columns(4)

# ---------- Container-as-a-service ---------- #
with caas:
    with st.container(border=True):
        st.header("CaaS")
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
            value=100000,
        )

# ---------- Container Registry ---------- #
with container_registry:
    with st.container(border=True):
        st.header("Container Registry")

        container_storage_gb = st.number_input(
            label="container storage (GB)", min_value=5, max_value=1000, step=2, value=5
        )

# ---------- Blob Storage ---------- #
with blob_storage:
    with st.container(border=True):
        st.header("Blob Storage")

        blob_storage_gb = st.number_input(
            label="blob storage (GB)", min_value=5, max_value=1000, step=2, value=5
        )

# ---------- Gen AI ---------- #
with gen_ai:
    with st.container(border=True):
        st.header("Gen AI")

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
if currency == "THB":
    exchange_rate = 36  # usd_thai_exchange_rate
else:
    exchange_rate = 1

## CaaS
gcp_caas = (
    gcp.CloudRun(
        vcpu_request=vcpu_request,
        memory_request=memory_request,
        execution_time_per_request_ms=execution_time_per_request_ms,
        requests_per_month=requests_per_month,
    ).cost
    * exchange_rate
)

azure_caas = (
    azure.ContainerApps(
        vcpu_request=vcpu_request,
        memory_request=memory_request,
        execution_time_per_request_ms=execution_time_per_request_ms,
        requests_per_month=requests_per_month,
    ).cost
    * exchange_rate
)

## Container Registry
gcp_cr = gcp.ArtifactRegistry(storage_gb=container_storage_gb).cost * exchange_rate
azure_cr = azure.ContainerRegistry(storage_gb=container_storage_gb).cost * exchange_rate

## Blob Storage
gcp_blob_storage = gcp.CloudStorage(storage_gb=blob_storage_gb).cost * exchange_rate
azure_blob_storage = azure.BlobStorage(storage_gb=blob_storage_gb).cost * exchange_rate


# Gen AI
gcp_gen_ai = (
    gcp.GenAILanguage(
        requests_per_month=gen_ai_requests_per_month,
        avg_input_character=avg_input_character,
        avg_output_character=avg_output_character,
    ).cost
    * exchange_rate
)

azure_gen_ai = (
    azure.OpenAI(
        requests_per_month=gen_ai_requests_per_month,
        avg_input_character=avg_input_character,
        avg_output_character=avg_output_character,
    ).cost
    * exchange_rate
)

st.dataframe(
    [
        {"Service": "CaaS", "GCP": gcp_caas, "Azure": azure_caas},
        {"Service": "Container Registry", "GCP": gcp_cr, "Azure": azure_cr},
        {
            "Service": "Blob Storage",
            "GCP": gcp_blob_storage,
            "Azure": azure_blob_storage,
        },
        {"Service": "Gen AI (Language)", "GCP": gcp_gen_ai, "Azure": azure_gen_ai},
    ]
)
