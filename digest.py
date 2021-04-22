import boto3
import pipes
client = boto3.client("ecr")
details = client.describe_images(repositoryName='hardin-senado-votacoes', imageIds=[{'imageTag': 'latest'}])
digest = details["imageDetails"][0]["imageDigest"]
print("export DIGEST=%s" % (pipes.quote(str(digest))))