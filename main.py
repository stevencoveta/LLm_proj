import json
import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri

try:
	role = sagemaker.get_execution_role()
except ValueError:
	iam = boto3.client('iam')
	#role = iam.get_role(RoleName='sagemaker_execution_role')['Role']['Arn']
	role = 'arn:aws:iam::244485512626:role/sagemaker_execution_role'


# Hub Model configuration. https://huggingface.co/models
hub = {
	'HF_MODEL_ID':'tiiuae/falcon-40b-instruct',
	'SM_NUM_GPUS': json.dumps(8)
}



# create Hugging Face Model Class
huggingface_model = HuggingFaceModel(
	image_uri=get_huggingface_llm_image_uri("huggingface",version="1.4.2"),
	env=hub,
	role=role, 
)

# deploy model to SageMaker Inference
predictor = huggingface_model.deploy(
	initial_instance_count=1,
	instance_type="ml.p4d.24xlarge",
	container_startup_health_check_timeout=2100,
  )
  
# send request
predictor.predict({
	"inputs": "My name is Julien and I like to",
})