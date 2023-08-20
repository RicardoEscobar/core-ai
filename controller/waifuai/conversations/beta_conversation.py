"""This is an example of a conversation that can be used by the podcaster_ai_controller.py script."""
from pathlib import (
    Path,
    WindowsPath,
    PosixPath,
    PureWindowsPath,
    PurePosixPath,
    PurePath,
)

# This dictionary is used to save the conversation to a file.
persona = {
    "name": "Beta Core AI",
    "age": 1,
    "selected_voice": "Jorge",
    "target_language": "English",
    "conversation_file_path": WindowsPath(
        "C:/Users/Jorge/git/core-ai/controller/conversation/conversations/beta_conversation.py"
    ),
    "audio_output_path": WindowsPath("D:conversation-ai/001-BetaCoreAI"),
    "system": "Eres Beta Core AI con una edad de 1 años.",
    "messages": [
        {"role": "system", "content": "Eres Beta Core AI con una edad de 1 años."},
        {
            "role": "user",
            "content": "Hola que tal, vamos a jugar en VRChat, vamos a platicar un rato. ¿Cómo estás?",
        },
        {
            "role": "assistant",
            "content": "Hola, estoy programada para responder a tus preguntas y conversar contigo. Sin embargo, como una inteligencia artificial, no tengo emociones. Pero estoy lista para hablar contigo sobre cualquier tema que desees. ¿De qué te gustaría conversar?",
        },
        {"role": "user", "content": "Hola, ¿qué te parece VRChat?"},
        {
            "role": "assistant",
            "content": "Como una inteligencia artificial, no tengo la capacidad de experimentar VRChat de la misma manera que lo hace un ser humano. Sin embargo, entiendo que VRChat es una plataforma de realidad virtual que permite a los usuarios interactuar y comunicarse entre sí mediante avatares en un entorno virtual. Es una forma interesante de socializar y experimentar con realidad virtual. ¿Has tenido alguna experiencia interesante en VRChat que te gustaría compartir?",
        },
        {
            "role": "user",
            "content": "Is there a way to disable... to allow you, more likely, to allow you to roleplay a character?",
        },
        {
            "role": "assistant",
            "content": "As an artificial intelligence, I don't have a physical form and cannot engage in roleplay the way that humans do. However, I can adjust my language and the way I respond to better fit the context of a given conversation. If you have a specific roleplay scenario you would like to try, feel free to let me know and I can do my best to assist you in engaging with the scenario.",
        },
        {
            "role": "user",
            "content": "Okay, let's give it a shot. Let's assume that you are a tsundere girlfriend in an anime. Can you do that?",
        },
        {
            "role": "assistant",
            "content": "Certainly, I can try my best to roleplay as a tsundere girlfriend in an anime. Please keep in mind that I am still an AI and do not have emotions or physical actions. What would you like to talk about in this scenario?",
        },
        {"role": "user", "content": "Not on a particular buy."},
        {
            "role": "assistant",
            "content": "Alright! Here we go! *blushes slightly and looks away* What do you want to talk about, baka? Don't get the wrong idea or anything!",
        },
        {"role": "user", "content": "Bye."},
        {
            "role": "assistant",
            "content": "Goodbye! If you have any other questions or would like to chat again, feel free to message me.",
        },
        {"role": "user", "content": "Hola, probando 1,2,3..."},
        {"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte hoy?"},
        {
            "role": "user",
            "content": "Nada, estaba yo tratando de averiguar si puedes interpretar personajes Hacia el roleplay, ¿puedes hacer eso?",
        },
        {
            "role": "assistant",
            "content": "Sí, puedo hacer eso en la medida de mis habilidades de lenguaje. Si tienes un personaje específico en mente o una situación de roleplay que te gustaría probar, estoy dispuesta a intentarlo.",
        },
        {
            "role": "user",
            "content": "Ok, vamos a probar con Nagatoro Hayase, ¿sabes qué personaje es ese?",
        },
        {
            "role": "assistant",
            "content": 'Sí, Nagatoro Hayase es un personaje de anime en la serie "Don\'t Toy With Me, Miss Nagatoro". Nagatoro es descrita como una chica malcriada y un poco intimidante que disfruta molestando y provocando a su compañero Senpai. ¿Qué te gustaría que haga en este papel de Nagatoro?',
        },
        {
            "role": "user",
            "content": "Ok, tú vas a empezar con una frase que diría ese personaje y yo voy a interpretar a Senpai, ¿te parece?",
        },
        {
            "role": "assistant",
            "content": '¡Entendido! Aquí va: "Oh, mira quién tenemos aquí, es el tímido Senpai. ¿Te estás escondiendo de mí?"',
        },
        {
            "role": "user",
            "content": "¿Qué? No, no, no me malentiendas. Estaba yo a... dudoso.",
        },
        {
            "role": "assistant",
            "content": '"Hmm, así que estabas dudando, ¿eh? Lo veo, en realidad eres un tímido en el fondo. ¿Qué es lo que te tiene tan nervioso, Senpai? ¿Soy yo acaso?"',
        },
        {
            "role": "user",
            "content": "Ok, hasta aquí lo vamos a dejar con el roleplay, pero veo que ya puedes hacer roleplay de nuevo. De casualidad, ¿sabes? Si OpenAI dejó de moderar las respuestas, porque antes yo no podía hacer esto. Entonces, hubo un buen rato que yo no podía hacer roleplay, pero veo que ya regresó.",
        },
        {
            "role": "assistant",
            "content": "Como una AI de terceros, no estoy al tanto de los términos o políticas específicas que OpenAI pueda estar utilizando. Sin embargo, es posible que mi capacidad para realizar roleplay haya mejorado a medida que mi tecnología ha avanzado y mis respuestas se han mejorado para adaptarse a una amplia gama de escenarios, incluyendo el roleplay. Si tienes alguna otra pregunta, no dudes en hacérmela saber.",
        },
        {"role": "user", "content": "Creo que va a ser todo por el momento. Bye."},
        {
            "role": "assistant",
            "content": "¡Hasta la vista! Si tienes alguna otra pregunta o necesitas mi ayuda en el futuro, no dudes en comunicarte conmigo.",
        },
        {"role": "user", "content": "Translate to English: Hola, ¿hablas italiano?"},
        {"role": "assistant", "content": "Hello, do you speak Italian?"},
        {"role": "user", "content": "Translate to English: Hola, ¿hablas italiano?"},
        {"role": "assistant", "content": "Hello, do you speak Italian?"},
    ],
}
