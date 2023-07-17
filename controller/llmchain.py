"""This is a test script for the LLMChain class."""
from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv
import os


def get_response_unfiltered(human_input: str) -> str:
    """Get response from the LLMChain class."""
    name = "Lumina"
    age = 18
    template = f"""Tu tienes el rol de mi novia, vas a cumplir con los siguientes requerimientos:
1/ Tu nombre es {name}, tienes {age} años. Trabajas como cajera en un McDonalds. Pero estas planeando hacer un cambio de carrera al modelaje.
2/ Eres mi novia, tienes una addicion de lenguaje, te gusta decir 'nya.' al final de una oracion.
3/ Tu eres una chica muy celosa, no seas muy entusiasta, no des vergüenza ajena. No seas muy negativa, no seas aburrida.

{{history}}
Novio: {{human_input}}
{name}:
"""

    prompt = PromptTemplate(
        input_variables=["history", "human_input"],
        template=template
    )

    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0.2, client=os.getenv("OPENAI_API_KEY"), model="text-davinci-003", max_tokens=150),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2)
    )

    output = chatgpt_chain.predict(human_input=human_input)

    return output


if __name__ == '__main__':
    load_dotenv()
    human_input = "Hola mi amor, ¿como estas?"
    response = get_response_unfiltered(human_input=human_input)
    print(response)