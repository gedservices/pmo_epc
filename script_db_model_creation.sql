-- =========================================================
-- PMO DATABASE - FULL SCHEMA + DEMO DATA (POSTGRES)
-- =========================================================

-- =========================
-- CLEAN RESET (OPTIONNEL)
-- =========================
drop table if exists historique_avancement cascade;
drop table if exists risques cascade;
drop table if exists couts cascade;
drop table if exists taches cascade;
drop table if exists projets cascade;
drop table if exists utilisateurs cascade;
drop table if exists disciplines cascade;
drop table if exists entites cascade;

-- =========================
-- ENTITES
-- =========================
create table entites (
  id bigint generated always as identity primary key,
  nom varchar(100) not null unique
);

-- =========================
-- DISCIPLINES
-- =========================
create table disciplines (
  id bigint generated always as identity primary key,
  code varchar(10) not null unique,
  nom varchar(100) not null
);

-- =========================
-- UTILISATEURS
-- =========================
create table utilisateurs (
  id bigint generated always as identity primary key,
  nom varchar(100) not null,
  prenom varchar(100) not null,
  email varchar(150),
  entite_id bigint references entites(id),
  role varchar(30) default 'MEMBER',
  actif boolean default true
);

-- =========================
-- PROJETS
-- =========================
create table projets (
  id bigint generated always as identity primary key,
  code varchar(50) unique,
  nom varchar(255) not null,
  description text,

  statut varchar(30) check (
    statut in ('Ouvert','En cours','En attente','Suspendu','Clôturé','Annulé')
  ),

  priorite varchar(30),

  responsable_id bigint references utilisateurs(id),
  entite_id bigint references entites(id),

  date_debut_prevue date,
  date_fin_prevue date,
  date_debut_reelle date,
  date_fin_reelle date,

  budget_prevu numeric default 0,
  budget_reel numeric default 0,

  progression_calculee numeric default 0
);

-- =========================
-- TACHES
-- =========================
create table taches (
  id bigint generated always as identity primary key,
  projet_id bigint references projets(id) on delete cascade,

  nom varchar(255),
  description text,

  statut varchar(30),
  poids numeric check (poids >= 0 and poids <= 100),
  avancement numeric default 0 check (avancement >= 0 and avancement <= 100),

  date_debut_prevue date,
  date_fin_prevue date,
  date_debut_reelle date,
  date_fin_reelle date,

  responsable_id bigint references utilisateurs(id),
  discipline_id bigint references disciplines(id)
);

-- =========================
-- COUTS
-- =========================
create table couts (
  id bigint generated always as identity primary key,
  projet_id bigint references projets(id) on delete cascade,

  libelle varchar(255),
  cout_prevu numeric,
  cout_reel numeric,
  date_cout date
);

-- =========================
-- RISQUES
-- =========================
create table risques (
  id bigint generated always as identity primary key,
  projet_id bigint references projets(id) on delete cascade,

  titre varchar(255),
  description text,
  probabilite int check (probabilite between 1 and 5),
  impact int check (impact between 1 and 5),

  criticite int generated always as (probabilite * impact) stored,

  statut varchar(30)
);

-- =========================
-- HISTORIQUE AVANCEMENT
-- =========================
create table historique_avancement (
  id bigint generated always as identity primary key,
  projet_id bigint references projets(id) on delete cascade,

  date_snapshot date,
  avancement_reel numeric,
  avancement_prevu numeric
);

-- =========================================================
-- DATA SETUP
-- =========================================================

insert into entites (nom) values
('Direction'),('Finance'),('IT'),('Maintenance'),('RH'),('Production');

insert into disciplines (code, nom) values
('ELE','Electricité'),
('INS','Instrumentation'),
('MECA','Mécanique'),
('PJM','Project Management'),
('CIV','Génie Civil'),
('HSE','Sécurité');

insert into utilisateurs (nom, prenom, email, entite_id, role) values
('MBA OYONE','Joel','joel@demo.com',1,'PMO'),
('ETENDINO','Yorick','yorick@demo.com',4,'MANAGER'),
('OBIANG','Jean-Marie','jm@demo.com',3,'MEMBER');

-- =========================================================
-- PROJETS
-- =========================================================

insert into projets (
  code, nom, description, statut, priorite,
  responsable_id, entite_id,
  date_debut_prevue, date_fin_prevue,
  budget_prevu, budget_reel, progression_calculee
) values
('P-001','Projet A - IT Upgrade','Modernisation infrastructure IT','En cours','Critique',1,3,'2026-06-01','2026-07-15',50000,52000,45),
('P-002','Projet B - Maintenance','Maintenance usine','En cours','Haute',2,4,'2026-06-10','2026-08-01',30000,28000,70),
('P-003','Projet C - HSE Audit','Audit sécurité site','En attente','Moyen',1,5,'2026-07-01','2026-09-01',20000,0,10);

-- =========================================================
-- TACHES
-- =========================================================

insert into taches (
  projet_id, nom, statut, poids, avancement,
  date_debut_prevue, date_fin_prevue,
  responsable_id, discipline_id
) values
(1,'Analyse infra','En cours',30,80,'2026-06-01','2026-06-10',1,4),
(1,'Migration serveurs','En cours',40,50,'2026-06-10','2026-06-25',2,1),
(1,'Tests système','En attente',30,10,'2026-06-25','2026-07-10',3,3),

(2,'Inspection machines','Terminée',50,100,'2026-06-10','2026-06-20',2,3),
(2,'Remplacement pièces','En cours',50,40,'2026-06-20','2026-07-20',2,3),

(3,'Audit HSE','En cours',100,10,'2026-07-01','2026-07-15',1,6);

-- =========================================================
-- COUTS
-- =========================================================

insert into couts (projet_id, libelle, cout_prevu, cout_reel, date_cout) values
(1,'Matériel IT',30000,32000,'2026-06-15'),
(1,'Services externes',20000,20000,'2026-06-20'),

(2,'Pièces machines',15000,14000,'2026-06-25'),
(2,'Main d’œuvre',15000,14000,'2026-07-01'),

(3,'Audit externe',20000,0,'2026-07-05');

-- =========================================================
-- RISQUES
-- =========================================================

insert into risques (projet_id, titre, description, probabilite, impact, statut) values
(1,'Retard migration','Complexité technique',4,5,'Ouvert'),
(2,'Panne machine','Arrêt production possible',3,4,'En cours'),
(3,'Non conformité','Audit critique',2,5,'Ouvert');

-- =========================================================
-- HISTORIQUE AVANCEMENT
-- =========================================================

insert into historique_avancement (projet_id, date_snapshot, avancement_reel, avancement_prevu) values
(1,'2026-06-01',10,12),
(1,'2026-06-10',25,30),
(1,'2026-06-20',40,50),
(1,'2026-06-30',45,60),

(2,'2026-06-10',20,20),
(2,'2026-06-20',50,40),
(2,'2026-06-30',70,65),

(3,'2026-07-01',5,10),
(3,'2026-07-10',10,20);

-- =========================================================
-- END
-- =========================================================