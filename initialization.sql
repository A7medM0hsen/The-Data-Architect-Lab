-- الخطوة 1: تهيئة البيئة وإنشاء قاعدة البيانات والـ Schema
-- ---------------------------------------------------------------------
USE ROLE ACCOUNTADMIN;

-- إنشاء قاعدة البيانات
CREATE DATABASE IF NOT EXISTS AIRLINE_DB;

-- إنشاء الـ Schema الخاصة بالبيانات الخام
CREATE SCHEMA IF NOT EXISTS AIRLINE_DB.RAW;

-- تحديد البيئة الافتراضية للعمل
USE DATABASE AIRLINE_DB;
USE SCHEMA RAW;
USE WAREHOUSE COMPUTE_WH;


-- ---------------------------------------------------------------------
-- الخطوة 2: إنشاء المخزن الداخلي (Internal Stage) لرفع الملفات
-- ---------------------------------------------------------------------
CREATE OR REPLACE STAGE AIRLINE_DB.RAW.SNOWFLAKE_INTERNAL_STAGE
  DIRECTORY = (ENABLE = TRUE);
