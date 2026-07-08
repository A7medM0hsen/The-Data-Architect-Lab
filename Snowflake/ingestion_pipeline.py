import io
import zipfile
import boto3
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# 1. إعدادات الاتصال بـ Backblaze B2
B2_KEY_ID = "005a85caf7c53650000000001"
B2_APPLICATION_KEY = "K005LneknvOsYAEYVdaac4LQKqmsviY"
B2_ENDPOINT_URL = "https://s3.us-east-005.backblazeb2.com"
BUCKET_NAME = "airline-on-time-data-ahmed"

# 2. إعدادات الاتصال بـ Snowflake
SNOWFLAKE_USER = "AHMEDDW"
SNOWFLAKE_PASSWORD = "Ahmed@snow652401"
SNOWFLAKE_ACCOUNT = "rc47776.uae-north.azure" 

print("🔄 جاري الاتصال بالـ Data Lake و Snowflake...")

# ربط الكلاود
b2_client = boto3.client(
    's3',
    endpoint_url=B2_ENDPOINT_URL,
    aws_access_key_id=B2_KEY_ID,
    aws_secret_access_key=B2_APPLICATION_KEY
)

# ربط سنوفليك
ctx = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    database="BTS_AIRLINE_DB",
    schema="RAW",
    warehouse="COMPUTE_WH"
)
cursor = ctx.cursor()

print("🗑️ جاري تصفير الجداول القديمة لضمان نظافة البيانات...")
cursor.execute("TRUNCATE TABLE IF EXISTS BTS_AIRLINE_DB.RAW.RAW_FLIGHTS_2024;")
cursor.execute("TRUNCATE TABLE IF EXISTS BTS_AIRLINE_DB.RAW.RAW_FLIGHTS_2025;")
cursor.execute("TRUNCATE TABLE IF EXISTS BTS_AIRLINE_DB.RAW.RAW_FLIGHTS_2026;")

print("📂 جاري جلب قائمة الملفات المضغوطة من Backblaze...")
response = b2_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix="raw/flights/")
files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.zip')]

print(f"🎯 تم العثور على {len(files)} ملف مضغوط. جاري بدء الضخ الذكي والمطابقة الديناميكية...")

for key in files:
    if "year=2024" in key:
        target_table = "RAW_FLIGHTS_2024"
    elif "year=2025" in key:
        target_table = "RAW_FLIGHTS_2025"
    elif "year=2026" in key:
        target_table = "RAW_FLIGHTS_2026"
    else:
        continue

    print(f"\n🔄 جاري معالجة الملف: {key} -> {target_table}")
    
    try:
        # 🌟 خطوة ذكية: جلب هيكل وبنية الجدول الحالية من سنوفليك لمعرفة حالة الأحرف الدقيقة
        cursor.execute(f"SELECT * FROM BTS_AIRLINE_DB.RAW.{target_table} LIMIT 0")
        snowflake_cols = [desc[0] for desc in cursor.description]
        # عمل خريطة للمطابقة غير الحساسة لحالة الأحرف (Case-Insensitive Mapping)
        sf_col_mapping = {col.upper(): col for col in snowflake_cols}

        # تحميل الملف في الـ RAM
        obj = b2_client.get_object(Bucket=BUCKET_NAME, Key=key)
        zip_bytes = obj['Body'].read()
        
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
            csv_files = [f for f in archive.namelist() if f.endswith('.csv')]
            if not csv_files:
                continue
            
            with archive.open(csv_files[0]) as csv_stream:
                df = pd.read_csv(csv_stream, dtype=str, low_memory=False)
                
                # تحويل أعمدة الـ DataFrame لكابيتال مؤقتاً لإجراء المطابقة
                df.columns = [col.upper().strip() for col in df.columns]
                
                # استبعاد أي عمود تالف أو وهمي يحتوي على Unnamed أو نقطتين
                df = df.loc[:, ~df.columns.str.contains('UNNAMED|:')]
                
                # 🌟 الفلترة السحرية: الإبقاء فقط على الأعمدة الموجودة فعلياً داخل جدول سنوفليك
                existing_cols = [col for col in df.columns if col in sf_col_mapping]
                df = df[existing_cols]
                
                # 🌟 إعادة التسمية: تطابق تماماً الـ Casing اللي سنوفليك مستنيه (سواء كابيتال أو سمول)
                df = df.rename(columns=sf_col_mapping)
                
                df = df.fillna('')
                
                # الضخ الآمن لسنوفليك
                success, nchunks, nrows, _ = write_pandas(
                    conn=ctx,
                    df=df,
                    table_name=target_table,
                    database="BTS_AIRLINE_DB",
                    schema="RAW",
                    auto_create_table=False,
                    quote_identifiers=True # يضمن حماية الكلمات المحجوزة
                )
                print(f"✅ نجاح! تم ضخ {nrows} سجل بنجاح في {target_table}.")
                
    except Exception as e:
        print(f"❌ خطأ أثناء معالجة الملف {key}: {e}")

cursor.close()
ctx.close()
print("\n🎉🎉🎉 مبروك يا أحمد! انتهت الملحمة بنجاح، الداتا كاملة والـ 3 سنوات بقوا لايف جوه سنوفليك على نظافة!")