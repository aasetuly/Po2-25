import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

st.set_page_config(page_title="APEC PETROTECHNIC", layout="wide")

# ---------------- USERS ----------------
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "TEST": {
            "password": "TEST",
            "role": "Student",
            "name": "Асетулы Азамат",
            "dob": "19.01.2010",
            "phone": "+77021241250",
            "group": "АИУ-1-25"
        },
        "teacher1": {
            "password": "1234",
            "role": "Teacher",
            "name": "Преподаватель",
            "dob": "01.01.1980",
            "phone": "+77010000000",
            "group": "ALL"
        },
        "admin": {
            "password": "admin",
            "role": "Administrator",
            "name": "Admin System",
            "dob": "01.01.2000",
            "phone": "+77019999999",
            "group": "ALL"
        }
    }

# ---------------- SESSION ----------------
defaults = {
    "auth": False,
    "user": None,
    "page": "schedule",
    "gpa_grades": [],
    "account_requests": [],
    "org_requests": [],
    "modal": None,
    "success_msg": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def set_page(p):
    st.session_state.page = p
    st.rerun()

def logout():
    st.session_state.auth = False
    st.session_state.user = None
    st.session_state.modal = None
    st.session_state.success_msg = None
    st.session_state.page = "schedule"
    st.rerun()

def open_modal(name):
    st.session_state.modal = name
    st.session_state.success_msg = None
    st.rerun()

def close_modal():
    st.session_state.modal = None
    st.session_state.success_msg = None
    st.rerun()

# ---------------- DATA ----------------
SCHEDULE = {
    "АИУ-1-25": [
        ["Понедельник", "09:00", "Программирование"],
        ["Среда", "14:00", "AI"]
    ],
    "АИУ-2-25": [
        ["Вторник", "11:00", "Сети"]
    ]
}

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Manrope:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Manrope', sans-serif; }

@keyframes fadeInUp {
    from { opacity:0; transform:translateY(20px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeIn {
    from { opacity:0; }
    to   { opacity:1; }
}

.big-title {
    text-align:center;
    font-family:'Bebas Neue',sans-serif;
    font-size:36px;
    letter-spacing:6px;
    color:#e8e8e8;
    margin-bottom:6px;
    animation: fadeInUp 0.5s ease both;
}

/* ── CARD BUTTONS ── */
.card-col div[data-testid="stButton"] > button {
    height: 150px !important;
    background: linear-gradient(135deg,#1a1a1a,#252525) !important;
    border: 1px solid #333 !important;
    border-radius: 16px !important;
    color: #e8e8e8 !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    white-space: pre-wrap !important;
    line-height: 1.7 !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease !important;
    animation: fadeInUp 0.5s ease both !important;
}
.card-col div[data-testid="stButton"] > button:hover {
    transform: translateY(-5px) scale(1.03) !important;
    background: linear-gradient(135deg,#222,#2d2d2d) !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.55) !important;
    border-color: #555 !important;
}

/* ── SUPPORT ITEMS ── */
.sup-item {
    background: #181818;
    border-left: 3px solid #3a3a3a;
    border-radius: 10px;
    padding: 13px 16px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
    animation: fadeInUp 0.4s ease both;
}
.sup-item:hover { border-left-color: #777; }
.sup-prob { color: #bbb; font-size: 13px; margin-bottom: 4px; }
.sup-ans  { color: #e8e8e8; font-size: 14px; font-weight: 600; }

/* ── BADGE ── */
.badge {
    display: inline-block; padding: 3px 10px;
    border-radius: 20px; font-size: 12px; font-weight: 700;
}
.badge-pending  { background:#3a3000; color:#f0c000; }
.badge-approved { background:#003a10; color:#00e050; }
.badge-rejected { background:#3a0000; color:#ff5555; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ================================================================
#  MODAL PAGES  — each is a full page render, st.stop() at end
# ================================================================

if st.session_state.modal == "account":
    st.markdown("<div class='big-title'>📩 ЗАПРОС СОЗДАНИЯ АККАУНТА</div>", unsafe_allow_html=True)
    st.markdown("")

    if st.session_state.success_msg:
        st.success(st.session_state.success_msg)
        st.markdown("")
        if st.button("← Назад на главную", use_container_width=True):
            close_modal()
        st.stop()

    iin   = st.text_input("ИИН (12 цифр)", placeholder="123456789012")
    email = st.text_input("Email", placeholder="example@mail.com")
    phone = st.text_input("Номер телефона", placeholder="+7 700 000 00 00")
    name  = st.text_input("Полное имя", placeholder="Иванов Иван Иванович")
    st.markdown("")

    c1, c2 = st.columns(2)
    send   = c1.button("📤 Отправить", use_container_width=True)
    cancel = c2.button("✖ Отмена / Назад", use_container_width=True)

    if send:
        if iin and email and phone and name:
            st.session_state.account_requests.append({
                "id": str(uuid.uuid4())[:8],
                "type": "account",
                "iin": iin, "email": email, "phone": phone, "name": name,
                "status": "pending",
                "created": datetime.now().strftime("%d.%m.%Y %H:%M")
            })
            st.session_state.success_msg = "✅ Заявка отправлена! Администратор рассмотрит её в течение 24 часов."
            st.rerun()
        else:
            st.error("⚠️ Пожалуйста, заполните все поля")

    if cancel:
        close_modal()

    st.stop()


elif st.session_state.modal == "org":
    st.markdown("<div class='big-title'>🏢 ПОДКЛЮЧЕНИЕ К ОРГАНИЗАЦИИ</div>", unsafe_allow_html=True)
    st.markdown("")

    if st.session_state.success_msg:
        st.success(st.session_state.success_msg)
        st.markdown("")
        if st.button("← Назад на главную", use_container_width=True):
            close_modal()
        st.stop()

    org_name = st.text_input("Наименование организации", placeholder="ТОО «Компания»")
    bin_num  = st.text_input("БИН организации", placeholder="123456789012")
    company  = st.text_input("Название компании", placeholder="APEC Petrotechnic")
    role_req = st.selectbox("Запрашиваемые права доступа",
                            ["Сотрудник", "Менеджер", "Директор", "Администратор"])
    st.markdown("")

    c1, c2 = st.columns(2)
    send   = c1.button("📤 Отправить", use_container_width=True)
    cancel = c2.button("✖ Отмена / Назад", use_container_width=True)

    if send:
        if org_name and bin_num and company:
            st.session_state.org_requests.append({
                "id": str(uuid.uuid4())[:8],
                "type": "org",
                "org_name": org_name, "bin": bin_num,
                "company": company, "role": role_req,
                "status": "pending",
                "created": datetime.now().strftime("%d.%m.%Y %H:%M")
            })
            st.session_state.success_msg = "✅ Запрос отправлен администратору!"
            st.rerun()
        else:
            st.error("⚠️ Заполните все поля")

    if cancel:
        close_modal()

    st.stop()


elif st.session_state.modal == "support":
    st.markdown("<div class='big-title'>🛠 ТЕХНИЧЕСКАЯ ПОДДЕРЖКА</div>", unsafe_allow_html=True)
    st.markdown("")

    problems = [
        ("❌ Не запускается система",
         "Попробуйте полностью перезапустить браузер или очистить кэш (Ctrl+Shift+Del). "
         "Если не помогает — перезагрузите устройство."),
        ("❌ Аккаунт не создаётся",
         "Подождите — администрация должна одобрить вашу заявку. "
         "Обычно это занимает до 24 часов в рабочие дни."),
        ("❌ Ошибка входа — неверный логин или пароль",
         "Проверьте правильность данных. Логин и пароль чувствительны к регистру. "
         "Убедитесь, что выбрана правильная роль."),
        ("❌ Расписание не отображается",
         "Убедитесь, что вы привязаны к группе. "
         "Обратитесь к администратору для проверки вашего профиля."),
        ("❌ Заявка зависла в статусе «Ожидание»",
         "Администратор ещё не обработал запрос. "
         "Если прошло более 48 часов — напишите через сайт apec.edu.kz."),
        ("❌ Белый экран / приложение не загружается",
         "Откройте страницу в режиме инкогнито или другом браузере. "
         "Проверьте интернет-соединение и попробуйте снова."),
        ("❌ Не отображается группа в профиле",
         "Группа назначается администратором при создании аккаунта. "
         "Свяжитесь с администрацией для уточнения."),
    ]

    for prob, ans in problems:
        st.markdown(f"""
        <div class='sup-item'>
            <div class='sup-prob'>{prob}</div>
            <div class='sup-ans'>→ {ans}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    if st.button("← Назад на главную", use_container_width=True):
        close_modal()
    st.stop()


elif st.session_state.modal == "qa":
    st.markdown("<div class='big-title'>❓ ЧАСТЫЕ ВОПРОСЫ</div>", unsafe_allow_html=True)
    st.markdown("")

    qas = [
        ("Как узнать своё расписание?",
         "Войдите в систему → перейдите во вкладку «Расписание». "
         "Расписание привязано к вашей группе."),
        ("Как рассчитывается GPA?",
         "A = 4, B = 3, C = 2, D = 1, F = 0. "
         "GPA — среднее арифметическое всех ваших оценок."),
        ("Можно ли сменить группу?",
         "Да. Обратитесь к администратору — он внесёт изменения в ваш профиль."),
        ("Сколько ждать одобрения аккаунта?",
         "Обычно до 24 часов в рабочие дни. В праздники — до 48 часов."),
        ("Можно ли войти с другого устройства?",
         "Да, система доступна с любого устройства через браузер."),
        ("Забыл пароль — что делать?",
         "Обратитесь к администратору. "
         "Самостоятельного сброса пока нет — он сбросит вручную."),
    ]

    for q, a in qas:
        st.markdown(f"""
        <div class='sup-item'>
            <div class='sup-prob'>💬 {q}</div>
            <div class='sup-ans'>→ {a}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    if st.button("← Назад на главную", use_container_width=True):
        close_modal()
    st.stop()



if not st.session_state.auth:

    st.markdown("<div class='big-title'>ACS — APEC — CONTROL — SERVICE</div>",
                unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;margin-bottom:14px;animation:fadeIn 0.7s ease both;">
        <a href="https://apec.edu.kz/" target="_blank">
            <img src="https://apec.edu.kz/assets/main_logo.png" width="100">
        </a>
    </div>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown("### 🔐 Авторизация")
        login_in = st.text_input("ЛОГИН")
        pass_in  = st.text_input("ПАРОЛЬ", type="password")
        role_in  = st.radio("Роль", ["Student", "Teacher", "Administrator"])

        if st.button("ВОЙТИ", use_container_width=True):
            db = st.session_state.users_db
            if (login_in in db
                    and db[login_in]["password"] == pass_in
                    and db[login_in]["role"] == role_in):
                st.session_state.auth = True
                st.session_state.user = db[login_in]
                st.rerun()
            else:
                st.error("Ошибка входа: проверьте логин, пароль и роль")

    st.markdown("---")
    st.markdown(
        "<div class='big-title' style='font-size:20px;letter-spacing:4px;margin-top:6px;'>"
        "📌 ACS SERVICES</div>",
        unsafe_allow_html=True)

    st.markdown("<div class='card-col'>", unsafe_allow_html=True)
    r1, r2 = st.columns(2), st.columns(2)

    with r1[0]:
        if st.button("📩\n\nСоздание аккаунта\nИИН · Email · Телефон",
                     use_container_width=True, key="card_acc"):
            open_modal("account")
    with r1[1]:
        if st.button("🏢\n\nПодключение к организации\nБИН · Компания · Права",
                     use_container_width=True, key="card_org"):
            open_modal("org")
    with r2[0]:
        if st.button("🛠\n\nТехподдержка\nОшибки · Вход · Система",
                     use_container_width=True, key="card_sup"):
            open_modal("support")
    with r2[1]:
        if st.button("❓\n\nQ&A\nЧастые вопросы",
                     use_container_width=True, key="card_qa"):
            open_modal("qa")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()



user = st.session_state.user

st.markdown("<div class='big-title'>ACS — APEC — CONTROL — SERVICE</div>",
            unsafe_allow_html=True)

c_logo, c_nav, c_user = st.columns([1, 5, 1])
with c_logo:
    st.image("https://apec.edu.kz/assets/main_logo.png", width=55)
with c_nav:
    n1, n2, n3, n4 = st.columns(4)
    if n1.button("📚 Расписание", use_container_width=True): set_page("schedule")
    if n2.button("👥 Группы",     use_container_width=True): set_page("groups")
    if n3.button("🧮 GPA",        use_container_width=True): set_page("gpa")
    if n4.button("🚪 Выйти",      use_container_width=True): logout()
with c_user:
    st.markdown(
        f"<div style='text-align:right;font-size:13px;color:#aaa;padding-top:6px;'>"
        f"{user['name']}<br><span style='color:#666;font-size:11px;'>{user['role']}</span></div>",
        unsafe_allow_html=True)

st.markdown("---")


if user["role"] == "Student":

    if st.session_state.page == "schedule":
        st.title("📚 Расписание")
        grp = user.get("group", "")
        if grp in SCHEDULE:
            df = pd.DataFrame(SCHEDULE[grp], columns=["День", "Время", "Предмет"])
            st.table(df)
        else:
            st.info("Расписание для вашей группы не найдено.")

    elif st.session_state.page == "gpa":
        st.title("🧮 GPA Калькулятор")
        mapping = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
        grade = st.selectbox("Выберите оценку", list(mapping.keys()))
        c1, c2 = st.columns(2)
        if c1.button("➕ Добавить",  use_container_width=True):
            st.session_state.gpa_grades.append(grade)
        if c2.button("🗑 Очистить", use_container_width=True):
            st.session_state.gpa_grades = []

        if st.session_state.gpa_grades:
            st.write("Оценки:", "  ·  ".join(st.session_state.gpa_grades))
            if st.button("📊 Рассчитать GPA", use_container_width=True):
                gpa = sum(mapping[g] for g in st.session_state.gpa_grades) / \
                      len(st.session_state.gpa_grades)
                color = "#00e050" if gpa >= 3 else "#f0c000" if gpa >= 2 else "#ff5555"
                st.markdown(
                    f"<div style='font-size:52px;font-weight:800;color:{color};"
                    f"text-align:center;margin-top:16px;'>GPA: {gpa:.2f}</div>",
                    unsafe_allow_html=True)

    elif st.session_state.page == "groups":
        st.title("👥 Группы")
        st.info(f"Ваша группа: **{user.get('group', '-')}**")


elif user["role"] == "Teacher":
    st.title("👨‍🏫 Панель преподавателя")
    for grp, sched in SCHEDULE.items():
        st.subheader(f"Группа: {grp}")
        df = pd.DataFrame(sched, columns=["День", "Время", "Предмет"])
        st.table(df)


elif user["role"] == "Administrator":
    st.title("🛠 Панель Администратора")
    tab1, tab2, tab3 = st.tabs(
        ["📩 Заявки — аккаунты", "🏢 Заявки — организации", "👤 Все пользователи"])

    with tab1:
        reqs = st.session_state.account_requests
        pending_n = sum(1 for r in reqs if r["status"] == "pending")
        st.markdown(f"**Всего заявок: {len(reqs)} · Ожидают: {pending_n}**")

        if not reqs:
            st.info("Заявок пока нет.")
        else:
            for i, r in enumerate(reqs):
                b_cls  = {"pending":"badge-pending","approved":"badge-approved",
                          "rejected":"badge-rejected"}[r["status"]]
                b_text = {"pending":"⏳ Ожидание","approved":"✅ Одобрено",
                          "rejected":"❌ Отклонено"}[r["status"]]
                with st.expander(f"#{r['id']} — {r['name']} [{r['created']}]"):
                    st.markdown(f"<span class='badge {b_cls}'>{b_text}</span>",
                                unsafe_allow_html=True)
                    st.write(f"**ИИН:** {r['iin']}")
                    st.write(f"**Email:** {r['email']}")
                    st.write(f"**Телефон:** {r['phone']}")
                    st.write(f"**Имя:** {r['name']}")
                    if r["status"] == "pending":
                        st.markdown("**Создать аккаунт:**")
                        ca, cb, cc = st.columns(3)
                        nl = ca.text_input("Логин",  key=f"lg_{i}")
                        np_ = cb.text_input("Пароль", key=f"pw_{i}")
                        ng = cc.text_input("Группа", key=f"gp_{i}",
                                           placeholder="АИУ-1-25")
                        col_a, col_r = st.columns(2)
                        if col_a.button("✅ Одобрить", key=f"ap_{i}",
                                        use_container_width=True):
                            if nl and np_ and ng:
                                st.session_state.users_db[nl] = {
                                    "password": np_, "role": "Student",
                                    "name": r["name"], "dob": "-",
                                    "phone": r["phone"], "group": ng
                                }
                                st.session_state.account_requests[i]["status"] = "approved"
                                st.success(f"Аккаунт «{nl}» создан!")
                                st.rerun()
                            else:
                                st.error("Введите логин, пароль и группу")
                        if col_r.button("❌ Отклонить", key=f"rj_{i}",
                                        use_container_width=True):
                            st.session_state.account_requests[i]["status"] = "rejected"
                            st.rerun()

    with tab2:
        org_reqs = st.session_state.org_requests
        if not org_reqs:
            st.info("Заявок на организации пока нет.")
        else:
            for i, r in enumerate(org_reqs):
                b_cls  = {"pending":"badge-pending","approved":"badge-approved",
                          "rejected":"badge-rejected"}[r["status"]]
                b_text = {"pending":"⏳ Ожидание","approved":"✅ Одобрено",
                          "rejected":"❌ Отклонено"}[r["status"]]
                with st.expander(f"#{r['id']} — {r['org_name']} [{r['created']}]"):
                    st.markdown(f"<span class='badge {b_cls}'>{b_text}</span>",
                                unsafe_allow_html=True)
                    st.write(f"**Организация:** {r['org_name']}")
                    st.write(f"**БИН:** {r['bin']}")
                    st.write(f"**Компания:** {r['company']}")
                    st.write(f"**Права:** {r['role']}")
                    if r["status"] == "pending":
                        col_a, col_r = st.columns(2)
                        if col_a.button("✅ Одобрить", key=f"oa_{i}",
                                        use_container_width=True):
                            st.session_state.org_requests[i]["status"] = "approved"
                            st.rerun()
                        if col_r.button("❌ Отклонить", key=f"or_{i}",
                                        use_container_width=True):
                            st.session_state.org_requests[i]["status"] = "rejected"
                            st.rerun()

    with tab3:
        rows = []
        for uname, udata in st.session_state.users_db.items():
            rows.append({
                "Логин":   uname,
                "Имя":     udata.get("name", "-"),
                "Роль":    udata.get("role", "-"),
                "Группа":  udata.get("group", "-"),
                "Телефон": udata.get("phone", "-"),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)