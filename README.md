# 💙 MacLoving - Backend

Backend do projeto **MacLoving**, uma plataforma pensada para casais criarem e guardarem memórias juntos através de álbuns digitais.

> 🚧 Projeto em desenvolvimento — ainda em fase inicial (MVP)

---

## ✨ Sobre o projeto

O MacLoving é um SaaS que permite que casais:

* 📸 Criem álbuns de fotos
* 💭 Guardem momentos especiais
* ❤️ Registrem memórias importantes juntos

Este repositório contém o backend da aplicação, responsável por autenticação, gerenciamento de dados e lógica de negócio.

---

## 🚀 Tecnologias utilizadas

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT (autenticação)
* Structlog (logging estruturado)

---

## 🧠 Funcionalidades atuais

* 🔐 Sistema de autenticação com JWT
* 📁 CRUD de álbuns
* 📊 Paginação com `skip` e `limit`
* 🧾 Logging estruturado com request_id
* ⚙️ Middleware personalizado

---

## 📦 Estrutura do projeto (resumida)

```
app/
├── core/        # Configurações, segurança, logging
├── models/      # Modelos do banco
├── repositories/# Acesso ao banco (camada de dados)
├── api/         # Rotas (endpoints)
```

---

## ⚠️ Status do projeto

Esse projeto ainda está no início do desenvolvimento.

## 🎯 Próximos passos

* [ ] Implementar camada de services
* [ ] Melhorar segurança (refresh token, etc.)
* [ ] Upload de imagens
* [ ] Permissões entre usuários
* [ ] Deploy em produção


## 🤝 Contribuição

O projeto ainda está em desenvolvimento pessoal, mas feedbacks são bem-vindos!

---

## 📌 Autor

Desenvolvido por Rodney-JM por enquanto 💻
(Em constante evolução 🚀)

---
