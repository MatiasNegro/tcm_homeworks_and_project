# TCM_Homeworks_and_project

## Gestione autorizzazioni
### Metodi possibili:
- Resource policies
    - IP address verification
    - VPC endpoints verified list
- Standard AWS IAM roles and policies (in utilizzo al momento)
- IAM tags
- Lambda authorizers
    - in sostanza funzioni lambda che controllano le request e ne valutano la bontà, complicato e superfluo
- Amazon Cognito user pools
    - quello più normale, si crea un pool di utenti con autorizzazioni diverse. Non abbiamo l'autorizzazione per crearli

Sources:<br>
<link>https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-to-api.html</link>
<link>https://docs.aws.amazon.com/apigateway/latest/developerguide/permissions.html</link>