-- This file inserts the default data into the user.platform table.

INSERT INTO "user".platform (name, description)
VALUES 
('VRChat','VRChat is a social VR platform where users can create and share their own virtual worlds, avatars, and experiences.'),
('Discord','Discord is a free and secure all-in-one voice and text chat for gamers.'),
('Twitter','Twitter is an American microblogging and social networking service on which users post and interact with messages known as "tweets".'),
('Twitch','Twitch is a live streaming video platform owned by Twitch Interactive, a subsidiary of Amazon.'),
('YouTube','YouTube is an American online video-sharing platform headquartered in San Bruno, California.'),
('Instagram','Instagram is an American photo and video sharing social networking service owned by Facebook, Inc.'),
('TikTok','TikTok is a Chinese video-sharing social networking service owned by ByteDance, a Beijing-based internet technology company founded in 2012 by Zhang Yiming.'),
('LinkedIn','LinkedIn is an American business and employment-oriented service that operates via websites and mobile apps.'),
('Google','Google is an American multinational technology company that specializes in Internet-related services and products, which include online advertising technologies, search engine, cloud computing, software, and hardware.')
ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description
RETURNING *;