--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.7
-- Dumped by pg_dump version 9.5.1

-- Started on 2017-07-17 16:09:09 PDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 14 (class 2615 OID 173171)
-- Name: odm2; Type: SCHEMA; Schema: -; Owner: -
--

CREATE EXTENSION if not exists postgis;
CREATE EXTENSION if not exists postgis_topology;
CREATE EXTENSION if not exists fuzzystrmatch;
CREATE EXTENSION if not exists postgis_tiger_geoCoder;

DROP SCHEMA IF EXISTS odm2 CASCADE;
DROP SCHEMA IF EXISTS admin CASCADE;
DROP SCHEMA IF EXISTS odm2extra CASCADE;

CREATE SCHEMA admin;

CREATE SCHEMA odm2;


--
-- TOC entry 15 (class 2615 OID 173172)
-- Name: odm2extra; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA odm2extra;


SET search_path = odm2, pg_catalog;

--
-- TOC entry 1789 (class 1255 OID 175139)
-- Name: MeasurementResultValsToResultsCountvalue(); Type: FUNCTION; Schema: odm2; Owner: -
--

CREATE FUNCTION "MeasurementResultValsToResultsCountvalue"() RETURNS void
    LANGUAGE sql
    AS $$UPDATE odm2.results SET valuecount = 
(SELECT count(measurementresultvalues.resultid) as valuecount2       
from odm2.measurementresultvalues where measurementresultvalues.resultid = results.resultid group by measurementresultvalues.resultid);
$$;


SET search_path = odm2extra, pg_catalog;

--
-- TOC entry 1790 (class 1255 OID 175140)
-- Name: measurementresultvalstoresultscountvalue(); Type: FUNCTION; Schema: odm2extra; Owner: -
--

CREATE FUNCTION measurementresultvalstoresultscountvalue() RETURNS void
    LANGUAGE sql
    AS $$UPDATE odm2.results SET valuecount = 
(SELECT count(measurementresultvalues.resultid) as valuecount2       
from odm2.measurementresultvalues where measurementresultvalues.resultid = results.resultid group by measurementresultvalues.resultid);
$$;


SET search_path = odm2, pg_catalog;

SET default_with_oids = false;

--
-- TOC entry 263 (class 1259 OID 175141)
-- Name: actionannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE actionannotations (
    bridgeid integer NOT NULL,
    actionid integer NOT NULL,
    annotationid integer NOT NULL
);


--
-- TOC entry 264 (class 1259 OID 175144)
-- Name: actionannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE actionannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5600 (class 0 OID 0)
-- Dependencies: 264
-- Name: actionannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE actionannotations_bridgeid_seq OWNED BY actionannotations.bridgeid;


--
-- TOC entry 265 (class 1259 OID 175146)
-- Name: actionby; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE actionby (
    bridgeid integer NOT NULL,
    actionid integer NOT NULL,
    affiliationid integer NOT NULL,
    isactionlead boolean NOT NULL,
    roledescription character varying(5000)
);


--
-- TOC entry 266 (class 1259 OID 175152)
-- Name: actionby_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE actionby_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5601 (class 0 OID 0)
-- Dependencies: 266
-- Name: actionby_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE actionby_bridgeid_seq OWNED BY actionby.bridgeid;


--
-- TOC entry 267 (class 1259 OID 175154)
-- Name: actiondirectives; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE actiondirectives (
    bridgeid integer NOT NULL,
    actionid integer NOT NULL,
    directiveid integer NOT NULL
);


--
-- TOC entry 268 (class 1259 OID 175157)
-- Name: actiondirectives_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE actiondirectives_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5602 (class 0 OID 0)
-- Dependencies: 268
-- Name: actiondirectives_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE actiondirectives_bridgeid_seq OWNED BY actiondirectives.bridgeid;


--
-- TOC entry 269 (class 1259 OID 175159)
-- Name: actionextensionpropertyvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE actionextensionpropertyvalues (
    bridgeid integer NOT NULL,
    actionid integer NOT NULL,
    propertyid integer NOT NULL,
    propertyvalue character varying(255) NOT NULL
);


--
-- TOC entry 270 (class 1259 OID 175162)
-- Name: actionextensionpropertyvalues_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE actionextensionpropertyvalues_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5603 (class 0 OID 0)
-- Dependencies: 270
-- Name: actionextensionpropertyvalues_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE actionextensionpropertyvalues_bridgeid_seq OWNED BY actionextensionpropertyvalues.bridgeid;


--
-- TOC entry 271 (class 1259 OID 175164)
-- Name: actions; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE actions (
    actionid integer NOT NULL,
    actiontypecv character varying(255) NOT NULL,
    methodid integer NOT NULL,
    begindatetime timestamp without time zone NOT NULL,
    begindatetimeutcoffset integer NOT NULL,
    enddatetime timestamp without time zone,
    enddatetimeutcoffset integer,
    actiondescription character varying(5000),
    actionfilelink character varying(255)
);


--
-- TOC entry 272 (class 1259 OID 175170)
-- Name: actions_actionid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE actions_actionid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5604 (class 0 OID 0)
-- Dependencies: 272
-- Name: actions_actionid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE actions_actionid_seq OWNED BY actions.actionid;


--
-- TOC entry 273 (class 1259 OID 175172)
-- Name: affiliations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE affiliations (
    affiliationid integer NOT NULL,
    personid integer NOT NULL,
    organizationid integer,
    isprimaryorganizationcontact boolean,
    affiliationstartdate date NOT NULL,
    affiliationenddate date,
    primaryphone character varying(50),
    primaryemail character varying(255) NOT NULL,
    primaryaddress character varying(255),
    personlink character varying(255)
);


--
-- TOC entry 274 (class 1259 OID 175178)
-- Name: affiliations_affiliationid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE affiliations_affiliationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5605 (class 0 OID 0)
-- Dependencies: 274
-- Name: affiliations_affiliationid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE affiliations_affiliationid_seq OWNED BY affiliations.affiliationid;


--
-- TOC entry 275 (class 1259 OID 175180)
-- Name: annotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE annotations (
    annotationid integer NOT NULL,
    annotationtypecv character varying(255) NOT NULL,
    annotationcode character varying(50),
    annotationtext character varying(500) NOT NULL,
    annotationdatetime timestamp without time zone,
    annotationutcoffset integer,
    annotationlink character varying(255),
    annotatorid integer,
    citationid integer
);


--
-- TOC entry 276 (class 1259 OID 175186)
-- Name: annotations_annotationid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE annotations_annotationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5606 (class 0 OID 0)
-- Dependencies: 276
-- Name: annotations_annotationid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE annotations_annotationid_seq OWNED BY annotations.annotationid;


--
-- TOC entry 277 (class 1259 OID 175188)
-- Name: auth_group; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


--
-- TOC entry 278 (class 1259 OID 175191)
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5607 (class 0 OID 0)
-- Dependencies: 278
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- TOC entry 279 (class 1259 OID 175193)
-- Name: auth_group_permissions; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- TOC entry 280 (class 1259 OID 175196)
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5608 (class 0 OID 0)
-- Dependencies: 280
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- TOC entry 281 (class 1259 OID 175198)
-- Name: auth_permission; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- TOC entry 282 (class 1259 OID 175201)
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5609 (class 0 OID 0)
-- Dependencies: 282
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- TOC entry 283 (class 1259 OID 175203)
-- Name: auth_user; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


--
-- TOC entry 284 (class 1259 OID 175206)
-- Name: auth_user_groups; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- TOC entry 285 (class 1259 OID 175209)
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5610 (class 0 OID 0)
-- Dependencies: 285
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- TOC entry 286 (class 1259 OID 175211)
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5611 (class 0 OID 0)
-- Dependencies: 286
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- TOC entry 287 (class 1259 OID 175213)
-- Name: auth_user_user_permissions; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- TOC entry 288 (class 1259 OID 175216)
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5612 (class 0 OID 0)
-- Dependencies: 288
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- TOC entry 289 (class 1259 OID 175218)
-- Name: authorlists; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE authorlists (
    bridgeid integer NOT NULL,
    citationid integer NOT NULL,
    personid integer NOT NULL,
    authororder integer NOT NULL
);


--
-- TOC entry 290 (class 1259 OID 175221)
-- Name: authorlists_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE authorlists_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5613 (class 0 OID 0)
-- Dependencies: 290
-- Name: authorlists_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE authorlists_bridgeid_seq OWNED BY authorlists.bridgeid;


--
-- TOC entry 291 (class 1259 OID 175223)
-- Name: calibrationactions; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE calibrationactions (
    actionid integer NOT NULL,
    calibrationcheckvalue double precision,
    instrumentoutputvariableid integer NOT NULL,
    calibrationequation character varying(255)
);


--
-- TOC entry 292 (class 1259 OID 175226)
-- Name: calibrationreferenceequipment; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE calibrationreferenceequipment (
    bridgeid integer NOT NULL,
    actionid integer NOT NULL,
    equipmentid integer NOT NULL
);


--
-- TOC entry 293 (class 1259 OID 175229)
-- Name: calibrationreferenceequipment_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE calibrationreferenceequipment_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5614 (class 0 OID 0)
-- Dependencies: 293
-- Name: calibrationreferenceequipment_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE calibrationreferenceequipment_bridgeid_seq OWNED BY calibrationreferenceequipment.bridgeid;


--
-- TOC entry 294 (class 1259 OID 175231)
-- Name: calibrationstandards; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE calibrationstandards (
    bridgeid integer NOT NULL,
    actionid integer NOT NULL,
    referencematerialid integer NOT NULL
);


--
-- TOC entry 295 (class 1259 OID 175234)
-- Name: calibrationstandards_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE calibrationstandards_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5615 (class 0 OID 0)
-- Dependencies: 295
-- Name: calibrationstandards_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE calibrationstandards_bridgeid_seq OWNED BY calibrationstandards.bridgeid;


--
-- TOC entry 296 (class 1259 OID 175236)
-- Name: categoricalresults; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE categoricalresults (
    resultid bigint NOT NULL,
    xlocation double precision,
    xlocationunitsid integer,
    ylocation double precision,
    ylocationunitsid integer,
    zlocation double precision,
    zlocationunitsid integer,
    spatialreferenceid integer,
    qualitycodecv character varying(255) NOT NULL
);


--
-- TOC entry 297 (class 1259 OID 175239)
-- Name: categoricalresultvalueannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE categoricalresultvalueannotations (
    bridgeid integer NOT NULL,
    valueid bigint NOT NULL,
    annotationid integer NOT NULL
);


--
-- TOC entry 298 (class 1259 OID 175242)
-- Name: categoricalresultvalueannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE categoricalresultvalueannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5616 (class 0 OID 0)
-- Dependencies: 298
-- Name: categoricalresultvalueannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE categoricalresultvalueannotations_bridgeid_seq OWNED BY categoricalresultvalueannotations.bridgeid;


--
-- TOC entry 299 (class 1259 OID 175244)
-- Name: categoricalresultvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE categoricalresultvalues (
    valueid bigint NOT NULL,
    resultid bigint NOT NULL,
    datavalue character varying(255) NOT NULL,
    valuedatetime timestamp without time zone NOT NULL,
    valuedatetimeutcoffset integer NOT NULL
);


--
-- TOC entry 300 (class 1259 OID 175247)
-- Name: categoricalresultvalues_valueid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE categoricalresultvalues_valueid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5617 (class 0 OID 0)
-- Dependencies: 300
-- Name: categoricalresultvalues_valueid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE categoricalresultvalues_valueid_seq OWNED BY categoricalresultvalues.valueid;


--
-- TOC entry 301 (class 1259 OID 175249)
-- Name: citationextensionpropertyvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE citationextensionpropertyvalues (
    bridgeid integer NOT NULL,
    citationid integer NOT NULL,
    propertyid integer NOT NULL,
    propertyvalue character varying(255) NOT NULL
);


--
-- TOC entry 302 (class 1259 OID 175252)
-- Name: citationextensionpropertyvalues_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE citationextensionpropertyvalues_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5618 (class 0 OID 0)
-- Dependencies: 302
-- Name: citationextensionpropertyvalues_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE citationextensionpropertyvalues_bridgeid_seq OWNED BY citationextensionpropertyvalues.bridgeid;


--
-- TOC entry 303 (class 1259 OID 175254)
-- Name: citationexternalidentifiers; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE citationexternalidentifiers (
    bridgeid integer NOT NULL,
    citationid integer NOT NULL,
    externalidentifiersystemid integer NOT NULL,
    citationexternalidentifier character varying(255) NOT NULL,
    citationexternalidentifieruri character varying(255)
);


--
-- TOC entry 304 (class 1259 OID 175260)
-- Name: citationexternalidentifiers_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE citationexternalidentifiers_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5619 (class 0 OID 0)
-- Dependencies: 304
-- Name: citationexternalidentifiers_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE citationexternalidentifiers_bridgeid_seq OWNED BY citationexternalidentifiers.bridgeid;


--
-- TOC entry 305 (class 1259 OID 175262)
-- Name: citations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE citations (
    citationid integer NOT NULL,
    title character varying(255) NOT NULL,
    publisher character varying(255) NOT NULL,
    publicationyear integer NOT NULL,
    citationlink character varying(255)
);


--
-- TOC entry 306 (class 1259 OID 175268)
-- Name: citations_citationid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE citations_citationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5620 (class 0 OID 0)
-- Dependencies: 306
-- Name: citations_citationid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE citations_citationid_seq OWNED BY citations.citationid;


