# 📝 Analisador de Sentimentos com Flask + Hugging Face

Este projeto é uma aplicação web simples para **análise de sentimentos em textos**.  
Ele utiliza o modelo [`nlptown/bert-base-multilingual-uncased-sentiment`](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment) da Hugging Face para classificar mensagens como:

- 😊 **Positivas**
- 😐 **Neutras**
- 😠 **Negativas**

A interface foi feita em **Flask + HTML/CSS**, com histórico de análises e opção de exportar relatórios em **CSV e PDF**.

---

## 🚀 Funcionalidades
- Inserir texto e obter análise de sentimento.
- Classificação em **positivo, neutro ou negativo**.
- Percentual de confiança da predição.
- Histórico das últimas análises.
- Exportar resultados para **CSV** ou **PDF**.
- Botão para **encerrar o servidor**.

---

## 🛠️ Tecnologias
- [Python 3.10+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Transformers (Hugging Face)](https://huggingface.co/transformers/)
- [ReportLab](https://www.reportlab.com/) (geração de PDF)
- HTML + CSS (frontend simples)

---

## 📦 Como rodar o projeto

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/analise-sentimentos-flask.git
cd analise-sentimentos-flask
