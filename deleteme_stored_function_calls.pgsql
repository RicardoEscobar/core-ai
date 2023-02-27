-- Test stored functions:
-- Insert a new platform:
SELECT "user".insert_platform('Twitch', 'Twitch (Twitch.tv) is an online live streaming video platform with a focus on gaming. The name Twitch comes from the term twitch gaming, which refers to fast action games that test reflexes, such as first person shooter games. Twitch is part of Twitch Interactive and is a subsidiary of Amazon.');
SELECT "user".insert_platform('VRChat', 'VRChat is a downloadable virtual reality social platform available for use on the Oculus Quest, Oculus Rift, HTC Vive, and Valve Index virtual reality hardware. Users can sign in, choose an avatar, and visit different rooms to interact with others in a variety of social activities.');
SELECT "user".insert_platform('WhatsApp', $$WhatsApp is a "free" cross-platform messaging service. It lets users of iPhone and Android smartphones and Mac and Windows PC call and exchange text, photo, audio and video messages with others across the globe for free, regardless of the recipient's device.$$);

-- Insert a new account:
SELECT "user".insert_account('RicardoEscobar', 1);
SELECT "user".insert_account('JorgeEscobar', 2);
-- Insert a new summary:
SELECT "fine-tunning".insert_summary('summary1');
-- Update a platform:
SELECT "user".update_platform(1, 'platform2', 'description2');
-- Update an account:
SELECT "user".update_account(1, 'account2', 1);
-- Update a summary:
SELECT "fine-tunning".update_summary(1, 'summary2');
-- Delete a platform:
SELECT "user".delete_platform(1);
-- Delete an account:
SELECT "user".delete_account(1);
-- Delete a summary:
SELECT "fine-tunning".delete_summary(1);