--
-- TOC entry 307 (class 1259 OID 175270)
-- Name: cv_actiontype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_actiontype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 308 (class 1259 OID 175276)
-- Name: cv_aggregationstatistic; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_aggregationstatistic (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(1000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 309 (class 1259 OID 175282)
-- Name: cv_annotationtype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_annotationtype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(1000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 310 (class 1259 OID 175288)
-- Name: cv_censorcode; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_censorcode (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(1000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 311 (class 1259 OID 175294)
-- Name: cv_dataqualitytype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_dataqualitytype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(1000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 312 (class 1259 OID 175300)
-- Name: cv_datasettype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_datasettype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(1000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 313 (class 1259 OID 175306)
-- Name: cv_directivetype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_directivetype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(1000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 314 (class 1259 OID 175312)
-- Name: cv_elevationdatum; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_elevationdatum (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(1000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 315 (class 1259 OID 175318)
-- Name: cv_equipmenttype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_equipmenttype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(1000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 316 (class 1259 OID 175324)
-- Name: cv_medium; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_medium (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 317 (class 1259 OID 175330)
-- Name: cv_methodtype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_methodtype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 318 (class 1259 OID 175336)
-- Name: cv_organizationtype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_organizationtype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 319 (class 1259 OID 175342)
-- Name: cv_propertydatatype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_propertydatatype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 320 (class 1259 OID 175348)
-- Name: cv_qualitycode; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_qualitycode (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 321 (class 1259 OID 175354)
-- Name: cv_referencematerialmedium; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_referencematerialmedium (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(1000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 322 (class 1259 OID 175360)
-- Name: cv_relationshiptype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_relationshiptype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 323 (class 1259 OID 175366)
-- Name: cv_resulttype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_resulttype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 324 (class 1259 OID 175372)
-- Name: cv_sampledmedium; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_sampledmedium (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(1000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 325 (class 1259 OID 175378)
-- Name: cv_samplingfeaturegeotype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_samplingfeaturegeotype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 326 (class 1259 OID 175384)
-- Name: cv_samplingfeaturetype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_samplingfeaturetype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(10000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 327 (class 1259 OID 175390)
-- Name: cv_sitetype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_sitetype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 328 (class 1259 OID 175396)
-- Name: cv_spatialoffsettype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_spatialoffsettype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 329 (class 1259 OID 175402)
-- Name: cv_speciation; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_speciation (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 330 (class 1259 OID 175408)
-- Name: cv_specimenmedium; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_specimenmedium (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(1000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 331 (class 1259 OID 175414)
-- Name: cv_specimentype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_specimentype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 332 (class 1259 OID 175420)
-- Name: cv_status; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_status (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 333 (class 1259 OID 175426)
-- Name: cv_taxonomicclassifiertype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_taxonomicclassifiertype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 334 (class 1259 OID 175432)
-- Name: cv_unitstype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_unitstype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 335 (class 1259 OID 175438)
-- Name: cv_variablename; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_variablename (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 336 (class 1259 OID 175444)
-- Name: cv_variabletype; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE cv_variabletype (
    term character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    definition character varying(5000),
    category character varying(255),
    sourcevocabularyuri character varying(255)
);


--
-- TOC entry 337 (class 1259 OID 175450)
-- Name: dataloggerfilecolumns; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE dataloggerfilecolumns (
    dataloggerfilecolumnid integer NOT NULL,
    resultid bigint,
    dataloggerfileid integer NOT NULL,
    instrumentoutputvariableid integer NOT NULL,
    columnlabel character varying(50) NOT NULL,
    columndescription character varying(5000),
    measurementequation character varying(255),
    scaninterval double precision,
    scanintervalunitsid integer,
    recordinginterval double precision,
    recordingintervalunitsid integer,
    aggregationstatisticcv character varying(255)
);


--
-- TOC entry 338 (class 1259 OID 175456)
-- Name: dataloggerfilecolumns_dataloggerfilecolumnid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE dataloggerfilecolumns_dataloggerfilecolumnid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5621 (class 0 OID 0)
-- Dependencies: 338
-- Name: dataloggerfilecolumns_dataloggerfilecolumnid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE dataloggerfilecolumns_dataloggerfilecolumnid_seq OWNED BY dataloggerfilecolumns.dataloggerfilecolumnid;


--
-- TOC entry 339 (class 1259 OID 175458)
-- Name: dataloggerfiles; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE dataloggerfiles (
    dataloggerfileid integer NOT NULL,
    programid integer NOT NULL,
    dataloggerfilename character varying(255) NOT NULL,
    dataloggerfiledescription character varying(5000),
    dataloggerfilelink character varying(255)
);


--
-- TOC entry 340 (class 1259 OID 175464)
-- Name: dataloggerfiles_dataloggerfileid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE dataloggerfiles_dataloggerfileid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5622 (class 0 OID 0)
-- Dependencies: 340
-- Name: dataloggerfiles_dataloggerfileid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE dataloggerfiles_dataloggerfileid_seq OWNED BY dataloggerfiles.dataloggerfileid;


--
-- TOC entry 341 (class 1259 OID 175466)
-- Name: dataloggerprogramfiles; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE dataloggerprogramfiles (
    programid integer NOT NULL,
    affiliationid integer NOT NULL,
    programname character varying(255) NOT NULL,
    programdescription character varying(5000),
    programversion character varying(50),
    programfilelink character varying(255)
);


--
-- TOC entry 342 (class 1259 OID 175472)
-- Name: dataloggerprogramfiles_programid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE dataloggerprogramfiles_programid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5623 (class 0 OID 0)
-- Dependencies: 342
-- Name: dataloggerprogramfiles_programid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE dataloggerprogramfiles_programid_seq OWNED BY dataloggerprogramfiles.programid;


--
-- TOC entry 343 (class 1259 OID 175474)
-- Name: dataquality_dataqualityid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE dataquality_dataqualityid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 344 (class 1259 OID 175476)
-- Name: dataquality; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE dataquality (
    dataqualityid integer DEFAULT nextval('dataquality_dataqualityid_seq'::regclass) NOT NULL,
    dataqualitytypecv character varying(255) NOT NULL,
    dataqualitycode character varying(255) NOT NULL,
    dataqualityvalue double precision,
    dataqualityvalueunitsid integer,
    dataqualitydescription character varying(5000),
    dataqualitylink character varying(255)
);


--
-- TOC entry 345 (class 1259 OID 175483)
-- Name: datasetcitations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE datasetcitations (
    bridgeid integer NOT NULL,
    datasetid integer NOT NULL,
    relationshiptypecv character varying(255) NOT NULL,
    citationid integer NOT NULL
);


--
-- TOC entry 346 (class 1259 OID 175486)
-- Name: datasetcitations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE datasetcitations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5624 (class 0 OID 0)
-- Dependencies: 346
-- Name: datasetcitations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE datasetcitations_bridgeid_seq OWNED BY datasetcitations.bridgeid;


--
-- TOC entry 347 (class 1259 OID 175488)
-- Name: datasets; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE datasets (
    datasetid integer NOT NULL,
    datasetuuid uuid NOT NULL,
    datasettypecv character varying(255) NOT NULL,
    datasetcode character varying(50) NOT NULL,
    datasettitle character varying(255) NOT NULL,
    datasetabstract character varying(5000) NOT NULL
);


--
-- TOC entry 348 (class 1259 OID 175494)
-- Name: datasets_datasetid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE datasets_datasetid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5625 (class 0 OID 0)
-- Dependencies: 348
-- Name: datasets_datasetid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE datasets_datasetid_seq OWNED BY datasets.datasetid;


--
-- TOC entry 349 (class 1259 OID 175496)
-- Name: datasetsresults; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE datasetsresults (
    bridgeid integer NOT NULL,
    datasetid integer NOT NULL,
    resultid bigint NOT NULL
);


--
-- TOC entry 350 (class 1259 OID 175499)
-- Name: datasetsresults_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE datasetsresults_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5626 (class 0 OID 0)
-- Dependencies: 350
-- Name: datasetsresults_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE datasetsresults_bridgeid_seq OWNED BY datasetsresults.bridgeid;


--
-- TOC entry 351 (class 1259 OID 175501)
-- Name: derivationequations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE derivationequations (
    derivationequationid integer NOT NULL,
    derivationequation character varying(255) NOT NULL
);


--
-- TOC entry 352 (class 1259 OID 175504)
-- Name: derivationequations_derivationequationid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE derivationequations_derivationequationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5627 (class 0 OID 0)
-- Dependencies: 352
-- Name: derivationequations_derivationequationid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE derivationequations_derivationequationid_seq OWNED BY derivationequations.derivationequationid;


--
-- TOC entry 353 (class 1259 OID 175506)
-- Name: directives; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE directives (
    directiveid integer NOT NULL,
    directivetypecv character varying(255) NOT NULL,
    directivedescription character varying(500) NOT NULL
);


--
-- TOC entry 354 (class 1259 OID 175512)
-- Name: directives_directiveid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE directives_directiveid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5628 (class 0 OID 0)
-- Dependencies: 354
-- Name: directives_directiveid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE directives_directiveid_seq OWNED BY directives.directiveid;


--
-- TOC entry 355 (class 1259 OID 175514)
-- Name: django_admin_log; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- TOC entry 356 (class 1259 OID 175521)
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5629 (class 0 OID 0)
-- Dependencies: 356
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- TOC entry 357 (class 1259 OID 175523)
-- Name: django_content_type; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL,
    name character varying(50) DEFAULT 'someName'::character varying NOT NULL
);


--
-- TOC entry 358 (class 1259 OID 175527)
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5630 (class 0 OID 0)
-- Dependencies: 358
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- TOC entry 359 (class 1259 OID 175529)
-- Name: django_migrations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- TOC entry 360 (class 1259 OID 175535)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5631 (class 0 OID 0)
-- Dependencies: 360
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- TOC entry 361 (class 1259 OID 175537)
-- Name: django_session; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- TOC entry 362 (class 1259 OID 175543)
-- Name: equipment; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE equipment (
    equipmentid integer NOT NULL,
    equipmentcode character varying(50) NOT NULL,
    equipmentname character varying(255) NOT NULL,
    equipmenttypecv character varying(255) NOT NULL,
    equipmentmodelid integer NOT NULL,
    equipmentserialnumber character varying(50) NOT NULL,
    equipmentownerid integer NOT NULL,
    equipmentvendorid integer NOT NULL,
    equipmentpurchasedate timestamp without time zone NOT NULL,
    equipmentpurchaseordernumber character varying(50),
    equipmentdescription character varying(500),
    equipmentdocumentationlink character varying(255)
);


--
-- TOC entry 363 (class 1259 OID 175549)
-- Name: equipment_equipmentid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE equipment_equipmentid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5632 (class 0 OID 0)
-- Dependencies: 363
-- Name: equipment_equipmentid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE equipment_equipmentid_seq OWNED BY equipment.equipmentid;


--
-- TOC entry 364 (class 1259 OID 175551)
-- Name: equipmentannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE equipmentannotations (
    bridgeid integer NOT NULL,
    equipmentid integer NOT NULL,
    annotationid integer NOT NULL
);


--
-- TOC entry 365 (class 1259 OID 175554)
-- Name: equipmentannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE equipmentannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5633 (class 0 OID 0)
-- Dependencies: 365
-- Name: equipmentannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE equipmentannotations_bridgeid_seq OWNED BY equipmentannotations.bridgeid;


--
-- TOC entry 366 (class 1259 OID 175556)
-- Name: equipmentmodels; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE equipmentmodels (
    equipmentmodelid integer NOT NULL,
    modelmanufacturerid integer NOT NULL,
    modelpartnumber character varying(50),
    modelname character varying(255) NOT NULL,
    modeldescription character varying(5000),
    isinstrument boolean NOT NULL,
    modelspecificationsfilelink character varying(255),
    modellink character varying(255)
);


--
-- TOC entry 367 (class 1259 OID 175562)
-- Name: equipmentmodels_equipmentmodelid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE equipmentmodels_equipmentmodelid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5634 (class 0 OID 0)
-- Dependencies: 367
-- Name: equipmentmodels_equipmentmodelid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE equipmentmodels_equipmentmodelid_seq OWNED BY equipmentmodels.equipmentmodelid;


--
-- TOC entry 368 (class 1259 OID 175564)
-- Name: equipmentused; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE equipmentused (
    bridgeid integer NOT NULL,
    actionid integer NOT NULL,
    equipmentid integer NOT NULL
);


--
-- TOC entry 369 (class 1259 OID 175567)
-- Name: equipmentused_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE equipmentused_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5635 (class 0 OID 0)
-- Dependencies: 369
-- Name: equipmentused_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE equipmentused_bridgeid_seq OWNED BY equipmentused.bridgeid;


--
-- TOC entry 370 (class 1259 OID 175569)
-- Name: extensionproperties; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE extensionproperties (
    propertyid integer NOT NULL,
    propertyname character varying(255) NOT NULL,
    propertydescription character varying(5000),
    propertydatatypecv character varying(255) NOT NULL,
    propertyunitsid integer
);


--
-- TOC entry 371 (class 1259 OID 175575)
-- Name: extensionproperties_propertyid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE extensionproperties_propertyid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5636 (class 0 OID 0)
-- Dependencies: 371
-- Name: extensionproperties_propertyid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE extensionproperties_propertyid_seq OWNED BY extensionproperties.propertyid;


--
-- TOC entry 372 (class 1259 OID 175577)
-- Name: externalidentifiersystemid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE externalidentifiersystemid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 373 (class 1259 OID 175579)
-- Name: externalidentifiersystems; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE externalidentifiersystems (
    externalidentifiersystemid integer DEFAULT nextval('externalidentifiersystemid_seq'::regclass) NOT NULL,
    externalidentifiersystemname character varying(255) NOT NULL,
    identifiersystemorganizationid integer NOT NULL,
    externalidentifiersystemdescription character varying(5000),
    externalidentifiersystemurl character varying(255)
);


--
-- TOC entry 374 (class 1259 OID 175586)
-- Name: featureactions; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE featureactions (
    featureactionid integer NOT NULL,
    samplingfeatureid integer NOT NULL,
    actionid integer NOT NULL
);


--
-- TOC entry 375 (class 1259 OID 175589)
-- Name: featureactions_featureactionid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE featureactions_featureactionid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5637 (class 0 OID 0)
-- Dependencies: 375
-- Name: featureactions_featureactionid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE featureactions_featureactionid_seq OWNED BY featureactions.featureactionid;


--
-- TOC entry 376 (class 1259 OID 175591)
-- Name: instrumentoutputvariables; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE instrumentoutputvariables (
    instrumentoutputvariableid integer NOT NULL,
    modelid integer NOT NULL,
    variableid integer NOT NULL,
    instrumentmethodid integer NOT NULL,
    instrumentresolution character varying(255),
    instrumentaccuracy character varying(255),
    instrumentrawoutputunitsid integer NOT NULL
);


--
-- TOC entry 377 (class 1259 OID 175597)
-- Name: instrumentoutputvariables_instrumentoutputvariableid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE instrumentoutputvariables_instrumentoutputvariableid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5638 (class 0 OID 0)
-- Dependencies: 377
-- Name: instrumentoutputvariables_instrumentoutputvariableid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE instrumentoutputvariables_instrumentoutputvariableid_seq OWNED BY instrumentoutputvariables.instrumentoutputvariableid;


--
-- TOC entry 378 (class 1259 OID 175599)
-- Name: maintenanceactions; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE maintenanceactions (
    actionid integer NOT NULL,
    isfactoryservice boolean NOT NULL,
    maintenancecode character varying(50),
    maintenancereason character varying(500)
);


--
-- TOC entry 379 (class 1259 OID 175605)
-- Name: measurementresults; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE measurementresults (
    resultid bigint NOT NULL,
    xlocation double precision,
    xlocationunitsid integer,
    ylocation double precision,
    ylocationunitsid integer,
    zlocation double precision,
    zlocationunitsid integer,
    spatialreferenceid integer,
    censorcodecv character varying(255) NOT NULL,
    qualitycodecv character varying(255) NOT NULL,
    aggregationstatisticcv character varying(255) NOT NULL,
    timeaggregationinterval double precision NOT NULL,
    timeaggregationintervalunitsid integer NOT NULL
);


--
-- TOC entry 380 (class 1259 OID 175611)
-- Name: measurementresultvalueannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE measurementresultvalueannotations (
    bridgeid integer NOT NULL,
    valueid bigint NOT NULL,
    annotationid integer NOT NULL
);


--
-- TOC entry 381 (class 1259 OID 175614)
-- Name: measurementresultvalueannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE measurementresultvalueannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5639 (class 0 OID 0)
-- Dependencies: 381
-- Name: measurementresultvalueannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE measurementresultvalueannotations_bridgeid_seq OWNED BY measurementresultvalueannotations.bridgeid;


--
-- TOC entry 382 (class 1259 OID 175616)
-- Name: measurementresultvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE measurementresultvalues (
    valueid bigint NOT NULL,
    resultid bigint NOT NULL,
    datavalue double precision NOT NULL,
    valuedatetime timestamp without time zone NOT NULL,
    valuedatetimeutcoffset integer NOT NULL
);


--
-- TOC entry 383 (class 1259 OID 175619)
-- Name: measurementresultvalues_valueid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE measurementresultvalues_valueid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5640 (class 0 OID 0)
-- Dependencies: 383
-- Name: measurementresultvalues_valueid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE measurementresultvalues_valueid_seq OWNED BY measurementresultvalues.valueid;


--
-- TOC entry 384 (class 1259 OID 175621)
-- Name: methodannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE methodannotations (
    bridgeid integer NOT NULL,
    methodid integer NOT NULL,
    annotationid integer NOT NULL
);


--
-- TOC entry 385 (class 1259 OID 175624)
-- Name: methodannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE methodannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5641 (class 0 OID 0)
-- Dependencies: 385
-- Name: methodannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE methodannotations_bridgeid_seq OWNED BY methodannotations.bridgeid;


--
-- TOC entry 386 (class 1259 OID 175626)
-- Name: methodcitations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE methodcitations (
    bridgeid integer NOT NULL,
    methodid integer NOT NULL,
    relationshiptypecv character varying(255) NOT NULL,
    citationid integer NOT NULL
);


--
-- TOC entry 387 (class 1259 OID 175629)
-- Name: methodcitations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE methodcitations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5642 (class 0 OID 0)
-- Dependencies: 387
-- Name: methodcitations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE methodcitations_bridgeid_seq OWNED BY methodcitations.bridgeid;


--
-- TOC entry 388 (class 1259 OID 175631)
-- Name: methodextensionpropertyvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE methodextensionpropertyvalues (
    bridgeid integer NOT NULL,
    methodid integer NOT NULL,
    propertyid integer NOT NULL,
    propertyvalue character varying(255) NOT NULL
);


--
-- TOC entry 389 (class 1259 OID 175634)
-- Name: methodextensionpropertyvalues_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE methodextensionpropertyvalues_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5643 (class 0 OID 0)
-- Dependencies: 389
-- Name: methodextensionpropertyvalues_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE methodextensionpropertyvalues_bridgeid_seq OWNED BY methodextensionpropertyvalues.bridgeid;


--
-- TOC entry 390 (class 1259 OID 175636)
-- Name: methodexternalidentifiers; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE methodexternalidentifiers (
    bridgeid integer NOT NULL,
    methodid integer NOT NULL,
    externalidentifiersystemid integer NOT NULL,
    methodexternalidentifier character varying(255) NOT NULL,
    methodexternalidentifieruri character varying(255)
);


--
-- TOC entry 391 (class 1259 OID 175642)
-- Name: methodexternalidentifiers_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE methodexternalidentifiers_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5644 (class 0 OID 0)
-- Dependencies: 391
-- Name: methodexternalidentifiers_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE methodexternalidentifiers_bridgeid_seq OWNED BY methodexternalidentifiers.bridgeid;


--
-- TOC entry 392 (class 1259 OID 175644)
-- Name: methods; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE methods (
    methodid integer NOT NULL,
    methodtypecv character varying(255) NOT NULL,
    methodcode character varying(50) NOT NULL,
    methodname character varying(255) NOT NULL,
    methoddescription character varying(5000),
    methodlink character varying(255),
    organizationid integer
);


--
-- TOC entry 393 (class 1259 OID 175650)
-- Name: methods_methodid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE methods_methodid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5645 (class 0 OID 0)
-- Dependencies: 393
-- Name: methods_methodid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE methods_methodid_seq OWNED BY methods.methodid;


--
-- TOC entry 394 (class 1259 OID 175652)
-- Name: modelaffiliations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE modelaffiliations (
    bridgeid integer NOT NULL,
    modelid integer NOT NULL,
    affiliationid integer NOT NULL,
    isprimary boolean NOT NULL,
    roledescription character varying(5000)
);


--
-- TOC entry 395 (class 1259 OID 175658)
-- Name: modelaffiliations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE modelaffiliations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5646 (class 0 OID 0)
-- Dependencies: 395
-- Name: modelaffiliations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE modelaffiliations_bridgeid_seq OWNED BY modelaffiliations.bridgeid;


--
-- TOC entry 396 (class 1259 OID 175660)
-- Name: models; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE models (
    modelid integer NOT NULL,
    modelcode character varying(50) NOT NULL,
    modelname character varying(255) NOT NULL,
    modeldescription character varying(5000),
    version character varying(255),
    modellink character varying(255)
);


--
-- TOC entry 397 (class 1259 OID 175666)
-- Name: models_modelid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE models_modelid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5647 (class 0 OID 0)
-- Dependencies: 397
-- Name: models_modelid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE models_modelid_seq OWNED BY models.modelid;


--
-- TOC entry 398 (class 1259 OID 175668)
-- Name: organizations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE organizations (
    organizationid integer NOT NULL,
    organizationtypecv character varying(255) NOT NULL,
    organizationcode character varying(50) NOT NULL,
    organizationname character varying(255) NOT NULL,
    organizationdescription character varying(5000),
    organizationlink character varying(255),
    parentorganizationid integer
);


--
-- TOC entry 399 (class 1259 OID 175674)
-- Name: organizations_organizationid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE organizations_organizationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5648 (class 0 OID 0)
-- Dependencies: 399
-- Name: organizations_organizationid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE organizations_organizationid_seq OWNED BY organizations.organizationid;


--
-- TOC entry 400 (class 1259 OID 175676)
-- Name: people; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE people (
    personid integer NOT NULL,
    personfirstname character varying(255) NOT NULL,
    personmiddlename character varying(255),
    personlastname character varying(255) NOT NULL
);


--
-- TOC entry 401 (class 1259 OID 175682)
-- Name: people_personid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE people_personid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5649 (class 0 OID 0)
-- Dependencies: 401
-- Name: people_personid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE people_personid_seq OWNED BY people.personid;


--
-- TOC entry 402 (class 1259 OID 175684)
-- Name: personexternalidentifiers; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE personexternalidentifiers (
    bridgeid integer NOT NULL,
    personid integer NOT NULL,
    externalidentifiersystemid integer NOT NULL,
    personexternalidentifier character varying(255) NOT NULL,
    personexternalidentifieruri character varying(255)
);


--
-- TOC entry 403 (class 1259 OID 175690)
-- Name: personexternalidentifiers_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE personexternalidentifiers_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5650 (class 0 OID 0)
-- Dependencies: 403
-- Name: personexternalidentifiers_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE personexternalidentifiers_bridgeid_seq OWNED BY personexternalidentifiers.bridgeid;


--
-- TOC entry 404 (class 1259 OID 175692)
-- Name: pointcoverageresults; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE pointcoverageresults (
    resultid bigint NOT NULL,
    zlocation double precision,
    zlocationunitsid integer,
    spatialreferenceid integer,
    intendedxspacing double precision,
    intendedxspacingunitsid integer,
    intendedyspacing double precision,
    intendedyspacingunitsid integer,
    aggregationstatisticcv character varying(255) NOT NULL,
    timeaggregationinterval double precision NOT NULL,
    timeaggregationintervalunitsid integer NOT NULL
);


--
-- TOC entry 405 (class 1259 OID 175695)
-- Name: pointcoverageresultvalueannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE pointcoverageresultvalueannotations (
    bridgeid bigint NOT NULL,
    valueid bigint NOT NULL,
    annotationid integer NOT NULL
);


--
-- TOC entry 406 (class 1259 OID 175698)
-- Name: pointcoverageresultvalueannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE pointcoverageresultvalueannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5651 (class 0 OID 0)
-- Dependencies: 406
-- Name: pointcoverageresultvalueannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE pointcoverageresultvalueannotations_bridgeid_seq OWNED BY pointcoverageresultvalueannotations.bridgeid;


--
-- TOC entry 407 (class 1259 OID 175700)
-- Name: pointcoverageresultvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE pointcoverageresultvalues (
    valueid bigint NOT NULL,
    resultid bigint NOT NULL,
    datavalue bigint NOT NULL,
    valuedatetime timestamp without time zone NOT NULL,
    valuedatetimeutcoffset integer NOT NULL,
    xlocation double precision NOT NULL,
    xlocationunitsid integer NOT NULL,
    ylocation double precision NOT NULL,
    ylocationunitsid integer NOT NULL,
    censorcodecv character varying(255) NOT NULL,
    qualitycodecv character varying(255) NOT NULL
);


--
-- TOC entry 408 (class 1259 OID 175706)
-- Name: pointcoverageresultvalues_valueid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE pointcoverageresultvalues_valueid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5652 (class 0 OID 0)
-- Dependencies: 408
-- Name: pointcoverageresultvalues_valueid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE pointcoverageresultvalues_valueid_seq OWNED BY pointcoverageresultvalues.valueid;


--
-- TOC entry 409 (class 1259 OID 175708)
-- Name: processdataloggerfile_id_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE processdataloggerfile_id_seq
    START WITH 1
    INCREMENT BY 1
    MINVALUE 0
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 410 (class 1259 OID 175710)
-- Name: processinglevels; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE processinglevels (
    processinglevelid integer NOT NULL,
    processinglevelcode character varying(50) NOT NULL,
    definition character varying(5000),
    explanation character varying(5000)
);


--
-- TOC entry 411 (class 1259 OID 175716)
-- Name: processinglevels_processinglevelid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE processinglevels_processinglevelid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5653 (class 0 OID 0)
-- Dependencies: 411
-- Name: processinglevels_processinglevelid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE processinglevels_processinglevelid_seq OWNED BY processinglevels.processinglevelid;


--
-- TOC entry 412 (class 1259 OID 175718)
-- Name: profileresults; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE profileresults (
    resultid bigint NOT NULL,
    xlocation double precision,
    xlocationunitsid integer,
    ylocation double precision,
    ylocationunitsid integer,
    spatialreferenceid integer,
    intendedzspacing double precision,
    intendedzspacingunitsid integer,
    intendedtimespacing double precision,
    intendedtimespacingunitsid integer,
    aggregationstatisticcv character varying(255) NOT NULL
);


--
-- TOC entry 413 (class 1259 OID 175721)
-- Name: profileresultvalueannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE profileresultvalueannotations (
    bridgeid integer NOT NULL,
    valueid bigint NOT NULL,
    annotationid integer NOT NULL
);


--
-- TOC entry 414 (class 1259 OID 175724)
-- Name: profileresultvalueannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE profileresultvalueannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5654 (class 0 OID 0)
-- Dependencies: 414
-- Name: profileresultvalueannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE profileresultvalueannotations_bridgeid_seq OWNED BY profileresultvalueannotations.bridgeid;


--
-- TOC entry 415 (class 1259 OID 175726)
-- Name: profileresultvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE profileresultvalues (
    valueid bigint NOT NULL,
    resultid bigint NOT NULL,
    datavalue double precision NOT NULL,
    valuedatetime timestamp without time zone NOT NULL,
    valuedatetimeutcoffset integer NOT NULL,
    zlocation double precision NOT NULL,
    zaggregationinterval double precision NOT NULL,
    zlocationunitsid integer NOT NULL,
    censorcodecv character varying(255) NOT NULL,
    qualitycodecv character varying(255) NOT NULL,
    timeaggregationinterval double precision NOT NULL,
    timeaggregationintervalunitsid integer NOT NULL
);


--
-- TOC entry 416 (class 1259 OID 175732)
-- Name: profileresultvalues_valueid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE profileresultvalues_valueid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5655 (class 0 OID 0)
-- Dependencies: 416
-- Name: profileresultvalues_valueid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE profileresultvalues_valueid_seq OWNED BY profileresultvalues.valueid;


--
-- TOC entry 417 (class 1259 OID 175734)
-- Name: referencematerialexternalidentifiers; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE referencematerialexternalidentifiers (
    bridgeid integer NOT NULL,
    referencematerialid integer NOT NULL,
    externalidentifiersystemid integer NOT NULL,
    referencematerialexternalidentifier character varying(255) NOT NULL,
    referencematerialexternalidentifieruri character varying(255)
);


--
-- TOC entry 418 (class 1259 OID 175740)
-- Name: referencematerialexternalidentifiers_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE referencematerialexternalidentifiers_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5656 (class 0 OID 0)
-- Dependencies: 418
-- Name: referencematerialexternalidentifiers_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE referencematerialexternalidentifiers_bridgeid_seq OWNED BY referencematerialexternalidentifiers.bridgeid;


--
-- TOC entry 419 (class 1259 OID 175742)
-- Name: referencematerials; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE referencematerials (
    referencematerialid integer NOT NULL,
    referencematerialmediumcv character varying(255) NOT NULL,
    referencematerialorganizationid integer NOT NULL,
    referencematerialcode character varying(50) NOT NULL,
    referencemateriallotcode character varying(255),
    referencematerialpurchasedate timestamp without time zone,
    referencematerialexpirationdate timestamp without time zone,
    referencematerialcertificatelink character varying(255),
    samplingfeatureid integer
);


--
-- TOC entry 420 (class 1259 OID 175748)
-- Name: referencematerialvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE referencematerialvalues (
    referencematerialvalueid integer NOT NULL,
    referencematerialid integer NOT NULL,
    referencematerialvalue double precision NOT NULL,
    referencematerialaccuracy double precision,
    variableid integer NOT NULL,
    unitsid integer NOT NULL,
    citationid integer NOT NULL
);


--
-- TOC entry 421 (class 1259 OID 175751)
-- Name: relatedactions; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE relatedactions (
    relationid integer NOT NULL,
    actionid integer NOT NULL,
    relationshiptypecv character varying(255) NOT NULL,
    relatedactionid integer NOT NULL
);


--
-- TOC entry 422 (class 1259 OID 175754)
-- Name: relatedactions_relationid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE relatedactions_relationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5657 (class 0 OID 0)
-- Dependencies: 422
-- Name: relatedactions_relationid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE relatedactions_relationid_seq OWNED BY relatedactions.relationid;


--
-- TOC entry 423 (class 1259 OID 175756)
-- Name: relatedannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE relatedannotations (
    relationid integer NOT NULL,
    annotationid integer NOT NULL,
    relationshiptypecv character varying(255) NOT NULL,
    relatedannotationid integer NOT NULL
);


--
-- TOC entry 424 (class 1259 OID 175759)
-- Name: relatedannotations_relationid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE relatedannotations_relationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5658 (class 0 OID 0)
-- Dependencies: 424
-- Name: relatedannotations_relationid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE relatedannotations_relationid_seq OWNED BY relatedannotations.relationid;


--
-- TOC entry 425 (class 1259 OID 175761)
-- Name: relatedcitations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE relatedcitations (
    relationid integer NOT NULL,
    citationid integer NOT NULL,
    relationshiptypecv character varying(255) NOT NULL,
    relatedcitationid integer NOT NULL
);


--
-- TOC entry 426 (class 1259 OID 175764)
-- Name: relatedcitations_relationid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE relatedcitations_relationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5659 (class 0 OID 0)
-- Dependencies: 426
-- Name: relatedcitations_relationid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE relatedcitations_relationid_seq OWNED BY relatedcitations.relationid;


--
-- TOC entry 427 (class 1259 OID 175766)
-- Name: relateddatasets; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE relateddatasets (
    relationid integer NOT NULL,
    datasetid integer NOT NULL,
    relationshiptypecv character varying(255) NOT NULL,
    relateddatasetid integer NOT NULL,
    versioncode character varying(50)
);


--
-- TOC entry 428 (class 1259 OID 175769)
-- Name: relateddatasets_relationid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE relateddatasets_relationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5660 (class 0 OID 0)
-- Dependencies: 428
-- Name: relateddatasets_relationid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE relateddatasets_relationid_seq OWNED BY relateddatasets.relationid;


--
-- TOC entry 429 (class 1259 OID 175771)
-- Name: relatedequipment; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE relatedequipment (
    relationid integer NOT NULL,
    equipmentid integer NOT NULL,
    relationshiptypecv character varying(255) NOT NULL,
    relatedequipmentid integer NOT NULL,
    relationshipstartdatetime timestamp without time zone NOT NULL,
    relationshipstartdatetimeutcoffset integer NOT NULL,
    relationshipenddatetime timestamp without time zone,
    relationshipenddatetimeutcoffset integer
);


--
-- TOC entry 430 (class 1259 OID 175774)
-- Name: relatedequipment_relationid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE relatedequipment_relationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5661 (class 0 OID 0)
-- Dependencies: 430
-- Name: relatedequipment_relationid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE relatedequipment_relationid_seq OWNED BY relatedequipment.relationid;


--
-- TOC entry 431 (class 1259 OID 175776)
-- Name: relatedfeatures; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE relatedfeatures (
    relationid integer NOT NULL,
    samplingfeatureid integer NOT NULL,
    relationshiptypecv character varying(255) NOT NULL,
    relatedfeatureid integer NOT NULL,
    spatialoffsetid integer
);


--
-- TOC entry 432 (class 1259 OID 175779)
-- Name: relatedfeatures_relationid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE relatedfeatures_relationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5662 (class 0 OID 0)
-- Dependencies: 432
-- Name: relatedfeatures_relationid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE relatedfeatures_relationid_seq OWNED BY relatedfeatures.relationid;


--
-- TOC entry 433 (class 1259 OID 175781)
-- Name: relatedmodels; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE relatedmodels (
    relatedid integer NOT NULL,
    modelid integer NOT NULL,
    relationshiptypecv character varying(255) NOT NULL,
    relatedmodelid integer NOT NULL
);


--
-- TOC entry 434 (class 1259 OID 175784)
-- Name: relatedmodels_relatedid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE relatedmodels_relatedid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5663 (class 0 OID 0)
-- Dependencies: 434
-- Name: relatedmodels_relatedid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE relatedmodels_relatedid_seq OWNED BY relatedmodels.relatedid;


--
-- TOC entry 435 (class 1259 OID 175786)
-- Name: relatedresults; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE relatedresults (
    relationid integer NOT NULL,
    resultid bigint NOT NULL,
    relationshiptypecv character varying(255) NOT NULL,
    relatedresultid bigint NOT NULL,
    versioncode character varying(50),
    relatedresultsequencenumber integer
);


--
-- TOC entry 436 (class 1259 OID 175789)
-- Name: relatedresults_relationid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE relatedresults_relationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5664 (class 0 OID 0)
-- Dependencies: 436
-- Name: relatedresults_relationid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE relatedresults_relationid_seq OWNED BY relatedresults.relationid;


--
-- TOC entry 437 (class 1259 OID 175791)
-- Name: resultannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE resultannotations (
    bridgeid integer NOT NULL,
    resultid bigint NOT NULL,
    annotationid integer NOT NULL,
    begindatetime timestamp without time zone NOT NULL,
    enddatetime timestamp without time zone NOT NULL
);


--
-- TOC entry 438 (class 1259 OID 175794)
-- Name: resultannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE resultannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5665 (class 0 OID 0)
-- Dependencies: 438
-- Name: resultannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE resultannotations_bridgeid_seq OWNED BY resultannotations.bridgeid;


--
-- TOC entry 439 (class 1259 OID 175796)
-- Name: resultderivationequations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE resultderivationequations (
    resultid bigint NOT NULL,
    derivationequationid integer NOT NULL
);


--
-- TOC entry 440 (class 1259 OID 175799)
-- Name: resultextensionpropertyvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE resultextensionpropertyvalues (
    bridgeid integer NOT NULL,
    resultid bigint NOT NULL,
    propertyid integer NOT NULL,
    propertyvalue character varying(255) NOT NULL
);


--
-- TOC entry 441 (class 1259 OID 175802)
-- Name: resultextensionpropertyvalues_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE resultextensionpropertyvalues_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5666 (class 0 OID 0)
-- Dependencies: 441
-- Name: resultextensionpropertyvalues_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE resultextensionpropertyvalues_bridgeid_seq OWNED BY resultextensionpropertyvalues.bridgeid;


--
-- TOC entry 442 (class 1259 OID 175804)
-- Name: resultnormalizationvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE resultnormalizationvalues (
    resultid bigint NOT NULL,
    normalizedbyreferencematerialvalueid integer NOT NULL
);


--
-- TOC entry 443 (class 1259 OID 175807)
-- Name: results; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE results (
    resultid bigint NOT NULL,
    resultuuid uuid NOT NULL,
    featureactionid integer NOT NULL,
    resulttypecv character varying(255) NOT NULL,
    variableid integer NOT NULL,
    unitsid integer NOT NULL,
    taxonomicclassifierid integer,
    processinglevelid integer NOT NULL,
    resultdatetime timestamp without time zone,
    resultdatetimeutcoffset bigint,
    validdatetime timestamp without time zone,
    validdatetimeutcoffset bigint,
    statuscv character varying(255),
    sampledmediumcv character varying(255) NOT NULL,
    valuecount integer NOT NULL
);


--
-- TOC entry 444 (class 1259 OID 175813)
-- Name: results_resultid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE results_resultid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5667 (class 0 OID 0)
-- Dependencies: 444
-- Name: results_resultid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE results_resultid_seq OWNED BY results.resultid;


--
-- TOC entry 445 (class 1259 OID 175815)
-- Name: resultsdataquality; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE resultsdataquality (
    bridgeid integer NOT NULL,
    resultid bigint NOT NULL,
    dataqualityid integer NOT NULL
);


--
-- TOC entry 446 (class 1259 OID 175818)
-- Name: resultsdataquality_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE resultsdataquality_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5668 (class 0 OID 0)
-- Dependencies: 446
-- Name: resultsdataquality_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE resultsdataquality_bridgeid_seq OWNED BY resultsdataquality.bridgeid;


--
-- TOC entry 447 (class 1259 OID 175820)
-- Name: samplingfeatureannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE samplingfeatureannotations (
    bridgeid integer NOT NULL,
    samplingfeatureid integer NOT NULL,
    annotationid integer NOT NULL
);


--
-- TOC entry 448 (class 1259 OID 175823)
-- Name: samplingfeatureannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE samplingfeatureannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5669 (class 0 OID 0)
-- Dependencies: 448
-- Name: samplingfeatureannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE samplingfeatureannotations_bridgeid_seq OWNED BY samplingfeatureannotations.bridgeid;


--
-- TOC entry 449 (class 1259 OID 175825)
-- Name: samplingfeatureextensionpropertyvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE samplingfeatureextensionpropertyvalues (
    bridgeid integer NOT NULL,
    samplingfeatureid integer NOT NULL,
    propertyid integer NOT NULL,
    propertyvalue character varying(255) NOT NULL
);


--
-- TOC entry 450 (class 1259 OID 175828)
-- Name: samplingfeatureextensionpropertyvalues_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE samplingfeatureextensionpropertyvalues_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5670 (class 0 OID 0)
-- Dependencies: 450
-- Name: samplingfeatureextensionpropertyvalues_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE samplingfeatureextensionpropertyvalues_bridgeid_seq OWNED BY samplingfeatureextensionpropertyvalues.bridgeid;


--
-- TOC entry 451 (class 1259 OID 175830)
-- Name: samplingfeatureexternalidentifiers; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE samplingfeatureexternalidentifiers (
    bridgeid integer NOT NULL,
    samplingfeatureid integer NOT NULL,
    externalidentifiersystemid integer NOT NULL,
    samplingfeatureexternalidentifier character varying(255) NOT NULL,
    samplingfeatureexternalidentifieruri character varying(255)
);


--
-- TOC entry 452 (class 1259 OID 175836)
-- Name: samplingfeatureexternalidentifiers_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE samplingfeatureexternalidentifiers_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5671 (class 0 OID 0)
-- Dependencies: 452
-- Name: samplingfeatureexternalidentifiers_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE samplingfeatureexternalidentifiers_bridgeid_seq OWNED BY samplingfeatureexternalidentifiers.bridgeid;


--
-- TOC entry 453 (class 1259 OID 175838)
-- Name: samplingfeatures; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE samplingfeatures (
    samplingfeatureid integer NOT NULL,
    samplingfeatureuuid uuid NOT NULL,
    samplingfeaturetypecv character varying(255) NOT NULL,
    samplingfeaturecode character varying(50) NOT NULL,
    samplingfeaturename character varying(255),
    samplingfeaturedescription character varying(5000),
    samplingfeaturegeotypecv character varying(255),
    featuregeometry public.geometry,
    elevation_m double precision,
    elevationdatumcv character varying(255),
    featuregeometrywkt character varying(8000)[]
);


--
-- TOC entry 454 (class 1259 OID 175844)
-- Name: samplingfeatures_samplingfeatureid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE samplingfeatures_samplingfeatureid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5672 (class 0 OID 0)
-- Dependencies: 454
-- Name: samplingfeatures_samplingfeatureid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE samplingfeatures_samplingfeatureid_seq OWNED BY samplingfeatures.samplingfeatureid;


--
-- TOC entry 455 (class 1259 OID 175846)
-- Name: sectionresults; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE sectionresults (
    resultid bigint NOT NULL,
    ylocation double precision,
    ylocationunitsid integer,
    spatialreferenceid integer,
    intendedxspacing double precision,
    intendedxspacingunitsid integer,
    intendedzspacing double precision,
    intendedzspacingunitsid integer,
    intendedtimespacing double precision,
    intendedtimespacingunitsid integer,
    aggregationstatisticcv character varying(255) NOT NULL
);


--
-- TOC entry 456 (class 1259 OID 175849)
-- Name: sectionresultvalueannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE sectionresultvalueannotations (
    bridgeid integer NOT NULL,
    valueid bigint NOT NULL,
    annotationid integer NOT NULL
);


--
-- TOC entry 457 (class 1259 OID 175852)
-- Name: sectionresultvalueannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE sectionresultvalueannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5673 (class 0 OID 0)
-- Dependencies: 457
-- Name: sectionresultvalueannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE sectionresultvalueannotations_bridgeid_seq OWNED BY sectionresultvalueannotations.bridgeid;


--
-- TOC entry 458 (class 1259 OID 175854)
-- Name: sectionresultvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE sectionresultvalues (
    valueid bigint NOT NULL,
    resultid bigint NOT NULL,
    datavalue double precision NOT NULL,
    valuedatetime bigint NOT NULL,
    valuedatetimeutcoffset bigint NOT NULL,
    xlocation double precision NOT NULL,
    xaggregationinterval double precision NOT NULL,
    xlocationunitsid integer NOT NULL,
    zlocation bigint NOT NULL,
    zaggregationinterval double precision NOT NULL,
    zlocationunitsid integer NOT NULL,
    censorcodecv character varying(255) NOT NULL,
    qualitycodecv character varying(255) NOT NULL,
    aggregationstatisticcv character varying(255) NOT NULL,
    timeaggregationinterval double precision NOT NULL,
    timeaggregationintervalunitsid integer NOT NULL
);


--
-- TOC entry 459 (class 1259 OID 175860)
-- Name: sectionresultvalues_valueid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE sectionresultvalues_valueid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5674 (class 0 OID 0)
-- Dependencies: 459
-- Name: sectionresultvalues_valueid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE sectionresultvalues_valueid_seq OWNED BY sectionresultvalues.valueid;


--
-- TOC entry 460 (class 1259 OID 175862)
-- Name: simulations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE simulations (
    simulationid integer NOT NULL,
    actionid integer NOT NULL,
    simulationname character varying(255) NOT NULL,
    simulationdescription character varying(5000),
    simulationstartdatetime timestamp without time zone NOT NULL,
    simulationstartdatetimeutcoffset integer NOT NULL,
    simulationenddatetime timestamp without time zone NOT NULL,
    simulationenddatetimeutcoffset integer NOT NULL,
    timestepvalue double precision NOT NULL,
    timestepunitsid integer NOT NULL,
    inputdatasetid integer,
    modelid integer NOT NULL
);


--
-- TOC entry 461 (class 1259 OID 175868)
-- Name: simulations_simulationid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE simulations_simulationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5675 (class 0 OID 0)
-- Dependencies: 461
-- Name: simulations_simulationid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE simulations_simulationid_seq OWNED BY simulations.simulationid;


--
-- TOC entry 462 (class 1259 OID 175870)
-- Name: sites; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE sites (
    samplingfeatureid integer NOT NULL,
    sitetypecv character varying(255) NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    spatialreferenceid integer NOT NULL
);


--
-- TOC entry 463 (class 1259 OID 175873)
-- Name: spatialoffsets; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE spatialoffsets (
    spatialoffsetid integer NOT NULL,
    spatialoffsettypecv character varying(255) NOT NULL,
    offset1value double precision NOT NULL,
    offset1unitid integer NOT NULL,
    offset2value double precision,
    offset2unitid integer,
    offset3value double precision,
    offset3unitid integer
);


--
-- TOC entry 464 (class 1259 OID 175876)
-- Name: spatialreferenceexternalidentifiers; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE spatialreferenceexternalidentifiers (
    bridgeid integer NOT NULL,
    spatialreferenceid integer NOT NULL,
    externalidentifiersystemid integer NOT NULL,
    spatialreferenceexternalidentifier character varying(255) NOT NULL,
    spatialreferenceexternalidentifieruri character varying(255)
);


--
-- TOC entry 465 (class 1259 OID 175882)
-- Name: spatialreferenceexternalidentifiers_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE spatialreferenceexternalidentifiers_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5676 (class 0 OID 0)
-- Dependencies: 465
-- Name: spatialreferenceexternalidentifiers_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE spatialreferenceexternalidentifiers_bridgeid_seq OWNED BY spatialreferenceexternalidentifiers.bridgeid;


--
-- TOC entry 466 (class 1259 OID 175884)
-- Name: spatialreferences; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE spatialreferences (
    spatialreferenceid integer NOT NULL,
    srscode character varying(50),
    srsname character varying(255) NOT NULL,
    srsdescription character varying(5000),
    srslink character varying(255)
);


--
-- TOC entry 467 (class 1259 OID 175890)
-- Name: spatialreferences_spatialreferenceid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE spatialreferences_spatialreferenceid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5677 (class 0 OID 0)
-- Dependencies: 467
-- Name: spatialreferences_spatialreferenceid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE spatialreferences_spatialreferenceid_seq OWNED BY spatialreferences.spatialreferenceid;


--
-- TOC entry 468 (class 1259 OID 175892)
-- Name: specimenbatchpostions; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE specimenbatchpostions (
    featureactionid integer NOT NULL,
    batchpositionnumber integer NOT NULL,
    batchpositionlabel character varying(255)
);


--
-- TOC entry 469 (class 1259 OID 175895)
-- Name: specimens; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE specimens (
    samplingfeatureid integer NOT NULL,
    specimentypecv character varying(255) NOT NULL,
    specimenmediumcv character varying(255) NOT NULL,
    isfieldspecimen boolean NOT NULL
);


--
-- TOC entry 470 (class 1259 OID 175901)
-- Name: specimentaxonomicclassifiers; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE specimentaxonomicclassifiers (
    bridgeid integer NOT NULL,
    samplingfeatureid integer NOT NULL,
    taxonomicclassifierid integer NOT NULL,
    citationid integer
);


--
-- TOC entry 471 (class 1259 OID 175904)
-- Name: specimentaxonomicclassifiers_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE specimentaxonomicclassifiers_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5678 (class 0 OID 0)
-- Dependencies: 471
-- Name: specimentaxonomicclassifiers_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE specimentaxonomicclassifiers_bridgeid_seq OWNED BY specimentaxonomicclassifiers.bridgeid;


--
-- TOC entry 472 (class 1259 OID 175906)
-- Name: spectraresults; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE spectraresults (
    resultid bigint NOT NULL,
    xlocation double precision,
    xlocationunitsid integer,
    ylocation double precision,
    ylocationunitsid integer,
    zlocation double precision,
    zlocationunitsid integer,
    spatialreferenceid integer,
    intendedwavelengthspacing double precision,
    intendedwavelengthspacingunitsid integer,
    aggregationstatisticcv character varying(255) NOT NULL
);


--
-- TOC entry 473 (class 1259 OID 175909)
-- Name: spectraresultvalueannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE spectraresultvalueannotations (
    bridgeid integer NOT NULL,
    valueid bigint NOT NULL,
    annotationid integer NOT NULL
);


--
-- TOC entry 474 (class 1259 OID 175912)
-- Name: spectraresultvalueannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE spectraresultvalueannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5679 (class 0 OID 0)
-- Dependencies: 474
-- Name: spectraresultvalueannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE spectraresultvalueannotations_bridgeid_seq OWNED BY spectraresultvalueannotations.bridgeid;


--
-- TOC entry 475 (class 1259 OID 175914)
-- Name: spectraresultvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE spectraresultvalues (
    valueid bigint NOT NULL,
    resultid bigint NOT NULL,
    datavalue double precision NOT NULL,
    valuedatetime timestamp without time zone NOT NULL,
    valuedatetimeutcoffset integer NOT NULL,
    excitationwavelength double precision NOT NULL,
    emissionwavelength double precision NOT NULL,
    wavelengthunitsid integer NOT NULL,
    censorcodecv character varying(255) NOT NULL,
    qualitycodecv character varying(255) NOT NULL,
    timeaggregationinterval double precision NOT NULL,
    timeaggregationintervalunitsid integer NOT NULL
);


--
-- TOC entry 476 (class 1259 OID 175920)
-- Name: spectraresultvalues_valueid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE spectraresultvalues_valueid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5680 (class 0 OID 0)
-- Dependencies: 476
-- Name: spectraresultvalues_valueid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE spectraresultvalues_valueid_seq OWNED BY spectraresultvalues.valueid;


--
-- TOC entry 477 (class 1259 OID 175922)
-- Name: taxonomicclassifierexternalidentifiers; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE taxonomicclassifierexternalidentifiers (
    bridgeid integer NOT NULL,
    taxonomicclassifierid integer NOT NULL,
    externalidentifiersystemid integer NOT NULL,
    taxonomicclassifierexternalidentifier character varying(255) NOT NULL,
    taxonomicclassifierexternalidentifieruri character varying(255)
);


--
-- TOC entry 478 (class 1259 OID 175928)
-- Name: taxonomicclassifierexternalidentifiers_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE taxonomicclassifierexternalidentifiers_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5681 (class 0 OID 0)
-- Dependencies: 478
-- Name: taxonomicclassifierexternalidentifiers_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE taxonomicclassifierexternalidentifiers_bridgeid_seq OWNED BY taxonomicclassifierexternalidentifiers.bridgeid;


--
-- TOC entry 479 (class 1259 OID 175930)
-- Name: taxonomicclassifiers; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE taxonomicclassifiers (
    taxonomicclassifierid integer NOT NULL,
    taxonomicclassifiertypecv character varying(255) NOT NULL,
    taxonomicclassifiername character varying(255) NOT NULL,
    taxonomicclassifiercommonname character varying(255),
    taxonomicclassifierdescription character varying(5000),
    parenttaxonomicclassifierid integer
);


--
-- TOC entry 480 (class 1259 OID 175936)
-- Name: timeseriesresults; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE timeseriesresults (
    resultid bigint NOT NULL,
    xlocation double precision,
    xlocationunitsid integer,
    ylocation double precision,
    ylocationunitsid integer,
    zlocation double precision,
    zlocationunitsid integer,
    spatialreferenceid integer,
    intendedtimespacing double precision,
    intendedtimespacingunitsid integer,
    aggregationstatisticcv character varying(255) NOT NULL
);


--
-- TOC entry 481 (class 1259 OID 175939)
-- Name: timeseriesresultvalueannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE timeseriesresultvalueannotations (
    bridgeid integer NOT NULL,
    valueid bigint NOT NULL,
    annotationid integer NOT NULL
);


--
-- TOC entry 482 (class 1259 OID 175942)
-- Name: timeseriesresultvalueannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE timeseriesresultvalueannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5682 (class 0 OID 0)
-- Dependencies: 482
-- Name: timeseriesresultvalueannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE timeseriesresultvalueannotations_bridgeid_seq OWNED BY timeseriesresultvalueannotations.bridgeid;


--
-- TOC entry 483 (class 1259 OID 175944)
-- Name: timeseriesresultvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE timeseriesresultvalues (
    valueid bigint NOT NULL,
    resultid bigint NOT NULL,
    datavalue double precision NOT NULL,
    valuedatetime timestamp without time zone NOT NULL,
    valuedatetimeutcoffset integer NOT NULL,
    censorcodecv character varying(255) NOT NULL,
    qualitycodecv character varying(255) NOT NULL,
    timeaggregationinterval double precision NOT NULL,
    timeaggregationintervalunitsid integer NOT NULL
);


--
-- TOC entry 484 (class 1259 OID 175950)
-- Name: timeseriesresultvalues_valueid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE timeseriesresultvalues_valueid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5683 (class 0 OID 0)
-- Dependencies: 484
-- Name: timeseriesresultvalues_valueid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE timeseriesresultvalues_valueid_seq OWNED BY timeseriesresultvalues.valueid;


--
-- TOC entry 485 (class 1259 OID 175952)
-- Name: trajectoryresults; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE trajectoryresults (
    resultid bigint NOT NULL,
    spatialreferenceid integer,
    intendedtrajectoryspacing double precision,
    intendedtrajectoryspacingunitsid integer,
    intendedtimespacing double precision,
    intendedtimespacingunitsid integer,
    aggregationstatisticcv character varying(255) NOT NULL
);


--
-- TOC entry 486 (class 1259 OID 175955)
-- Name: trajectoryresultvalueannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE trajectoryresultvalueannotations (
    bridgeid integer NOT NULL,
    valueid bigint NOT NULL,
    annotationid integer NOT NULL
);


--
-- TOC entry 487 (class 1259 OID 175958)
-- Name: trajectoryresultvalueannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE trajectoryresultvalueannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5684 (class 0 OID 0)
-- Dependencies: 487
-- Name: trajectoryresultvalueannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE trajectoryresultvalueannotations_bridgeid_seq OWNED BY trajectoryresultvalueannotations.bridgeid;


--
-- TOC entry 488 (class 1259 OID 175960)
-- Name: trajectoryresultvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE trajectoryresultvalues (
    valueid bigint NOT NULL,
    resultid bigint NOT NULL,
    datavalue double precision NOT NULL,
    valuedatetime timestamp without time zone NOT NULL,
    valuedatetimeutcoffset integer NOT NULL,
    xlocation double precision NOT NULL,
    xlocationunitsid integer NOT NULL,
    ylocation double precision NOT NULL,
    ylocationunitsid integer NOT NULL,
    zlocation double precision NOT NULL,
    zlocationunitsid integer NOT NULL,
    trajectorydistance double precision NOT NULL,
    trajectorydistanceaggregationinterval double precision NOT NULL,
    trajectorydistanceunitsid integer NOT NULL,
    censorcodecv character varying(255) NOT NULL,
    qualitycodecv character varying(255) NOT NULL,
    timeaggregationinterval double precision NOT NULL,
    timeaggregationintervalunitsid integer NOT NULL
);


--
-- TOC entry 489 (class 1259 OID 175966)
-- Name: trajectoryresultvalues_valueid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE trajectoryresultvalues_valueid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5685 (class 0 OID 0)
-- Dependencies: 489
-- Name: trajectoryresultvalues_valueid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE trajectoryresultvalues_valueid_seq OWNED BY trajectoryresultvalues.valueid;


--
-- TOC entry 490 (class 1259 OID 175968)
-- Name: transectresults; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE transectresults (
    resultid bigint NOT NULL,
    zlocation double precision,
    zlocationunitsid integer,
    spatialreferenceid integer,
    intendedtransectspacing double precision,
    intendedtransectspacingunitsid integer,
    intendedtimespacing double precision,
    intendedtimespacingunitsid integer,
    aggregationstatisticcv character varying(255) NOT NULL
);


--
-- TOC entry 491 (class 1259 OID 175971)
-- Name: transectresultvalueannotations; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE transectresultvalueannotations (
    bridgeid integer NOT NULL,
    valueid bigint NOT NULL,
    annotationid integer NOT NULL
);


--
-- TOC entry 492 (class 1259 OID 175974)
-- Name: transectresultvalueannotations_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE transectresultvalueannotations_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5686 (class 0 OID 0)
-- Dependencies: 492
-- Name: transectresultvalueannotations_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE transectresultvalueannotations_bridgeid_seq OWNED BY transectresultvalueannotations.bridgeid;


--
-- TOC entry 493 (class 1259 OID 175976)
-- Name: transectresultvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE transectresultvalues (
    valueid bigint NOT NULL,
    resultid bigint NOT NULL,
    datavalue double precision NOT NULL,
    valuedatetime timestamp without time zone NOT NULL,
    valuedatetimeutcoffset timestamp without time zone NOT NULL,
    xlocation double precision NOT NULL,
    xlocationunitsid integer NOT NULL,
    ylocation double precision NOT NULL,
    ylocationunitsid integer NOT NULL,
    transectdistance double precision NOT NULL,
    transectdistanceaggregationinterval double precision NOT NULL,
    transectdistanceunitsid integer NOT NULL,
    censorcodecv character varying(255) NOT NULL,
    qualitycodecv character varying(255) NOT NULL,
    aggregationstatisticcv character varying(255) NOT NULL,
    timeaggregationinterval double precision NOT NULL,
    timeaggregationintervalunitsid integer NOT NULL
);


--
-- TOC entry 494 (class 1259 OID 175982)
-- Name: transectresultvalues_valueid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE transectresultvalues_valueid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5687 (class 0 OID 0)
-- Dependencies: 494
-- Name: transectresultvalues_valueid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE transectresultvalues_valueid_seq OWNED BY transectresultvalues.valueid;


--
-- TOC entry 495 (class 1259 OID 175984)
-- Name: units; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE units (
    unitsid integer NOT NULL,
    unitstypecv character varying(255) NOT NULL,
    unitsabbreviation character varying(50) NOT NULL,
    unitsname character varying(255) NOT NULL,
    unitslink character varying(255)
);


--
-- TOC entry 496 (class 1259 OID 175990)
-- Name: units_unitsid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE units_unitsid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5688 (class 0 OID 0)
-- Dependencies: 496
-- Name: units_unitsid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE units_unitsid_seq OWNED BY units.unitsid;


--
-- TOC entry 497 (class 1259 OID 175992)
-- Name: variableextensionpropertyvalues; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE variableextensionpropertyvalues (
    bridgeid integer NOT NULL,
    variableid integer NOT NULL,
    propertyid integer NOT NULL,
    propertyvalue character varying(255) NOT NULL
);


--
-- TOC entry 498 (class 1259 OID 175995)
-- Name: variableextensionpropertyvalues_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE variableextensionpropertyvalues_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5689 (class 0 OID 0)
-- Dependencies: 498
-- Name: variableextensionpropertyvalues_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE variableextensionpropertyvalues_bridgeid_seq OWNED BY variableextensionpropertyvalues.bridgeid;


--
-- TOC entry 499 (class 1259 OID 175997)
-- Name: variableexternalidentifiers; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE variableexternalidentifiers (
    bridgeid integer NOT NULL,
    variableid integer NOT NULL,
    externalidentifiersystemid integer NOT NULL,
    variableexternalidentifier character varying(255) NOT NULL,
    variableexternalidentifieruri character varying(255)
);


--
-- TOC entry 500 (class 1259 OID 176003)
-- Name: variableexternalidentifiers_bridgeid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE variableexternalidentifiers_bridgeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5690 (class 0 OID 0)
-- Dependencies: 500
-- Name: variableexternalidentifiers_bridgeid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE variableexternalidentifiers_bridgeid_seq OWNED BY variableexternalidentifiers.bridgeid;


--
-- TOC entry 501 (class 1259 OID 176005)
-- Name: variables; Type: TABLE; Schema: odm2; Owner: -
--

CREATE TABLE variables (
    variableid integer NOT NULL,
    variabletypecv character varying(255) NOT NULL,
    variablecode character varying(50) NOT NULL,
    variablenamecv character varying(255) NOT NULL,
    variabledefinition character varying(500),
    speciationcv character varying(255),
    nodatavalue double precision NOT NULL
);


--
-- TOC entry 502 (class 1259 OID 176011)
-- Name: variables_variableid_seq; Type: SEQUENCE; Schema: odm2; Owner: -
--

CREATE SEQUENCE variables_variableid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5691 (class 0 OID 0)
-- Dependencies: 502
-- Name: variables_variableid_seq; Type: SEQUENCE OWNED BY; Schema: odm2; Owner: -
--

ALTER SEQUENCE variables_variableid_seq OWNED BY variables.variableid;


SET search_path = odm2extra, pg_catalog;

--
-- TOC entry 503 (class 1259 OID 176013)
-- Name: Measurementresultvaluefile; Type: TABLE; Schema: odm2extra; Owner: -
--

CREATE TABLE "Measurementresultvaluefile" (
    "valueFileid" integer NOT NULL,
    "valueFile" character varying(100) NOT NULL,
    resultid bigint NOT NULL
);


--
-- TOC entry 504 (class 1259 OID 176016)
-- Name: Measurementresultvaluefile_valueFileid_seq; Type: SEQUENCE; Schema: odm2extra; Owner: -
--

CREATE SEQUENCE "Measurementresultvaluefile_valueFileid_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 5692 (class 0 OID 0)
-- Dependencies: 504
-- Name: Measurementresultvaluefile_valueFileid_seq; Type: SEQUENCE OWNED BY; Schema: odm2extra; Owner: -
--

ALTER SEQUENCE "Measurementresultvaluefile_valueFileid_seq" OWNED BY "Measurementresultvaluefile"."valueFileid";


--
-- TOC entry 505 (class 1259 OID 176018)
-- Name: featureactionNamesid_seq; Type: SEQUENCE; Schema: odm2extra; Owner: -
--

CREATE SEQUENCE "featureactionNamesid_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 506 (class 1259 OID 176020)
-- Name: featureactionsNames; Type: TABLE; Schema: odm2extra; Owner: -
--

CREATE TABLE "featureactionsNames" (
    featureactionid integer NOT NULL,
    name character(500),
    "featureactionNamesid" integer DEFAULT nextval('"featureactionNamesid_seq"'::regclass) NOT NULL
);


--
-- TOC entry 507 (class 1259 OID 176027)
-- Name: processdataloggerfile_id_seq; Type: SEQUENCE; Schema: odm2extra; Owner: -
--

CREATE SEQUENCE processdataloggerfile_id_seq
    START WITH 30
    INCREMENT BY 1
    MINVALUE 0
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 508 (class 1259 OID 176029)
-- Name: processdataloggerfile; Type: TABLE; Schema: odm2extra; Owner: -
--

CREATE TABLE processdataloggerfile (
    processdataloggerfileid integer DEFAULT nextval('processdataloggerfile_id_seq'::regclass) NOT NULL,
    dataloggerfileid integer NOT NULL,
    "processingCode" character varying(255),
    date_processed timestamp with time zone NOT NULL,
    databeginson integer,
    columnheaderson integer
);


--
-- TOC entry 509 (class 1259 OID 176033)
-- Name: timeseriesresultvaluesext; Type: VIEW; Schema: odm2extra; Owner: -
--

CREATE VIEW timeseriesresultvaluesext AS
 SELECT timeseriesresultvalues.valueid,
    timeseriesresultvalues.datavalue,
    timeseriesresultvalues.valuedatetime,
    timeseriesresultvalues.valuedatetimeutcoffset,
    timeseriesresultvalues.censorcodecv,
    timeseriesresultvalues.qualitycodecv,
    timeseriesresultvalues.timeaggregationinterval,
    timeseriesresultvalues.timeaggregationintervalunitsid,
    samplingfeatures.samplingfeaturename,
    samplingfeatures.samplingfeaturetypecv,
    processinglevels.processinglevelcode,
    variables.variablecode,
    units.unitsabbreviation,
    timeseriesresultvalues.resultid,
    cv_aggregationstatistic.name AS aggregationstatisticname
   FROM odm2.timeseriesresultvalues,
    odm2.timeseriesresults,
    odm2.results,
    odm2.featureactions,
    odm2.samplingfeatures,
    odm2.processinglevels,
    odm2.variables,
    odm2.units,
    odm2.cv_aggregationstatistic
  WHERE ((timeseriesresultvalues.resultid = timeseriesresults.resultid) AND (timeseriesresults.resultid = results.resultid) AND ((timeseriesresults.aggregationstatisticcv)::text = (cv_aggregationstatistic.name)::text) AND (results.featureactionid = featureactions.featureactionid) AND (results.processinglevelid = processinglevels.processinglevelid) AND (results.variableid = variables.variableid) AND (results.unitsid = units.unitsid) AND (featureactions.samplingfeatureid = samplingfeatures.samplingfeatureid))
  ORDER BY timeseriesresultvalues.datavalue DESC;


--
-- TOC entry 510 (class 1259 OID 176038)
-- Name: timeseriesresultvaluesextwannotations; Type: VIEW; Schema: odm2extra; Owner: -
--

CREATE VIEW timeseriesresultvaluesextwannotations AS
 SELECT timeseriesresultvalues.valueid,
    timeseriesresultvalues.datavalue,
    timeseriesresultvalues.valuedatetime,
    timeseriesresultvalues.valuedatetimeutcoffset,
    timeseriesresultvalues.censorcodecv,
    timeseriesresultvalues.qualitycodecv,
    timeseriesresultvalues.timeaggregationinterval,
    timeseriesresultvalues.timeaggregationintervalunitsid,
    samplingfeatures.samplingfeaturename,
    processinglevels.processinglevelcode,
    variables.variablecode,
    units.unitsabbreviation,
    timeseriesresultvalues.resultid,
    cv_aggregationstatistic.name AS aggregationstatisticname,
    annotations.annotationtext
   FROM odm2.timeseriesresultvalues,
    odm2.timeseriesresults,
    odm2.results,
    odm2.featureactions,
    odm2.samplingfeatures,
    odm2.processinglevels,
    odm2.variables,
    odm2.units,
    odm2.cv_aggregationstatistic,
    odm2.timeseriesresultvalueannotations,
    odm2.annotations
  WHERE ((timeseriesresultvalues.resultid = timeseriesresults.resultid) AND (timeseriesresultvalues.valueid = timeseriesresultvalueannotations.valueid) AND (timeseriesresults.resultid = results.resultid) AND ((timeseriesresults.aggregationstatisticcv)::text = (cv_aggregationstatistic.name)::text) AND (results.featureactionid = featureactions.featureactionid) AND (results.processinglevelid = processinglevels.processinglevelid) AND (results.variableid = variables.variableid) AND (results.unitsid = units.unitsid) AND (featureactions.samplingfeatureid = samplingfeatures.samplingfeatureid) AND (timeseriesresultvalueannotations.annotationid = annotations.annotationid))
  ORDER BY timeseriesresultvalues.datavalue DESC;


SET search_path = odm2, pg_catalog;

--
-- TOC entry 4749 (class 2604 OID 176043)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actionannotations ALTER COLUMN bridgeid SET DEFAULT nextval('actionannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4750 (class 2604 OID 176044)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actionby ALTER COLUMN bridgeid SET DEFAULT nextval('actionby_bridgeid_seq'::regclass);


--
-- TOC entry 4751 (class 2604 OID 176045)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actiondirectives ALTER COLUMN bridgeid SET DEFAULT nextval('actiondirectives_bridgeid_seq'::regclass);


--
-- TOC entry 4752 (class 2604 OID 176046)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actionextensionpropertyvalues ALTER COLUMN bridgeid SET DEFAULT nextval('actionextensionpropertyvalues_bridgeid_seq'::regclass);


--
-- TOC entry 4753 (class 2604 OID 176047)
-- Name: actionid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actions ALTER COLUMN actionid SET DEFAULT nextval('actions_actionid_seq'::regclass);


--
-- TOC entry 4754 (class 2604 OID 176048)
-- Name: affiliationid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY affiliations ALTER COLUMN affiliationid SET DEFAULT nextval('affiliations_affiliationid_seq'::regclass);


--
-- TOC entry 4755 (class 2604 OID 176049)
-- Name: annotationid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY annotations ALTER COLUMN annotationid SET DEFAULT nextval('annotations_annotationid_seq'::regclass);


--
-- TOC entry 4756 (class 2604 OID 176050)
-- Name: id; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- TOC entry 4757 (class 2604 OID 176051)
-- Name: id; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- TOC entry 4758 (class 2604 OID 176052)
-- Name: id; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- TOC entry 4759 (class 2604 OID 176053)
-- Name: id; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- TOC entry 4760 (class 2604 OID 176054)
-- Name: id; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- TOC entry 4761 (class 2604 OID 176055)
-- Name: id; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- TOC entry 4762 (class 2604 OID 176056)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY authorlists ALTER COLUMN bridgeid SET DEFAULT nextval('authorlists_bridgeid_seq'::regclass);


--
-- TOC entry 4763 (class 2604 OID 176057)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY calibrationreferenceequipment ALTER COLUMN bridgeid SET DEFAULT nextval('calibrationreferenceequipment_bridgeid_seq'::regclass);


--
-- TOC entry 4764 (class 2604 OID 176058)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY calibrationstandards ALTER COLUMN bridgeid SET DEFAULT nextval('calibrationstandards_bridgeid_seq'::regclass);


--
-- TOC entry 4765 (class 2604 OID 176059)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY categoricalresultvalueannotations ALTER COLUMN bridgeid SET DEFAULT nextval('categoricalresultvalueannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4766 (class 2604 OID 176060)
-- Name: valueid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY categoricalresultvalues ALTER COLUMN valueid SET DEFAULT nextval('categoricalresultvalues_valueid_seq'::regclass);


--
-- TOC entry 4767 (class 2604 OID 176061)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY citationextensionpropertyvalues ALTER COLUMN bridgeid SET DEFAULT nextval('citationextensionpropertyvalues_bridgeid_seq'::regclass);


--
-- TOC entry 4768 (class 2604 OID 176062)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY citationexternalidentifiers ALTER COLUMN bridgeid SET DEFAULT nextval('citationexternalidentifiers_bridgeid_seq'::regclass);


--
-- TOC entry 4769 (class 2604 OID 176063)
-- Name: citationid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY citations ALTER COLUMN citationid SET DEFAULT nextval('citations_citationid_seq'::regclass);


--
-- TOC entry 4770 (class 2604 OID 176064)
-- Name: dataloggerfilecolumnid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerfilecolumns ALTER COLUMN dataloggerfilecolumnid SET DEFAULT nextval('dataloggerfilecolumns_dataloggerfilecolumnid_seq'::regclass);


--
-- TOC entry 4771 (class 2604 OID 176065)
-- Name: dataloggerfileid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerfiles ALTER COLUMN dataloggerfileid SET DEFAULT nextval('dataloggerfiles_dataloggerfileid_seq'::regclass);


--
-- TOC entry 4772 (class 2604 OID 176066)
-- Name: programid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerprogramfiles ALTER COLUMN programid SET DEFAULT nextval('dataloggerprogramfiles_programid_seq'::regclass);


--
-- TOC entry 4774 (class 2604 OID 176067)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY datasetcitations ALTER COLUMN bridgeid SET DEFAULT nextval('datasetcitations_bridgeid_seq'::regclass);


--
-- TOC entry 4775 (class 2604 OID 176068)
-- Name: datasetid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY datasets ALTER COLUMN datasetid SET DEFAULT nextval('datasets_datasetid_seq'::regclass);


--
-- TOC entry 4776 (class 2604 OID 176069)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY datasetsresults ALTER COLUMN bridgeid SET DEFAULT nextval('datasetsresults_bridgeid_seq'::regclass);


--
-- TOC entry 4777 (class 2604 OID 176070)
-- Name: derivationequationid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY derivationequations ALTER COLUMN derivationequationid SET DEFAULT nextval('derivationequations_derivationequationid_seq'::regclass);


--
-- TOC entry 4778 (class 2604 OID 176071)
-- Name: directiveid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY directives ALTER COLUMN directiveid SET DEFAULT nextval('directives_directiveid_seq'::regclass);


--
-- TOC entry 4779 (class 2604 OID 176072)
-- Name: id; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- TOC entry 4782 (class 2604 OID 176073)
-- Name: id; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- TOC entry 4783 (class 2604 OID 176074)
-- Name: id; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- TOC entry 4784 (class 2604 OID 176075)
-- Name: equipmentid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipment ALTER COLUMN equipmentid SET DEFAULT nextval('equipment_equipmentid_seq'::regclass);


--
-- TOC entry 4785 (class 2604 OID 176076)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipmentannotations ALTER COLUMN bridgeid SET DEFAULT nextval('equipmentannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4786 (class 2604 OID 176077)
-- Name: equipmentmodelid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipmentmodels ALTER COLUMN equipmentmodelid SET DEFAULT nextval('equipmentmodels_equipmentmodelid_seq'::regclass);


--
-- TOC entry 4787 (class 2604 OID 176078)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipmentused ALTER COLUMN bridgeid SET DEFAULT nextval('equipmentused_bridgeid_seq'::regclass);


--
-- TOC entry 4788 (class 2604 OID 176079)
-- Name: propertyid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY extensionproperties ALTER COLUMN propertyid SET DEFAULT nextval('extensionproperties_propertyid_seq'::regclass);


--
-- TOC entry 4790 (class 2604 OID 176080)
-- Name: featureactionid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY featureactions ALTER COLUMN featureactionid SET DEFAULT nextval('featureactions_featureactionid_seq'::regclass);


--
-- TOC entry 4791 (class 2604 OID 176081)
-- Name: instrumentoutputvariableid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY instrumentoutputvariables ALTER COLUMN instrumentoutputvariableid SET DEFAULT nextval('instrumentoutputvariables_instrumentoutputvariableid_seq'::regclass);


--
-- TOC entry 4792 (class 2604 OID 176082)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresultvalueannotations ALTER COLUMN bridgeid SET DEFAULT nextval('measurementresultvalueannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4793 (class 2604 OID 176083)
-- Name: valueid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresultvalues ALTER COLUMN valueid SET DEFAULT nextval('measurementresultvalues_valueid_seq'::regclass);


--
-- TOC entry 4794 (class 2604 OID 176084)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodannotations ALTER COLUMN bridgeid SET DEFAULT nextval('methodannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4795 (class 2604 OID 176085)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodcitations ALTER COLUMN bridgeid SET DEFAULT nextval('methodcitations_bridgeid_seq'::regclass);


--
-- TOC entry 4796 (class 2604 OID 176086)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodextensionpropertyvalues ALTER COLUMN bridgeid SET DEFAULT nextval('methodextensionpropertyvalues_bridgeid_seq'::regclass);


--
-- TOC entry 4797 (class 2604 OID 176087)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodexternalidentifiers ALTER COLUMN bridgeid SET DEFAULT nextval('methodexternalidentifiers_bridgeid_seq'::regclass);


--
-- TOC entry 4798 (class 2604 OID 176088)
-- Name: methodid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methods ALTER COLUMN methodid SET DEFAULT nextval('methods_methodid_seq'::regclass);


--
-- TOC entry 4799 (class 2604 OID 176089)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY modelaffiliations ALTER COLUMN bridgeid SET DEFAULT nextval('modelaffiliations_bridgeid_seq'::regclass);


--
-- TOC entry 4800 (class 2604 OID 176090)
-- Name: modelid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY models ALTER COLUMN modelid SET DEFAULT nextval('models_modelid_seq'::regclass);


--
-- TOC entry 4801 (class 2604 OID 176091)
-- Name: organizationid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY organizations ALTER COLUMN organizationid SET DEFAULT nextval('organizations_organizationid_seq'::regclass);


--
-- TOC entry 4802 (class 2604 OID 176092)
-- Name: personid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY people ALTER COLUMN personid SET DEFAULT nextval('people_personid_seq'::regclass);


--
-- TOC entry 4803 (class 2604 OID 176093)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY personexternalidentifiers ALTER COLUMN bridgeid SET DEFAULT nextval('personexternalidentifiers_bridgeid_seq'::regclass);


--
-- TOC entry 4804 (class 2604 OID 176094)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresultvalueannotations ALTER COLUMN bridgeid SET DEFAULT nextval('pointcoverageresultvalueannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4805 (class 2604 OID 176095)
-- Name: valueid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresultvalues ALTER COLUMN valueid SET DEFAULT nextval('pointcoverageresultvalues_valueid_seq'::regclass);


--
-- TOC entry 4806 (class 2604 OID 176096)
-- Name: processinglevelid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY processinglevels ALTER COLUMN processinglevelid SET DEFAULT nextval('processinglevels_processinglevelid_seq'::regclass);


--
-- TOC entry 4807 (class 2604 OID 176097)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresultvalueannotations ALTER COLUMN bridgeid SET DEFAULT nextval('profileresultvalueannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4808 (class 2604 OID 176098)
-- Name: valueid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresultvalues ALTER COLUMN valueid SET DEFAULT nextval('profileresultvalues_valueid_seq'::regclass);


--
-- TOC entry 4809 (class 2604 OID 176099)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY referencematerialexternalidentifiers ALTER COLUMN bridgeid SET DEFAULT nextval('referencematerialexternalidentifiers_bridgeid_seq'::regclass);


--
-- TOC entry 4810 (class 2604 OID 176100)
-- Name: relationid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedactions ALTER COLUMN relationid SET DEFAULT nextval('relatedactions_relationid_seq'::regclass);


--
-- TOC entry 4811 (class 2604 OID 176101)
-- Name: relationid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedannotations ALTER COLUMN relationid SET DEFAULT nextval('relatedannotations_relationid_seq'::regclass);


--
-- TOC entry 4812 (class 2604 OID 176102)
-- Name: relationid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedcitations ALTER COLUMN relationid SET DEFAULT nextval('relatedcitations_relationid_seq'::regclass);


--
-- TOC entry 4813 (class 2604 OID 176103)
-- Name: relationid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relateddatasets ALTER COLUMN relationid SET DEFAULT nextval('relateddatasets_relationid_seq'::regclass);


--
-- TOC entry 4814 (class 2604 OID 176104)
-- Name: relationid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedequipment ALTER COLUMN relationid SET DEFAULT nextval('relatedequipment_relationid_seq'::regclass);


--
-- TOC entry 4815 (class 2604 OID 176105)
-- Name: relationid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedfeatures ALTER COLUMN relationid SET DEFAULT nextval('relatedfeatures_relationid_seq'::regclass);


--
-- TOC entry 4816 (class 2604 OID 176106)
-- Name: relatedid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedmodels ALTER COLUMN relatedid SET DEFAULT nextval('relatedmodels_relatedid_seq'::regclass);


--
-- TOC entry 4817 (class 2604 OID 176107)
-- Name: relationid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedresults ALTER COLUMN relationid SET DEFAULT nextval('relatedresults_relationid_seq'::regclass);


--
-- TOC entry 4818 (class 2604 OID 176108)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultannotations ALTER COLUMN bridgeid SET DEFAULT nextval('resultannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4819 (class 2604 OID 176109)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultextensionpropertyvalues ALTER COLUMN bridgeid SET DEFAULT nextval('resultextensionpropertyvalues_bridgeid_seq'::regclass);


--
-- TOC entry 4820 (class 2604 OID 176110)
-- Name: resultid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY results ALTER COLUMN resultid SET DEFAULT nextval('results_resultid_seq'::regclass);


--
-- TOC entry 4821 (class 2604 OID 176111)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultsdataquality ALTER COLUMN bridgeid SET DEFAULT nextval('resultsdataquality_bridgeid_seq'::regclass);


--
-- TOC entry 4822 (class 2604 OID 176112)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatureannotations ALTER COLUMN bridgeid SET DEFAULT nextval('samplingfeatureannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4823 (class 2604 OID 176113)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatureextensionpropertyvalues ALTER COLUMN bridgeid SET DEFAULT nextval('samplingfeatureextensionpropertyvalues_bridgeid_seq'::regclass);


--
-- TOC entry 4824 (class 2604 OID 176114)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatureexternalidentifiers ALTER COLUMN bridgeid SET DEFAULT nextval('samplingfeatureexternalidentifiers_bridgeid_seq'::regclass);


--
-- TOC entry 4825 (class 2604 OID 176115)
-- Name: samplingfeatureid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatures ALTER COLUMN samplingfeatureid SET DEFAULT nextval('samplingfeatures_samplingfeatureid_seq'::regclass);


--
-- TOC entry 4826 (class 2604 OID 176116)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresultvalueannotations ALTER COLUMN bridgeid SET DEFAULT nextval('sectionresultvalueannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4827 (class 2604 OID 176117)
-- Name: valueid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresultvalues ALTER COLUMN valueid SET DEFAULT nextval('sectionresultvalues_valueid_seq'::regclass);


--
-- TOC entry 4828 (class 2604 OID 176118)
-- Name: simulationid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY simulations ALTER COLUMN simulationid SET DEFAULT nextval('simulations_simulationid_seq'::regclass);


--
-- TOC entry 4829 (class 2604 OID 176119)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spatialreferenceexternalidentifiers ALTER COLUMN bridgeid SET DEFAULT nextval('spatialreferenceexternalidentifiers_bridgeid_seq'::regclass);


--
-- TOC entry 4830 (class 2604 OID 176120)
-- Name: spatialreferenceid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spatialreferences ALTER COLUMN spatialreferenceid SET DEFAULT nextval('spatialreferences_spatialreferenceid_seq'::regclass);


--
-- TOC entry 4831 (class 2604 OID 176121)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY specimentaxonomicclassifiers ALTER COLUMN bridgeid SET DEFAULT nextval('specimentaxonomicclassifiers_bridgeid_seq'::regclass);


--
-- TOC entry 4832 (class 2604 OID 176122)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresultvalueannotations ALTER COLUMN bridgeid SET DEFAULT nextval('spectraresultvalueannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4833 (class 2604 OID 176123)
-- Name: valueid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresultvalues ALTER COLUMN valueid SET DEFAULT nextval('spectraresultvalues_valueid_seq'::regclass);


--
-- TOC entry 4834 (class 2604 OID 176124)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY taxonomicclassifierexternalidentifiers ALTER COLUMN bridgeid SET DEFAULT nextval('taxonomicclassifierexternalidentifiers_bridgeid_seq'::regclass);


--
-- TOC entry 4835 (class 2604 OID 176125)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresultvalueannotations ALTER COLUMN bridgeid SET DEFAULT nextval('timeseriesresultvalueannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4836 (class 2604 OID 176126)
-- Name: valueid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresultvalues ALTER COLUMN valueid SET DEFAULT nextval('timeseriesresultvalues_valueid_seq'::regclass);


--
-- TOC entry 4837 (class 2604 OID 176127)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalueannotations ALTER COLUMN bridgeid SET DEFAULT nextval('trajectoryresultvalueannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4838 (class 2604 OID 176128)
-- Name: valueid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalues ALTER COLUMN valueid SET DEFAULT nextval('trajectoryresultvalues_valueid_seq'::regclass);


--
-- TOC entry 4839 (class 2604 OID 176129)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalueannotations ALTER COLUMN bridgeid SET DEFAULT nextval('transectresultvalueannotations_bridgeid_seq'::regclass);


--
-- TOC entry 4840 (class 2604 OID 176130)
-- Name: valueid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalues ALTER COLUMN valueid SET DEFAULT nextval('transectresultvalues_valueid_seq'::regclass);


--
-- TOC entry 4841 (class 2604 OID 176131)
-- Name: unitsid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY units ALTER COLUMN unitsid SET DEFAULT nextval('units_unitsid_seq'::regclass);


--
-- TOC entry 4842 (class 2604 OID 176132)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY variableextensionpropertyvalues ALTER COLUMN bridgeid SET DEFAULT nextval('variableextensionpropertyvalues_bridgeid_seq'::regclass);


--
-- TOC entry 4843 (class 2604 OID 176133)
-- Name: bridgeid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY variableexternalidentifiers ALTER COLUMN bridgeid SET DEFAULT nextval('variableexternalidentifiers_bridgeid_seq'::regclass);


--
-- TOC entry 4844 (class 2604 OID 176134)
-- Name: variableid; Type: DEFAULT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY variables ALTER COLUMN variableid SET DEFAULT nextval('variables_variableid_seq'::regclass);


SET search_path = odm2extra, pg_catalog;

--
-- TOC entry 4845 (class 2604 OID 176135)
-- Name: valueFileid; Type: DEFAULT; Schema: odm2extra; Owner: -
--

ALTER TABLE ONLY "Measurementresultvaluefile" ALTER COLUMN "valueFileid" SET DEFAULT nextval('"Measurementresultvaluefile_valueFileid_seq"'::regclass);


SET search_path = odm2, pg_catalog;

--
-- TOC entry 4849 (class 2606 OID 176137)
-- Name: actionannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actionannotations
    ADD CONSTRAINT actionannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 4851 (class 2606 OID 176139)
-- Name: actionby_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actionby
    ADD CONSTRAINT actionby_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 4853 (class 2606 OID 176141)
-- Name: actiondirectives_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actiondirectives
    ADD CONSTRAINT actiondirectives_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 4855 (class 2606 OID 176143)
-- Name: actionextensionpropertyvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actionextensionpropertyvalues
    ADD CONSTRAINT actionextensionpropertyvalues_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 4857 (class 2606 OID 176145)
-- Name: actions_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actions
    ADD CONSTRAINT actions_pkey PRIMARY KEY (actionid);


--
-- TOC entry 4859 (class 2606 OID 176147)
-- Name: affiliations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY affiliations
    ADD CONSTRAINT affiliations_pkey PRIMARY KEY (affiliationid);


--
-- TOC entry 4861 (class 2606 OID 176149)
-- Name: annotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY annotations
    ADD CONSTRAINT annotations_pkey PRIMARY KEY (annotationid);


--
-- TOC entry 4864 (class 2606 OID 176151)
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 4870 (class 2606 OID 176153)
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- TOC entry 4872 (class 2606 OID 176155)
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 4866 (class 2606 OID 176157)
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 4875 (class 2606 OID 176159)
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- TOC entry 4877 (class 2606 OID 176161)
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 4886 (class 2606 OID 176163)
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 4888 (class 2606 OID 176165)
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- TOC entry 4879 (class 2606 OID 176167)
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 4892 (class 2606 OID 176169)
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 4894 (class 2606 OID 176171)
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- TOC entry 4882 (class 2606 OID 177990)
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- TOC entry 4896 (class 2606 OID 176175)
-- Name: authorlists_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY authorlists
    ADD CONSTRAINT authorlists_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 4898 (class 2606 OID 176177)
-- Name: calibrationactions_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY calibrationactions
    ADD CONSTRAINT calibrationactions_pkey PRIMARY KEY (actionid);


--
-- TOC entry 4900 (class 2606 OID 176179)
-- Name: calibrationreferenceequipment_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY calibrationreferenceequipment
    ADD CONSTRAINT calibrationreferenceequipment_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 4902 (class 2606 OID 176181)
-- Name: calibrationstandards_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY calibrationstandards
    ADD CONSTRAINT calibrationstandards_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 4904 (class 2606 OID 176183)
-- Name: categoricalresults_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY categoricalresults
    ADD CONSTRAINT categoricalresults_pkey PRIMARY KEY (resultid);


--
-- TOC entry 4906 (class 2606 OID 176185)
-- Name: categoricalresultvalueannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY categoricalresultvalueannotations
    ADD CONSTRAINT categoricalresultvalueannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 4908 (class 2606 OID 176187)
-- Name: categoricalresultvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY categoricalresultvalues
    ADD CONSTRAINT categoricalresultvalues_pkey PRIMARY KEY (valueid);


--
-- TOC entry 4910 (class 2606 OID 176189)
-- Name: citationextensionpropertyvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY citationextensionpropertyvalues
    ADD CONSTRAINT citationextensionpropertyvalues_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 4912 (class 2606 OID 176191)
-- Name: citationexternalidentifiers_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY citationexternalidentifiers
    ADD CONSTRAINT citationexternalidentifiers_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 4914 (class 2606 OID 176193)
-- Name: citations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY citations
    ADD CONSTRAINT citations_pkey PRIMARY KEY (citationid);


--
-- TOC entry 4916 (class 2606 OID 176195)
-- Name: cv_actiontype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_actiontype
    ADD CONSTRAINT cv_actiontype_pkey PRIMARY KEY (name);


--
-- TOC entry 4918 (class 2606 OID 176197)
-- Name: cv_aggregationstatistic_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_aggregationstatistic
    ADD CONSTRAINT cv_aggregationstatistic_pkey PRIMARY KEY (name);


--
-- TOC entry 4920 (class 2606 OID 176199)
-- Name: cv_annotationtype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_annotationtype
    ADD CONSTRAINT cv_annotationtype_pkey PRIMARY KEY (name);


--
-- TOC entry 4922 (class 2606 OID 176201)
-- Name: cv_censorcode_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_censorcode
    ADD CONSTRAINT cv_censorcode_pkey PRIMARY KEY (name);


--
-- TOC entry 4924 (class 2606 OID 176203)
-- Name: cv_dataqualitytype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_dataqualitytype
    ADD CONSTRAINT cv_dataqualitytype_pkey PRIMARY KEY (name);


--
-- TOC entry 4926 (class 2606 OID 176205)
-- Name: cv_datasettypecv_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_datasettype
    ADD CONSTRAINT cv_datasettypecv_pkey PRIMARY KEY (name);


--
-- TOC entry 4928 (class 2606 OID 176207)
-- Name: cv_directivetype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_directivetype
    ADD CONSTRAINT cv_directivetype_pkey PRIMARY KEY (name);


--
-- TOC entry 4930 (class 2606 OID 176209)
-- Name: cv_elevationdatum_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_elevationdatum
    ADD CONSTRAINT cv_elevationdatum_pkey PRIMARY KEY (name);


--
-- TOC entry 4932 (class 2606 OID 176211)
-- Name: cv_equipmenttype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_equipmenttype
    ADD CONSTRAINT cv_equipmenttype_pkey PRIMARY KEY (name);


--
-- TOC entry 4934 (class 2606 OID 176213)
-- Name: cv_medium_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_medium
    ADD CONSTRAINT cv_medium_pkey PRIMARY KEY (name);


--
-- TOC entry 4936 (class 2606 OID 176215)
-- Name: cv_methodtype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_methodtype
    ADD CONSTRAINT cv_methodtype_pkey PRIMARY KEY (name);


--
-- TOC entry 4938 (class 2606 OID 176217)
-- Name: cv_organizationtype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_organizationtype
    ADD CONSTRAINT cv_organizationtype_pkey PRIMARY KEY (name);


--
-- TOC entry 4940 (class 2606 OID 176219)
-- Name: cv_propertydatatype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_propertydatatype
    ADD CONSTRAINT cv_propertydatatype_pkey PRIMARY KEY (name);


--
-- TOC entry 4942 (class 2606 OID 176221)
-- Name: cv_qualitycode_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_qualitycode
    ADD CONSTRAINT cv_qualitycode_pkey PRIMARY KEY (name);


--
-- TOC entry 4944 (class 2606 OID 176223)
-- Name: cv_referencematerialmedium_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_referencematerialmedium
    ADD CONSTRAINT cv_referencematerialmedium_pkey PRIMARY KEY (name);


--
-- TOC entry 4946 (class 2606 OID 176225)
-- Name: cv_relationshiptype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_relationshiptype
    ADD CONSTRAINT cv_relationshiptype_pkey PRIMARY KEY (name);


--
-- TOC entry 4948 (class 2606 OID 176227)
-- Name: cv_resulttype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_resulttype
    ADD CONSTRAINT cv_resulttype_pkey PRIMARY KEY (name);


--
-- TOC entry 4950 (class 2606 OID 176229)
-- Name: cv_sampledmedium_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_sampledmedium
    ADD CONSTRAINT cv_sampledmedium_pkey PRIMARY KEY (name);


--
-- TOC entry 4952 (class 2606 OID 176231)
-- Name: cv_samplingfeaturegeotype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_samplingfeaturegeotype
    ADD CONSTRAINT cv_samplingfeaturegeotype_pkey PRIMARY KEY (name);


--
-- TOC entry 4954 (class 2606 OID 176233)
-- Name: cv_samplingfeaturetype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_samplingfeaturetype
    ADD CONSTRAINT cv_samplingfeaturetype_pkey PRIMARY KEY (name);


--
-- TOC entry 4956 (class 2606 OID 176235)
-- Name: cv_sitetype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_sitetype
    ADD CONSTRAINT cv_sitetype_pkey PRIMARY KEY (name);


--
-- TOC entry 4958 (class 2606 OID 176237)
-- Name: cv_spatialoffsettype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_spatialoffsettype
    ADD CONSTRAINT cv_spatialoffsettype_pkey PRIMARY KEY (name);


--
-- TOC entry 4960 (class 2606 OID 176239)
-- Name: cv_speciation_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_speciation
    ADD CONSTRAINT cv_speciation_pkey PRIMARY KEY (name);


--
-- TOC entry 4962 (class 2606 OID 176241)
-- Name: cv_specimenmedium_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_specimenmedium
    ADD CONSTRAINT cv_specimenmedium_pkey PRIMARY KEY (name);


--
-- TOC entry 4964 (class 2606 OID 176243)
-- Name: cv_specimentype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_specimentype
    ADD CONSTRAINT cv_specimentype_pkey PRIMARY KEY (name);


--
-- TOC entry 4966 (class 2606 OID 176245)
-- Name: cv_status_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_status
    ADD CONSTRAINT cv_status_pkey PRIMARY KEY (name);


--
-- TOC entry 4968 (class 2606 OID 176247)
-- Name: cv_taxonomicclassifiertype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_taxonomicclassifiertype
    ADD CONSTRAINT cv_taxonomicclassifiertype_pkey PRIMARY KEY (name);


--
-- TOC entry 4970 (class 2606 OID 176249)
-- Name: cv_unitstype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_unitstype
    ADD CONSTRAINT cv_unitstype_pkey PRIMARY KEY (name);


--
-- TOC entry 4972 (class 2606 OID 176251)
-- Name: cv_variablename_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_variablename
    ADD CONSTRAINT cv_variablename_pkey PRIMARY KEY (name);


--
-- TOC entry 4974 (class 2606 OID 176253)
-- Name: cv_variabletype_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY cv_variabletype
    ADD CONSTRAINT cv_variabletype_pkey PRIMARY KEY (name);


--
-- TOC entry 4976 (class 2606 OID 176255)
-- Name: dataloggerfilecolumns_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerfilecolumns
    ADD CONSTRAINT dataloggerfilecolumns_pkey PRIMARY KEY (dataloggerfilecolumnid);


--
-- TOC entry 4978 (class 2606 OID 176257)
-- Name: dataloggerfiles_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerfiles
    ADD CONSTRAINT dataloggerfiles_pkey PRIMARY KEY (dataloggerfileid);


--
-- TOC entry 4980 (class 2606 OID 176259)
-- Name: dataloggerprogramfiles_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerprogramfiles
    ADD CONSTRAINT dataloggerprogramfiles_pkey PRIMARY KEY (programid);


--
-- TOC entry 4982 (class 2606 OID 176261)
-- Name: dataquality_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataquality
    ADD CONSTRAINT dataquality_pkey PRIMARY KEY (dataqualityid);


--
-- TOC entry 4984 (class 2606 OID 176263)
-- Name: datasetcitations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY datasetcitations
    ADD CONSTRAINT datasetcitations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 4986 (class 2606 OID 176265)
-- Name: datasets_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY datasets
    ADD CONSTRAINT datasets_pkey PRIMARY KEY (datasetid);


--
-- TOC entry 4988 (class 2606 OID 176267)
-- Name: datasetsresults_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY datasetsresults
    ADD CONSTRAINT datasetsresults_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 4990 (class 2606 OID 176269)
-- Name: derivationequations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY derivationequations
    ADD CONSTRAINT derivationequations_pkey PRIMARY KEY (derivationequationid);


--
-- TOC entry 4992 (class 2606 OID 176271)
-- Name: directives_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY directives
    ADD CONSTRAINT directives_pkey PRIMARY KEY (directiveid);


--
-- TOC entry 4996 (class 2606 OID 176273)
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 4998 (class 2606 OID 176275)
-- Name: django_content_type_app_label_6fe277f5_uniq; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_6fe277f5_uniq UNIQUE (app_label, model);


--
-- TOC entry 5000 (class 2606 OID 176277)
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 5002 (class 2606 OID 176279)
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 5005 (class 2606 OID 176281)
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 5008 (class 2606 OID 176283)
-- Name: equipment_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipment
    ADD CONSTRAINT equipment_pkey PRIMARY KEY (equipmentid);


--
-- TOC entry 5010 (class 2606 OID 176285)
-- Name: equipmentannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipmentannotations
    ADD CONSTRAINT equipmentannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5012 (class 2606 OID 176287)
-- Name: equipmentmodels_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipmentmodels
    ADD CONSTRAINT equipmentmodels_pkey PRIMARY KEY (equipmentmodelid);


--
-- TOC entry 5014 (class 2606 OID 176289)
-- Name: equipmentused_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipmentused
    ADD CONSTRAINT equipmentused_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5016 (class 2606 OID 176291)
-- Name: extensionproperties_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY extensionproperties
    ADD CONSTRAINT extensionproperties_pkey PRIMARY KEY (propertyid);


--
-- TOC entry 5018 (class 2606 OID 176293)
-- Name: externalidentifiersystems_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY externalidentifiersystems
    ADD CONSTRAINT externalidentifiersystems_pkey PRIMARY KEY (externalidentifiersystemid);


--
-- TOC entry 5020 (class 2606 OID 176295)
-- Name: featureactions_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY featureactions
    ADD CONSTRAINT featureactions_pkey PRIMARY KEY (featureactionid);


--
-- TOC entry 5022 (class 2606 OID 176297)
-- Name: instrumentoutputvariables_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY instrumentoutputvariables
    ADD CONSTRAINT instrumentoutputvariables_pkey PRIMARY KEY (instrumentoutputvariableid);


--
-- TOC entry 5024 (class 2606 OID 176299)
-- Name: maintenanceactions_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY maintenanceactions
    ADD CONSTRAINT maintenanceactions_pkey PRIMARY KEY (actionid);


--
-- TOC entry 5026 (class 2606 OID 176301)
-- Name: measurementresults_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresults
    ADD CONSTRAINT measurementresults_pkey PRIMARY KEY (resultid);


--
-- TOC entry 5028 (class 2606 OID 176303)
-- Name: measurementresultvalueannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresultvalueannotations
    ADD CONSTRAINT measurementresultvalueannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5030 (class 2606 OID 176305)
-- Name: measurementresultvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresultvalues
    ADD CONSTRAINT measurementresultvalues_pkey PRIMARY KEY (valueid);


--
-- TOC entry 5032 (class 2606 OID 176307)
-- Name: methodannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodannotations
    ADD CONSTRAINT methodannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5034 (class 2606 OID 176309)
-- Name: methodcitations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodcitations
    ADD CONSTRAINT methodcitations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5036 (class 2606 OID 176311)
-- Name: methodextensionpropertyvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodextensionpropertyvalues
    ADD CONSTRAINT methodextensionpropertyvalues_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5038 (class 2606 OID 176313)
-- Name: methodexternalidentifiers_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodexternalidentifiers
    ADD CONSTRAINT methodexternalidentifiers_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5040 (class 2606 OID 176315)
-- Name: methods_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methods
    ADD CONSTRAINT methods_pkey PRIMARY KEY (methodid);


--
-- TOC entry 5042 (class 2606 OID 176317)
-- Name: modelaffiliations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY modelaffiliations
    ADD CONSTRAINT modelaffiliations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5044 (class 2606 OID 176319)
-- Name: models_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY models
    ADD CONSTRAINT models_pkey PRIMARY KEY (modelid);


--
-- TOC entry 5046 (class 2606 OID 176321)
-- Name: organizations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (organizationid);


--
-- TOC entry 5048 (class 2606 OID 176323)
-- Name: people_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY people
    ADD CONSTRAINT people_pkey PRIMARY KEY (personid);


--
-- TOC entry 5050 (class 2606 OID 176325)
-- Name: personexternalidentifiers_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY personexternalidentifiers
    ADD CONSTRAINT personexternalidentifiers_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5052 (class 2606 OID 176327)
-- Name: pointcoverageresults_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresults
    ADD CONSTRAINT pointcoverageresults_pkey PRIMARY KEY (resultid);


--
-- TOC entry 5054 (class 2606 OID 176329)
-- Name: pointcoverageresultvalueannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresultvalueannotations
    ADD CONSTRAINT pointcoverageresultvalueannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5056 (class 2606 OID 176331)
-- Name: pointcoverageresultvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresultvalues
    ADD CONSTRAINT pointcoverageresultvalues_pkey PRIMARY KEY (valueid);


--
-- TOC entry 5058 (class 2606 OID 176333)
-- Name: processinglevels_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY processinglevels
    ADD CONSTRAINT processinglevels_pkey PRIMARY KEY (processinglevelid);


--
-- TOC entry 5060 (class 2606 OID 176335)
-- Name: profileresults_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresults
    ADD CONSTRAINT profileresults_pkey PRIMARY KEY (resultid);


--
-- TOC entry 5062 (class 2606 OID 176337)
-- Name: profileresultvalueannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresultvalueannotations
    ADD CONSTRAINT profileresultvalueannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5064 (class 2606 OID 176339)
-- Name: profileresultvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresultvalues
    ADD CONSTRAINT profileresultvalues_pkey PRIMARY KEY (valueid);


--
-- TOC entry 5066 (class 2606 OID 176341)
-- Name: referencematerialexternalidentifiers_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY referencematerialexternalidentifiers
    ADD CONSTRAINT referencematerialexternalidentifiers_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5068 (class 2606 OID 176343)
-- Name: referencematerials_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY referencematerials
    ADD CONSTRAINT referencematerials_pkey PRIMARY KEY (referencematerialid);


--
-- TOC entry 5070 (class 2606 OID 176345)
-- Name: referencematerialvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY referencematerialvalues
    ADD CONSTRAINT referencematerialvalues_pkey PRIMARY KEY (referencematerialvalueid);


--
-- TOC entry 5072 (class 2606 OID 176347)
-- Name: relatedactions_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedactions
    ADD CONSTRAINT relatedactions_pkey PRIMARY KEY (relationid);


--
-- TOC entry 5074 (class 2606 OID 176349)
-- Name: relatedannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedannotations
    ADD CONSTRAINT relatedannotations_pkey PRIMARY KEY (relationid);


--
-- TOC entry 5076 (class 2606 OID 176351)
-- Name: relatedcitations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedcitations
    ADD CONSTRAINT relatedcitations_pkey PRIMARY KEY (relationid);


--
-- TOC entry 5078 (class 2606 OID 176353)
-- Name: relateddatasets_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relateddatasets
    ADD CONSTRAINT relateddatasets_pkey PRIMARY KEY (relationid);


--
-- TOC entry 5080 (class 2606 OID 176355)
-- Name: relatedequipment_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedequipment
    ADD CONSTRAINT relatedequipment_pkey PRIMARY KEY (relationid);


--
-- TOC entry 5082 (class 2606 OID 176357)
-- Name: relatedfeatures_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedfeatures
    ADD CONSTRAINT relatedfeatures_pkey PRIMARY KEY (relationid);


--
-- TOC entry 5084 (class 2606 OID 176359)
-- Name: relatedmodels_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedmodels
    ADD CONSTRAINT relatedmodels_pkey PRIMARY KEY (relatedid);


--
-- TOC entry 5086 (class 2606 OID 176361)
-- Name: relatedresults_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedresults
    ADD CONSTRAINT relatedresults_pkey PRIMARY KEY (relationid);


--
-- TOC entry 5088 (class 2606 OID 176363)
-- Name: resultannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultannotations
    ADD CONSTRAINT resultannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5090 (class 2606 OID 176365)
-- Name: resultderivationequations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultderivationequations
    ADD CONSTRAINT resultderivationequations_pkey PRIMARY KEY (resultid);


--
-- TOC entry 5092 (class 2606 OID 176367)
-- Name: resultextensionpropertyvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultextensionpropertyvalues
    ADD CONSTRAINT resultextensionpropertyvalues_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5094 (class 2606 OID 176369)
-- Name: resultnormalizationvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultnormalizationvalues
    ADD CONSTRAINT resultnormalizationvalues_pkey PRIMARY KEY (resultid);


--
-- TOC entry 5096 (class 2606 OID 176371)
-- Name: results_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY results
    ADD CONSTRAINT results_pkey PRIMARY KEY (resultid);


--
-- TOC entry 5098 (class 2606 OID 176373)
-- Name: resultsdataquality_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultsdataquality
    ADD CONSTRAINT resultsdataquality_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5100 (class 2606 OID 176375)
-- Name: samplingfeatureannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatureannotations
    ADD CONSTRAINT samplingfeatureannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5102 (class 2606 OID 176377)
-- Name: samplingfeatureextensionpropertyvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatureextensionpropertyvalues
    ADD CONSTRAINT samplingfeatureextensionpropertyvalues_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5104 (class 2606 OID 176379)
-- Name: samplingfeatureexternalidentifiers_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatureexternalidentifiers
    ADD CONSTRAINT samplingfeatureexternalidentifiers_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5106 (class 2606 OID 176381)
-- Name: samplingfeatures_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatures
    ADD CONSTRAINT samplingfeatures_pkey PRIMARY KEY (samplingfeatureid);


--
-- TOC entry 5108 (class 2606 OID 176383)
-- Name: sectionresults_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresults
    ADD CONSTRAINT sectionresults_pkey PRIMARY KEY (resultid);


--
-- TOC entry 5110 (class 2606 OID 176385)
-- Name: sectionresultvalueannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresultvalueannotations
    ADD CONSTRAINT sectionresultvalueannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5112 (class 2606 OID 176387)
-- Name: sectionresultvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresultvalues
    ADD CONSTRAINT sectionresultvalues_pkey PRIMARY KEY (valueid);


--
-- TOC entry 5114 (class 2606 OID 176389)
-- Name: simulations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY simulations
    ADD CONSTRAINT simulations_pkey PRIMARY KEY (simulationid);


--
-- TOC entry 5116 (class 2606 OID 176391)
-- Name: sites_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sites
    ADD CONSTRAINT sites_pkey PRIMARY KEY (samplingfeatureid);


--
-- TOC entry 5118 (class 2606 OID 176393)
-- Name: spatialoffsets_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spatialoffsets
    ADD CONSTRAINT spatialoffsets_pkey PRIMARY KEY (spatialoffsetid);


--
-- TOC entry 5120 (class 2606 OID 176395)
-- Name: spatialreferenceexternalidentifiers_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spatialreferenceexternalidentifiers
    ADD CONSTRAINT spatialreferenceexternalidentifiers_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5122 (class 2606 OID 176397)
-- Name: spatialreferences_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spatialreferences
    ADD CONSTRAINT spatialreferences_pkey PRIMARY KEY (spatialreferenceid);


--
-- TOC entry 5124 (class 2606 OID 176399)
-- Name: specimenbatchpostions_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY specimenbatchpostions
    ADD CONSTRAINT specimenbatchpostions_pkey PRIMARY KEY (featureactionid);


--
-- TOC entry 5126 (class 2606 OID 176401)
-- Name: specimens_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY specimens
    ADD CONSTRAINT specimens_pkey PRIMARY KEY (samplingfeatureid);


--
-- TOC entry 5128 (class 2606 OID 176403)
-- Name: specimentaxonomicclassifiers_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY specimentaxonomicclassifiers
    ADD CONSTRAINT specimentaxonomicclassifiers_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5130 (class 2606 OID 176405)
-- Name: spectraresults_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresults
    ADD CONSTRAINT spectraresults_pkey PRIMARY KEY (resultid);


--
-- TOC entry 5132 (class 2606 OID 176407)
-- Name: spectraresultvalueannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresultvalueannotations
    ADD CONSTRAINT spectraresultvalueannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5134 (class 2606 OID 176409)
-- Name: spectraresultvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresultvalues
    ADD CONSTRAINT spectraresultvalues_pkey PRIMARY KEY (valueid);


--
-- TOC entry 5136 (class 2606 OID 176411)
-- Name: taxonomicclassifierexternalidentifiers_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY taxonomicclassifierexternalidentifiers
    ADD CONSTRAINT taxonomicclassifierexternalidentifiers_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5138 (class 2606 OID 176413)
-- Name: taxonomicclassifiers_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY taxonomicclassifiers
    ADD CONSTRAINT taxonomicclassifiers_pkey PRIMARY KEY (taxonomicclassifierid);


--
-- TOC entry 5140 (class 2606 OID 176415)
-- Name: timeseriesresults_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresults
    ADD CONSTRAINT timeseriesresults_pkey PRIMARY KEY (resultid);


--
-- TOC entry 5142 (class 2606 OID 176417)
-- Name: timeseriesresultvalueannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresultvalueannotations
    ADD CONSTRAINT timeseriesresultvalueannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5144 (class 2606 OID 176419)
-- Name: timeseriesresultvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresultvalues
    ADD CONSTRAINT timeseriesresultvalues_pkey PRIMARY KEY (valueid);


--
-- TOC entry 5146 (class 2606 OID 176421)
-- Name: trajectoryresults_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresults
    ADD CONSTRAINT trajectoryresults_pkey PRIMARY KEY (resultid);


--
-- TOC entry 5148 (class 2606 OID 176423)
-- Name: trajectoryresultvalueannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalueannotations
    ADD CONSTRAINT trajectoryresultvalueannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5150 (class 2606 OID 176425)
-- Name: trajectoryresultvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalues
    ADD CONSTRAINT trajectoryresultvalues_pkey PRIMARY KEY (valueid);


--
-- TOC entry 5152 (class 2606 OID 176427)
-- Name: transectresults_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresults
    ADD CONSTRAINT transectresults_pkey PRIMARY KEY (resultid);


--
-- TOC entry 5154 (class 2606 OID 176429)
-- Name: transectresultvalueannotations_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalueannotations
    ADD CONSTRAINT transectresultvalueannotations_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5156 (class 2606 OID 176431)
-- Name: transectresultvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalues
    ADD CONSTRAINT transectresultvalues_pkey PRIMARY KEY (valueid);


--
-- TOC entry 5158 (class 2606 OID 176433)
-- Name: units_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY units
    ADD CONSTRAINT units_pkey PRIMARY KEY (unitsid);


--
-- TOC entry 5160 (class 2606 OID 176435)
-- Name: variableextensionpropertyvalues_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY variableextensionpropertyvalues
    ADD CONSTRAINT variableextensionpropertyvalues_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5162 (class 2606 OID 176437)
-- Name: variableexternalidentifiers_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY variableexternalidentifiers
    ADD CONSTRAINT variableexternalidentifiers_pkey PRIMARY KEY (bridgeid);


--
-- TOC entry 5164 (class 2606 OID 176439)
-- Name: variables_pkey; Type: CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY variables
    ADD CONSTRAINT variables_pkey PRIMARY KEY (variableid);


SET search_path = odm2extra, pg_catalog;

--
-- TOC entry 5167 (class 2606 OID 176441)
-- Name: Measurementresultvaluefile_pkey; Type: CONSTRAINT; Schema: odm2extra; Owner: -
--

ALTER TABLE ONLY "Measurementresultvaluefile"
    ADD CONSTRAINT "Measurementresultvaluefile_pkey" PRIMARY KEY ("valueFileid");


--
-- TOC entry 5169 (class 2606 OID 176443)
-- Name: featureactionNamesid; Type: CONSTRAINT; Schema: odm2extra; Owner: -
--

ALTER TABLE ONLY "featureactionsNames"
    ADD CONSTRAINT "featureactionNamesid" PRIMARY KEY ("featureactionNamesid");


--
-- TOC entry 5171 (class 2606 OID 176445)
-- Name: processdataloggerfile_pkey; Type: CONSTRAINT; Schema: odm2extra; Owner: -
--

ALTER TABLE ONLY processdataloggerfile
    ADD CONSTRAINT processdataloggerfile_pkey PRIMARY KEY (processdataloggerfileid);


SET search_path = odm2, pg_catalog;

--
-- TOC entry 4862 (class 1259 OID 176446)
-- Name: auth_group_name_5f992433_like; Type: INDEX; Schema: odm2; Owner: -
--

CREATE INDEX auth_group_name_5f992433_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 4867 (class 1259 OID 176447)
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: odm2; Owner: -
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- TOC entry 4868 (class 1259 OID 176448)
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: odm2; Owner: -
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- TOC entry 4873 (class 1259 OID 176449)
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: odm2; Owner: -
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- TOC entry 4883 (class 1259 OID 176450)
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: odm2; Owner: -
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- TOC entry 4884 (class 1259 OID 176451)
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: odm2; Owner: -
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- TOC entry 4889 (class 1259 OID 176452)
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: odm2; Owner: -
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- TOC entry 4890 (class 1259 OID 176453)
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: odm2; Owner: -
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- TOC entry 4880 (class 1259 OID 177991)
-- Name: auth_user_username_505058ae_like; Type: INDEX; Schema: odm2; Owner: -
--

CREATE INDEX auth_user_username_505058ae_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- TOC entry 4993 (class 1259 OID 176455)
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: odm2; Owner: -
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- TOC entry 4994 (class 1259 OID 176456)
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: odm2; Owner: -
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- TOC entry 5003 (class 1259 OID 176457)
-- Name: django_session_de54fa62; Type: INDEX; Schema: odm2; Owner: -
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- TOC entry 5006 (class 1259 OID 176458)
-- Name: django_session_session_key_527ee3a7_like; Type: INDEX; Schema: odm2; Owner: -
--

CREATE INDEX django_session_session_key_527ee3a7_like ON django_session USING btree (session_key varchar_pattern_ops);


SET search_path = odm2extra, pg_catalog;

--
-- TOC entry 5165 (class 1259 OID 176459)
-- Name: Measurementresultvaluefile_7bab5296; Type: INDEX; Schema: odm2extra; Owner: -
--

CREATE INDEX "Measurementresultvaluefile_7bab5296" ON "Measurementresultvaluefile" USING btree (resultid);


SET search_path = odm2, pg_catalog;

--
-- TOC entry 5188 (class 2606 OID 176460)
-- Name: auth_group_permissi_permission_id_71823a7_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissi_permission_id_71823a7_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5187 (class 2606 OID 176465)
-- Name: auth_group_permissions_group_id_778c86bf_fk_auth_group_id; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_778c86bf_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5189 (class 2606 OID 176470)
-- Name: auth_permiss_content_type_id_462e91fd_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_462e91fd_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5191 (class 2606 OID 176475)
-- Name: auth_user_groups_group_id_5ea98db_fk_auth_group_id; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_5ea98db_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5190 (class 2606 OID 176480)
-- Name: auth_user_groups_user_id_822adec_fk_auth_user_id; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_822adec_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5193 (class 2606 OID 176485)
-- Name: auth_user_user_per_permission_id_66eb27a8_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_66eb27a8_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5192 (class 2606 OID 176490)
-- Name: auth_user_user_permissions_user_id_afd3cc7_fk_auth_user_id; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_afd3cc7_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5230 (class 2606 OID 176495)
-- Name: django_admin_content_type_id_25ba5dc2_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_25ba5dc2_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5229 (class 2606 OID 176500)
-- Name: django_admin_log_user_id_b5c47cb_fk_auth_user_id; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_b5c47cb_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5173 (class 2606 OID 176505)
-- Name: fk_actionannotations_actions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actionannotations
    ADD CONSTRAINT fk_actionannotations_actions FOREIGN KEY (actionid) REFERENCES actions(actionid) ON DELETE CASCADE;


--
-- TOC entry 5172 (class 2606 OID 176510)
-- Name: fk_actionannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actionannotations
    ADD CONSTRAINT fk_actionannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5177 (class 2606 OID 176515)
-- Name: fk_actiondirectives_actions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actiondirectives
    ADD CONSTRAINT fk_actiondirectives_actions FOREIGN KEY (actionid) REFERENCES actions(actionid) ON DELETE CASCADE;


--
-- TOC entry 5176 (class 2606 OID 176520)
-- Name: fk_actiondirectives_directives; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actiondirectives
    ADD CONSTRAINT fk_actiondirectives_directives FOREIGN KEY (directiveid) REFERENCES directives(directiveid) ON DELETE CASCADE;


--
-- TOC entry 5179 (class 2606 OID 176525)
-- Name: fk_actionextensionpropertyvalues_actions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actionextensionpropertyvalues
    ADD CONSTRAINT fk_actionextensionpropertyvalues_actions FOREIGN KEY (actionid) REFERENCES actions(actionid) ON DELETE CASCADE;


--
-- TOC entry 5178 (class 2606 OID 176530)
-- Name: fk_actionextensionpropertyvalues_extensionproperties; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actionextensionpropertyvalues
    ADD CONSTRAINT fk_actionextensionpropertyvalues_extensionproperties FOREIGN KEY (propertyid) REFERENCES extensionproperties(propertyid) ON DELETE CASCADE;


--
-- TOC entry 5175 (class 2606 OID 176535)
-- Name: fk_actionpeople_actions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actionby
    ADD CONSTRAINT fk_actionpeople_actions FOREIGN KEY (actionid) REFERENCES actions(actionid) ON DELETE CASCADE;


--
-- TOC entry 5174 (class 2606 OID 176540)
-- Name: fk_actionpeople_affiliations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actionby
    ADD CONSTRAINT fk_actionpeople_affiliations FOREIGN KEY (affiliationid) REFERENCES affiliations(affiliationid) ON DELETE CASCADE;


--
-- TOC entry 5181 (class 2606 OID 176545)
-- Name: fk_actions_cv_actiontype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actions
    ADD CONSTRAINT fk_actions_cv_actiontype FOREIGN KEY (actiontypecv) REFERENCES cv_actiontype(name) ON DELETE CASCADE;


--
-- TOC entry 5180 (class 2606 OID 176550)
-- Name: fk_actions_methods; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY actions
    ADD CONSTRAINT fk_actions_methods FOREIGN KEY (methodid) REFERENCES methods(methodid) ON DELETE CASCADE;


--
-- TOC entry 5183 (class 2606 OID 176555)
-- Name: fk_affiliations_organizations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY affiliations
    ADD CONSTRAINT fk_affiliations_organizations FOREIGN KEY (organizationid) REFERENCES organizations(organizationid) ON DELETE CASCADE;


--
-- TOC entry 5182 (class 2606 OID 176560)
-- Name: fk_affiliations_people; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY affiliations
    ADD CONSTRAINT fk_affiliations_people FOREIGN KEY (personid) REFERENCES people(personid) ON DELETE CASCADE;


--
-- TOC entry 5186 (class 2606 OID 176565)
-- Name: fk_annotations_citations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY annotations
    ADD CONSTRAINT fk_annotations_citations FOREIGN KEY (citationid) REFERENCES citations(citationid) ON DELETE CASCADE;


--
-- TOC entry 5185 (class 2606 OID 176570)
-- Name: fk_annotations_cv_annotationtype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY annotations
    ADD CONSTRAINT fk_annotations_cv_annotationtype FOREIGN KEY (annotationtypecv) REFERENCES cv_annotationtype(name) ON DELETE CASCADE;


--
-- TOC entry 5184 (class 2606 OID 176575)
-- Name: fk_annotations_people; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY annotations
    ADD CONSTRAINT fk_annotations_people FOREIGN KEY (annotatorid) REFERENCES people(personid) ON DELETE CASCADE;


--
-- TOC entry 5195 (class 2606 OID 176580)
-- Name: fk_authorlists_citations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY authorlists
    ADD CONSTRAINT fk_authorlists_citations FOREIGN KEY (citationid) REFERENCES citations(citationid) ON DELETE CASCADE;


--
-- TOC entry 5194 (class 2606 OID 176585)
-- Name: fk_authorlists_people; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY authorlists
    ADD CONSTRAINT fk_authorlists_people FOREIGN KEY (personid) REFERENCES people(personid) ON DELETE CASCADE;


--
-- TOC entry 5197 (class 2606 OID 176590)
-- Name: fk_calibrationactions_actions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY calibrationactions
    ADD CONSTRAINT fk_calibrationactions_actions FOREIGN KEY (actionid) REFERENCES actions(actionid) ON DELETE CASCADE;


--
-- TOC entry 5196 (class 2606 OID 176595)
-- Name: fk_calibrationactions_instrumentoutputvariables; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY calibrationactions
    ADD CONSTRAINT fk_calibrationactions_instrumentoutputvariables FOREIGN KEY (instrumentoutputvariableid) REFERENCES instrumentoutputvariables(instrumentoutputvariableid) ON DELETE CASCADE;


--
-- TOC entry 5199 (class 2606 OID 176600)
-- Name: fk_calibrationreferenceequipment_calibrationactions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY calibrationreferenceequipment
    ADD CONSTRAINT fk_calibrationreferenceequipment_calibrationactions FOREIGN KEY (actionid) REFERENCES calibrationactions(actionid) ON DELETE CASCADE;


--
-- TOC entry 5198 (class 2606 OID 176605)
-- Name: fk_calibrationreferenceequipment_equipment; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY calibrationreferenceequipment
    ADD CONSTRAINT fk_calibrationreferenceequipment_equipment FOREIGN KEY (equipmentid) REFERENCES equipment(equipmentid) ON DELETE CASCADE;


--
-- TOC entry 5201 (class 2606 OID 176610)
-- Name: fk_calibrationstandards_calibrationactions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY calibrationstandards
    ADD CONSTRAINT fk_calibrationstandards_calibrationactions FOREIGN KEY (actionid) REFERENCES calibrationactions(actionid) ON DELETE CASCADE;


--
-- TOC entry 5204 (class 2606 OID 176615)
-- Name: fk_categoricalresults_cv_qualitycode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY categoricalresults
    ADD CONSTRAINT fk_categoricalresults_cv_qualitycode FOREIGN KEY (qualitycodecv) REFERENCES cv_qualitycode(name) ON DELETE CASCADE;


--
-- TOC entry 5203 (class 2606 OID 176620)
-- Name: fk_categoricalresults_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY categoricalresults
    ADD CONSTRAINT fk_categoricalresults_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5202 (class 2606 OID 176625)
-- Name: fk_categoricalresults_spatialreferences; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY categoricalresults
    ADD CONSTRAINT fk_categoricalresults_spatialreferences FOREIGN KEY (spatialreferenceid) REFERENCES spatialreferences(spatialreferenceid) ON DELETE CASCADE;


--
-- TOC entry 5206 (class 2606 OID 176630)
-- Name: fk_categoricalresultvalueannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY categoricalresultvalueannotations
    ADD CONSTRAINT fk_categoricalresultvalueannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5205 (class 2606 OID 176635)
-- Name: fk_categoricalresultvalueannotations_categoricalresultvalues; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY categoricalresultvalueannotations
    ADD CONSTRAINT fk_categoricalresultvalueannotations_categoricalresultvalues FOREIGN KEY (valueid) REFERENCES categoricalresultvalues(valueid) ON DELETE CASCADE;


--
-- TOC entry 5207 (class 2606 OID 176640)
-- Name: fk_categoricalresultvalues_categoricalresults; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY categoricalresultvalues
    ADD CONSTRAINT fk_categoricalresultvalues_categoricalresults FOREIGN KEY (resultid) REFERENCES categoricalresults(resultid) ON DELETE CASCADE;


--
-- TOC entry 5209 (class 2606 OID 176645)
-- Name: fk_citationextensionpropertyvalues_citations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY citationextensionpropertyvalues
    ADD CONSTRAINT fk_citationextensionpropertyvalues_citations FOREIGN KEY (citationid) REFERENCES citations(citationid) ON DELETE CASCADE;


--
-- TOC entry 5208 (class 2606 OID 176650)
-- Name: fk_citationextensionpropertyvalues_extensionproperties; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY citationextensionpropertyvalues
    ADD CONSTRAINT fk_citationextensionpropertyvalues_extensionproperties FOREIGN KEY (propertyid) REFERENCES extensionproperties(propertyid) ON DELETE CASCADE;


--
-- TOC entry 5211 (class 2606 OID 176655)
-- Name: fk_citationexternalidentifiers_citations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY citationexternalidentifiers
    ADD CONSTRAINT fk_citationexternalidentifiers_citations FOREIGN KEY (citationid) REFERENCES citations(citationid) ON DELETE CASCADE;


--
-- TOC entry 5210 (class 2606 OID 176660)
-- Name: fk_citationexternalidentifiers_externalidentifiersystems; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY citationexternalidentifiers
    ADD CONSTRAINT fk_citationexternalidentifiers_externalidentifiersystems FOREIGN KEY (externalidentifiersystemid) REFERENCES externalidentifiersystems(externalidentifiersystemid) ON DELETE CASCADE;


--
-- TOC entry 5217 (class 2606 OID 176665)
-- Name: fk_dataloggerfilecolumns_cv_aggregationstatistic; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerfilecolumns
    ADD CONSTRAINT fk_dataloggerfilecolumns_cv_aggregationstatistic FOREIGN KEY (aggregationstatisticcv) REFERENCES cv_aggregationstatistic(name) ON DELETE CASCADE;


--
-- TOC entry 5216 (class 2606 OID 176670)
-- Name: fk_dataloggerfilecolumns_dataloggerfiles; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerfilecolumns
    ADD CONSTRAINT fk_dataloggerfilecolumns_dataloggerfiles FOREIGN KEY (dataloggerfileid) REFERENCES dataloggerfiles(dataloggerfileid) ON DELETE CASCADE;


--
-- TOC entry 5215 (class 2606 OID 176675)
-- Name: fk_dataloggerfilecolumns_instrumentoutputvariables; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerfilecolumns
    ADD CONSTRAINT fk_dataloggerfilecolumns_instrumentoutputvariables FOREIGN KEY (instrumentoutputvariableid) REFERENCES instrumentoutputvariables(instrumentoutputvariableid) ON DELETE CASCADE;


--
-- TOC entry 5214 (class 2606 OID 176680)
-- Name: fk_dataloggerfilecolumns_recordingunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerfilecolumns
    ADD CONSTRAINT fk_dataloggerfilecolumns_recordingunits FOREIGN KEY (recordingintervalunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5213 (class 2606 OID 176685)
-- Name: fk_dataloggerfilecolumns_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerfilecolumns
    ADD CONSTRAINT fk_dataloggerfilecolumns_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5212 (class 2606 OID 176690)
-- Name: fk_dataloggerfilecolumns_scanunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerfilecolumns
    ADD CONSTRAINT fk_dataloggerfilecolumns_scanunits FOREIGN KEY (scanintervalunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5218 (class 2606 OID 176695)
-- Name: fk_dataloggerfiles_dataloggerprogramfiles; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerfiles
    ADD CONSTRAINT fk_dataloggerfiles_dataloggerprogramfiles FOREIGN KEY (programid) REFERENCES dataloggerprogramfiles(programid) ON DELETE CASCADE;


--
-- TOC entry 5219 (class 2606 OID 176700)
-- Name: fk_dataloggerprogramfiles_affiliations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataloggerprogramfiles
    ADD CONSTRAINT fk_dataloggerprogramfiles_affiliations FOREIGN KEY (affiliationid) REFERENCES affiliations(affiliationid) ON DELETE CASCADE;


--
-- TOC entry 5221 (class 2606 OID 176705)
-- Name: fk_dataquality_cv_dataqualitytype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataquality
    ADD CONSTRAINT fk_dataquality_cv_dataqualitytype FOREIGN KEY (dataqualitytypecv) REFERENCES cv_dataqualitytype(name) ON DELETE CASCADE;


--
-- TOC entry 5220 (class 2606 OID 176710)
-- Name: fk_dataquality_units; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY dataquality
    ADD CONSTRAINT fk_dataquality_units FOREIGN KEY (dataqualityvalueunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5224 (class 2606 OID 176715)
-- Name: fk_datasetcitations_citations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY datasetcitations
    ADD CONSTRAINT fk_datasetcitations_citations FOREIGN KEY (citationid) REFERENCES citations(citationid) ON DELETE CASCADE;


--
-- TOC entry 5223 (class 2606 OID 176720)
-- Name: fk_datasetcitations_cv_relationshiptype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY datasetcitations
    ADD CONSTRAINT fk_datasetcitations_cv_relationshiptype FOREIGN KEY (relationshiptypecv) REFERENCES cv_relationshiptype(name) ON DELETE CASCADE;


--
-- TOC entry 5222 (class 2606 OID 176725)
-- Name: fk_datasetcitations_datasets; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY datasetcitations
    ADD CONSTRAINT fk_datasetcitations_datasets FOREIGN KEY (datasetid) REFERENCES datasets(datasetid) ON DELETE CASCADE;


--
-- TOC entry 5225 (class 2606 OID 176730)
-- Name: fk_datasets_cv_datasettypecv; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY datasets
    ADD CONSTRAINT fk_datasets_cv_datasettypecv FOREIGN KEY (datasettypecv) REFERENCES cv_datasettype(name) ON DELETE CASCADE;


--
-- TOC entry 5227 (class 2606 OID 176735)
-- Name: fk_datasetsresults_datasets; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY datasetsresults
    ADD CONSTRAINT fk_datasetsresults_datasets FOREIGN KEY (datasetid) REFERENCES datasets(datasetid) ON DELETE CASCADE;


--
-- TOC entry 5226 (class 2606 OID 176740)
-- Name: fk_datasetsresults_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY datasetsresults
    ADD CONSTRAINT fk_datasetsresults_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5228 (class 2606 OID 176745)
-- Name: fk_directives_cv_directivetype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY directives
    ADD CONSTRAINT fk_directives_cv_directivetype FOREIGN KEY (directivetypecv) REFERENCES cv_directivetype(name) ON DELETE CASCADE;


--
-- TOC entry 5234 (class 2606 OID 176750)
-- Name: fk_equipment_cv_equipmenttype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipment
    ADD CONSTRAINT fk_equipment_cv_equipmenttype FOREIGN KEY (equipmenttypecv) REFERENCES cv_equipmenttype(name) ON DELETE CASCADE;


--
-- TOC entry 5233 (class 2606 OID 176755)
-- Name: fk_equipment_equipmentmodels; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipment
    ADD CONSTRAINT fk_equipment_equipmentmodels FOREIGN KEY (equipmentmodelid) REFERENCES equipmentmodels(equipmentmodelid) ON DELETE CASCADE;


--
-- TOC entry 5232 (class 2606 OID 176760)
-- Name: fk_equipment_organizations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipment
    ADD CONSTRAINT fk_equipment_organizations FOREIGN KEY (equipmentvendorid) REFERENCES organizations(organizationid) ON DELETE CASCADE;


--
-- TOC entry 5231 (class 2606 OID 176765)
-- Name: fk_equipment_people; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipment
    ADD CONSTRAINT fk_equipment_people FOREIGN KEY (equipmentownerid) REFERENCES people(personid) ON DELETE CASCADE;


--
-- TOC entry 5239 (class 2606 OID 176770)
-- Name: fk_equipmentactions_actions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipmentused
    ADD CONSTRAINT fk_equipmentactions_actions FOREIGN KEY (actionid) REFERENCES actions(actionid) ON DELETE CASCADE;


--
-- TOC entry 5238 (class 2606 OID 176775)
-- Name: fk_equipmentactions_equipment; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipmentused
    ADD CONSTRAINT fk_equipmentactions_equipment FOREIGN KEY (equipmentid) REFERENCES equipment(equipmentid) ON DELETE CASCADE;


--
-- TOC entry 5236 (class 2606 OID 176780)
-- Name: fk_equipmentannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipmentannotations
    ADD CONSTRAINT fk_equipmentannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5235 (class 2606 OID 176785)
-- Name: fk_equipmentannotations_equipment; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipmentannotations
    ADD CONSTRAINT fk_equipmentannotations_equipment FOREIGN KEY (equipmentid) REFERENCES equipment(equipmentid) ON DELETE CASCADE;


--
-- TOC entry 5237 (class 2606 OID 176790)
-- Name: fk_equipmentmodels_organizations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY equipmentmodels
    ADD CONSTRAINT fk_equipmentmodels_organizations FOREIGN KEY (modelmanufacturerid) REFERENCES organizations(organizationid) ON DELETE CASCADE;


--
-- TOC entry 5241 (class 2606 OID 176795)
-- Name: fk_extensionproperties_cv_propertydatatype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY extensionproperties
    ADD CONSTRAINT fk_extensionproperties_cv_propertydatatype FOREIGN KEY (propertydatatypecv) REFERENCES cv_propertydatatype(name) ON DELETE CASCADE;


--
-- TOC entry 5240 (class 2606 OID 176800)
-- Name: fk_extensionproperties_units; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY extensionproperties
    ADD CONSTRAINT fk_extensionproperties_units FOREIGN KEY (propertyunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5242 (class 2606 OID 176805)
-- Name: fk_externalidentifiersystems_organizations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY externalidentifiersystems
    ADD CONSTRAINT fk_externalidentifiersystems_organizations FOREIGN KEY (identifiersystemorganizationid) REFERENCES organizations(organizationid) ON DELETE CASCADE;


--
-- TOC entry 5244 (class 2606 OID 176810)
-- Name: fk_featureactions_actions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY featureactions
    ADD CONSTRAINT fk_featureactions_actions FOREIGN KEY (actionid) REFERENCES actions(actionid) ON DELETE CASCADE;


--
-- TOC entry 5243 (class 2606 OID 176815)
-- Name: fk_featureactions_samplingfeatures; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY featureactions
    ADD CONSTRAINT fk_featureactions_samplingfeatures FOREIGN KEY (samplingfeatureid) REFERENCES samplingfeatures(samplingfeatureid) ON DELETE CASCADE;


--
-- TOC entry 5333 (class 2606 OID 176820)
-- Name: fk_featureparents_featuresparent; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedfeatures
    ADD CONSTRAINT fk_featureparents_featuresparent FOREIGN KEY (relatedfeatureid) REFERENCES samplingfeatures(samplingfeatureid) ON DELETE CASCADE;


--
-- TOC entry 5332 (class 2606 OID 176825)
-- Name: fk_featureparents_samplingfeatures; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedfeatures
    ADD CONSTRAINT fk_featureparents_samplingfeatures FOREIGN KEY (samplingfeatureid) REFERENCES samplingfeatures(samplingfeatureid) ON DELETE CASCADE;


--
-- TOC entry 5331 (class 2606 OID 176830)
-- Name: fk_featureparents_spatialoffsets; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedfeatures
    ADD CONSTRAINT fk_featureparents_spatialoffsets FOREIGN KEY (spatialoffsetid) REFERENCES spatialoffsets(spatialoffsetid) ON DELETE CASCADE;


--
-- TOC entry 5200 (class 2606 OID 176835)
-- Name: fk_fieldcalibrationstandards_referencematerials; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY calibrationstandards
    ADD CONSTRAINT fk_fieldcalibrationstandards_referencematerials FOREIGN KEY (referencematerialid) REFERENCES referencematerials(referencematerialid) ON DELETE CASCADE;


--
-- TOC entry 5248 (class 2606 OID 176840)
-- Name: fk_instrumentoutputvariables_equipmentmodels; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY instrumentoutputvariables
    ADD CONSTRAINT fk_instrumentoutputvariables_equipmentmodels FOREIGN KEY (modelid) REFERENCES equipmentmodels(equipmentmodelid) ON DELETE CASCADE;


--
-- TOC entry 5247 (class 2606 OID 176845)
-- Name: fk_instrumentoutputvariables_methods; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY instrumentoutputvariables
    ADD CONSTRAINT fk_instrumentoutputvariables_methods FOREIGN KEY (instrumentmethodid) REFERENCES methods(methodid) ON DELETE CASCADE;


--
-- TOC entry 5246 (class 2606 OID 176850)
-- Name: fk_instrumentoutputvariables_units; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY instrumentoutputvariables
    ADD CONSTRAINT fk_instrumentoutputvariables_units FOREIGN KEY (instrumentrawoutputunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5245 (class 2606 OID 176855)
-- Name: fk_instrumentoutputvariables_variables; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY instrumentoutputvariables
    ADD CONSTRAINT fk_instrumentoutputvariables_variables FOREIGN KEY (variableid) REFERENCES variables(variableid) ON DELETE CASCADE;


--
-- TOC entry 5249 (class 2606 OID 176860)
-- Name: fk_maintenanceactions_actions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY maintenanceactions
    ADD CONSTRAINT fk_maintenanceactions_actions FOREIGN KEY (actionid) REFERENCES actions(actionid) ON DELETE CASCADE;


--
-- TOC entry 5258 (class 2606 OID 176865)
-- Name: fk_measurementresults_aiunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresults
    ADD CONSTRAINT fk_measurementresults_aiunits FOREIGN KEY (timeaggregationintervalunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5257 (class 2606 OID 176870)
-- Name: fk_measurementresults_cv_aggregationstatistic; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresults
    ADD CONSTRAINT fk_measurementresults_cv_aggregationstatistic FOREIGN KEY (aggregationstatisticcv) REFERENCES cv_aggregationstatistic(name) ON DELETE CASCADE;


--
-- TOC entry 5256 (class 2606 OID 176875)
-- Name: fk_measurementresults_cv_censorcode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresults
    ADD CONSTRAINT fk_measurementresults_cv_censorcode FOREIGN KEY (censorcodecv) REFERENCES cv_censorcode(name) ON DELETE CASCADE;


--
-- TOC entry 5255 (class 2606 OID 176880)
-- Name: fk_measurementresults_cv_qualitycode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresults
    ADD CONSTRAINT fk_measurementresults_cv_qualitycode FOREIGN KEY (qualitycodecv) REFERENCES cv_qualitycode(name) ON DELETE CASCADE;


--
-- TOC entry 5254 (class 2606 OID 176885)
-- Name: fk_measurementresults_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresults
    ADD CONSTRAINT fk_measurementresults_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5253 (class 2606 OID 176890)
-- Name: fk_measurementresults_spatialreferences; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresults
    ADD CONSTRAINT fk_measurementresults_spatialreferences FOREIGN KEY (spatialreferenceid) REFERENCES spatialreferences(spatialreferenceid) ON DELETE CASCADE;


--
-- TOC entry 5252 (class 2606 OID 176895)
-- Name: fk_measurementresults_xunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresults
    ADD CONSTRAINT fk_measurementresults_xunits FOREIGN KEY (xlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5251 (class 2606 OID 176900)
-- Name: fk_measurementresults_yunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresults
    ADD CONSTRAINT fk_measurementresults_yunits FOREIGN KEY (ylocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5250 (class 2606 OID 176905)
-- Name: fk_measurementresults_zunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresults
    ADD CONSTRAINT fk_measurementresults_zunits FOREIGN KEY (zlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5260 (class 2606 OID 176910)
-- Name: fk_measurementresultvalueannotations_measurementresultvalues; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresultvalueannotations
    ADD CONSTRAINT fk_measurementresultvalueannotations_measurementresultvalues FOREIGN KEY (valueid) REFERENCES measurementresultvalues(valueid) ON DELETE CASCADE;


--
-- TOC entry 5261 (class 2606 OID 176923)
-- Name: fk_measurementresultvalues_measurementresults; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresultvalues
    ADD CONSTRAINT fk_measurementresultvalues_measurementresults FOREIGN KEY (resultid) REFERENCES measurementresults(resultid) ON DELETE CASCADE;


--
-- TOC entry 5263 (class 2606 OID 176932)
-- Name: fk_methodannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodannotations
    ADD CONSTRAINT fk_methodannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5262 (class 2606 OID 176937)
-- Name: fk_methodannotations_methods; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodannotations
    ADD CONSTRAINT fk_methodannotations_methods FOREIGN KEY (methodid) REFERENCES methods(methodid) ON DELETE CASCADE;


--
-- TOC entry 5266 (class 2606 OID 176942)
-- Name: fk_methodcitations_citations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodcitations
    ADD CONSTRAINT fk_methodcitations_citations FOREIGN KEY (citationid) REFERENCES citations(citationid) ON DELETE CASCADE;


--
-- TOC entry 5265 (class 2606 OID 176947)
-- Name: fk_methodcitations_cv_relationshiptype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodcitations
    ADD CONSTRAINT fk_methodcitations_cv_relationshiptype FOREIGN KEY (relationshiptypecv) REFERENCES cv_relationshiptype(name) ON DELETE CASCADE;


--
-- TOC entry 5264 (class 2606 OID 176952)
-- Name: fk_methodcitations_methods; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodcitations
    ADD CONSTRAINT fk_methodcitations_methods FOREIGN KEY (methodid) REFERENCES methods(methodid) ON DELETE CASCADE;


--
-- TOC entry 5268 (class 2606 OID 176957)
-- Name: fk_methodextensionpropertyvalues_extensionproperties; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodextensionpropertyvalues
    ADD CONSTRAINT fk_methodextensionpropertyvalues_extensionproperties FOREIGN KEY (propertyid) REFERENCES extensionproperties(propertyid) ON DELETE CASCADE;


--
-- TOC entry 5267 (class 2606 OID 176962)
-- Name: fk_methodextensionpropertyvalues_methods; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodextensionpropertyvalues
    ADD CONSTRAINT fk_methodextensionpropertyvalues_methods FOREIGN KEY (methodid) REFERENCES methods(methodid) ON DELETE CASCADE;


--
-- TOC entry 5270 (class 2606 OID 176967)
-- Name: fk_methodexternalidentifiers_externalidentifiersystems; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodexternalidentifiers
    ADD CONSTRAINT fk_methodexternalidentifiers_externalidentifiersystems FOREIGN KEY (externalidentifiersystemid) REFERENCES externalidentifiersystems(externalidentifiersystemid) ON DELETE CASCADE;


--
-- TOC entry 5269 (class 2606 OID 176972)
-- Name: fk_methodexternalidentifiers_methods; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methodexternalidentifiers
    ADD CONSTRAINT fk_methodexternalidentifiers_methods FOREIGN KEY (methodid) REFERENCES methods(methodid) ON DELETE CASCADE;


--
-- TOC entry 5272 (class 2606 OID 176977)
-- Name: fk_methods_cv_methodtype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methods
    ADD CONSTRAINT fk_methods_cv_methodtype FOREIGN KEY (methodtypecv) REFERENCES cv_methodtype(name) ON DELETE CASCADE;


--
-- TOC entry 5271 (class 2606 OID 176982)
-- Name: fk_methods_organizations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY methods
    ADD CONSTRAINT fk_methods_organizations FOREIGN KEY (organizationid) REFERENCES organizations(organizationid) ON DELETE CASCADE;


--
-- TOC entry 5274 (class 2606 OID 176987)
-- Name: fk_modelaffiliations_affiliations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY modelaffiliations
    ADD CONSTRAINT fk_modelaffiliations_affiliations FOREIGN KEY (affiliationid) REFERENCES affiliations(affiliationid) ON DELETE CASCADE;


--
-- TOC entry 5273 (class 2606 OID 176992)
-- Name: fk_modelaffiliations_models; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY modelaffiliations
    ADD CONSTRAINT fk_modelaffiliations_models FOREIGN KEY (modelid) REFERENCES models(modelid) ON DELETE CASCADE;


--
-- TOC entry 5276 (class 2606 OID 176997)
-- Name: fk_organizations_cv_organizationtype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY organizations
    ADD CONSTRAINT fk_organizations_cv_organizationtype FOREIGN KEY (organizationtypecv) REFERENCES cv_organizationtype(name) ON DELETE CASCADE;


--
-- TOC entry 5275 (class 2606 OID 177002)
-- Name: fk_organizations_organizations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY organizations
    ADD CONSTRAINT fk_organizations_organizations FOREIGN KEY (parentorganizationid) REFERENCES organizations(organizationid) ON DELETE CASCADE;


--
-- TOC entry 5417 (class 2606 OID 177007)
-- Name: fk_parenttaxon_taxon; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY taxonomicclassifiers
    ADD CONSTRAINT fk_parenttaxon_taxon FOREIGN KEY (parenttaxonomicclassifierid) REFERENCES taxonomicclassifiers(taxonomicclassifierid) ON DELETE CASCADE;


--
-- TOC entry 5278 (class 2606 OID 177012)
-- Name: fk_personexternalidentifiers_externalidentifiersystems; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY personexternalidentifiers
    ADD CONSTRAINT fk_personexternalidentifiers_externalidentifiersystems FOREIGN KEY (externalidentifiersystemid) REFERENCES externalidentifiersystems(externalidentifiersystemid) ON DELETE CASCADE;


--
-- TOC entry 5277 (class 2606 OID 177017)
-- Name: fk_personexternalidentifiers_people; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY personexternalidentifiers
    ADD CONSTRAINT fk_personexternalidentifiers_people FOREIGN KEY (personid) REFERENCES people(personid) ON DELETE CASCADE;


--
-- TOC entry 5284 (class 2606 OID 177022)
-- Name: fk_pointcoverageresults_cv_aggregationstatistic; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresults
    ADD CONSTRAINT fk_pointcoverageresults_cv_aggregationstatistic FOREIGN KEY (aggregationstatisticcv) REFERENCES cv_aggregationstatistic(name) ON DELETE CASCADE;


--
-- TOC entry 5283 (class 2606 OID 177027)
-- Name: fk_pointcoverageresults_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresults
    ADD CONSTRAINT fk_pointcoverageresults_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5282 (class 2606 OID 177032)
-- Name: fk_pointcoverageresults_spatialreferences; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresults
    ADD CONSTRAINT fk_pointcoverageresults_spatialreferences FOREIGN KEY (spatialreferenceid) REFERENCES spatialreferences(spatialreferenceid) ON DELETE CASCADE;


--
-- TOC entry 5281 (class 2606 OID 177037)
-- Name: fk_pointcoverageresults_xunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresults
    ADD CONSTRAINT fk_pointcoverageresults_xunits FOREIGN KEY (intendedxspacingunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5280 (class 2606 OID 177042)
-- Name: fk_pointcoverageresults_yunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresults
    ADD CONSTRAINT fk_pointcoverageresults_yunits FOREIGN KEY (intendedyspacingunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5279 (class 2606 OID 177047)
-- Name: fk_pointcoverageresults_zunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresults
    ADD CONSTRAINT fk_pointcoverageresults_zunits FOREIGN KEY (zlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5286 (class 2606 OID 177052)
-- Name: fk_pointcoverageresultvalueannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresultvalueannotations
    ADD CONSTRAINT fk_pointcoverageresultvalueannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5285 (class 2606 OID 177057)
-- Name: fk_pointcoverageresultvalueannotations_pointcoverageresultvalue; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresultvalueannotations
    ADD CONSTRAINT fk_pointcoverageresultvalueannotations_pointcoverageresultvalue FOREIGN KEY (valueid) REFERENCES pointcoverageresultvalues(valueid) ON DELETE CASCADE;


--
-- TOC entry 5291 (class 2606 OID 177062)
-- Name: fk_pointcoverageresultvalues_cv_censorcode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresultvalues
    ADD CONSTRAINT fk_pointcoverageresultvalues_cv_censorcode FOREIGN KEY (censorcodecv) REFERENCES cv_censorcode(name) ON DELETE CASCADE;


--
-- TOC entry 5290 (class 2606 OID 177067)
-- Name: fk_pointcoverageresultvalues_cv_qualitycode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresultvalues
    ADD CONSTRAINT fk_pointcoverageresultvalues_cv_qualitycode FOREIGN KEY (qualitycodecv) REFERENCES cv_qualitycode(name) ON DELETE CASCADE;


--
-- TOC entry 5289 (class 2606 OID 177072)
-- Name: fk_pointcoverageresultvalues_pointcoverageresults; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresultvalues
    ADD CONSTRAINT fk_pointcoverageresultvalues_pointcoverageresults FOREIGN KEY (resultid) REFERENCES pointcoverageresults(resultid) ON DELETE CASCADE;


--
-- TOC entry 5288 (class 2606 OID 177077)
-- Name: fk_pointcoverageresultvalues_xunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresultvalues
    ADD CONSTRAINT fk_pointcoverageresultvalues_xunits FOREIGN KEY (xlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5287 (class 2606 OID 177082)
-- Name: fk_pointcoverageresultvalues_yunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY pointcoverageresultvalues
    ADD CONSTRAINT fk_pointcoverageresultvalues_yunits FOREIGN KEY (ylocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5298 (class 2606 OID 177087)
-- Name: fk_profileresults_cv_aggregationstatistic; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresults
    ADD CONSTRAINT fk_profileresults_cv_aggregationstatistic FOREIGN KEY (aggregationstatisticcv) REFERENCES cv_aggregationstatistic(name) ON DELETE CASCADE;


--
-- TOC entry 5297 (class 2606 OID 177092)
-- Name: fk_profileresults_dunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresults
    ADD CONSTRAINT fk_profileresults_dunits FOREIGN KEY (intendedzspacingunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5296 (class 2606 OID 177097)
-- Name: fk_profileresults_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresults
    ADD CONSTRAINT fk_profileresults_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5295 (class 2606 OID 177102)
-- Name: fk_profileresults_spatialreferences; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresults
    ADD CONSTRAINT fk_profileresults_spatialreferences FOREIGN KEY (spatialreferenceid) REFERENCES spatialreferences(spatialreferenceid) ON DELETE CASCADE;


--
-- TOC entry 5294 (class 2606 OID 177107)
-- Name: fk_profileresults_tunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresults
    ADD CONSTRAINT fk_profileresults_tunits FOREIGN KEY (intendedtimespacingunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5293 (class 2606 OID 177112)
-- Name: fk_profileresults_xunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresults
    ADD CONSTRAINT fk_profileresults_xunits FOREIGN KEY (xlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5292 (class 2606 OID 177117)
-- Name: fk_profileresults_yunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresults
    ADD CONSTRAINT fk_profileresults_yunits FOREIGN KEY (ylocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5300 (class 2606 OID 177122)
-- Name: fk_profileresultvalueannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresultvalueannotations
    ADD CONSTRAINT fk_profileresultvalueannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5299 (class 2606 OID 177127)
-- Name: fk_profileresultvalueannotations_profileresultvalues; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresultvalueannotations
    ADD CONSTRAINT fk_profileresultvalueannotations_profileresultvalues FOREIGN KEY (valueid) REFERENCES profileresultvalues(valueid) ON DELETE CASCADE;


--
-- TOC entry 5305 (class 2606 OID 177133)
-- Name: fk_profileresultvalues_aiunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresultvalues
    ADD CONSTRAINT fk_profileresultvalues_aiunits FOREIGN KEY (timeaggregationintervalunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5304 (class 2606 OID 177138)
-- Name: fk_profileresultvalues_cv_censorcode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresultvalues
    ADD CONSTRAINT fk_profileresultvalues_cv_censorcode FOREIGN KEY (censorcodecv) REFERENCES cv_censorcode(name) ON DELETE CASCADE;


--
-- TOC entry 5303 (class 2606 OID 177143)
-- Name: fk_profileresultvalues_cv_qualitycode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresultvalues
    ADD CONSTRAINT fk_profileresultvalues_cv_qualitycode FOREIGN KEY (qualitycodecv) REFERENCES cv_qualitycode(name) ON DELETE CASCADE;


--
-- TOC entry 5302 (class 2606 OID 177148)
-- Name: fk_profileresultvalues_dunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresultvalues
    ADD CONSTRAINT fk_profileresultvalues_dunits FOREIGN KEY (zlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5301 (class 2606 OID 177153)
-- Name: fk_profileresultvalues_profileresults; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY profileresultvalues
    ADD CONSTRAINT fk_profileresultvalues_profileresults FOREIGN KEY (resultid) REFERENCES profileresults(resultid) ON DELETE CASCADE;


--
-- TOC entry 5310 (class 2606 OID 177158)
-- Name: fk_referencematerials_cv_referencematerialmedium; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY referencematerials
    ADD CONSTRAINT fk_referencematerials_cv_referencematerialmedium FOREIGN KEY (referencematerialmediumcv) REFERENCES cv_referencematerialmedium(name) ON DELETE CASCADE;


--
-- TOC entry 5309 (class 2606 OID 177163)
-- Name: fk_referencematerials_organizations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY referencematerials
    ADD CONSTRAINT fk_referencematerials_organizations FOREIGN KEY (referencematerialorganizationid) REFERENCES organizations(organizationid) ON DELETE CASCADE;


--
-- TOC entry 5308 (class 2606 OID 177168)
-- Name: fk_referencematerials_samplingfeatures; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY referencematerials
    ADD CONSTRAINT fk_referencematerials_samplingfeatures FOREIGN KEY (samplingfeatureid) REFERENCES samplingfeatures(samplingfeatureid) ON DELETE CASCADE;


--
-- TOC entry 5314 (class 2606 OID 177173)
-- Name: fk_referencematerialvalues_citations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY referencematerialvalues
    ADD CONSTRAINT fk_referencematerialvalues_citations FOREIGN KEY (citationid) REFERENCES citations(citationid) ON DELETE CASCADE;


--
-- TOC entry 5313 (class 2606 OID 177178)
-- Name: fk_referencematerialvalues_referencematerials; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY referencematerialvalues
    ADD CONSTRAINT fk_referencematerialvalues_referencematerials FOREIGN KEY (referencematerialid) REFERENCES referencematerials(referencematerialid) ON DELETE CASCADE;


--
-- TOC entry 5312 (class 2606 OID 177183)
-- Name: fk_referencematerialvalues_units; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY referencematerialvalues
    ADD CONSTRAINT fk_referencematerialvalues_units FOREIGN KEY (unitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5311 (class 2606 OID 177188)
-- Name: fk_referencematerialvalues_variables; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY referencematerialvalues
    ADD CONSTRAINT fk_referencematerialvalues_variables FOREIGN KEY (variableid) REFERENCES variables(variableid) ON DELETE CASCADE;


--
-- TOC entry 5307 (class 2606 OID 177193)
-- Name: fk_refmaterialextidentifiers_extidentifiersystems; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY referencematerialexternalidentifiers
    ADD CONSTRAINT fk_refmaterialextidentifiers_extidentifiersystems FOREIGN KEY (externalidentifiersystemid) REFERENCES externalidentifiersystems(externalidentifiersystemid) ON DELETE CASCADE;


--
-- TOC entry 5306 (class 2606 OID 177199)
-- Name: fk_refmaterialextidentifiers_refmaterials; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY referencematerialexternalidentifiers
    ADD CONSTRAINT fk_refmaterialextidentifiers_refmaterials FOREIGN KEY (referencematerialid) REFERENCES referencematerials(referencematerialid) ON DELETE CASCADE;


--
-- TOC entry 5317 (class 2606 OID 177204)
-- Name: fk_relatedactions_actions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedactions
    ADD CONSTRAINT fk_relatedactions_actions FOREIGN KEY (actionid) REFERENCES actions(actionid) ON DELETE CASCADE;


--
-- TOC entry 5316 (class 2606 OID 177209)
-- Name: fk_relatedactions_actions_arerelated; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedactions
    ADD CONSTRAINT fk_relatedactions_actions_arerelated FOREIGN KEY (relatedactionid) REFERENCES actions(actionid) ON DELETE CASCADE;


--
-- TOC entry 5315 (class 2606 OID 177214)
-- Name: fk_relatedactions_cv_relationshiptype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedactions
    ADD CONSTRAINT fk_relatedactions_cv_relationshiptype FOREIGN KEY (relationshiptypecv) REFERENCES cv_relationshiptype(name) ON DELETE CASCADE;


--
-- TOC entry 5320 (class 2606 OID 177219)
-- Name: fk_relatedannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedannotations
    ADD CONSTRAINT fk_relatedannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5319 (class 2606 OID 177224)
-- Name: fk_relatedannotations_annotations_arerelated; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedannotations
    ADD CONSTRAINT fk_relatedannotations_annotations_arerelated FOREIGN KEY (relatedannotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5318 (class 2606 OID 177229)
-- Name: fk_relatedannotations_cv_relationshiptype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedannotations
    ADD CONSTRAINT fk_relatedannotations_cv_relationshiptype FOREIGN KEY (relationshiptypecv) REFERENCES cv_relationshiptype(name) ON DELETE CASCADE;


--
-- TOC entry 5323 (class 2606 OID 177234)
-- Name: fk_relatedcitations_citations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedcitations
    ADD CONSTRAINT fk_relatedcitations_citations FOREIGN KEY (citationid) REFERENCES citations(citationid) ON DELETE CASCADE;


--
-- TOC entry 5322 (class 2606 OID 177239)
-- Name: fk_relatedcitations_citations_arerelated; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedcitations
    ADD CONSTRAINT fk_relatedcitations_citations_arerelated FOREIGN KEY (relatedcitationid) REFERENCES citations(citationid) ON DELETE CASCADE;


--
-- TOC entry 5321 (class 2606 OID 177244)
-- Name: fk_relatedcitations_cv_relationshiptype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedcitations
    ADD CONSTRAINT fk_relatedcitations_cv_relationshiptype FOREIGN KEY (relationshiptypecv) REFERENCES cv_relationshiptype(name) ON DELETE CASCADE;


--
-- TOC entry 5326 (class 2606 OID 177249)
-- Name: fk_relateddatasets_cv_relationshiptype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relateddatasets
    ADD CONSTRAINT fk_relateddatasets_cv_relationshiptype FOREIGN KEY (relationshiptypecv) REFERENCES cv_relationshiptype(name) ON DELETE CASCADE;


--
-- TOC entry 5325 (class 2606 OID 177254)
-- Name: fk_relateddatasets_datasets; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relateddatasets
    ADD CONSTRAINT fk_relateddatasets_datasets FOREIGN KEY (datasetid) REFERENCES datasets(datasetid) ON DELETE CASCADE;


--
-- TOC entry 5324 (class 2606 OID 177259)
-- Name: fk_relateddatasets_datasets_arerelated; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relateddatasets
    ADD CONSTRAINT fk_relateddatasets_datasets_arerelated FOREIGN KEY (relateddatasetid) REFERENCES datasets(datasetid) ON DELETE CASCADE;


--
-- TOC entry 5329 (class 2606 OID 177264)
-- Name: fk_relatedequipment_cv_relationshiptype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedequipment
    ADD CONSTRAINT fk_relatedequipment_cv_relationshiptype FOREIGN KEY (relationshiptypecv) REFERENCES cv_relationshiptype(name) ON DELETE CASCADE;


--
-- TOC entry 5328 (class 2606 OID 177269)
-- Name: fk_relatedequipment_equipment; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedequipment
    ADD CONSTRAINT fk_relatedequipment_equipment FOREIGN KEY (equipmentid) REFERENCES equipment(equipmentid) ON DELETE CASCADE;


--
-- TOC entry 5327 (class 2606 OID 177274)
-- Name: fk_relatedequipment_equipment_arerelated; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedequipment
    ADD CONSTRAINT fk_relatedequipment_equipment_arerelated FOREIGN KEY (relatedequipmentid) REFERENCES equipment(equipmentid) ON DELETE CASCADE;


--
-- TOC entry 5330 (class 2606 OID 177279)
-- Name: fk_relatedfeatures_cv_relationshiptype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedfeatures
    ADD CONSTRAINT fk_relatedfeatures_cv_relationshiptype FOREIGN KEY (relationshiptypecv) REFERENCES cv_relationshiptype(name) ON DELETE CASCADE;


--
-- TOC entry 5335 (class 2606 OID 177284)
-- Name: fk_relatedmodels_cv_relationshiptype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedmodels
    ADD CONSTRAINT fk_relatedmodels_cv_relationshiptype FOREIGN KEY (relationshiptypecv) REFERENCES cv_relationshiptype(name) ON DELETE CASCADE;


--
-- TOC entry 5334 (class 2606 OID 177289)
-- Name: fk_relatedmodels_models; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedmodels
    ADD CONSTRAINT fk_relatedmodels_models FOREIGN KEY (modelid) REFERENCES models(modelid) ON DELETE CASCADE;


--
-- TOC entry 5338 (class 2606 OID 177294)
-- Name: fk_relatedresults_cv_relationshiptype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedresults
    ADD CONSTRAINT fk_relatedresults_cv_relationshiptype FOREIGN KEY (relationshiptypecv) REFERENCES cv_relationshiptype(name) ON DELETE CASCADE;


--
-- TOC entry 5337 (class 2606 OID 177299)
-- Name: fk_relatedresults_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedresults
    ADD CONSTRAINT fk_relatedresults_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5336 (class 2606 OID 177304)
-- Name: fk_relatedresults_results_arerelated; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY relatedresults
    ADD CONSTRAINT fk_relatedresults_results_arerelated FOREIGN KEY (relatedresultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5340 (class 2606 OID 177309)
-- Name: fk_resultannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultannotations
    ADD CONSTRAINT fk_resultannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5339 (class 2606 OID 177314)
-- Name: fk_resultannotations_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultannotations
    ADD CONSTRAINT fk_resultannotations_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5342 (class 2606 OID 177319)
-- Name: fk_resultderivationequations_derivationequations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultderivationequations
    ADD CONSTRAINT fk_resultderivationequations_derivationequations FOREIGN KEY (derivationequationid) REFERENCES derivationequations(derivationequationid) ON DELETE CASCADE;


--
-- TOC entry 5341 (class 2606 OID 177324)
-- Name: fk_resultderivationequations_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultderivationequations
    ADD CONSTRAINT fk_resultderivationequations_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5344 (class 2606 OID 177329)
-- Name: fk_resultextensionpropertyvalues_extensionproperties; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultextensionpropertyvalues
    ADD CONSTRAINT fk_resultextensionpropertyvalues_extensionproperties FOREIGN KEY (propertyid) REFERENCES extensionproperties(propertyid) ON DELETE CASCADE;


--
-- TOC entry 5343 (class 2606 OID 177334)
-- Name: fk_resultextensionpropertyvalues_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultextensionpropertyvalues
    ADD CONSTRAINT fk_resultextensionpropertyvalues_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5346 (class 2606 OID 177339)
-- Name: fk_resultnormalizationvalues_referencematerialvalues; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultnormalizationvalues
    ADD CONSTRAINT fk_resultnormalizationvalues_referencematerialvalues FOREIGN KEY (normalizedbyreferencematerialvalueid) REFERENCES referencematerialvalues(referencematerialvalueid) ON DELETE CASCADE;


--
-- TOC entry 5345 (class 2606 OID 177344)
-- Name: fk_resultnormalizationvalues_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultnormalizationvalues
    ADD CONSTRAINT fk_resultnormalizationvalues_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5354 (class 2606 OID 177349)
-- Name: fk_results_cv_medium; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY results
    ADD CONSTRAINT fk_results_cv_medium FOREIGN KEY (sampledmediumcv) REFERENCES cv_medium(name) ON DELETE CASCADE;


--
-- TOC entry 5353 (class 2606 OID 177354)
-- Name: fk_results_cv_resulttype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY results
    ADD CONSTRAINT fk_results_cv_resulttype FOREIGN KEY (resulttypecv) REFERENCES cv_resulttype(name) ON DELETE CASCADE;


--
-- TOC entry 5352 (class 2606 OID 177359)
-- Name: fk_results_cv_status; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY results
    ADD CONSTRAINT fk_results_cv_status FOREIGN KEY (statuscv) REFERENCES cv_status(name) ON DELETE CASCADE;


--
-- TOC entry 5351 (class 2606 OID 177364)
-- Name: fk_results_featureactions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY results
    ADD CONSTRAINT fk_results_featureactions FOREIGN KEY (featureactionid) REFERENCES featureactions(featureactionid) ON DELETE CASCADE;


--
-- TOC entry 5350 (class 2606 OID 177369)
-- Name: fk_results_processinglevels; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY results
    ADD CONSTRAINT fk_results_processinglevels FOREIGN KEY (processinglevelid) REFERENCES processinglevels(processinglevelid) ON DELETE CASCADE;


--
-- TOC entry 5349 (class 2606 OID 177374)
-- Name: fk_results_taxonomicclassifiers; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY results
    ADD CONSTRAINT fk_results_taxonomicclassifiers FOREIGN KEY (taxonomicclassifierid) REFERENCES taxonomicclassifiers(taxonomicclassifierid) ON DELETE CASCADE;


--
-- TOC entry 5348 (class 2606 OID 177379)
-- Name: fk_results_units; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY results
    ADD CONSTRAINT fk_results_units FOREIGN KEY (unitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5347 (class 2606 OID 177384)
-- Name: fk_results_variables; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY results
    ADD CONSTRAINT fk_results_variables FOREIGN KEY (variableid) REFERENCES variables(variableid) ON DELETE CASCADE;


--
-- TOC entry 5356 (class 2606 OID 177389)
-- Name: fk_resultsdataquality_dataquality; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultsdataquality
    ADD CONSTRAINT fk_resultsdataquality_dataquality FOREIGN KEY (dataqualityid) REFERENCES dataquality(dataqualityid) ON DELETE CASCADE;


--
-- TOC entry 5355 (class 2606 OID 177394)
-- Name: fk_resultsdataquality_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY resultsdataquality
    ADD CONSTRAINT fk_resultsdataquality_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5259 (class 2606 OID 177399)
-- Name: fk_resultvalueannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY measurementresultvalueannotations
    ADD CONSTRAINT fk_resultvalueannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5358 (class 2606 OID 177406)
-- Name: fk_samplingfeatureannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatureannotations
    ADD CONSTRAINT fk_samplingfeatureannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5357 (class 2606 OID 177411)
-- Name: fk_samplingfeatureannotations_samplingfeatures; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatureannotations
    ADD CONSTRAINT fk_samplingfeatureannotations_samplingfeatures FOREIGN KEY (samplingfeatureid) REFERENCES samplingfeatures(samplingfeatureid) ON DELETE CASCADE;


--
-- TOC entry 5360 (class 2606 OID 177416)
-- Name: fk_samplingfeatureextensionpropertyvalues_extensionproperties; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatureextensionpropertyvalues
    ADD CONSTRAINT fk_samplingfeatureextensionpropertyvalues_extensionproperties FOREIGN KEY (propertyid) REFERENCES extensionproperties(propertyid) ON DELETE CASCADE;


--
-- TOC entry 5359 (class 2606 OID 177421)
-- Name: fk_samplingfeatureextensionpropertyvalues_samplingfeatures; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatureextensionpropertyvalues
    ADD CONSTRAINT fk_samplingfeatureextensionpropertyvalues_samplingfeatures FOREIGN KEY (samplingfeatureid) REFERENCES samplingfeatures(samplingfeatureid) ON DELETE CASCADE;


--
-- TOC entry 5362 (class 2606 OID 177426)
-- Name: fk_samplingfeatureexternalidentifiers_externalidentifiersystems; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatureexternalidentifiers
    ADD CONSTRAINT fk_samplingfeatureexternalidentifiers_externalidentifiersystems FOREIGN KEY (externalidentifiersystemid) REFERENCES externalidentifiersystems(externalidentifiersystemid) ON DELETE CASCADE;


--
-- TOC entry 5361 (class 2606 OID 177431)
-- Name: fk_samplingfeatureexternalidentifiers_samplingfeatures; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatureexternalidentifiers
    ADD CONSTRAINT fk_samplingfeatureexternalidentifiers_samplingfeatures FOREIGN KEY (samplingfeatureid) REFERENCES samplingfeatures(samplingfeatureid) ON DELETE CASCADE;


--
-- TOC entry 5365 (class 2606 OID 177436)
-- Name: fk_samplingfeatures_cv_elevationdatum; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatures
    ADD CONSTRAINT fk_samplingfeatures_cv_elevationdatum FOREIGN KEY (elevationdatumcv) REFERENCES cv_elevationdatum(name) ON DELETE CASCADE;


--
-- TOC entry 5364 (class 2606 OID 177441)
-- Name: fk_samplingfeatures_cv_samplingfeaturegeotype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatures
    ADD CONSTRAINT fk_samplingfeatures_cv_samplingfeaturegeotype FOREIGN KEY (samplingfeaturegeotypecv) REFERENCES cv_samplingfeaturegeotype(name) ON DELETE CASCADE;


--
-- TOC entry 5363 (class 2606 OID 177446)
-- Name: fk_samplingfeatures_cv_samplingfeaturetype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY samplingfeatures
    ADD CONSTRAINT fk_samplingfeatures_cv_samplingfeaturetype FOREIGN KEY (samplingfeaturetypecv) REFERENCES cv_samplingfeaturetype(name) ON DELETE CASCADE;


--
-- TOC entry 5372 (class 2606 OID 177451)
-- Name: fk_sectionresults_cv_aggregationstatistic; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresults
    ADD CONSTRAINT fk_sectionresults_cv_aggregationstatistic FOREIGN KEY (aggregationstatisticcv) REFERENCES cv_aggregationstatistic(name) ON DELETE CASCADE;


--
-- TOC entry 5371 (class 2606 OID 177456)
-- Name: fk_sectionresults_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresults
    ADD CONSTRAINT fk_sectionresults_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5370 (class 2606 OID 177461)
-- Name: fk_sectionresults_spatialreferences; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresults
    ADD CONSTRAINT fk_sectionresults_spatialreferences FOREIGN KEY (spatialreferenceid) REFERENCES spatialreferences(spatialreferenceid) ON DELETE CASCADE;


--
-- TOC entry 5369 (class 2606 OID 177466)
-- Name: fk_sectionresults_tmunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresults
    ADD CONSTRAINT fk_sectionresults_tmunits FOREIGN KEY (intendedtimespacingunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5368 (class 2606 OID 177471)
-- Name: fk_sectionresults_units; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresults
    ADD CONSTRAINT fk_sectionresults_units FOREIGN KEY (ylocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5367 (class 2606 OID 177476)
-- Name: fk_sectionresults_xunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresults
    ADD CONSTRAINT fk_sectionresults_xunits FOREIGN KEY (intendedxspacingunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5366 (class 2606 OID 177481)
-- Name: fk_sectionresults_zunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresults
    ADD CONSTRAINT fk_sectionresults_zunits FOREIGN KEY (intendedzspacingunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5374 (class 2606 OID 177486)
-- Name: fk_sectionresultvalueannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresultvalueannotations
    ADD CONSTRAINT fk_sectionresultvalueannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5373 (class 2606 OID 177491)
-- Name: fk_sectionresultvalueannotations_sectionresultvalues; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresultvalueannotations
    ADD CONSTRAINT fk_sectionresultvalueannotations_sectionresultvalues FOREIGN KEY (valueid) REFERENCES sectionresultvalues(valueid) ON DELETE CASCADE;


--
-- TOC entry 5381 (class 2606 OID 177496)
-- Name: fk_sectionresultvalues_aiunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresultvalues
    ADD CONSTRAINT fk_sectionresultvalues_aiunits FOREIGN KEY (timeaggregationintervalunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5380 (class 2606 OID 177501)
-- Name: fk_sectionresultvalues_cv_aggregationstatistic; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresultvalues
    ADD CONSTRAINT fk_sectionresultvalues_cv_aggregationstatistic FOREIGN KEY (aggregationstatisticcv) REFERENCES cv_aggregationstatistic(name) ON DELETE CASCADE;


--
-- TOC entry 5379 (class 2606 OID 177506)
-- Name: fk_sectionresultvalues_cv_censorcode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresultvalues
    ADD CONSTRAINT fk_sectionresultvalues_cv_censorcode FOREIGN KEY (censorcodecv) REFERENCES cv_censorcode(name) ON DELETE CASCADE;


--
-- TOC entry 5378 (class 2606 OID 177511)
-- Name: fk_sectionresultvalues_cv_qualitycode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresultvalues
    ADD CONSTRAINT fk_sectionresultvalues_cv_qualitycode FOREIGN KEY (qualitycodecv) REFERENCES cv_qualitycode(name) ON DELETE CASCADE;


--
-- TOC entry 5377 (class 2606 OID 177516)
-- Name: fk_sectionresultvalues_sectionresults; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresultvalues
    ADD CONSTRAINT fk_sectionresultvalues_sectionresults FOREIGN KEY (resultid) REFERENCES sectionresults(resultid) ON DELETE CASCADE;


--
-- TOC entry 5376 (class 2606 OID 177521)
-- Name: fk_sectionresultvalues_xunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresultvalues
    ADD CONSTRAINT fk_sectionresultvalues_xunits FOREIGN KEY (xlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5375 (class 2606 OID 177526)
-- Name: fk_sectionresultvalues_zunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sectionresultvalues
    ADD CONSTRAINT fk_sectionresultvalues_zunits FOREIGN KEY (zlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5383 (class 2606 OID 177531)
-- Name: fk_simulations_actions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY simulations
    ADD CONSTRAINT fk_simulations_actions FOREIGN KEY (actionid) REFERENCES actions(actionid) ON DELETE CASCADE;


--
-- TOC entry 5382 (class 2606 OID 177536)
-- Name: fk_simulations_models; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY simulations
    ADD CONSTRAINT fk_simulations_models FOREIGN KEY (modelid) REFERENCES models(modelid) ON DELETE CASCADE;


--
-- TOC entry 5386 (class 2606 OID 177541)
-- Name: fk_sites_cv_sitetype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sites
    ADD CONSTRAINT fk_sites_cv_sitetype FOREIGN KEY (sitetypecv) REFERENCES cv_sitetype(name) ON DELETE CASCADE;


--
-- TOC entry 5385 (class 2606 OID 177546)
-- Name: fk_sites_samplingfeatures; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sites
    ADD CONSTRAINT fk_sites_samplingfeatures FOREIGN KEY (samplingfeatureid) REFERENCES samplingfeatures(samplingfeatureid) ON DELETE CASCADE;


--
-- TOC entry 5384 (class 2606 OID 177551)
-- Name: fk_sites_spatialreferences; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY sites
    ADD CONSTRAINT fk_sites_spatialreferences FOREIGN KEY (spatialreferenceid) REFERENCES spatialreferences(spatialreferenceid) ON DELETE CASCADE;


--
-- TOC entry 5390 (class 2606 OID 177556)
-- Name: fk_spatialoffsets_cv_spatialoffsettype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spatialoffsets
    ADD CONSTRAINT fk_spatialoffsets_cv_spatialoffsettype FOREIGN KEY (spatialoffsettypecv) REFERENCES cv_spatialoffsettype(name) ON DELETE CASCADE;


--
-- TOC entry 5389 (class 2606 OID 177561)
-- Name: fk_spatialoffsets_offset1units; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spatialoffsets
    ADD CONSTRAINT fk_spatialoffsets_offset1units FOREIGN KEY (offset1unitid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5388 (class 2606 OID 177566)
-- Name: fk_spatialoffsets_offset2units; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spatialoffsets
    ADD CONSTRAINT fk_spatialoffsets_offset2units FOREIGN KEY (offset2unitid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5387 (class 2606 OID 177571)
-- Name: fk_spatialoffsets_offset3units; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spatialoffsets
    ADD CONSTRAINT fk_spatialoffsets_offset3units FOREIGN KEY (offset3unitid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5392 (class 2606 OID 177576)
-- Name: fk_spatialreferenceexternalidentifiers_externalidentifiersystem; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spatialreferenceexternalidentifiers
    ADD CONSTRAINT fk_spatialreferenceexternalidentifiers_externalidentifiersystem FOREIGN KEY (externalidentifiersystemid) REFERENCES externalidentifiersystems(externalidentifiersystemid) ON DELETE CASCADE;


--
-- TOC entry 5391 (class 2606 OID 177581)
-- Name: fk_spatialreferenceexternalidentifiers_spatialreferences; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spatialreferenceexternalidentifiers
    ADD CONSTRAINT fk_spatialreferenceexternalidentifiers_spatialreferences FOREIGN KEY (spatialreferenceid) REFERENCES spatialreferences(spatialreferenceid) ON DELETE CASCADE;


--
-- TOC entry 5393 (class 2606 OID 177586)
-- Name: fk_specimenbatchpostions_featureactions; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY specimenbatchpostions
    ADD CONSTRAINT fk_specimenbatchpostions_featureactions FOREIGN KEY (featureactionid) REFERENCES featureactions(featureactionid) ON DELETE CASCADE;


--
-- TOC entry 5396 (class 2606 OID 177591)
-- Name: fk_specimens_cv_specimenmedium; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY specimens
    ADD CONSTRAINT fk_specimens_cv_specimenmedium FOREIGN KEY (specimenmediumcv) REFERENCES cv_specimenmedium(name) ON DELETE CASCADE;


--
-- TOC entry 5395 (class 2606 OID 177596)
-- Name: fk_specimens_cv_specimentype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY specimens
    ADD CONSTRAINT fk_specimens_cv_specimentype FOREIGN KEY (specimentypecv) REFERENCES cv_specimentype(name) ON DELETE CASCADE;


--
-- TOC entry 5394 (class 2606 OID 177601)
-- Name: fk_specimens_samplingfeatures; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY specimens
    ADD CONSTRAINT fk_specimens_samplingfeatures FOREIGN KEY (samplingfeatureid) REFERENCES samplingfeatures(samplingfeatureid) ON DELETE CASCADE;


--
-- TOC entry 5399 (class 2606 OID 177606)
-- Name: fk_specimentaxonomicclassifiers_citations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY specimentaxonomicclassifiers
    ADD CONSTRAINT fk_specimentaxonomicclassifiers_citations FOREIGN KEY (citationid) REFERENCES citations(citationid) ON DELETE CASCADE;


--
-- TOC entry 5398 (class 2606 OID 177611)
-- Name: fk_specimentaxonomicclassifiers_specimens; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY specimentaxonomicclassifiers
    ADD CONSTRAINT fk_specimentaxonomicclassifiers_specimens FOREIGN KEY (samplingfeatureid) REFERENCES specimens(samplingfeatureid) ON DELETE CASCADE;


--
-- TOC entry 5397 (class 2606 OID 177616)
-- Name: fk_specimentaxonomicclassifiers_taxonomicclassifiers; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY specimentaxonomicclassifiers
    ADD CONSTRAINT fk_specimentaxonomicclassifiers_taxonomicclassifiers FOREIGN KEY (taxonomicclassifierid) REFERENCES taxonomicclassifiers(taxonomicclassifierid) ON DELETE CASCADE;


--
-- TOC entry 5406 (class 2606 OID 177621)
-- Name: fk_spectraresults_cv_aggregationstatistic; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresults
    ADD CONSTRAINT fk_spectraresults_cv_aggregationstatistic FOREIGN KEY (aggregationstatisticcv) REFERENCES cv_aggregationstatistic(name) ON DELETE CASCADE;


--
-- TOC entry 5405 (class 2606 OID 177626)
-- Name: fk_spectraresults_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresults
    ADD CONSTRAINT fk_spectraresults_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5404 (class 2606 OID 177631)
-- Name: fk_spectraresults_spatialreferences; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresults
    ADD CONSTRAINT fk_spectraresults_spatialreferences FOREIGN KEY (spatialreferenceid) REFERENCES spatialreferences(spatialreferenceid) ON DELETE CASCADE;


--
-- TOC entry 5403 (class 2606 OID 177636)
-- Name: fk_spectraresults_units; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresults
    ADD CONSTRAINT fk_spectraresults_units FOREIGN KEY (intendedwavelengthspacingunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5402 (class 2606 OID 177641)
-- Name: fk_spectraresults_xunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresults
    ADD CONSTRAINT fk_spectraresults_xunits FOREIGN KEY (xlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5401 (class 2606 OID 177646)
-- Name: fk_spectraresults_yunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresults
    ADD CONSTRAINT fk_spectraresults_yunits FOREIGN KEY (ylocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5400 (class 2606 OID 177651)
-- Name: fk_spectraresults_zunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresults
    ADD CONSTRAINT fk_spectraresults_zunits FOREIGN KEY (zlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5408 (class 2606 OID 177656)
-- Name: fk_spectraresultvalueannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresultvalueannotations
    ADD CONSTRAINT fk_spectraresultvalueannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5407 (class 2606 OID 177661)
-- Name: fk_spectraresultvalueannotations_spectraresultvalues; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresultvalueannotations
    ADD CONSTRAINT fk_spectraresultvalueannotations_spectraresultvalues FOREIGN KEY (valueid) REFERENCES spectraresultvalues(valueid) ON DELETE CASCADE;


--
-- TOC entry 5413 (class 2606 OID 177666)
-- Name: fk_spectraresultvalues_aiunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresultvalues
    ADD CONSTRAINT fk_spectraresultvalues_aiunits FOREIGN KEY (timeaggregationintervalunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5412 (class 2606 OID 177671)
-- Name: fk_spectraresultvalues_cv_censorcode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresultvalues
    ADD CONSTRAINT fk_spectraresultvalues_cv_censorcode FOREIGN KEY (censorcodecv) REFERENCES cv_censorcode(name) ON DELETE CASCADE;


--
-- TOC entry 5411 (class 2606 OID 177676)
-- Name: fk_spectraresultvalues_cv_qualitycode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresultvalues
    ADD CONSTRAINT fk_spectraresultvalues_cv_qualitycode FOREIGN KEY (qualitycodecv) REFERENCES cv_qualitycode(name) ON DELETE CASCADE;


--
-- TOC entry 5410 (class 2606 OID 177681)
-- Name: fk_spectraresultvalues_spectraresults; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresultvalues
    ADD CONSTRAINT fk_spectraresultvalues_spectraresults FOREIGN KEY (resultid) REFERENCES spectraresults(resultid) ON DELETE CASCADE;


--
-- TOC entry 5409 (class 2606 OID 177686)
-- Name: fk_spectraresultvalues_wunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY spectraresultvalues
    ADD CONSTRAINT fk_spectraresultvalues_wunits FOREIGN KEY (wavelengthunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5415 (class 2606 OID 177691)
-- Name: fk_taxonomicclassifierextids_extidsystems; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY taxonomicclassifierexternalidentifiers
    ADD CONSTRAINT fk_taxonomicclassifierextids_extidsystems FOREIGN KEY (externalidentifiersystemid) REFERENCES externalidentifiersystems(externalidentifiersystemid) ON DELETE CASCADE;


--
-- TOC entry 5414 (class 2606 OID 177696)
-- Name: fk_taxonomicclassifierextids_taxonomicclassifiers; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY taxonomicclassifierexternalidentifiers
    ADD CONSTRAINT fk_taxonomicclassifierextids_taxonomicclassifiers FOREIGN KEY (taxonomicclassifierid) REFERENCES taxonomicclassifiers(taxonomicclassifierid) ON DELETE CASCADE;


--
-- TOC entry 5416 (class 2606 OID 177701)
-- Name: fk_taxonomicclassifiers_cv_taxonomicclassifiertype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY taxonomicclassifiers
    ADD CONSTRAINT fk_taxonomicclassifiers_cv_taxonomicclassifiertype FOREIGN KEY (taxonomicclassifiertypecv) REFERENCES cv_taxonomicclassifiertype(name) ON DELETE CASCADE;


--
-- TOC entry 5424 (class 2606 OID 177706)
-- Name: fk_timeseriesresults_cv_aggregationstatistic; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresults
    ADD CONSTRAINT fk_timeseriesresults_cv_aggregationstatistic FOREIGN KEY (aggregationstatisticcv) REFERENCES cv_aggregationstatistic(name) ON DELETE CASCADE;


--
-- TOC entry 5423 (class 2606 OID 177711)
-- Name: fk_timeseriesresults_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresults
    ADD CONSTRAINT fk_timeseriesresults_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5422 (class 2606 OID 177716)
-- Name: fk_timeseriesresults_spatialreferences; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresults
    ADD CONSTRAINT fk_timeseriesresults_spatialreferences FOREIGN KEY (spatialreferenceid) REFERENCES spatialreferences(spatialreferenceid) ON DELETE CASCADE;


--
-- TOC entry 5421 (class 2606 OID 177721)
-- Name: fk_timeseriesresults_tunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresults
    ADD CONSTRAINT fk_timeseriesresults_tunits FOREIGN KEY (intendedtimespacingunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5420 (class 2606 OID 177726)
-- Name: fk_timeseriesresults_xunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresults
    ADD CONSTRAINT fk_timeseriesresults_xunits FOREIGN KEY (xlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5419 (class 2606 OID 177731)
-- Name: fk_timeseriesresults_yunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresults
    ADD CONSTRAINT fk_timeseriesresults_yunits FOREIGN KEY (ylocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5418 (class 2606 OID 177736)
-- Name: fk_timeseriesresults_zunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresults
    ADD CONSTRAINT fk_timeseriesresults_zunits FOREIGN KEY (zlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5426 (class 2606 OID 177741)
-- Name: fk_timeseriesresultvalueannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresultvalueannotations
    ADD CONSTRAINT fk_timeseriesresultvalueannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5425 (class 2606 OID 177746)
-- Name: fk_timeseriesresultvalueannotations_timeseriesresultvalues; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresultvalueannotations
    ADD CONSTRAINT fk_timeseriesresultvalueannotations_timeseriesresultvalues FOREIGN KEY (valueid) REFERENCES timeseriesresultvalues(valueid) ON DELETE CASCADE;


--
-- TOC entry 5430 (class 2606 OID 177751)
-- Name: fk_timeseriesresultvalues_aiunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresultvalues
    ADD CONSTRAINT fk_timeseriesresultvalues_aiunits FOREIGN KEY (timeaggregationintervalunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5429 (class 2606 OID 177757)
-- Name: fk_timeseriesresultvalues_cv_censorcode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresultvalues
    ADD CONSTRAINT fk_timeseriesresultvalues_cv_censorcode FOREIGN KEY (censorcodecv) REFERENCES cv_censorcode(name) ON DELETE CASCADE;


--
-- TOC entry 5428 (class 2606 OID 177762)
-- Name: fk_timeseriesresultvalues_cv_qualitycode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresultvalues
    ADD CONSTRAINT fk_timeseriesresultvalues_cv_qualitycode FOREIGN KEY (qualitycodecv) REFERENCES cv_qualitycode(name) ON DELETE CASCADE;


--
-- TOC entry 5427 (class 2606 OID 177767)
-- Name: fk_timeseriesresultvalues_timeseriesresults; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY timeseriesresultvalues
    ADD CONSTRAINT fk_timeseriesresultvalues_timeseriesresults FOREIGN KEY (resultid) REFERENCES timeseriesresults(resultid) ON DELETE CASCADE;


--
-- TOC entry 5435 (class 2606 OID 177772)
-- Name: fk_trajectoryresults_cv_aggregationstatistic; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresults
    ADD CONSTRAINT fk_trajectoryresults_cv_aggregationstatistic FOREIGN KEY (aggregationstatisticcv) REFERENCES cv_aggregationstatistic(name) ON DELETE CASCADE;


--
-- TOC entry 5434 (class 2606 OID 177777)
-- Name: fk_trajectoryresults_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresults
    ADD CONSTRAINT fk_trajectoryresults_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5433 (class 2606 OID 177782)
-- Name: fk_trajectoryresults_spatialreferences; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresults
    ADD CONSTRAINT fk_trajectoryresults_spatialreferences FOREIGN KEY (spatialreferenceid) REFERENCES spatialreferences(spatialreferenceid) ON DELETE CASCADE;


--
-- TOC entry 5432 (class 2606 OID 177787)
-- Name: fk_trajectoryresults_tsunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresults
    ADD CONSTRAINT fk_trajectoryresults_tsunits FOREIGN KEY (intendedtrajectoryspacingunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5431 (class 2606 OID 177792)
-- Name: fk_trajectoryresults_tunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresults
    ADD CONSTRAINT fk_trajectoryresults_tunits FOREIGN KEY (intendedtimespacingunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5437 (class 2606 OID 177797)
-- Name: fk_trajectoryresultvalueannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalueannotations
    ADD CONSTRAINT fk_trajectoryresultvalueannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5436 (class 2606 OID 177802)
-- Name: fk_trajectoryresultvalueannotations_trajectoryresultvalues; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalueannotations
    ADD CONSTRAINT fk_trajectoryresultvalueannotations_trajectoryresultvalues FOREIGN KEY (valueid) REFERENCES trajectoryresultvalues(valueid) ON DELETE CASCADE;


--
-- TOC entry 5445 (class 2606 OID 177807)
-- Name: fk_trajectoryresultvalues_aiunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalues
    ADD CONSTRAINT fk_trajectoryresultvalues_aiunits FOREIGN KEY (timeaggregationintervalunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5444 (class 2606 OID 177812)
-- Name: fk_trajectoryresultvalues_cv_censorcode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalues
    ADD CONSTRAINT fk_trajectoryresultvalues_cv_censorcode FOREIGN KEY (censorcodecv) REFERENCES cv_censorcode(name) ON DELETE CASCADE;


--
-- TOC entry 5443 (class 2606 OID 177817)
-- Name: fk_trajectoryresultvalues_cv_qualitycode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalues
    ADD CONSTRAINT fk_trajectoryresultvalues_cv_qualitycode FOREIGN KEY (qualitycodecv) REFERENCES cv_qualitycode(name) ON DELETE CASCADE;


--
-- TOC entry 5442 (class 2606 OID 177822)
-- Name: fk_trajectoryresultvalues_distanceunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalues
    ADD CONSTRAINT fk_trajectoryresultvalues_distanceunits FOREIGN KEY (trajectorydistanceunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5441 (class 2606 OID 177827)
-- Name: fk_trajectoryresultvalues_trajectoryresults; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalues
    ADD CONSTRAINT fk_trajectoryresultvalues_trajectoryresults FOREIGN KEY (resultid) REFERENCES trajectoryresults(resultid) ON DELETE CASCADE;


--
-- TOC entry 5440 (class 2606 OID 177832)
-- Name: fk_trajectoryresultvalues_xunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalues
    ADD CONSTRAINT fk_trajectoryresultvalues_xunits FOREIGN KEY (xlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5439 (class 2606 OID 177837)
-- Name: fk_trajectoryresultvalues_yunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalues
    ADD CONSTRAINT fk_trajectoryresultvalues_yunits FOREIGN KEY (ylocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5438 (class 2606 OID 177842)
-- Name: fk_trajectoryresultvalues_zunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY trajectoryresultvalues
    ADD CONSTRAINT fk_trajectoryresultvalues_zunits FOREIGN KEY (zlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5451 (class 2606 OID 177847)
-- Name: fk_transectresults_cv_aggregationstatistic; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresults
    ADD CONSTRAINT fk_transectresults_cv_aggregationstatistic FOREIGN KEY (aggregationstatisticcv) REFERENCES cv_aggregationstatistic(name) ON DELETE CASCADE;


--
-- TOC entry 5450 (class 2606 OID 177852)
-- Name: fk_transectresults_results; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresults
    ADD CONSTRAINT fk_transectresults_results FOREIGN KEY (resultid) REFERENCES results(resultid) ON DELETE CASCADE;


--
-- TOC entry 5449 (class 2606 OID 177857)
-- Name: fk_transectresults_spatialreferences; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresults
    ADD CONSTRAINT fk_transectresults_spatialreferences FOREIGN KEY (spatialreferenceid) REFERENCES spatialreferences(spatialreferenceid) ON DELETE CASCADE;


--
-- TOC entry 5448 (class 2606 OID 177862)
-- Name: fk_transectresults_tmunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresults
    ADD CONSTRAINT fk_transectresults_tmunits FOREIGN KEY (intendedtimespacingunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5447 (class 2606 OID 177867)
-- Name: fk_transectresults_tsunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresults
    ADD CONSTRAINT fk_transectresults_tsunits FOREIGN KEY (intendedtransectspacingunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5446 (class 2606 OID 177872)
-- Name: fk_transectresults_units; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresults
    ADD CONSTRAINT fk_transectresults_units FOREIGN KEY (zlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5453 (class 2606 OID 177877)
-- Name: fk_transectresultvalueannotations_annotations; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalueannotations
    ADD CONSTRAINT fk_transectresultvalueannotations_annotations FOREIGN KEY (annotationid) REFERENCES annotations(annotationid) ON DELETE CASCADE;


--
-- TOC entry 5452 (class 2606 OID 177882)
-- Name: fk_transectresultvalueannotations_transectresultvalues; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalueannotations
    ADD CONSTRAINT fk_transectresultvalueannotations_transectresultvalues FOREIGN KEY (valueid) REFERENCES transectresultvalues(valueid) ON DELETE CASCADE;


--
-- TOC entry 5461 (class 2606 OID 177887)
-- Name: fk_transectresultvalues_aiunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalues
    ADD CONSTRAINT fk_transectresultvalues_aiunits FOREIGN KEY (timeaggregationintervalunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5460 (class 2606 OID 177892)
-- Name: fk_transectresultvalues_cv_aggregationstatistic; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalues
    ADD CONSTRAINT fk_transectresultvalues_cv_aggregationstatistic FOREIGN KEY (aggregationstatisticcv) REFERENCES cv_aggregationstatistic(name) ON DELETE CASCADE;


--
-- TOC entry 5459 (class 2606 OID 177897)
-- Name: fk_transectresultvalues_cv_censorcode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalues
    ADD CONSTRAINT fk_transectresultvalues_cv_censorcode FOREIGN KEY (censorcodecv) REFERENCES cv_censorcode(name) ON DELETE CASCADE;


--
-- TOC entry 5458 (class 2606 OID 177902)
-- Name: fk_transectresultvalues_cv_qualitycode; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalues
    ADD CONSTRAINT fk_transectresultvalues_cv_qualitycode FOREIGN KEY (qualitycodecv) REFERENCES cv_qualitycode(name) ON DELETE CASCADE;


--
-- TOC entry 5457 (class 2606 OID 177907)
-- Name: fk_transectresultvalues_distanceunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalues
    ADD CONSTRAINT fk_transectresultvalues_distanceunits FOREIGN KEY (transectdistanceunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5456 (class 2606 OID 177912)
-- Name: fk_transectresultvalues_transectresults; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalues
    ADD CONSTRAINT fk_transectresultvalues_transectresults FOREIGN KEY (resultid) REFERENCES transectresults(resultid) ON DELETE CASCADE;


--
-- TOC entry 5455 (class 2606 OID 177917)
-- Name: fk_transectresultvalues_xunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalues
    ADD CONSTRAINT fk_transectresultvalues_xunits FOREIGN KEY (xlocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5454 (class 2606 OID 177922)
-- Name: fk_transectresultvalues_yunits; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY transectresultvalues
    ADD CONSTRAINT fk_transectresultvalues_yunits FOREIGN KEY (ylocationunitsid) REFERENCES units(unitsid) ON DELETE CASCADE;


--
-- TOC entry 5462 (class 2606 OID 177927)
-- Name: fk_units_cv_unitstype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY units
    ADD CONSTRAINT fk_units_cv_unitstype FOREIGN KEY (unitstypecv) REFERENCES cv_unitstype(name) ON DELETE CASCADE;


--
-- TOC entry 5464 (class 2606 OID 177932)
-- Name: fk_variableextensionpropertyvalues_extensionproperties; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY variableextensionpropertyvalues
    ADD CONSTRAINT fk_variableextensionpropertyvalues_extensionproperties FOREIGN KEY (propertyid) REFERENCES extensionproperties(propertyid) ON DELETE CASCADE;


--
-- TOC entry 5463 (class 2606 OID 177937)
-- Name: fk_variableextensionpropertyvalues_variables; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY variableextensionpropertyvalues
    ADD CONSTRAINT fk_variableextensionpropertyvalues_variables FOREIGN KEY (variableid) REFERENCES variables(variableid) ON DELETE CASCADE;


--
-- TOC entry 5466 (class 2606 OID 177942)
-- Name: fk_variableexternalidentifiers_externalidentifiersystems; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY variableexternalidentifiers
    ADD CONSTRAINT fk_variableexternalidentifiers_externalidentifiersystems FOREIGN KEY (externalidentifiersystemid) REFERENCES externalidentifiersystems(externalidentifiersystemid) ON DELETE CASCADE;


--
-- TOC entry 5465 (class 2606 OID 177947)
-- Name: fk_variableexternalidentifiers_variables; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY variableexternalidentifiers
    ADD CONSTRAINT fk_variableexternalidentifiers_variables FOREIGN KEY (variableid) REFERENCES variables(variableid) ON DELETE CASCADE;


--
-- TOC entry 5469 (class 2606 OID 177952)
-- Name: fk_variables_cv_speciation; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY variables
    ADD CONSTRAINT fk_variables_cv_speciation FOREIGN KEY (speciationcv) REFERENCES cv_speciation(name) ON DELETE CASCADE;


--
-- TOC entry 5468 (class 2606 OID 177957)
-- Name: fk_variables_cv_variablename; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY variables
    ADD CONSTRAINT fk_variables_cv_variablename FOREIGN KEY (variablenamecv) REFERENCES cv_variablename(name) ON DELETE CASCADE;


--
-- TOC entry 5467 (class 2606 OID 177962)
-- Name: fk_variables_cv_variabletype; Type: FK CONSTRAINT; Schema: odm2; Owner: -
--

ALTER TABLE ONLY variables
    ADD CONSTRAINT fk_variables_cv_variabletype FOREIGN KEY (variabletypecv) REFERENCES cv_variabletype(name) ON DELETE CASCADE;


SET search_path = odm2extra, pg_catalog;

--
-- TOC entry 5470 (class 2606 OID 177967)
-- Name: Measurementres_resultid_12190167_fk_measurementresults_resultid; Type: FK CONSTRAINT; Schema: odm2extra; Owner: -
--

ALTER TABLE ONLY "Measurementresultvaluefile"
    ADD CONSTRAINT "Measurementres_resultid_12190167_fk_measurementresults_resultid" FOREIGN KEY (resultid) REFERENCES odm2.measurementresults(resultid) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5471 (class 2606 OID 177972)
-- Name: featureactionid; Type: FK CONSTRAINT; Schema: odm2extra; Owner: -
--

ALTER TABLE ONLY "featureactionsNames"
    ADD CONSTRAINT featureactionid FOREIGN KEY (featureactionid) REFERENCES odm2.featureactions(featureactionid);


--
-- TOC entry 5472 (class 2606 OID 177977)
-- Name: processdataloggerfile_dataloggerfileid_fkey; Type: FK CONSTRAINT; Schema: odm2extra; Owner: -
--

ALTER TABLE ONLY processdataloggerfile
    ADD CONSTRAINT processdataloggerfile_dataloggerfileid_fkey FOREIGN KEY (dataloggerfileid) REFERENCES odm2.dataloggerfiles(dataloggerfileid);


-- Completed on 2017-07-17 16:09:09 PDT

--
-- PostgreSQL database dump complete
--

