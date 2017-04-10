drop user mapping for openerp server onyma_ttk;
drop user mapping for postgres server onyma_ttk;
drop server onyma_ttk;

CREATE SERVER onyma_ttk FOREIGN DATA WRAPPER oracle_fdw OPTIONS (dbserver '//10.110.32.148:1521/onyma');
CREATE USER MAPPING FOR openerp SERVER onyma_ttk OPTIONS (user 'onyma_api', password 'onyma_api');
CREATE USER MAPPING FOR postgres SERVER onyma_ttk OPTIONS (user 'onyma_api', password 'onyma_api');

IMPORT FOREIGN SCHEMA "ONYMA_API" FROM SERVER onyma_ttk INTO onyma OPTIONS (case 'keep', readonly 'true');
IMPORT FOREIGN SCHEMA "O_MDB" FROM SERVER onyma_ttk INTO o_mdb OPTIONS (case 'keep', readonly 'true');
