-- =====================================================================
-- 1. SNOWPARK PYTHON STORED PROCEDURE FOR UNZIPPING & LOADING CSV
-- =====================================================================

CREATE OR REPLACE PROCEDURE AIRLINE_DB.RAW.LOAD_ZIP_DATA(FILE_RELATIVE_PATH VARCHAR, TARGET_TABLE VARCHAR)
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('snowflake-snowpark-python','pandas')
HANDLER = 'load_zipped_csv'
EXECUTE AS OWNER
AS $$
import io
import zipfile
import pandas as pd
from snowflake.snowpark.files import SnowflakeFile

def load_zipped_csv(session, file_relative_path, target_table):
    # فتح الملف المضغوط بأمان من الـ Internal Stage
    with SnowflakeFile.open(file_relative_path, 'rb') as f:
        zip_data = f.read()
        
        with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
            csv_files = [name for name in z.namelist() if name.endswith('.csv')]
            
            if not csv_files:
                return "Error: لم يتم العثور على ملف CSV داخل هذا الملف المضغوط."
            
            with z.open(csv_files[0]) as csv_f:
                # قراءة كل الأعمدة كنصوص لمنع أخطاء الـ Casting والتخمين الخاطئ من Pandas
                df = pd.read_csv(csv_f, dtype=str, low_memory=False)
                
                # استبدال قيم الـ NaN بنصوص فارغة لضمان إنشاء الأعمدة كـ VARCHAR مرن في سنوفليك
                df = df.fillna('')
            
            # صب البيانات في الجدول (يتم إنشاء الجدول تلقائياً إن لم يكن موجوداً)
            session.write_pandas(df, target_table.upper(), auto_create_table=True, overwrite=False)
            
    return f"Success: تم بنجاح تحميل ملف {csv_files[0]} داخل الجدول {target_table}"
$$;
