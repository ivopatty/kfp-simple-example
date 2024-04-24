# Compiling Components

To compile your components to a container run

```
kfp component  build training --no-push-image
```

If you want to validate the running of your pipeline, replace the image
name in the configuration with a valid Artifact Registry URL and run

```
kfp component  build training --push-image
``` 

instead.

# Run the pipeline

Running the pipeline on GCP can be done by running

```
python pipeline.py
```

This compiles the Python pipeline down to a a YAML
representation that Kubeflow understands

running `python run_pipeline.py` takes that YAML and deploys it to GCP