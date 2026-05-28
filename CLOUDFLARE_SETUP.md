# Configuração do Cloudflare Tunnel

## O que foi alterado?

O arquivo `app.py` foi modificado para iniciar automaticamente um **Cloudflare Tunnel** quando a aplicação é iniciada. Isso expõe sua aplicação local para a internet de forma segura.

## Pré-requisitos

### 1. Instalar Cloudflared

Cloudflared é um executable que você precisa instalar no seu sistema.

#### Windows:
```bash
# Usando Chocolatey (recomendado)
choco install cloudflare-warp

# Ou baixar manualmente de:
# https://github.com/cloudflare/cloudflared/releases
# E adicionar ao PATH do Windows
```

#### Alternativa - Usando winget:
```bash
winget install Cloudflare.Cloudflared
```

#### MacOS:
```bash
brew install cloudflare/cloudflare/cloudflared
```

#### Linux:
```bash
# Ubuntu/Debian
sudo apt-get install cloudflared

# RHEL/CentOS
sudo yum install cloudflared
```

### 2. Verificar Instalação

Abra o PowerShell/Terminal e execute:
```bash
cloudflared --version
```

Se receber um erro, o cloudflared não foi instalado corretamente.

## Como Usar

### Iniciar a Aplicação

Simplesmente execute como de costume:

```bash
python app.py
```

### O que Acontecerá

1. A aplicação Flask iniciará em `http://localhost:5000`
2. Um tunnel Cloudflare será criado automaticamente
3. Você verá uma URL pública no terminal, algo como:
   ```
   🔗 URL Pública do Tunnel: https://exemplo-aleatorio.trycloudflare.com
   ```
4. Você pode compartilhar essa URL publicamente para acessar sua aplicação de qualquer lugar

### Exemplo de Saída

```
 * Serving Flask app 'app'
 * Debug mode: on
🚀 Iniciando Cloudflare Tunnel...
✅ Cloudflare Tunnel iniciado com sucesso!
🔗 URL Pública do Tunnel: https://silver-mountain-123.trycloudflare.com
 * Running on http://localhost:5000
```

## Parar a Aplicação

Pressione `Ctrl+C` no terminal. Isso encerrará tanto o servidor Flask quanto o tunnel.

## Limitações

- A URL do tunnel **muda a cada reinicialização** da aplicação (sem autenticação)
- Para uma URL permanente, você precisa criar uma conta no Cloudflare e configurar um domínio

## Solução de Problemas

### "cloudflared not found"
- Certifique-se de que cloudflared foi instalado e está no PATH
- Reinicie seu terminal após instalar

### Tunnel não está funcionando
- Verifique sua conexão com a internet
- Tente executar `cloudflared tunnel --help` para confirmar a instalação

### Porta 5000 já está em uso
- Mude a porta em `app.py`: `app.run(port=5001, ...)`
- Ou mate o processo que está usando a porta

## Criar um Tunnel Permanente (Opcional)

Para uma URL permanente com seu próprio domínio:

1. Crie uma conta em [https://dash.cloudflare.com/](https://dash.cloudflare.com/)
2. Configure um domínio
3. Autentique com `cloudflared login`
4. Configure o tunnel permanentemente conforme a documentação do Cloudflare

## Referências

- [Cloudflare Tunnel Docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [GitHub Cloudflared](https://github.com/cloudflare/cloudflared)
