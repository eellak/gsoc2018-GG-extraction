CREATE TABLE IF NOT EXISTS `PAOrgs` (
	`id` INTEGER,
	`name`	TEXT, -- The Public Admin. Organization's name
	`description` TEXT, -- A short description of it
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `RespAs` (
	`id` INTEGER,
	`name`	TEXT, -- The Ministry's name, e.g. "Υπουργείο Οικονομικών" (Ministry of Finance)
	`description` TEXT, -- A short description of the Responsibility Assignment
	`PAOrg_id`	INTEGER, -- Shows which Public Organization this RespA is associated with
	PRIMARY KEY(`id`)
	FOREIGN KEY(`PAOrg_id`) REFERENCES `PAOrgs`(`id`)
);
CREATE TABLE IF NOT EXISTS `signatures` (
	`id`	INTEGER,
	`person_id`	INTEGER, -- The person this signature belongs to
	`issue_id`	INTEGER, -- The fek issue this signature was scraped from
	`data`	TEXT, -- Additional data for the signature, possibly extracted from the pdf
	PRIMARY KEY(`id`),
	FOREIGN KEY(`issue_id`) REFERENCES `issues`(`id`),
	FOREIGN KEY(`person_id`) REFERENCES `persons`(`id`)
);
CREATE TABLE IF NOT EXISTS `raw_signatures` (
	`id`	INTEGER,
	`person_name`	TEXT, -- The name of the person this signature belongs to
	`role`  TEXT, -- The role of the minister signing
	`issue_title`	TEXT, -- The name of the issues this signature was extracted from
	`issue_date` INTEGER NOT NULL, -- UNIX timestamp when the issue this signature was found on was published
	`regulation`    TEXT,
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `positions` (
	`id`	INTEGER,
	`role`	TEXT, -- The person's role, e.g. Minister, Deputy etc.
	`date_from`	INTEGER NOT NULL, -- UNIX timestamp when the person got this position
	`date_to`	INTEGER NOT NULL, -- UNIX timestamp when the person stopped being in this position
	`person_id`	INTEGER, -- Shows which person's position we're referencing
	`ministry_id`	INTEGER, -- Shows in which ministry this person is
	`cabinet_id`	INTEGER, -- References the cabinet in which this position was allocated
	PRIMARY KEY(`id`),
	FOREIGN KEY(`person_id`) REFERENCES `persons`(`id`),
	FOREIGN KEY(`ministry_id`) REFERENCES `ministries`(`id`),
	FOREIGN KEY(`cabinet_id`) REFERENCES `cabinets`(`id`)
);
CREATE TABLE IF NOT EXISTS `persons` (
	`id`	INTEGER,
	`name`	TEXT NOT NULL, -- The person's full name
	`political_party`	TEXT, -- The political party of this person, or Independent if there's no affiliation
	`birthdate`	INTEGER, -- UNIX timestamp of this person's date of birth
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `ministry_origins` (
    `type` TEXT, -- Shows how a ministry has originated. For example: Merger, Division, Renaming etc.
    `data` BLOB, -- Serialized  data further explaining the origin of the ministry. In case of mergers or renaming it
               -- will store the predecessors for example.
    `ministry_id` INTEGER,
    FOREIGN KEY(`ministry_id`) REFERENCES `ministries`(`id`)
);
CREATE TABLE IF NOT EXISTS `ministries` (
	`id` INTEGER,
	`name`	TEXT, -- The Ministry's name, e.g. "Υπουργείο Οικονομικών" (Ministry of Finance)
	`description` TEXT, -- A short description of the ministry
	`established` INT, -- UNIX timestamp noting when this ministry was established
	`disbanded` INT, -- UNIX timestamp noting when this ministry was disbanded (if it hasn't then it should store 0)
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `issues` (
	`id`	INTEGER,
	`title`	TEXT, -- The title of the fek issue
	`type`	TEXT, -- The type of the fek issue, e.g A, B, 	Α.Σ.Ε.Π. etc.
	`number`	INTEGER, -- The number of the issue
	`file`	TEXT, -- The issues pdf file location,
	`analyzed` INTEGER(1),
	`date`	INTEGER, -- UNIX timestamp when this fek issue was published
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `cabinets` (
	`id`	INTEGER,
	`title`	TEXT NOT NULL, -- The cabinet's title, e.g. "Κυβέρνηση Αλέξη Τσίπρα Σεπτεμβρίου 2015"
	`description`	TEXT, -- A general description for the cabinet
	`date_from`	INTEGER NOT NULL, -- UNIX timestamp containing the day the cabinet was formed
	`date_to`	INTEGER NOT NULL, -- UNIX timestamp containing the day the cabinet disbanded, 0 if still active
	PRIMARY KEY(`id`)
);