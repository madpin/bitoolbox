# BIToolbox

## Problemas
Se tiver problemas instalando pacotes, por conta do pip, use:

pip install --trusted-host pypi.python.org [pacote]

Para clonar esse repositório na rede da Catho:
```
git -c http.sslVerify=false clone https://github.com/madpin/bitoolbox
python .\bitoolbox\setup.py install
pip install --trusted-host pypi.python.org -r .\bitoolbox\requirements.txt
```

Para instalar em um ambiente "normal":
```
pip install --upgrade git+https://github.com/madpin/bitoolbox
```

## Datetools

## DBtools
Necessario configurar uma variavel de ambiente "bitoolbox_ini" com o caminho para um arquivo ini de acessos a base de dados!

```
[ALIAS_DO_BANCO]
host = banco_de_dados.uol.com.br
port = 3306
username = usuario
password = senha
charset = utf8
[schema = banco_xpto]
```

[Exemplo do meu arquivo](bitoolbox.md)
## Omnitools

## POGTools
Hahaha, juntando as pogs num modulo só.

## Pd Utils
Algumas configurações do Pandas:
```
pd.set_option('display.width', 135)
pd.set_option('display.max_rows', 999)
pd.set_option('display.max_colwidth', 999)
pd.set_option('display.max_columns', 25)
pd.set_option('precision', 2)
```


## Platform Tools

## BirstTools
```
[API_Birst]
host = banco_de_dados.uol.com.br
username = usuario
password = senha
```

## Logtools
Grupo de funções para gerenciar log.
## Track Sale Tools
Grupo de funções para gerenciar o Tracksale.

## Autores

* **Thiago MadPin** - trabalho inicial


Ps: Se já tiver um git e quiser configurar o SSL:
```
git config http.sslVerify false
```