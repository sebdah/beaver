SQLite format 3   @     Y   &                                                            Y -�#   �    &������                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
   
    m ���{N,���],
���|Z5
 � � � m                                                     & 1)Can delete accountdelete_account& 1)Can change accountchange_account  +#Can add accountadd_account) 5+Can delete log entrydelete_logentry) 5+Can change log entrychange_logentry# /%Can add log entryadd_logentry  +#Can delete sitedelete_site  +#Can change sitechange_site %Can add siteadd_site& 1)Can delete sessiondelete_session& 1)Can change sessionchange_session  +#Can add sessionadd_session/ ;1Can delete content typedelete_contenttype/ ;1Can change content typechange_contenttype)
 5+Can add content typeadd_contenttype 	 +#Can delete userdelete_user+ 7	/Can delete permissiondelete_permission" -%Can delete groupdelete_group  +#Can change userchange_user+ 7	/Can change permissionchange_permission" -%Can change groupchange_group %Can add useradd_user% 1	)Can add permissionadd_permission 'Can add groupadd_group
   $ ��h����V@'�������v`N9$                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            )delete_account)change_account#add_account+delete_logentry+change_logentry%add_logentry#delete_site#change_siteadd_site)delete_session)change_session#add_session1delete_contenttype1change_contenttype+add_contenttype
