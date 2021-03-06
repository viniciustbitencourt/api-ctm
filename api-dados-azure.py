#!/usr/bin/python3.9

import argparse
import requests
import urllib3
import base64
import json

usuario = 'svc_apidados'
senha = base64.b64decode(b'VmlhdmFyZWpvQDg1NDA=').decode('utf-8')

parser = argparse.ArgumentParser(description='Parse Argument')
parser.add_argument('endpoint', type=str, help='Extensao do arquivo')
parser.add_argument('port', type=int, help='Porta da api em rest Swagger - Exemplo: 8443')
parser.add_argument('url', type=str, help='Url para a request exemplo: /session/login ou /run/jobs/status')
parser.add_argument('method', type=str, help='Metodo GET ou POST')
parser.add_argument('jobname', type=str, help='Colocar o jobname - Exemplo: PDDL0232&application=S6 ou colocar PDDL0*(busca todos os jobs)')
#parser.add_argument('application', type=str, default=None, help='Para pesquisar um status do job, Exemplo EndedOK or EndedNotOK')
#parser.add_argument('status', type=str, default=None, help='Para pesquisar um status do job, Exemplo EndedOK or EndedNotOK')

args = parser.parse_args()

urllib3.disable_warnings()

#login basic teste
#----

def executa_job(args):
    
    endPoint = 'https://{endpoint}:{port}/automation-api'.format(endpoint=args.endpoint, port=args.port)
    user = '{usuario}'.format(usuario=usuario)
    passwd = '{senha}'.format(senha=senha)
    mensagem = ''

    try:
        r_login = requests.post(endPoint + '/session/login', json={"username": user, "password": passwd}, verify=False)
        print(r_login.content) #exibe o conteudo do token
        print(r_login.status_code) #retorna o exit code da requisicao

        if r_login.status_code != requests.codes.ok:
            print('Denied user, has no privilege to use Control-M API')
            exit(1) #testa se o usuario é validado para fazer a requisao via api
        token = r_login.json()['token']

        if args.method:
            if args.method == 'GET':
                try:
                    r = requests.get(endPoint + '{url}?jobname={jobname}'.format(url=args.url, jobname=args.jobname), headers={'Authorization': 'Bearer ' + token}, verify=False)
                    #carrega o valor do objeto jobId em JSON
                    data = json.loads(r.content)
                    jobid = data['statuses'][0]
                    jobid = jobid['jobId']
                    #POST request - alterar runNow ou rerun
                    rqpost = requests.post(endPoint + '/run/job/{jobid}/confirm'.format(jobid=jobid), headers={'Authorization': 'Bearer ' + token}, verify=False)
                    print(rqpost.content)
                    print(rqpost.status_code) #pode comentar essa linha para não sair com o return code
                    exit(rqpost.status_code == requests.codes.ok)

                    r_logout = requests.post(endPoint + '/session/logout', json={"username": user, "password": passwd}, verify=False)
                    print(r_logout)
                except requests.exceptions as e:
                    mensagem = 'Exception {e}'.format(e=e)
                    r = requests.get(args.url)
    
    except Exception as e:
        mensagem = 'erro'

if __name__ == '__main__':

    args= parser.parse_args()
    try:
        res = executa_job(args)
    except Exception as e:
        print(e)
        print('Erro no teste da url {args}'.format(args=args))