from kfp import dsl
from kfp.dsl import Input, Output, Dataset, Model

image_name="some-remote-gcr.io-image"

@dsl.component(
    base_image="python:3.11",
    target_image=image_name
)
def add(a: int, b:int) -> int:
    return a + b

@dsl.component(
        base_image="python:3.11",
        packages_to_install=["pandas"],
        target_image=image_name
)
def generate_data(length: int, output: Output[Dataset]):
    import pandas as pd
    r = range(0,length)
    data = pd.DataFrame({"a": r})
    data.write_csv(output.path)

@dsl.component(
        base_image="python:3.11",
        packages_to_install=["pandas", "numpy"],
        target_image=image_name
)
def split_dataset(dataset: Input[Dataset], train: Output[Dataset], test: Output[Dataset]) -> None:
    import pandas as pd
    data = pd.read_csv(dataset.path)
    data[:100].write_csv(train.path)
    data[100::].write_csv(test.path)

@dsl.component(
    base_image="python:3.11",
    packages_to_install=["tensorflow"],
    target_image=image_name
)
def train_model(train: Input[Dataset], model:  Output[Model]) -> None:
    import pandas as pd
    data = pd.read_csv(train.path)
    data.write(model.path)

@dsl.component(
    base_image="python:3.11",
    packages_to_install=["google-cloud-aiplatform==1.25.0"],
    target_image=image_name
)
def register_model(
    model: Input[Model],
    project_id: str
):
    from google.cloud import aiplatform

    aiplatform.init(project=project_id)

    aiplatform.Model.upload(
        display_name="demo-model",
        artifact_uri=model.uri,
        serving_container_image_uri="us-docker.pkg.dev/cloud-aiplatform/prediction/tf2-cpu.2-3:latest",
    )
