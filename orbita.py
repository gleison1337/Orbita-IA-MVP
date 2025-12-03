import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import json
import threading
import time
import requests
import google.generativeai as genai
import os

class AppAnaliseIncidentes:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Analisador de Incidentes AI (ServiceNow > Telegram)")
        self.root.geometry("600x700")
        
        # Variáveis de Configuração
        self.arquivo_path = tk.StringVar()
        self.api_key_gemini = tk.StringVar()
        self.token_telegram = tk.StringVar()
        self.chat_id_telegram = tk.StringVar()
        
        self.setup_ui()

    def setup_ui(self):
        # Frame de Configuração
        frame_config = tk.LabelFrame(self.root, text="Configurações e Chaves", padx=10, pady=10)
        frame_config.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_config, text="Gemini API Key:").grid(row=0, column=0, sticky="e")
        tk.Entry(frame_config, textvariable=self.api_key_gemini, width=40, show="*").grid(row=0, column=1, padx=5)
        
        tk.Label(frame_config, text="Telegram Token:").grid(row=1, column=0, sticky="e")
        tk.Entry(frame_config, textvariable=self.token_telegram, width=40, show="*").grid(row=1, column=1, padx=5)
        
        tk.Label(frame_config, text="Telegram Chat ID:").grid(row=2, column=0, sticky="e")
        tk.Entry(frame_config, textvariable=self.chat_id_telegram, width=40).grid(row=2, column=1, padx=5)

        # Frame de Arquivo
        frame_file = tk.LabelFrame(self.root, text="Arquivo de Dados", padx=10, pady=10)
        frame_file.pack(fill="x", padx=10, pady=5)
        
        tk.Entry(frame_file, textvariable=self.arquivo_path, width=50).pack(side="left", padx=5)
        tk.Button(frame_file, text="Selecionar incident.json", command=self.selecionar_arquivo).pack(side="left")

        # Botão de Ação
        self.btn_iniciar = tk.Button(self.root, text="🚀 INICIAR ANÁLISE COM IA", command=self.iniciar_thread, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_iniciar.pack(pady=10, fill="x", padx=20)

        # Área de Logs
        self.log_area = scrolledtext.ScrolledText(self.root, height=20, state='disabled', bg="#1e1e1e", fg="#00ff00")
        self.log_area.pack(fill="both", expand=True, padx=10, pady=5)

    def log(self, mensagem):
        """Escreve na tela preta de logs"""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, mensagem + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def selecionar_arquivo(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        self.arquivo_path.set(filename)

    def iniciar_thread(self):
        # Validação simples
        if not self.arquivo_path.get() or not self.api_key_gemini.get():
            messagebox.showwarning("Atenção", "Preencha a API Key e selecione o arquivo!")
            return
        
        # Bloqueia botão para não clicar 2x
        self.btn_iniciar.config(state="disabled", text="Processando... Aguarde...")
        
        # Inicia o processamento em segundo plano (Thread)
        threading.Thread(target=self.processar_dados).start()

    
    def carregar_regras(self):
        """Lê o arquivo de regras se ele existir"""
        nome_arquivo = "regras_empresa.txt"
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return "Nenhuma regra específica definida. Use as melhores práticas de TI padrão."

    def processar_dados(self):
        try:
            # Configura Gemini (Já atualizado para o modelo rápido que vimos)
            genai.configure(api_key=self.api_key_gemini.get())
            model = genai.GenerativeModel('gemini-2.5-flash') 
            
            # --- CARREGA AS REGRAS DA EMPRESA AQUI ---
            regras_internas = self.carregar_regras()
            self.log(f"📚 Base de Conhecimento carregada: {len(regras_internas)} caracteres.")
            
            self.log("📂 Lendo arquivo JSON...")
            
            with open(self.arquivo_path.get(), 'r', encoding='utf-8') as f:
                dados = json.load(f)
                
            lista_chamados = dados.get('records', dados) if isinstance(dados, dict) else dados
            total = len(lista_chamados)
            
            self.log(f"✅ Arquivo carregado! {total} chamados encontrados.")
            self.log("--------------------------------------------------")

            for i, ticket in enumerate(lista_chamados):
                numero = ticket.get('number', 'S/N')
                descricao = ticket.get('description', '')
                resumo = ticket.get('short_description', '')
                usuario = ticket.get('caller_id', 'Usuario')
                
                texto_limpo = f"Título: {resumo}\nDescrição: {descricao}".replace('\n', ' ')[:2000]
                
                self.log(f"🤖 [{i+1}/{total}] Analisando {numero} com base nas Regras...")
                
                # --- PROMPT ATUALIZADO COM REGRAS ---
                prompt = f"""
                Você é um Analista de Suporte Nível 2 Sênior, que está instruindo Analistas de Suporte que prestam suporte N1.
                Você os ensina, explica procedimentos do N1 e necessidades de escalonamento.

                ⚠️ IMPORTANTE - SIGA ESTAS REGRAS INTERNAS DA EMPRESA:
                {regras_internas}
                ---------------------------------------------------
                
                Analise o chamado abaixo aplicando as regras acima (se aplicável):
                
                DADOS DO CHAMADO:
                ID: {numero}
                Relato do Usuário: {texto_limpo}

                RESPOSTA (Formato Telegram):
                🎫 *Chamado:* {numero}
                👤 *Usuário:* {usuario}
                🌡️ *Humor:* (Analise brevemente)

                🔥 *Prioridade Real:* (Baixa/Média/Alta - justifique)

                📑 *Título do chamado:* (Faça um resumo do tema do chamado)

                🧠 *Diagnóstico:* (Qual regra foi aplicada ou qual o problema técnico?)

                🛠️ *Ação Sugerida:* (Passo a passo técnico baseado nas regras)
                """
                
                try:
                    response = model.generate_content(prompt)
                    texto_resposta = response.text
                    
                    self.enviar_telegram(texto_resposta)
                    self.log(f"📨 Relatório de {numero} enviado!")
                    
                except Exception as e:
                    self.log(f"❌ Erro na IA/Telegram para {numero}: {e}")

                time.sleep(3) 
            
            self.log("🏁 Processamento finalizado!")
            messagebox.showinfo("Sucesso", "Análise Concluída!")

        except Exception as e:
            self.log(f"❌ Erro Crítico: {str(e)}")
            self.btn_iniciar.config(state="normal", text="🚀 INICIAR ANÁLISE")

    def enviar_telegram(self, mensagem):
        token = self.token_telegram.get()
        chat_id = self.chat_id_telegram.get()
        
        if not token or not chat_id:
            return

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": chat_id, 
            "text": mensagem, 
            "parse_mode": "Markdown" # Permite negrito
        }
        requests.post(url, data=data)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppAnaliseIncidentes(root)
    root.mainloop()