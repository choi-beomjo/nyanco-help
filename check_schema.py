import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# characters 테이블의 스키마 확인
cursor.execute("PRAGMA table_info(characters)")
columns = cursor.fetchall()

print("Characters 테이블 구조:")
print("=" * 50)
for col in columns:
    print(f"컬럼명: {col[1]}, 타입: {col[2]}, Nullable: {col[3]}, 기본값: {col[4]}, PK: {col[5]}")

conn.close()
