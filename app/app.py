import boto3
import json
from CloudAtlas.DadosAbertos import SenadoFederal
from CloudAtlas.Utils import yesterday


def salvar_votacoes(votacoes, tipo="local", **kwargs):
    for votacao in votacoes:
        materia = votacao.get("CodigoMateria")
        if tipo == "local":
            with open(f"{materia}.json", "w") as f:
                json.dump(votacao, f)  
        if tipo == "s3":
            bucket = kwargs.get("bucket")
            prefix = kwargs.get("prefix")
            key = f"{prefix}/{materia}.json"
            s3 = boto3.resource('s3')
            s3.Object(bucket, key).put(Body=json.dumps(votacao).encode("utf-8"))

def handler(event, context):

    data, meta = yesterday(days=1)
    senado = SenadoFederal()
    content, response = senado.listar_votacoes(data=data.strftime("%Y%m%d"))
    votacoes = content.get("ListaVotacoes", {}).get("Votacoes", {}).get("Votacao")

    bucket = "cloudatlas-datalake"
    prefix = f"raw/senado/votacoes/{meta['ano']}/{meta['mes']}/{meta['dia']}"
    if votacoes is not None:
        salvar_votacoes(votacoes, tipo="s3", bucket=bucket, prefix=prefix)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
