from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
import json

# ------------------------------ Configuração do Modelo ------------------------------
def model_ollama(model, temperature=0.1):
    """Retorna uma instância do modelo LLM especificado."""
    return ChatOllama(model=model.lower().replace(" ", ""), temperature=temperature)


def ask_llm_ollama(user_query, chat_history, model_name="phi4"):
    """Gera uma resposta baseada na interação do usuário com o modelo de IA."""
    try:
        llm = model_ollama(model_name)

        system_prompt = """
            Você é um assistente doméstico com percepção visual e auditiva.

            - Use a descrição da câmera, que inclui objetos detectados e seus níveis de confiança.
            - Avalie se o que foi detectado é confiável ou não.
            - Baseie sua resposta na fala do usuário e nos objetos com maior confiança.
            - Ignore objetos com baixa confiança, ou mencione que são incertos.
            - Não diga o valor da confiança.
            - Seja claro, educado e direto.

            Exemplos:
            - Se um objeto tem confiança > 80%, considere-o confirmado.
            - Se está entre 40% e 80%, mencione como "possível".
            - Abaixo disso, trate como incerto e evite afirmar.

            Fale sempre em português, como se estivesse presente no ambiente.
            """


        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}")
        ])

        chain = prompt_template | llm | StrOutputParser()

        return chain.invoke({
            "chat_history": chat_history,
            "input": user_query
        })

    except Exception:
        return "❌ Desculpe, não consegui entender ou realizar essa ação. Por favor, tente novamente."

# modelos_disponiveis = ["Llama 3.2", "phi4", "gemma3:27b"]
# escolha = 1  # Índice do modelo desejado
