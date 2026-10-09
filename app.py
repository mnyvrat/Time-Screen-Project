import streamlit as st
import time
from pathlib import Path

from database import (
    get_random_question,
    add_participant,
    get_top_three,
    get_all_participants
)


st.set_page_config(
    page_title="Yazılım Geliştirme Kulübü Ekran Süresi Yarışması",
    page_icon="🎯",
    layout="centered"
)


# -------------------------
# SESSION STATE
# -------------------------

if "page" not in st.session_state:
    st.session_state.page = "login"

if "name" not in st.session_state:
    st.session_state.name = ""

if "phone" not in st.session_state:
    st.session_state.phone = ""

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "last_answer_correct" not in st.session_state:
    st.session_state.last_answer_correct = False

if "admin_open" not in st.session_state:
    st.session_state.admin_open = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "final_duration" not in st.session_state:
    st.session_state.final_duration = 0


# -------------------------
# GİRİŞ EKRANI
# -------------------------

if st.session_state.page == "login":

    st.title("Yazılım Geliştirme Kulübü Ekran Süresi Yarışması")
    st.write("Yarışmaya başlamak için  lütfen bilgilerinizi giriniz.")

    name = st.text_input("Ad Soyad")
    phone = st.text_input("Telefon Numarası")

    if st.button(
        "Yarışmaya Başla",
        use_container_width=True
    ):

        if name.strip() == "":
            st.warning("Lütfen adınızı girin.")

        elif phone.strip() == "":
            st.warning("Lütfen telefon numaranızı girin.")

        else:

            st.session_state.name = name
            st.session_state.phone = phone

            # Her seviyeden rastgele 1 soru seç
            questions = []

            for level in range(1, 6):

                question = get_random_question(level)

                if question is not None:
                    questions.append(question)

            # Her seviyede soru var mı?
            if len(questions) < 5:

                st.error(
                    "Her seviye için en az bir soru bulunması gerekiyor."
                )

            else:

                st.session_state.questions = questions

                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.answered = False
                st.session_state.last_answer_correct = False

                st.session_state.final_duration = 0

                # Yarışma süresi burada başlıyor
                st.session_state.start_time = time.time()

                st.session_state.page = "quiz"

                st.rerun()


# -------------------------
# QUIZ EKRANI
# -------------------------

elif st.session_state.page == "quiz":

    questions = st.session_state.questions
    index = st.session_state.current_question

    question = questions[index]

    # questions tablosundaki kolon sırası:
    #
    # 0 -> id
    # 1 -> question_text
    # 2 -> image_path
    # 3 -> option_a
    # 4 -> option_b
    # 5 -> option_c
    # 6 -> correct_answer
    # 7 -> level
    # 8 -> score

    question_text = question[1]
    image_path = question[2]

    option_a = question[3]
    option_b = question[4]
    option_c = question[5]

    correct_answer = question[6]
    level = question[7]
    question_score = question[8]

    st.title("Yazılım Geliştirme Kulübü Ekran Süresi Yarışması")

    st.write(
        f"**Soru {index + 1} / 5**"
    )

    st.progress(
        (index + 1) / 5
    )

    st.subheader(
        f"Seviye {level} — {question_score} Puan"
    )


    # -------------------------
    # GÖRSEL
    # -------------------------

    if image_path:
        image_file = Path(image_path)

        if image_file.exists():
            st.image(str(image_file), width=300)
        else:
            st.warning(f"Görsel bulunamadı: {image_path}")


    # -------------------------
    # SORU
    # -------------------------

    st.write(question_text)


    # -------------------------
    # HENÜZ CEVAPLANMADI
    # -------------------------

    if not st.session_state.answered:

        answer = st.radio(
            "Cevabınızı seçin:",
            [
                option_a,
                option_b,
                option_c
            ],
            index=None,
            key=f"question_{index}"
        )

        if st.button(
            "Cevabı Onayla",
            use_container_width=True
        ):

            if answer is None:

                st.warning(
                    "Lütfen bir cevap seçin."
                )

            else:

                st.session_state.answered = True

                if answer == correct_answer:

                    st.session_state.score += question_score
                    st.session_state.last_answer_correct = True

                else:

                    st.session_state.last_answer_correct = False


                # -------------------------
                # 5. SORU CEVAPLANDIYSA
                # SÜREYİ BURADA DURDUR
                # -------------------------

                if index == 4:

                    st.session_state.final_duration = (
                        time.time()
                        - st.session_state.start_time
                    )

                st.rerun()


    # -------------------------
    # CEVAPLANDI
    # -------------------------

    else:

        if st.session_state.last_answer_correct:

            st.success(
                f"✅ Doğru! +{question_score} puan"
            )

        else:

            st.error("❌ Yanlış!")

            st.info(
                f"Doğru cevap: {correct_answer}"
            )


        # Her iki durumda da toplam puanı göster
        st.write(
            f"Toplam puanın: "
            f"**{st.session_state.score}**"
        )


        # -------------------------
        # İLK 4 SORU
        # -------------------------

        if index < 4:

            if st.button(
                "Sonraki Soru ➡️",
                use_container_width=True
            ):

                st.session_state.current_question += 1

                st.session_state.answered = False
                st.session_state.last_answer_correct = False

                st.rerun()


        # -------------------------
        # 5. SORU TAMAMLANDI
        # -------------------------

        else:

            st.write(
                f"⏱️ Tamamlama süresi: "
                f"**{st.session_state.final_duration:.1f} saniye**"
            )

            if st.button(
                "Sonucu Gör 🏆",
                use_container_width=True
            ):

                add_participant(
                    st.session_state.name,
                    st.session_state.phone,
                    st.session_state.score,
                    st.session_state.final_duration
                )

                st.session_state.page = "result"

                st.session_state.answered = False
                st.session_state.last_answer_correct = False

                st.rerun()


