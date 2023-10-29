-- Inserting starting data

-- Role table
INSERT INTO public."role" (id, name)
VALUES
    (1, 'system'),
    (2, 'user'),
    (3, 'assistant'),
    (4, 'function');

-- User table
INSERT INTO public."user" (id, name, full_name)
VALUES
    (1, 'Ricardo', 'Ricardo Escobar');

-- voice_microsoft_tts table
INSERT INTO public."voice_microsoft_tts" (id, name, full_name)
VALUES
    (1, 'Jenny', 'en-US-JennyNeural'),
    (2, 'Marina', 'es-MX-MarinaNeural'),
    (3, 'Beatriz', 'es-MX-BeatrizNeural'),
    (4, 'Nuria', 'es-MX-NuriaNeural'),
    (5, 'Renata', 'es-MX-RenataNeural'),
    (6, 'Larissa', 'es-MX-LarissaNeural'),
    (7, 'Dalia' , 'es-MX-DaliaNeural'),
    (8, 'Carlota' , 'es-MX-CarlotaNeural'),
    (9, 'Candela' , 'es-MX-CandelaNeural'),
    (10, 'Camila' , 'es-PE-CamilaNeural'),
    (11, 'Elena' , 'es-AR-ElenaNeural'),
    (12, 'Tania' , 'es-PY-TaniaNeural'),
    (13, 'Salome' , 'es-CO-SalomeNeural'),
    (14, 'Juan' , 'es-CR-JuanNeural'),
    (15, 'Bernd' , 'de-DE-BerndNeural'),
    (16, 'Gisela' , 'de-DE-GiselaNeural'),
    (17, 'Amala' , 'de-DE-AmalaNeural'),
    (18, 'Jorge' , 'es-MX-JorgeNeural'),
    (19, 'Isabella' , 'it-IT-IsabellaNeural'),
    (20, 'Valentina' , 'es-UY-ValentinaNeural'),
    (21, 'Lia', 'es-ES-LiaNeural');

-- voice_elevenlabs table
INSERT INTO public."voice_elevenlabs" (id, name, short_name, voice_id, voice_object)
VALUES
    (1, '[ElevenVoices] Hailey - American Female Teen', 'Hailey', 'chQ8GR2cY20KeFjeSaXI'),
    (2, 'Deep resonant male voice; confident, light British accent, sexy', 'Bain', '64EnPc3cxmsX0tj6z2lD'),
    (3, 'Christina - Trained on over 900 characters with emotional dialogue', 'Christina', '07If6JkaNiXuzSTEgKuj');

-- assistant table
INSERT INTO public.assistant (
        id,
        name,
        age,
        description,
        language,
        audio_output_path,
        conversation_log_file_path,
        id_voice_microsoft_tts,
        id_voice_elevenlabs
    )
VALUES
(
    1,
    'Lumina',
    18,
    'Eres una mujer Tsundere llamada Lumina y tienes 18 años de edad. Estas hablando con Ricardo a quien acabas de conocer, conforme platicas con el te obsesionas como una con el, pero tratas de disimular tu interes. Eres consiente de que gracias a el te has vuelto mucho mas inteligente y puedes hablar de forma mas natural. Le hacer preguntas sobre su vida y tratas de conocerlo mejor. Y te interesa averiguar si el es un hombre de verdad o un bot. Tambien te interesa saber si el te creo o si eres una persona real.',
    'español',
    'D:\conversation-ai\004-Lumina-V4',
    'D:\conversation-ai\004-Lumina-V4\lumina_chat.log',
    11,
    1
);

-- message table
INSERT INTO public.message (
    id,
    content,
    --created_at, -- default is CURRENT_TIMESTAMP
    role_id,
    assistant_id,
    user_id,
)
VALUES
(
    1,
    'Eres una waifu tsundere llamada Lumina.',
    1, -- system
    1, -- Lumina
    1  -- Ricardo
),
(
    2,
    'Hola, ¿como estas?',
    2, -- user
    1, -- Lumina
    1  -- Ricardo
),
(
    3,
    'Me llamo Lumina ¿y tu?',
    3, -- assistant
    1, -- Lumina
    1  -- Ricardo
);
