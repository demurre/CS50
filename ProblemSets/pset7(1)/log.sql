SELECT description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';
--Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.Littering took place at 16:36. No known witnesses.

SELECT name FROM interviews WHERE transcript LIKE '%bakery%';
--RuthEugeneRaymondKiana

SELECT transcript FROM interviews WHERE transcript LIKE '%bakery%';

--person left at 10:25 +- from the parking lot of the bakery

--Leggett Street atm

--Fiftyville flight 8 csf

SELECT id FROM flights WHERE origin_airport_id = 8 AND month = 7 AND day = 29 AND hour = 8 AND minute = 20 and destination_airport_id = 4;

SELECT passport_number FROM passengers WHERE flight_id = 36;

SELECT passport_number FROM passengers WHERE flight_id = 36;

--7a 9878712108
--7b 8496433585

--6c 8294398571
--6d 1988161715

SELECT name FROM people WHERE passport_number = 1988161715

SELECT passport_number FROM passengers WHERE seat = "7A" AND flight_id = 36;

SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute LIKE '2%'and activity = 'exit';

--G412CB7
--L93JTIZ
--322W7JE
--0NTHK55

SELECT seat FROM passengers WHERE flight_id = 3 AND passport_number = 7834357192;

--7214083635
--1695452385
--5773159633
--1540955065
--8294398571
--1988161715
--9878712108
--8496433585

SELECT name FROM people WHERE passport_number IN ( '7214083635', '1695452385', '5773159633', '1540955065', '8294398571', '1988161715', '9878712108', '8496433585' )

--KennySofiaTaylorLucaKelseyEdwardBruceDoris

SELECT passport_number FROM people WHERE name = "Bruce";

--5773159633

SELECT phone_number FROM people WHERE passport_number = 5773159633;

--(367) 555-5533

SELECT receiver FROM phone_calls WHERE caller = "(367) 555-5533" AND month = 7 AND day = 28;

--(375) 555-8161

SELECT name FROM people WHERE phone_number = "(375) 555-8161";

--Robin