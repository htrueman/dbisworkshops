alter table "user"
    add user_password varchar2(10);


UPDATE "user" SET USER_EMAIL = 'BOB@GMAIL.COM', USER_PASSWORD = '111' WHERE USER_ID=1;
UPDATE "user" SET USER_EMAIL = 'PETRO@GMAIL.COM', USER_PASSWORD = '222' WHERE USER_ID=2;


CREATE SEQUENCE SEQ_USER INCREMENT BY 1 START WITH 3;

commit;