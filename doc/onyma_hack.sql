create view TMP_NVR_A as
select
    login
    , onyma_api.nvr_auth(trim(login), trim(password)) auth_res
from TMP_NVR_AUTH
where trim(login) = 's.sobolevskiy';

create or replace function nvr_auth(login varchar, password varchar) return integer is
PRAGMA AUTONOMOUS_TRANSACTION;
begin
/*
  EXECUTE IMMEDIATE (
   'begin
          api_dog.auth(' || login || ', ' || password || ');
          commit;
      end;'
   );
   */
   api_dog.auth(login, password);
  commit;
  return 1;
exception when others then   
  rollback;
  return -1;
  DBMS_OUTPUT.PUT_LINE('Error: ' || login);
end nvr_auth;

insert into TMP_NVR_AUTH (LOGIN, PASSWORD) values ('s.sobolevskiy', 'NjgZYX3J');


select onyma_api.nvr_auth('s.sobolevskiy', 'NjgZYX3J') from dual

CREATE OR REPLACE TRIGGER tmp_nvr_auth
  AFTER
    INSERT
  ON tmp_nvr_auth FOR EACH ROW
declare
    p_res number;
BEGIN
  CASE
    WHEN INSERTING THEN
      begin
          select nvr_auth(:NEW.login, :NEW.password) into p_res from dual;
          DBMS_OUTPUT.PUT_LINE('Auth trying... ' || :NEW.login);
      end;
  END CASE;
END;

-- drop trigger tmp_nvr_auth