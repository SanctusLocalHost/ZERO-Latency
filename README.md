# ZERO:LATENCY - LInux CApsLOck DElay FIx

Uma ferramenta de interface CLI (Command Line Interface) focada em corrigir permanentemente o Bug de atraso (delay) da tecla CapsLock em distribuições Linux rodando Wayland ou X11. `"EFeito BUg NO CAps LOck"`. 

---

### 📸 Screenshots

<img width="876" height="660" alt="image" src="https://github.com/user-attachments/assets/9f10d54e-930f-4de9-878d-ed439c55eb1e" />

<img width="876" height="660" alt="image" src="https://github.com/user-attachments/assets/1e3a7c8d-7802-498d-a07a-de78629a8def" />

<img width="876" height="660" alt="image" src="https://github.com/user-attachments/assets/b25b8560-5d9c-441e-924f-9c0242f597e9" />


---

### ⚙️ Como Funciona?

1. **Verificação Segura:** Faz a leitura do arquivo protegido do sistema `/usr/share/X11/xkb/symbols/capslock`.
2. **Backup Automático:** Salva a configuração original antes de qualquer modificação.
3. **Injeção de Patch:** Utiliza expressões regulares (Regex) para localizar o bloco `ctrl_modifier` e injeta a rotina correta (`type="ALPHABETIC"`, `repeat=No`, etc.) que anula a latência.

---

### 🛠️ Como Usar

**1. Baixe e execute (2 Cliques):**
- Faça o download do arquivo `ZeroLatency.py` aqui do repositório.
- Clique com o botão direito no arquivo > **Propriedades** > aba **Permissões** > Marque a opção **"Permitir execução do arquivo como um programa"**.
- Dê **2 cliques** no arquivo (se o sistema perguntar, escolha *"Executar no Terminal"*).

> *(Alternativamente, via terminal, basta abrir a pasta onde baixou e rodar: `python3 ZeroLatency.py`)*

**2. Após a correção aplicada pelo script:**
Para garantir que o Sistema Operacional assuma o Patch perfeitamente:
- Abra o seu utilitário de sistema (Ex: **Gnome Tweaks**).
- Vá em **Keyboard & Mouse** > **Additional Layout Options** > **Caps Lock behavior**.
- Ative a opção: **"Make Caps Lock an additional Ctrl"**.
