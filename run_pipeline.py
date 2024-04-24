import google.cloud.aiplatform as aip

job = aip.PipelineJob(
    display_name="model-test",
    template_path="component.yaml",
    location="europe-west1"
)

job.run(service_account="PROJECTCODE-compute@developer.gserviceaccount.com")