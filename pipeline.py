from kfp import dsl
from kfp import compiler
from training import train
from google_cloud_pipeline_components.v1.model import ModelUploadOp
from kfp.dsl import importer_node
from google_cloud_pipeline_components.types import artifact_types

@dsl.pipeline()
def pipeline(project_id: str):
    num_lines = train.add(a=50, b=50)
    all_data = train.generate_data(length=num_lines.output)
    split = train.split_dataset(dataset=all_data.output)
    model = train.train_model(train=split.outputs['train'])
    train.register_model(model=model.output, project_id=project_id)


compiler.Compiler().compile(pipeline, package_path='component.yaml')