# -------------------------
# SONUÇ EKRANI
# -------------------------

elif st.session_state.page == "result":

    st.title("🏆 Yarışma Tamamlandı")

    st.success(
        f"Tebrikler {st.session_state.name}!"
    )


    # -------------------------
    # PUAN
    # -------------------------

    st.metric(
        "Toplam Puan",
        f"{st.session_state.score} / 150"
    )


    # -------------------------
    # SÜRE
    # -------------------------

    st.write(
        f"⏱️ Tamamlama süresi: "
        f"**{st.session_state.final_duration:.1f} saniye**"
    )


    st.divider()


    # -------------------------
    # LEADERBOARD
    # -------------------------

    st.subheader("🏅 İlk 3 Yarışmacı")

    top_three = get_top_three()

    medals = [
        "🥇",
        "🥈",
        "🥉"
    ]

    for index, participant in enumerate(top_three):

        name = participant[0]
        score = participant[2]
        duration = participant[3]

        # Eski yarışmacılarda süre NULL olabilir
        if duration is not None:

            st.write(
                f"{medals[index]} "
                f"**{name}** — "
                f"{score} puan — "
                f"{duration:.1f} sn"
            )

        else:

            st.write(
                f"{medals[index]} "
                f"**{name}** — "
                f"{score} puan"
            )


    st.divider()


    # -------------------------
    # YÖNETİCİ PANELİ
    # -------------------------

    with st.expander("⚙ Yönetici Paneli"):

        admin_pin = st.text_input(
            "Yönetici PIN'i",
            type="password"
        )

        if st.button("Yönetici Girişi"):

            if admin_pin == "1234":

                st.session_state.admin_open = True

            else:

                st.error("PIN yanlış.")


    # -------------------------
    # YÖNETİCİ SONUÇLARI
    # -------------------------

    if st.session_state.admin_open:

        st.subheader("Yarışmacılar")

        participants = get_all_participants()

        for participant in participants:

            name = participant[0]
            phone = participant[1]
            score = participant[2]

            # get_all_participants fonksiyonunun
            # mevcut yapısına göre completed_at
            completed_at = participant[3]

            st.write(
                f"**{name}** — {score} puan"
            )

            st.caption(
                f"📞 {phone} | "
                f"🕒 {completed_at}"
            )

            st.divider()


    # -------------------------
    # YENİ YARIŞMACI
    # -------------------------

    if st.button(
        " Yeni Yarışmacı",
        use_container_width=True
    ):

        st.session_state.name = ""
        st.session_state.phone = ""

        st.session_state.questions = []

        st.session_state.current_question = 0

        st.session_state.score = 0

        st.session_state.answered = False
        st.session_state.last_answer_correct = False

        st.session_state.start_time = None
        st.session_state.final_duration = 0

        st.session_state.admin_open = False

        st.session_state.page = "login"

        st.rerun()