#delete_user		/delete_permission%delete_group#change_user	/change_permission%change_groupadd_user	)add_permission	add_group                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  �  ��$q                                                                                                                                                                  �++�Stableauth_permissionauth_permissionCREATE TABLE "auth_permission" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
)=Q+ indexsqlite_autoindex_auth_permission_1auth_permission�99�Utableauth_group_permissionsauth_group_permissionsCREATE TABLE "auth_group_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("group_id", "permission_id")
)K_9 indexsqlite_autoindex_auth_group_permissions_1auth_group_permissions�!!�ctableauth_groupauth_groupCREATE TABLE "auth_group" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(80) NOT NULL UNIQUE
)    Cm��                                                                                                                                                                                                                                                            3G! indexsqlite_autoindex_auth_group_1auth_group�'AA�Ytableauth_user_user_permissionsauth_user_user_permissionsCREATE TABLE "auth_user_user_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("user_id", "permission_id")
)SgA indexsqlite_autoindex_auth_user_user_permissions_1auth_user_user_permissions	�z	--�'tableauth_user_groupsauth_user_groupsCREATE TABLE "auth_user_groups" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id"),
    UNIQUE ("user_id", "group_id")
)?
S- indexsqlite_autoindex_auth_user_groups_1auth_user_groups                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  �  �u��                                                                                                                                                        �J�ctableauth_userauth_userCREATE TABLE "auth_user" (
    "id" integer NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "password" varchar(128) NOT NULL,
    "is_staff" bool NOT NULL,
    "is_active" bool NOT NULL,
    "is_superuser" bool NOT NULL,
    "last_login" datetime NOT NULL,
    "date_joined" datetime NOT NULL
)1E indexsqlite_autoindex_auth_user_1auth_user�33�Ctabledjango_content_typedjango_content_typeCREATE TABLE "django_content_type" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
)EY3 indexsqlite_autoindex_django_content_type_1django_content_type   ( ����r^A(                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 accountcoreaccount log entryadminlogentry sitesitessite sessionsessionssession( %%#content typecontenttypescontenttype userauthuser groupauthgroup !!permissionauthpermission
   k |����k��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   coreaccountadminlogentrysitessitesessionssession%#contenttypescontenttypeauthuserauthgroup!	authpermission    �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         �vM�{A98b0d77738aeb400c2c7f5ccc17ff888MzlmOTQ1YjY0MTViNjFlMzk4ODEzYTVjODVlN2Y3ZjZjODAwYWQ1NTqAAn1xAShVEl9hdXRoX3Vz
ZXJfYmFja2VuZHECVSljb3JlLmJhY2tlbmRzLkJlYXZlckF1dGhlbnRpY2F0aW9uQmFja2VuZHED
VQ1fYXV0aF91c2VyX2lkcQRLAXUu
2012-06-08 06:11:10.638942
� � ��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           $M98b0d77738aeb400c2c7f5ccc17ff888   $                                    �  �`�L                                                                                                                                         �D))�Ctabledjango_sessiondjango_sessionCREATE TABLE "django_session" (
    "session_key" varchar(40) NOT NULL PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" datetime NOT NULL
);O) indexsqlite_autoindex_django_session_1django_session�,##�tabledjango_sitedjango_siteCREATE TABLE "django_site" (
    "id" integer NOT NULL PRIMARY KEY,
    "domain" varchar(100) NOT NULL,
    "name" varchar(50) NOT NULL
)�1--�tabledjango_admin_logdjango_admin_logCREATE TABLE "django_admin_log" (
    "id" integer NOT NULL PRIMARY KEY,
    "action_time" datetime NOT NULL,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "content_type_id" integer REFERENCES "django_content_type" ("id"),
    "object_id" text,
    "object_repr" varchar(200) NOT NULL,
    "action_flag" smallint unsigned NOT NULL,
    "change_message" text NOT NULL
)   � �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           ##example.comexample.com                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 f f                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            �
 EAA	Usebastian.dahlgren@gmail.comcdalozo7SebastianDahlgren2012-05-25 06:25:14.3677982012-05-21 19:29:11.611096467c2ec2-b204-406d-9fd6-fe9106548463
   � �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      E	sebastian.dahlgren@gmail.com    p  p<�_                                                                                              �%%�ctablecore_accountcore_accountCREATE TABLE "core_account" (
    "id" integer NOT NULL PRIMARY KEY,
    "email" varchar(75) NOT NULL UNIQUE,
    "password" varchar(50) NOT NULL,
    "first_name" varchar(50) NOT NULL,
    "last_name" varchar(50) NOT NULL,
    "last_updated" datetime NOT NULL,
    "registered" datetime NOT NULL,
    "is_active" bool NOT NULL,
    "activation_key" varchar(50)
)7K% indexsqlite_autoindex_core_account_1core_account�=+�-indexauth_permission_e4470c6eauth_permissionCREATE INDEX "auth_permission_e4470c6e" ON "auth_permission" ("content_type_id")�K9�;indexauth_group_permissions_bda51c3cauth_group_permissionsCREATE INDEX "auth_group_permissions_bda51c3c" ON "auth_group_permissions" ("group_id")�K9�Eindexauth_group_permissions_1e014c8fauth_group_permissionsCREATE INDEX "auth_group_permissions_1e014c8f" ON "auth_group_permissions" ("permission_id")
   t ����������������������zt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
					
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 � �H�|                                                                                                                                                                                                                                                                                                                                                                                                             �(SA�Iindexauth_user_user_permissions_fbfc09f1auth_user_user_permissionsCREATE INDEX "auth_user_user_permissions_fbfc09f1" ON "auth_user_user_permissions" ("user_id")�.SA�Uindexauth_user_user_permissions_1e014c8fauth_user_user_permissions CREATE INDEX "auth_user_user_permissions_1e014c8f" ON "auth_user_user_permissions" ("permission_id")� ?-�!indexauth_user_groups_fbfc09f1auth_user_groups!CREATE INDEX "auth_user_groups_fbfc09f1" ON "auth_user_groups" ("user_id")�?-�#indexauth_user_groups_bda51c3cauth_user_groups"CREATE INDEX "auth_user_groups_bda51c3c" ON "auth_user_groups" ("group_id")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
   � ��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          =                          A2012-06-08 06:11:10.638942
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 t t�u                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |;)�!indexdjango_session_c25c2c28django_session#CREATE INDEX "django_session_c25c2c28" ON "django_session" ("expire_date")� ?-�!indexdjango_admin_log_fbfc09f1django_admin_log$CREATE INDEX "django_admin_log_fbfc09f1" ON "django_admin_log" ("user_id")�?-�1indexdjango_admin_log_e4470c6edjango_admin_log%CREATE INDEX "django_admin_log_e4470c6e" ON "django_admin_log" ("content_type_id")