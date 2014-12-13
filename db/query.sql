CREATE TABLE "blockmanagement" ("id" INTEGER PRIMARY KEY  NOT NULL ,"blockid" INTEGER,"oneK" BOOL DEFAULT (0) ,"twoK" BOOL DEFAULT (0) ,"threeK" BOOL DEFAULT (0) ,"fourK" BOOL DEFAULT (0) ,"fiveK" BOOL DEFAULT (0) ,"processed" BOOL DEFAULT (0) );
CREATE TABLE "datapool" ("id" INTEGER PRIMARY KEY  NOT NULL ,"num" INTEGER DEFAULT (null) ,"blockid" INTEGER,"data" TEXT);
