#!/usr/bin/python2.7

import argparse
import requests 
import urllib3
import base64

from config import usuario_ctm as usuario
from config import senha_ctm as senha

parser = argparse.ArgumentParser(description='Parse Argument')

parser.add_argument('endpoint', type=str, help='Extensao do arquivo')
parser.add_argument('port', type=int, help='Porta da api em rest Swagger - Exemplo: 8443')
parser.add_argument('url', type=str, help='Url para a request exemplo: /session/login')
parser.add_argument('method', type=str, help='Metodo POST')
parser.add_argument('jobname', type=str, help='Colocar o jobname - Exemplo: PDDL0232')
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
        #print(r_login.content)
        #print(r_login.status_code)

        if r_login.status_code != requests.codes.ok:
            exit(1) 
        token = r_login.json()['token']

        if args.method:
            if args.method == 'GET':
                try:
                    r = requests.get(endPoint + '{url}?jobname={jobname}'.format(url=args.url, jobname=args.jobname), headers={'Authorization': 'Bearer ' + token}, verify=False)
                    print(r.content)
                    print(r.status_code)
                    exit(r.status_code == requests.codes.ok)
                    r_logout = requests.post(endPoint + '/session/logout', json={"username": user, "password": passwd}, verify=False)
                except requests.exceptions as e:
                    mensagem = 'Exception {e}'.format(e=e)
                    r = requests.get(args.url)

            if args.method == 'POST':
                try:
                    r = requests.post(endPoint + '{url}'.format(url=args.url), headers={'Authorization': 'Bearer ' + token}, verify=False)
                    print(r.content)
                    print(r.status_code)
                    exit(r.status_code == requests.codes.ok)
                    r_logout = requests.post(endPoint + '/session/logout', json={"username": user, "password": passwd}, verify=False)
                except requests.exceptions as e:
                    mensagem = 'Exception {e}'.format(e=e)
                    r = requests.get(args.url)
    
    except Exception as e:
        mensagem = 'erro'

if __name__ == '__main__':

    args= parser.parse_args()
    try:
        res = executa_job(args)
        print(res)
    except Exception as e:
        print(e)
        print('Erro no teste da url {args}'.format(args=args))