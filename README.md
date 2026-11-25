# Beza — assistente de IA do Grupo Gade

O **Beza** é um plugin do Claude Code que ajuda colaboradores do Grupo Gade no dia a dia: **consulta o Painel de Resultados** (somente leitura, só o que o administrador liberar para a pessoa), **confere planilhas**, cria **dashboards**, **atas**, **procedimentos** e **checklists**, sempre com a regra **"sem conferência, sem entrega"**.

Este repositório é público de propósito (instalar não exige login no GitHub) e **não contém nenhuma senha, dado de cliente ou número do Painel**. Cada pessoa usa uma **senha própria do Beza**, entregue pelo administrador do Painel, que só abre o que ele liberou.

## Instalar (uma vez)
Pré-requisitos: Claude Code instalado e logado, **Python 3.8+** e **Git for Windows** (no Windows).

Cole **uma linha** no terminal:

```
claude plugin marketplace add GrupoGade-Dev/beza-adm && claude plugin install beza-adm@beza-adm
```

O Claude Code abre uma caixinha pedindo a **senha do Beza** (aparece mascarada). Cole a senha que o administrador entregou. Feche e abra o Claude Code: pronto.

- Senha errada ou trocada: `/plugin configure beza-adm@beza-adm` e cole a nova.
- Atualizar o Beza: `claude plugin marketplace update beza-adm && claude plugin update beza-adm@beza-adm`.
- Teste: *"Beza, o que você consegue buscar no Painel?"*

## Usar
Exemplos de pedidos:
- "Beza, como foi o caixa da Inside em outubro?"
- "Quantos clientes ativos a Inside tem, por carteira?"
- "Confira esta planilha de fechamento." (anexe o arquivo)
- "Faça um dashboard com esta planilha."
- "Aqui está a transcrição da reunião de hoje, faça a ata."
- "Monte o procedimento de admissão de colaborador, com checklist."

Arquivos gerados ficam em `Documentos/Beza Adm/`.

## Como o acesso ao Painel funciona (para o administrador)
- No Painel, tela **Acessos do Beza** (só administrador): cria o acesso da pessoa, marca o que ela pode buscar, troca a senha, desativa ou revoga. **Mudou lá, vale na próxima consulta**, sem reinstalar nada.
- O plugin só conhece a API somente leitura do Painel (`/api/beza/v1`). A permissão de cada informação é conferida **no servidor** a cada consulta; o Beza não tem como se dar acesso.
- A senha fica na caixinha do plugin (guardada pelo Claude Code, fora da conversa e de arquivos do projeto) e chega à ponte `scripts/painel_mcp.py` por variável de ambiente.

## Requisitos
- Python 3.8+ (a ponte do Painel usa só a biblioteca padrão; as skills de planilha pedem autorização para instalar `openpyxl` se faltar).
- Chrome ou Edge (para gerar PDF).
- Só para gravações de áudio/vídeo: `ffmpeg` e `openai-whisper`.

## Segurança
- Não envia e-mail nem acessa servidor, banco ou ERP. A única saída para a rede é a consulta somente leitura ao Painel, limitada pelo que o Painel liberar.
- Um hook bloqueia `ssh`, `sudo`, `docker`, `git push`, `rm -rf`, `curl | sh`, arquivos `.env`/chaves e a variável da senha. É uma barreira de processo; **a proteção real é o Painel** (senha por pessoa, permissão conferida no servidor, histórico de consultas).
- O original de qualquer planilha nunca é alterado: o Beza entrega uma cópia conferida.

## Manutenção
Ao mudar algo: subir `version` em `.claude-plugin/plugin.json`, `claude plugin validate . --strict`, `python3 -m unittest discover -s tests`, commit e push. Quem usa roda o comando de atualização acima.
Conteúdo da empresa: `contexto/empresa.md`. Logos em `assets/logos/`.
