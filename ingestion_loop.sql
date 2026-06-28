-- =====================================================================
-- 2. AUTOMATION LOOP FOR BULK INGESTION (24 ZIP FILES)
-- =====================================================================

-- رصد وتحديث قائمة الملفات المرفوعة في المخزن
LIST @AIRLINE_DB.RAW.SNOWFLAKE_INTERNAL_STAGE;

-- تشغيل الأتمتة الذكية للمرور على كافة ملفات السنتين وضخها
EXECUTE IMMEDIATE $$
DECLARE
  file_cursor CURSOR FOR SELECT "name" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
  full_path STRING;
  file_name STRING;
  target_table STRING;
  call_stmt STRING;
BEGIN
  FOR row_val IN file_cursor DO
    full_path := row_val."name";
    file_name := REGEXP_SUBSTR(full_path, '[^/]+$');
    
    -- تخطي أي ملفات ليست مضغوطة
    IF (file_name NOT LIKE '%.zip') THEN
      CONTINUE;
    END IF;
    
    -- توجيه البيانات للجدول الصحيح بناءً على سنة الملف المستخرجة من اسمه
    IF (file_name LIKE '%2024%') THEN
      target_table := 'RAW_FLIGHTS_2024';
    ELSEIF (file_name LIKE '%2025%') THEN
      target_table := 'RAW_FLIGHTS_2025';
    ELSE
      target_table := 'RAW_FLIGHTS_OTHERS';
    END IF;
    
    -- بناء الاستدعاء الديناميكي وتغليف الملف برابط مؤقت ومُشفر Scoped URL
    call_stmt := 'CALL AIRLINE_DB.RAW.LOAD_ZIP_DATA(BUILD_SCOPED_FILE_URL(''@AIRLINE_DB.RAW.SNOWFLAKE_INTERNAL_STAGE'', ''' || file_name || '''), ''' || target_table || ''')';
    
    -- تنفيذ الاستدعاء فوراً
    EXECUTE IMMEDIATE :call_stmt;
  END FOR;
  
  RETURN 'Success: تم فك وضخ السنتين بنجاح وعمل الـ Schema بشكل مرن ومقاوم للأخطاء!';
END;
$$;
