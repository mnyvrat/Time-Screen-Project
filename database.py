import sqlite3
import pandas as pd


# -------------------------
# DATABASE OLUŞTURMA
# -------------------------

def create_database():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            image_path TEXT,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            level INTEGER NOT NULL,
            score INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            score INTEGER NOT NULL,
            duration_seconds REAL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Eski veritabanında duration_seconds yoksa ekle
    try:
        cursor.execute("""
            ALTER TABLE participants
            ADD COLUMN duration_seconds REAL
        """)
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


# -------------------------
# EXCEL'DEN SORU AKTARMA
# -------------------------

def import_questions_from_excel():
    df = pd.read_csv("questions.csv")

    # Tamamen boş satırları kaldır
    df = df.dropna(how="all")

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    # Eski soruları temizle
    cursor.execute("DELETE FROM questions")

    for _, row in df.iterrows():

        # Zorunlu alanlardan biri boşsa satırı atla
        if (
            pd.isna(row["question_text"])
            or pd.isna(row["option_a"])
            or pd.isna(row["option_b"])
            or pd.isna(row["option_c"])
            or pd.isna(row["correct_answer"])
            or pd.isna(row["level"])
            or pd.isna(row["score"])
        ):
            continue

        image_path = row["image_path"]

        if pd.isna(image_path):
            image_path = None

        cursor.execute("""
            INSERT INTO questions (
                question_text,
                image_path,
                option_a,
                option_b,
                option_c,
                correct_answer,
                level,
                score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(row["question_text"]),
            image_path,
            str(row["option_a"]),
            str(row["option_b"]),
            str(row["option_c"]),
            str(row["correct_answer"]),
            int(row["level"]),
            int(row["score"])
        ))

    conn.commit()
    conn.close()

    print("Sorular Excel dosyasından başarıyla aktarıldı.")


# -------------------------
# YARIŞMACI EKLEME
# -------------------------

def add_participant(name, phone, score, duration_seconds):

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO participants (
            name,
            phone,
            score,
            duration_seconds
        )
        VALUES (?, ?, ?, ?)
    """, (
        name,
        phone,
        score,
        duration_seconds
    ))

    conn.commit()
    conn.close()


# -------------------------
# İLK 3 YARIŞMACI
# -------------------------

def get_top_three():

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            name,
            phone,
            score,
            duration_seconds
        FROM participants
        ORDER BY
            score DESC,
            CASE
                WHEN duration_seconds IS NULL THEN 1
                ELSE 0
            END ASC,
            duration_seconds ASC,
            completed_at ASC
        LIMIT 3
    """)

    top_three = cursor.fetchall()

    conn.close()

    return top_three


# -------------------------
# SORU EKLEME
# -------------------------

def add_question(
        question_text,
        option_a,
        option_b,
        option_c,
        correct_answer,
        level,
        score,
        image_path=None
):

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO questions (
            question_text,
            image_path,
            option_a,
            option_b,
            option_c,
            correct_answer,
            level,
            score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        question_text,
        image_path,
        option_a,
        option_b,
        option_c,
        correct_answer,
        level,
        score
    ))

    conn.commit()
    conn.close()


# -------------------------
# RASTGELE SORU GETİR
# -------------------------

def get_random_question(level):

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM questions
        WHERE level = ?
        ORDER BY RANDOM()
        LIMIT 1
    """, (level,))

    question = cursor.fetchone()

    conn.close()

    return question


# -------------------------
# TÜM YARIŞMACILAR
# -------------------------

def get_all_participants():

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            name,
            phone,
            score,
            duration_seconds,
            completed_at
        FROM participants
        ORDER BY
            score DESC,
            CASE
                WHEN duration_seconds IS NULL THEN 1
                ELSE 0
            END ASC,
            duration_seconds ASC,
            completed_at ASC
    """)

    participants = cursor.fetchall()

    conn.close()

    return participants


# -------------------------
# YARIŞMACILARI TEMİZLE
# SADECE GEREKTİĞİNDE KULLAN
# -------------------------

def clear_participants():

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM participants")

    conn.commit()
    conn.close()


# -------------------------
# DATABASE'I HAZIRLA
# -------------------------

create_database()

# Excel'e yeni soru eklediğindimport_questions_from_excele bunu 1 kez aç:
#import_questions_from_excel()
# Yarışmacıları tamamen silmek istediğinde bunu 1 kez aç:
#clear_participants()