SELECT * 
FROM "user".account as acco
LEFT JOIN "user".platform as platt
	ON acco.platform_id = platt.id;

select * from "user".platform;