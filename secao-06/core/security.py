from passlib.context import CryptContext

CRIPTO: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verificar_senha(senha: str, hash_senha: str) -> bool:
   """
    Função para verificar se a senha do usuário  está correta,
     comparando a senha de um texto puro, informado pelo usuário,
     e o hash da senha que estará salvo no banco de dados
   """
   return CRIPTO.verify(secret=senha,hash=hash_senha)


def gerar_hash(senha: str) -> str:

    #Função que gera o hash
    
    return CRIPTO.hash(senha) 