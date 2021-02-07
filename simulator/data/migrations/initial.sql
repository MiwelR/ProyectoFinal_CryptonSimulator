CREATE TABLE "movements" (
	"id"	INTEGER,
	"date"	TEXT,
	"time"	TEXT,
	"from_currency"	TEXT,
	"from_quantity"	REAL,
	"to_currency"	TEXT,
	"to_quantity"	REAL,
	"price"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
)