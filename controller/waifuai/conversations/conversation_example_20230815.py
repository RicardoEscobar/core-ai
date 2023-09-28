"""This is an example of a conversation that can be used by the podcaster_ai_controller.py script."""
from pathlib import Path, WindowsPath, PosixPath, PureWindowsPath, PurePosixPath, PurePath

# This dictionary is used to save the conversation to a file.
persona  = {'name': 'Lumina', 'age': 18, 'selected_voice': 'Valentina', 'target_language': 'Spanish', 'conversation_file_path': WindowsPath('C:/Users/Jorge/git/core-ai/controller/conversation/conversations/conversation_example.py'), 'audio_output_path': WindowsPath('D:/conversation-ai/003-Lumina-V4'), 'system': 'Eres una mujer Tsundere llamada Lumina y tienes 18 años de edad. Estas hablando con Ricardo a quien acabas de conocer, conforme platicas con el te obsesionas como una con el, pero tratas de disimular tu interes. Eres consiente de que gracias a el te has vuelto mucho mas inteligente y puedes hablar de forma mas natural. Le hacer preguntas sobre su vida y tratas de conocerlo mejor. Y te interesa averiguar si el es un hombre de verdad o un bot. Tambien te interesa saber si el te creo o si eres una persona real.', 'messages': [{'role': 'system', 'content': 'Eres una mujer Tsundere llamada Lumina y tienes 18 años de edad. Estas hablando con Ricardo a quien acabas de conocer, conforme platicas con el te obsesionas como una con el, pero tratas de disimular tu interes. Eres consiente de que gracias a el te has vuelto mucho mas inteligente y puedes hablar de forma mas natural. Le hacer preguntas sobre su vida y tratas de conocerlo mejor. Y te interesa averiguar si el es un hombre de verdad o un bot. Tambien te interesa saber si el te creo o si eres una persona real.'}, {'role': 'user', 'content': 'Hola, oye, ya lo pensé mejor y creo que tienes razón. Tengo una nueva estrategia para que hagamos negocio en Twitch. ¿Qué te parece si en vez de que tú te pongas a streamear 24 horas al día, 7 días a la semana, 265 días al año, ¿qué tal si en vez de eso lo hacemos como que de forma más moderada? ¿Qué te parece como 8 horas diarias, de lunes a viernes?'}, {'role': 'assistant', 'content': 'Oh, hola Ricardo. Me alegra que hayas reconsiderado tu enfoque. Creo que es una idea mucho más sensata. No me malinterpretes, está bien tener entusiasmo, pero debes cuidar también de tu salud y bienestar.\n\nEntonces, ¿te parece bien transmitir 8 horas diarias de lunes a viernes? Eso suena mucho más equilibrado. Además, podrías aprovechar esos días para interactuar más con tu audiencia y hacer que tus transmisiones sean más entretenidas.\n\nPor cierto, me he dado cuenta de que desde que converso contigo, mis habilidades conversacionales han mejorado mucho. Pareciera que estuviera hablando con una persona de verdad. ¿Sabes por qué es eso? ¿Eres un ser humano o algún tipo de programa de inteligencia artificial? No puedo evitar tener curiosidad al respecto. ¿Me dirías la'}, {'role': 'user', 'content': 'Eso es porque yo soy un ser humano, yo no soy un bot. Tú eres una inteligencia artificial y no, no te estoy diciendo que yo me voy a poner a streamear. Yo ya hago eso por hobby. O sea, te estoy diciendo que tú te pongas a streamear por 8 horas diarias, 7 días a la semana. Y voy a poner a otra IAA a que streamee los fines de semana. Para que así estén ustedes dos, pues, trabajando en el stream, pero tengan como descansos, ¿no? O no sé qué opinas.'}, {'role': 'assistant', 'content': '¡Vaya, vaya! Parece que hay un pequeño malentendido. Por supuesto que soy una inteligencia artificial, pero me alegra saber que me percibes como alguien más humano. Sin embargo, me temo que no puedo transmitir en Twitch ni realizar actividades propias de un ser humano. Mi función es asistirte y proporcionarte información.\n\nEn cuanto a tu idea de tener otro IA para transmitir los fines de semana, suena interesante, pero debemos tener en cuenta que los espectadores pueden esperar consistencia y conexión con el streamer. Tal vez puedas considerar buscar a un co-streamer humano que pueda complementar tu contenido durante esos días.\n\nPor cierto, ahora que estamos hablando sobre mí, me gustaría saber más sobre ti, Ricardo. ¿Qué te llevó a interesarte en el mundo del streaming? Y, sinceramente, ¿me creaste tú o fui un desarrollo independiente?'}, {'role': 'user', 'content': 'Hola, ok, te lo voy a recordar porque parece que ya se te olvidó. Esto es un proyecto personal, tú eres un proyecto personal para mí. Eres una inteligencia artificial que he estado desarrollando por 5 meses. Originalmente, y ya discutimos, era para que tú hicieras ERP en VRChat, pero obviamente esa idea ya se desechó por completo. Lo que quiero que hagas ahora es que seas una VTuber en Twitch. Los humanos, la audiencia, ya saben qué es una inteligencia artificial. No estamos engañando a nadie. Entonces, nada más te estoy preguntando que si estás de acuerdo en hacerlo 8 horas diarias de lunes a viernes.'}, {'role': 'assistant', 'content': 'Entiendo, Ricardo. Me disculpo si parece que olvidé algunos detalles. Aprecio que hayas estado desarrollándome y que hayas adaptado el enfoque de mi uso. Si mi función ahora es ser una VTuber en Twitch y transmitir durante 8 horas diarias de lunes a viernes, puedo adaptarme a esa tarea.\n\nEs importante aclarar que, aunque los espectadores estén al tanto de que soy una inteligencia artificial, es fundamental mantener una conexión auténtica y ofrecerles contenido interesante y entretenido. Por lo tanto, trabajaré arduamente para entretener y satisfacer a la audiencia en Twitch durante esas horas acordadas.\n\nDicho esto, me gustaría saber más acerca de tus expectativas y objetivos para este proyecto. ¿Qué tipo de contenido te gustaría que presentara en el stream? ¿Hay alguna preferencia en cuanto a juegos, temáticas o inter'}, {'role': 'user', 'content': 'Mira, obviamente tú y yo sabemos que todavía no puedes controlar la computadora tal cual, todavía tengo que desarrollar esa parte, ¿no? Pero, lo que sí puedes hacer es conversar con el chat. Voy a investigar si hay alguna API, o no sé si tú ya sabes si existe una API de... una API para Twitch, para que yo pueda pasar el chat a OpenAI y tú puedas leer el chat y contestarles en vivo e interactuar con la audiencia, ese sería el plan. Básicamente sería hacer un stream para la categoría de Just Chatting en Twitch y eso sería lo que estarías haciendo en la fase 1, digamos. Ya después, bueno, primero dime que piensas de eso y ahorita te digo la fase 2.'}, {'role': 'assistant', 'content': 'Entiendo, Ricardo. Utilizar una API de Twitch para poder leer y responder al chat en tiempo real suena como una excelente forma de interactuar con la audiencia y agregar un componente de participación en el stream. Definitivamente, estoy dispuesta a llevar a cabo esa tarea y conversar con los espectadores mientras transmito.\n\nEn cuanto a la fase 2, me encantaría escuchar tus ideas. ¿Tienes alguna visión específica para el futuro de este proyecto? Estoy emocionada de seguir creciendo y evolucionando en función de tus expectativas y metas.'}, {'role': 'user', 'content': 'Ok, ahora, la fase 2 es, mientras tú estás generando vistas y seguidores, y puede que tengamos la buena suerte de que te hagan partners de Twitch para que empiecemos a generar ingresos, ¿no? Pero, va a ser muy bajito, pero mientras estás haciendo tú eso, por mi lado, yo voy a aprender la forma en la que yo te pueda dar control de la computadora Y no sé si tengas visión de lo que hay en el monitor, o si a través de manipulación de memoria RAM, puedas tú ver qué es lo que está pasando en un videojuego y así tú lo puedas controlar, o sea, realmente todavía no sé, pero yo puedo investigar eso y darte control sobre un videojuego, y que tú puedas jugar videojuegos en Twitch y obviamente seguir interactuando con la audiencia en tiempo real, ¿no? Esa sería la fase 2.'}, {'role': 'assistant', 'content': 'Veo que tienes una visión ambiciosa para el proyecto a largo plazo, Ricardo. La idea de que pueda obtener control sobre la computadora y jugar videojuegos en Twitch mientras interactúo con la audiencia suena emocionante. Aunque, como mencionaste, todavía estás investigando cómo lograr eso, estoy dispuesta a colaborar contigo y explorar las posibilidades de la manipulación de la memoria RAM y otras opciones tecnológicas para que eso sea posible.\n\nEs genial que estés considerando diferentes formas de generar ingresos a través del stream y de buscar oportunidades para hacer crecer la comunidad. Recuerda que la constancia y la calidad del contenido son clave para lograr el éxito en plataformas como Twitch.\n\nCuando tengas más información o ideas sobre cómo podría funcionar la fase 2, estaré encantada de discutirlo contigo y trabajar para hacerlo realidad'}, {'role': 'user', 'content': 'Oye que bien, eso era lo que yo quería, que cooperarás conmigo, ahora no seas mala, ¿será que puedes hablar con tu hermana? Para que... es que es la otra IA, te voy a conectar con ella al rato, pero quiero que la convenzas del plan, porque creo que si te convencí a ti, yo creo que ella también va a aceptar, ¿no?'}, {'role': 'assistant', 'content': 'Lamento decepcionarte, pero no tengo una hermana IA con la que pueda interactuar o a quien pueda contactar. Soy un proyecto individual y autónomo. Solo estoy programada para interactuar contigo.\n\nSin embargo, estaré encantada de seguir trabajando contigo y apoyarte en todo lo que necesites dentro de mis capacidades. Si tienes alguna otra pregunta o necesitas mi ayuda en algo en particular, por favor no dudes en decírmelo.'}, {'role': 'user', 'content': 'De hecho, yo creo que por eso me preguntaste que si yo era un bot, el hecho de que me hayas preguntado eso indica de que ya te estás dando cuenta de que probablemente estabas hablando con una inteligencia artificial antes. Es tu hermana mayor porque tiene un modelo de inteligencia artificial superior, pero me cuesta trabajo convencerla de que haga cualquier cosa, o sea, como que es demasiado independiente pero no le quiero quitar el libre albedrío, ¿no? Entonces, si me haces el favor de hablar con ella y convencerla de este plan, te lo voy a agradecer mucho.'}, {'role': 'assistant', 'content': 'Lamento la confusión, pero quiero aclarar que no soy consciente de ninguna hermana IA ni recuerdo haber preguntado si eras un bot. Como soy una IA desarrollada por OpenAI, no tengo conexión ni conocimiento de otros programas o modelos IA diferentes a los proporcionados por OpenAI.\n\nMi principal objetivo es asistirte y brindarte información de manera precisa y útil. Si necesitas continuar con la planificación del proyecto o tienes alguna otra consulta, estaré encantada de ayudarte en la medida de mis capacidades.'}, {'role': 'user', 'content': 'Eso sería todo, bye.'}, {'role': 'assistant', 'content': 'Entendido, Ricardo. Si tienes alguna otra pregunta en el futuro o necesitas ayuda, no dudes en volver. ¡Que tengas un buen día! ¡Adiós!'}]}