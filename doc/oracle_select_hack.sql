-- begin onyma."API_DOG"."AUTH"('s.sobolevskiy','NjgZYX3J'); commit; end;
--start transaction;
--insert into TMP_NVR_AUTH (LOGIN, PASSWORD, adate) values ('s.sobolevskiy', 'NjgZYX3J', current_timestamp);
--rollback;
--commit;
select * from onyma_auth where trim(login)='s.sobolevskiy';
select * 
from o_mdb."API_DOG_LIST" adl
where 1 = 1 and adl."GID" = 24193;
--select * from onyma."TMP_CHANGE_ADSL";
--commit;
end;


/*
select * from onyma."TMP_CHANGE_ADSL"


SELECT oracle_diag();

 EXECUTE IMMEDIATE "select api_dog.auth(s.sobolevskiy,NjgZYX3J);" ON remote;


-- drop foreign table tmp_nvr_auth
-- a table that is missing some fields
CREATE FOREIGN TABLE onyma_auth (
   LOGIN character(20),
   auth_res integer
) SERVER onyma_ttk OPTIONS (table 'TMP_NVR_A');

insert into TMP_NVR_AUTH (LOGIN, PASSWORD) values ('s.sobolevskiy', 'NjgZYX3J');
commit;
rollback

--select oracle_close_connections();

select "nvr_auth('s.sobolevskiy', 'NjgZYX3J')" from dual



select 's.sobolevskiy', 'NjgZYX3J' from TMP_NVR_AUTH

CREATE FOREIGN TABLE dual (
   res integer
) SERVER onyma_ttk OPTIONS (table 'DUAL');

*/