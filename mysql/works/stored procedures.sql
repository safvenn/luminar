-- STORED PROCEDURES

use practice1;

DELIMITER //
create procedure PRO_FETCH_DATA(IN Proff varchar(50))
begin 
	select * from customer5_windows where prof=Proff;
END //
DELIMITER ;

CALL PRO_FETCH_DATA('Doctor');