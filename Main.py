import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
import re

st.set_page_config(page_title="APEC PETROTECHNIC", layout="wide")

if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "TEST": {
            "password": "TEST",
            "role": "Student",
            "name": "Асетулы Азамат",
            "dob": "19.01.2010",
            "phone": "+77021241250",
            "group": "АИУ-1-25",
            "banned": False
        },
        "student2": {
            "password": "1111",
            "role": "Student",
            "name": "Иванов Иван",
            "dob": "05.03.2009",
            "phone": "+77030000001",
            "group": "АИУ-2-25",
            "banned": False
        },
        "teacher1": {
            "password": "1234",
            "role": "Teacher",
            "name": "Преподаватель Алия",
            "dob": "01.01.1980",
            "phone": "+77010000000",
            "group": "ALL",
            "banned": False
        },
        "admin": {
            "password": "admin",
            "role": "Administrator",
            "name": "Admin System",
            "dob": "01.01.2000",
            "phone": "+77019999999",
            "group": "ALL",
            "banned": False
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
    "homeworks": [],
    "notifications": [],
    "lang": "ru",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- TRANSLATIONS ----------------
T = {
    "ru": {
        "title": "ACS — APEC — CONTROL — SERVICE",
        "login": "ВОЙТИ",
        "login_label": "ЛОГИН",
        "pass_label": "ПАРОЛЬ",
        "role_label": "Роль",
        "auth_title": "🔐 Авторизация",
        "services": "📌 ACS SERVICES",
        "schedule": "📚 Расписание",
        "groups": "👥 Группы",
        "gpa": "🧮 GPA",
        "logout": "🚪 Выйти",
        "profile": "👤 Профиль",
        "student_id": "🪪 Студенческий билет",
        "festivals": "🎉 Фестивали",
        "translate": "🌐 Язык",
        "your_group": "Ваша группа",
        "no_schedule": "Расписание для вашей группы не найдено.",
        "day": "День", "time": "Время", "subject": "Предмет",
        "add_grade": "➕ Добавить",
        "clear": "🗑 Очистить",
        "calc_gpa": "📊 Рассчитать GPA",
        "grades_label": "Оценки:",
        "select_grade": "Выберите оценку",
        "teacher_panel": "👨‍🏫 Панель преподавателя",
        "group_label": "Группа",
        "assign_hw": "📝 Задать домашнее задание",
        "assign_lesson": "📅 Назначить урок",
        "send_notif": "🔔 Отправить уведомление",
        "hw_list": "Список домашних заданий",
        "lesson_list": "Расписание уроков",
        "notif_list": "Отправленные уведомления",
        "admin_panel": "🛠 Панель Администратора",
        "tab_acc": "📩 Заявки — аккаунты",
        "tab_org": "🏢 Заявки — организации",
        "tab_users": "👤 Все пользователи",
        "tab_create": "➕ Создать аккаунт",
        "ban_user": "🚫 Заблокировать",
        "unban_user": "✅ Разблокировать",
        "delete_user": "🗑 Удалить",
        "banned_badge": "🚫 ЗАБЛОКИРОВАН",
        "login_col": "Логин", "name_col": "Имя", "role_col": "Роль",
        "group_col": "Группа", "phone_col": "Телефон", "status_col": "Статус",
        "actions_col": "Действия",
    },
    "en": {
        "title": "ACS — APEC — CONTROL — SERVICE",
        "login": "SIGN IN",
        "login_label": "LOGIN",
        "pass_label": "PASSWORD",
        "role_label": "Role",
        "auth_title": "🔐 Authorization",
        "services": "📌 ACS SERVICES",
        "schedule": "📚 Schedule",
        "groups": "👥 Groups",
        "gpa": "🧮 GPA",
        "logout": "🚪 Logout",
        "profile": "👤 Profile",
        "student_id": "🪪 Student ID",
        "festivals": "🎉 Festivals",
        "translate": "🌐 Language",
        "your_group": "Your group",
        "no_schedule": "No schedule found for your group.",
        "day": "Day", "time": "Time", "subject": "Subject",
        "add_grade": "➕ Add",
        "clear": "🗑 Clear",
        "calc_gpa": "📊 Calculate GPA",
        "grades_label": "Grades:",
        "select_grade": "Select grade",
        "teacher_panel": "👨‍🏫 Teacher Panel",
        "group_label": "Group",
        "assign_hw": "📝 Assign Homework",
        "assign_lesson": "📅 Schedule Lesson",
        "send_notif": "🔔 Send Notification",
        "hw_list": "Homework List",
        "lesson_list": "Lesson Schedule",
        "notif_list": "Sent Notifications",
        "admin_panel": "🛠 Administrator Panel",
        "tab_acc": "📩 Account Requests",
        "tab_org": "🏢 Org Requests",
        "tab_users": "👤 All Users",
        "tab_create": "➕ Create Account",
        "ban_user": "🚫 Ban",
        "unban_user": "✅ Unban",
        "delete_user": "🗑 Delete",
        "banned_badge": "🚫 BANNED",
        "login_col": "Login", "name_col": "Name", "role_col": "Role",
        "group_col": "Group", "phone_col": "Phone", "status_col": "Status",
        "actions_col": "Actions",
    }
}

def t(key):
    return T[st.session_state.lang].get(key, key)

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

# ================================================================
# VALIDATION HELPERS
# ================================================================

def validate_iin(iin: str):
    """ИИН: ровно 12 цифр, только цифры."""
    digits_only = re.sub(r'\D', '', iin)
    if not iin.isdigit():
        return False, "ИИН должен содержать только цифры"
    if len(iin) != 12:
        return False, f"ИИН должен быть ровно 12 цифр (сейчас: {len(iin)})"
    return True, ""

def validate_phone(phone: str):
    """Телефон: допускается «+» в начале, только цифры, не более 12 цифр."""
    stripped = phone.lstrip('+')
    if not stripped.isdigit():
        return False, "Телефон должен содержать только цифры (и «+» в начале)"
    digit_count = len(re.sub(r'\D', '', phone))
    if digit_count > 12:
        return False, f"Номер не должен превышать 12 цифр (сейчас: {digit_count})"
    if digit_count < 10:
        return False, f"Номер слишком короткий (минимум 10 цифр)"
    return True, ""

def field_hint(ok: bool, msg: str):
    """Показывает ошибку под полем."""
    if not ok:
        st.markdown(
            f"<div style='color:#ff5555;font-size:12px;margin-top:-10px;margin-bottom:8px;'>⚠ {msg}</div>",
            unsafe_allow_html=True
        )

# ---------------- DATA ----------------
SCHEDULE = {
    "АИУ-1-25": [
        ["Понедельник", "08:00", "Физкультура"],
        ["Понедельник", "09:00", "Программирование"],
        ["Понедельник", "11:00", "Математика"],
        ["Вторник",     "09:00", "Базы данных"],
        ["Вторник",     "11:00", "Английский язык"],
        ["Среда",       "09:00", "AI / Машинное обучение"],
        ["Среда",       "11:00", "Алгоритмы и структуры данных"],
        ["Среда",       "14:00", "Веб-разработка"],
        ["Четверг",     "09:00", "Операционные системы"],
        ["Четверг",     "11:00", "Физика"],
        ["Пятница",     "09:00", "Проектная деятельность"],
        ["Пятница",     "11:00", "История Казахстана"],
    ],
    "АИУ-2-25": [
        ["Понедельник", "09:00", "Сетевые технологии"],
        ["Понедельник", "11:00", "Математика"],
        ["Вторник",     "09:00", "Кибербезопасность"],
        ["Вторник",     "11:00", "Английский язык"],
        ["Среда",       "09:00", "Облачные технологии"],
        ["Среда",       "11:00", "Linux / DevOps"],
        ["Четверг",     "09:00", "Программирование на Python"],
        ["Четверг",     "11:00", "Физика"],
        ["Пятница",     "09:00", "Базы данных"],
        ["Пятница",     "11:00", "История Казахстана"],
    ],
    "ИС-1-25": [
        ["Понедельник", "09:00", "Информационные системы"],
        ["Вторник",     "09:00", "Проектирование ПО"],
        ["Среда",       "09:00", "UX/UI Дизайн"],
        ["Четверг",     "09:00", "1С: Предприятие"],
        ["Пятница",     "09:00", "Бизнес-аналитика"],
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
@keyframes pulse {
    0%,100% { opacity:1; }
    50%      { opacity:0.6; }
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
.badge-banned   { background:#3a0000; color:#ff5555; animation: pulse 1.5s infinite; }
.badge-active   { background:#003a10; color:#00e050; }

/* ── STAT CARDS ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 1.2rem 0;
    animation: fadeInUp 0.5s ease both;
}
.stat-card {
    background: #181818;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.stat-num  { font-size: 24px; font-weight: 800; color: #e8e8e8; }
.stat-label{ font-size: 11px; color: #666; margin-top: 4px; line-height: 1.4; }

/* ── ABOUT BLOCK ── */
.about-block {
    background: #181818;
    border-left: 3px solid #3a6a4a;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.25rem;
    margin: 1rem 0 1.5rem 0;
    animation: fadeInUp 0.5s ease both;
}
.about-block p { font-size: 13px; color: #999; line-height: 1.7; margin: 0; }
.about-block strong { color: #e8e8e8; }

/* ── STUDENT FEATURE CARDS ── */
.stu-section-title {
    font-size: 11px; color: #555; letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 10px; font-weight: 700;
}
.stu-cards-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 12px; margin-bottom: 1.5rem;
    animation: fadeInUp 0.5s ease both;
}
.stu-card {
    background: #181818; border: 1px solid #2a2a2a;
    border-radius: 14px; padding: 1.25rem;
    transition: border-color 0.2s, transform 0.2s;
}
.stu-card:hover { border-color: #444; transform: translateY(-3px); }
.stu-card-icon  { font-size: 26px; margin-bottom: 8px; }
.stu-card-title { font-size: 14px; font-weight: 700; color: #e8e8e8; margin-bottom: 6px; }
.stu-card-desc  { font-size: 12px; color: #777; line-height: 1.6; }
.stu-card-tag {
    display: inline-block; margin-top: 10px; font-size: 11px;
    background: #222; color: #555; border-radius: 20px;
    padding: 2px 10px; border: 1px solid #333;
}

/* ── STUDENT ID CARD ── */
.id-card {
    background: linear-gradient(135deg, #1a2a1a, #0d1a0d);
    border: 1px solid #2a4a2a;
    border-radius: 16px;
    padding: 1.5rem;
    max-width: 400px;
    margin: 0 auto;
    animation: fadeInUp 0.5s ease both;
}
.id-card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 1rem; }
.id-avatar {
    width: 60px; height: 60px; border-radius: 50%;
    background: #2a4a2a; display: flex; align-items: center;
    justify-content: center; font-size: 24px; flex-shrink: 0;
}
.id-name   { font-size: 16px; font-weight: 700; color: #e8e8e8; }
.id-role   { font-size: 12px; color: #5a8a5a; margin-top: 2px; }
.id-row    { display: flex; justify-content: space-between; padding: 6px 0;
             border-bottom: 1px solid #1a3a1a; font-size: 13px; }
.id-key    { color: #666; }
.id-val    { color: #ccc; font-weight: 600; }
.id-qr     { text-align: center; margin-top: 1rem; font-size: 11px; color: #3a6a3a; }

/* ── INFO ITEMS ── */
.info-item {
    background: #181818; border-left: 3px solid #2a5a3a;
    border-radius: 0 10px 10px 0; padding: 12px 16px;
    margin-bottom: 8px; animation: fadeInUp 0.3s ease both;
}
.info-item-title { color: #e8e8e8; font-size: 14px; font-weight: 700; }
.info-item-sub   { color: #666; font-size: 12px; margin-top: 3px; }
.info-item-body  { color: #aaa; font-size: 13px; margin-top: 6px; line-height: 1.5; }

/* ── VALIDATION HINT ── */
.val-ok  { color:#00e050; font-size:12px; margin-top:-10px; margin-bottom:8px; }
.val-err { color:#ff5555; font-size:12px; margin-top:-10px; margin-bottom:8px; }

/* ── CREATE ACCOUNT FORM ── */
.create-form-box {
    background: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    animation: fadeInUp 0.4s ease both;
}
.create-form-title {
    font-size: 14px; font-weight: 800; color: #e8e8e8;
    letter-spacing: 1px; text-transform: uppercase;
    margin-bottom: 1rem;
    padding-bottom: 8px;
    border-bottom: 1px solid #222;
}
.role-badge-student { background:#003a30; color:#00e0b0; border-radius:6px; padding:2px 10px; font-size:12px; font-weight:700; }
.role-badge-teacher { background:#003a5a; color:#00b0e0; border-radius:6px; padding:2px 10px; font-size:12px; font-weight:700; }
.role-badge-admin   { background:#3a0030; color:#e000b0; border-radius:6px; padding:2px 10px; font-size:12px; font-weight:700; }

/* ── FOOTER ── */
.acs-footer {
    border-top: 1px solid #222; padding-top: 1.2rem;
    margin-top: 0.5rem; animation: fadeInUp 0.5s ease both;
}
.footer-contacts { display: flex; gap: 1.5rem; flex-wrap: wrap; margin-bottom: 10px; }
.footer-contact  { font-size: 13px; color: #777; }
.footer-contact span { color: #bbb; }
.footer-copy     { font-size: 11px; color: #444; line-height: 1.7; }
.footer-copy strong { color: #555; }

/* ── BANNED WARNING ── */
.banned-warn {
    background: #2a0000; border: 1px solid #5a0000;
    border-radius: 10px; padding: 1rem 1.25rem;
    text-align: center; color: #ff5555;
    font-size: 15px; font-weight: 700;
    animation: pulse 1.5s infinite;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ================================================================
# LANGUAGE SWITCHER
# ================================================================
lang_col1, lang_col2 = st.columns([9, 1])
with lang_col2:
    if st.button("RU" if st.session_state.lang == "en" else "EN", key="lang_btn"):
        st.session_state.lang = "en" if st.session_state.lang == "ru" else "ru"
        st.rerun()


# ================================================================
# MODALS
# ================================================================

if st.session_state.modal == "account":
    st.markdown("<div class='big-title'>📩 ЗАПРОС СОЗДАНИЯ АККАУНТА</div>", unsafe_allow_html=True)
    st.markdown("")
    if st.session_state.success_msg:
        st.success(st.session_state.success_msg)
        if st.button("← Назад", use_container_width=True): close_modal()
        st.stop()

    iin   = st.text_input("ИИН (12 цифр)", placeholder="123456789012", max_chars=12)
    # Live IIN validation
    if iin:
        ok_iin, msg_iin = validate_iin(iin)
        st.markdown(
            f"<div class='{'val-ok' if ok_iin else 'val-err'}'>{'✓ ИИН корректен' if ok_iin else '⚠ ' + msg_iin}</div>",
            unsafe_allow_html=True
        )

    email = st.text_input("Email", placeholder="example@mail.com")
    phone = st.text_input("Номер телефона", placeholder="+77001234567", max_chars=13)
    # Live phone validation
    if phone:
        ok_ph, msg_ph = validate_phone(phone)
        st.markdown(
            f"<div class='{'val-ok' if ok_ph else 'val-err'}'>{'✓ Номер корректен' if ok_ph else '⚠ ' + msg_ph}</div>",
            unsafe_allow_html=True
        )

    name  = st.text_input("Полное имя", placeholder="Иванов Иван Иванович")
    c1, c2 = st.columns(2)
    if c1.button("📤 Отправить", use_container_width=True):
        ok_iin, msg_iin = validate_iin(iin) if iin else (False, "Введите ИИН")
        ok_ph,  msg_ph  = validate_phone(phone) if phone else (False, "Введите телефон")
        errors = []
        if not iin:   errors.append("Введите ИИН")
        elif not ok_iin: errors.append(msg_iin)
        if not email: errors.append("Введите Email")
        if not phone: errors.append("Введите телефон")
        elif not ok_ph: errors.append(msg_ph)
        if not name:  errors.append("Введите полное имя")
        if errors:
            for e in errors: st.error(f"⚠️ {e}")
        else:
            st.session_state.account_requests.append({
                "id": str(uuid.uuid4())[:8], "type": "account",
                "iin": iin, "email": email, "phone": phone, "name": name,
                "status": "pending", "created": datetime.now().strftime("%d.%m.%Y %H:%M")
            })
            st.session_state.success_msg = "✅ Заявка отправлена! Администратор рассмотрит в течение 24 ч."
            st.rerun()
    if c2.button("✖ Отмена", use_container_width=True): close_modal()
    st.stop()

elif st.session_state.modal == "org":
    st.markdown("<div class='big-title'>🏢 ПОДКЛЮЧЕНИЕ К ОРГАНИЗАЦИИ</div>", unsafe_allow_html=True)
    st.markdown("")
    if st.session_state.success_msg:
        st.success(st.session_state.success_msg)
        if st.button("← Назад", use_container_width=True): close_modal()
        st.stop()
    org_name = st.text_input("Наименование организации", placeholder="ТОО «Компания»")
    bin_num  = st.text_input("БИН организации (12 цифр)", placeholder="123456789012", max_chars=12)
    if bin_num:
        ok_bin, msg_bin = validate_iin(bin_num)  # same rule: 12 digits
        label = "БИН корректен" if ok_bin else msg_bin.replace("ИИН", "БИН")
        st.markdown(
            f"<div class='{'val-ok' if ok_bin else 'val-err'}'>{'✓ ' + label if ok_bin else '⚠ ' + label}</div>",
            unsafe_allow_html=True
        )
    company  = st.text_input("Название компании", placeholder="APEC Petrotechnic")
    role_req = st.selectbox("Запрашиваемые права доступа", ["Сотрудник", "Менеджер", "Директор", "Администратор"])
    c1, c2 = st.columns(2)
    if c1.button("📤 Отправить", use_container_width=True):
        ok_bin, msg_bin = validate_iin(bin_num) if bin_num else (False, "Введите БИН")
        errors = []
        if not org_name: errors.append("Введите наименование организации")
        if not bin_num:  errors.append("Введите БИН")
        elif not ok_bin: errors.append(msg_bin.replace("ИИН", "БИН"))
        if not company:  errors.append("Введите название компании")
        if errors:
            for e in errors: st.error(f"⚠️ {e}")
        else:
            st.session_state.org_requests.append({
                "id": str(uuid.uuid4())[:8], "type": "org",
                "org_name": org_name, "bin": bin_num,
                "company": company, "role": role_req,
                "status": "pending", "created": datetime.now().strftime("%d.%m.%Y %H:%M")
            })
            st.session_state.success_msg = "✅ Запрос отправлен!"
            st.rerun()
    if c2.button("✖ Отмена", use_container_width=True): close_modal()
    st.stop()

elif st.session_state.modal == "support":
    st.markdown("<div class='big-title'>🛠 ТЕХНИЧЕСКАЯ ПОДДЕРЖКА</div>", unsafe_allow_html=True)
    problems = [
        ("❌ Не запускается система", "Перезапустите браузер или очистите кэш (Ctrl+Shift+Del)."),
        ("❌ Аккаунт не создаётся", "Ожидайте одобрения администратора — до 24 часов."),
        ("❌ Ошибка входа", "Проверьте логин/пароль. Регистр важен. Роль должна совпадать."),
        ("❌ Расписание не отображается", "Убедитесь, что вы привязаны к группе."),
        ("❌ Заявка в статусе «Ожидание»", "Если более 48 ч — напишите на apec.edu.kz."),
        ("❌ Белый экран", "Попробуйте режим инкогнито или другой браузер."),
        ("❌ Нет группы в профиле", "Обратитесь к администратору для назначения группы."),
    ]
    for prob, ans in problems:
        st.markdown(f"<div class='sup-item'><div class='sup-prob'>{prob}</div><div class='sup-ans'>→ {ans}</div></div>", unsafe_allow_html=True)
    if st.button("← Назад на главную", use_container_width=True): close_modal()
    st.stop()

elif st.session_state.modal == "qa":
    st.markdown("<div class='big-title'>❓ ЧАСТЫЕ ВОПРОСЫ</div>", unsafe_allow_html=True)
    qas = [
        ("Как узнать своё расписание?", "Войдите → вкладка «Расписание». Привязано к группе."),
        ("Как рассчитывается GPA?", "A=4, B=3, C=2, D=1, F=0. GPA — среднее всех оценок."),
        ("Можно ли сменить группу?", "Да — обратитесь к администратору."),
        ("Сколько ждать одобрения?", "До 24 ч в рабочие дни, до 48 ч в праздники."),
        ("Можно войти с другого устройства?", "Да, система доступна через любой браузер."),
        ("Забыл пароль?", "Обратитесь к администратору — он сбросит вручную."),
    ]
    for q, a in qas:
        st.markdown(f"<div class='sup-item'><div class='sup-prob'>💬 {q}</div><div class='sup-ans'>→ {a}</div></div>", unsafe_allow_html=True)
    if st.button("← Назад на главную", use_container_width=True): close_modal()
    st.stop()

elif st.session_state.modal == "student_id":
    u = st.session_state.user
    st.markdown("<div class='big-title'>🪪 СТУДЕНЧЕСКИЙ БИЛЕТ</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='id-card'>
        <div class='id-card-header'>
            <div class='id-avatar'>🎓</div>
            <div>
                <div class='id-name'>{u['name']}</div>
                <div class='id-role'>Студент · APEC Petrotechnic</div>
            </div>
        </div>
        <div class='id-row'><span class='id-key'>Группа</span><span class='id-val'>{u.get('group','-')}</span></div>
        <div class='id-row'><span class='id-key'>Дата рождения</span><span class='id-val'>{u.get('dob','-')}</span></div>
        <div class='id-row'><span class='id-key'>Телефон</span><span class='id-val'>{u.get('phone','-')}</span></div>
        <div class='id-row'><span class='id-key'>Статус</span><span class='id-val' style='color:#00e050;'>Активен</span></div>
        <div class='id-qr'>▉▊▋ QR-код билета · ACS-{str(uuid.uuid4())[:8].upper()} ▋▊▉<br>Действителен: 2025–2026 уч. год</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("← Назад", use_container_width=True): close_modal()
    st.stop()

elif st.session_state.modal == "festivals":
    st.markdown("<div class='big-title'>🎉 ФЕСТИВАЛИ ДЛЯ СТУДЕНТОВ</div>", unsafe_allow_html=True)
    events = [
        ("🎵 Фестиваль «Жас Дарын»", "15 мая 2026", "Конкурс молодых талантов APEC. Музыка, танцы, стихи."),
        ("💻 HackATYRAU 2026",        "22–23 мая 2026", "Городской хакатон для студентов IT-специальностей. Призы от партнёров."),
        ("🏆 Спортивный турнир ACS",  "1 июня 2026", "Соревнования по футболу, волейболу, настольному теннису."),
        ("🎨 ArtFest APEC",           "10 июня 2026", "Выставка студенческих работ: рисунок, фото, дизайн."),
        ("🎓 День выпускника",        "28 июня 2026", "Торжественная церемония вручения дипломов 2026."),
    ]
    for title, date, desc in events:
        st.markdown(f"""
        <div class='info-item'>
            <div class='info-item-title'>{title}</div>
            <div class='info-item-sub'>📅 {date}</div>
            <div class='info-item-body'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("← Назад", use_container_width=True): close_modal()
    st.stop()


# ================================================================
# AUTH PAGE
# ================================================================

if not st.session_state.auth:
    st.markdown(f"<div class='big-title'>{t('title')}</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;margin-bottom:14px;animation:fadeIn 0.7s ease both;">
        <a href="https://apec.edu.kz/" target="_blank">
            <img src="https://apec.edu.kz/assets/main_logo.png" width="100">
        </a>
    </div>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(f"### {t('auth_title')}")
        login_in = st.text_input(t("login_label"))
        pass_in  = st.text_input(t("pass_label"), type="password")
        role_in  = st.radio(t("role_label"), ["Student", "Teacher", "Administrator"])

        if st.button(t("login"), use_container_width=True):
            db = st.session_state.users_db
            if (login_in in db
                    and db[login_in]["password"] == pass_in
                    and db[login_in]["role"] == role_in):
                if db[login_in].get("banned", False):
                    st.markdown("<div class='banned-warn'>🚫 Ваш аккаунт заблокирован. Обратитесь к администратору.</div>", unsafe_allow_html=True)
                else:
                    st.session_state.auth = True
                    st.session_state.user = db[login_in]
                    st.session_state.user["_login"] = login_in
                    st.rerun()
            else:
                st.error("Ошибка входа: проверьте логин, пароль и роль")

    st.markdown("---")
    st.markdown(f"<div class='big-title' style='font-size:20px;letter-spacing:4px;margin-top:6px;'>{t('services')}</div>", unsafe_allow_html=True)

    st.markdown("<div class='card-col'>", unsafe_allow_html=True)
    r1, r2 = st.columns(2), st.columns(2)
    with r1[0]:
        if st.button("📩\n\nСоздание аккаунта\nИИН · Email · Телефон", use_container_width=True, key="card_acc"): open_modal("account")
    with r1[1]:
        if st.button("🏢\n\nПодключение к организации\nБИН · Компания · Права", use_container_width=True, key="card_org"): open_modal("org")
    with r2[0]:
        if st.button("🛠\n\nТехподдержка\nОшибки · Вход · Система", use_container_width=True, key="card_sup"): open_modal("support")
    with r2[1]:
        if st.button("❓\n\nQ&A\nЧастые вопросы", use_container_width=True, key="card_qa"): open_modal("qa")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="stat-grid">
        <div class="stat-card"><div class="stat-num">20 000+</div><div class="stat-label">Студентов<br>в системе</div></div>
        <div class="stat-card"><div class="stat-num">1 500+</div><div class="stat-label">Преподавателей<br>и наставников</div></div>
        <div class="stat-card"><div class="stat-num">200+</div><div class="stat-label">Образовательных<br>учреждений</div></div>
    </div>
    <div class="about-block">
        <p><strong>ACS — APEC Control Service</strong> — самая современная платформа умного колледжа в Казахстане.
        Система объединяет расписания, успеваемость, студенческие заявки и административное управление
        в единой цифровой среде. Прозрачность, скорость и удобство для каждого участника процесса.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stu-section-title">Для студентов</div>
    <div class="stu-cards-grid">
        <div class="stu-card">
            <div class="stu-card-icon">🪪</div>
            <div class="stu-card-title">Студенческий билет</div>
            <div class="stu-card-desc">Цифровой билет с QR-кодом, привязанный к вашему профилю. Доступен в личном кабинете.</div>
            <div class="stu-card-tag">Войдите, чтобы получить</div>
        </div>
        <div class="stu-card">
            <div class="stu-card-icon">🎉</div>
            <div class="stu-card-title">Фестивали для студента</div>
            <div class="stu-card-desc">Мероприятия, конкурсы и фестивали колледжа. Регистрируйтесь прямо через ACS.</div>
            <div class="stu-card-tag">Войдите, чтобы смотреть</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="acs-footer">
        <div class="footer-contacts">
            <div class="footer-contact">💬 WhatsApp: <span>+7 702 124 12 50</span></div>
            <div class="footer-contact">✈️ Telegram: <span>@ACSHelpbot</span></div>
        </div>
        <div class="footer-copy">
            <strong>© 2026 College — ACS. Все права защищены.</strong><br>
            *Для населённых пунктов Республики Казахстан, доступных в разделе «Местоположение».
            На основании договора с уполномоченным государственным органом в сфере образования.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ================================================================
# AUTHENTICATED — sync user data from db
# ================================================================

user     = st.session_state.user
ulogin   = user.get("_login", "")
if ulogin and ulogin in st.session_state.users_db:
    live = st.session_state.users_db[ulogin]
    if live.get("banned", False):
        st.markdown("<div class='banned-warn'>🚫 Ваш аккаунт был заблокирован. Обратитесь к администратору.</div>", unsafe_allow_html=True)
        if st.button("Выйти"): logout()
        st.stop()

# ── NAV BAR ──
st.markdown(f"<div class='big-title'>{t('title')}</div>", unsafe_allow_html=True)

c_logo, c_nav, c_user_col = st.columns([1, 5, 1])
with c_logo:
    st.image("https://apec.edu.kz/assets/main_logo.png", width=55)
with c_nav:
    if user["role"] == "Student":
        n1, n2, n3, n4, n5, n6 = st.columns(6)
        if n1.button(t("schedule"),    use_container_width=True): set_page("schedule")
        if n2.button(t("groups"),      use_container_width=True): set_page("groups")
        if n3.button(t("gpa"),         use_container_width=True): set_page("gpa")
        if n4.button(t("student_id"),  use_container_width=True): open_modal("student_id")
        if n5.button(t("festivals"),   use_container_width=True): open_modal("festivals")
        if n6.button(t("logout"),      use_container_width=True): logout()
    elif user["role"] == "Teacher":
        n1, n2, n3, n4 = st.columns(4)
        if n1.button(t("schedule"),   use_container_width=True): set_page("schedule")
        if n2.button(t("assign_hw"),  use_container_width=True): set_page("hw")
        if n3.button(t("send_notif"), use_container_width=True): set_page("notif")
        if n4.button(t("logout"),     use_container_width=True): logout()
    else:
        n1, n2, n3 = st.columns(3)
        if n1.button(t("schedule"),    use_container_width=True): set_page("schedule")
        if n2.button(t("admin_panel"), use_container_width=True): set_page("admin")
        if n3.button(t("logout"),      use_container_width=True): logout()
with c_user_col:
    st.markdown(
        f"<div style='text-align:right;font-size:13px;color:#aaa;padding-top:6px;'>"
        f"{user['name']}<br><span style='color:#666;font-size:11px;'>{user['role']}</span></div>",
        unsafe_allow_html=True)

st.markdown("---")


# ================================================================
# STUDENT PAGES
# ================================================================
if user["role"] == "Student":

    grp = user.get("group", "")

    if st.session_state.page == "schedule":
        st.title(t("schedule"))

        my_notifs = [n for n in st.session_state.notifications if n["to_group"] in (grp, "ALL")]
        if my_notifs:
            st.markdown("#### 🔔 Уведомления")
            for n in reversed(my_notifs[-3:]):
                st.markdown(f"<div class='info-item'><div class='info-item-title'>📢 {n['message']}</div><div class='info-item-sub'>От: {n['created_by']} · {n['created']}</div></div>", unsafe_allow_html=True)
            st.markdown("")

        if grp in SCHEDULE:
            df = pd.DataFrame(SCHEDULE[grp], columns=[t("day"), t("time"), t("subject")])
            st.table(df)
        else:
            st.info(t("no_schedule"))

        my_hw = [h for h in st.session_state.homeworks if h["group"] in (grp, "ALL")]
        if my_hw:
            st.markdown("#### 📝 Домашние задания")
            for h in reversed(my_hw):
                st.markdown(f"""
                <div class='info-item'>
                    <div class='info-item-title'>{h['subject']}</div>
                    <div class='info-item-sub'>До: {h['due']} · Группа: {h['group']} · Задал: {h['created_by']}</div>
                    <div class='info-item-body'>{h['task']}</div>
                </div>
                """, unsafe_allow_html=True)

    elif st.session_state.page == "gpa":
        st.title(t("gpa"))
        mapping = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
        grade = st.selectbox(t("select_grade"), list(mapping.keys()))
        c1, c2 = st.columns(2)
        if c1.button(t("add_grade"),  use_container_width=True): st.session_state.gpa_grades.append(grade)
        if c2.button(t("clear"),      use_container_width=True): st.session_state.gpa_grades = []
        if st.session_state.gpa_grades:
            st.write(t("grades_label"), "  ·  ".join(st.session_state.gpa_grades))
            if st.button(t("calc_gpa"), use_container_width=True):
                gpa   = sum(mapping[g] for g in st.session_state.gpa_grades) / len(st.session_state.gpa_grades)
                color = "#00e050" if gpa >= 3 else "#f0c000" if gpa >= 2 else "#ff5555"
                st.markdown(f"<div style='font-size:52px;font-weight:800;color:{color};text-align:center;margin-top:16px;'>GPA: {gpa:.2f}</div>", unsafe_allow_html=True)

    elif st.session_state.page == "groups":
        st.title(t("groups"))
        st.info(f"{t('your_group')}: **{grp}**")


# ================================================================
# TEACHER PAGES
# ================================================================
elif user["role"] == "Teacher":

    if st.session_state.page == "schedule":
        st.title(t("teacher_panel"))
        for grp_name, sched in SCHEDULE.items():
            st.subheader(f"{t('group_label')}: {grp_name}")
            df = pd.DataFrame(sched, columns=[t("day"), t("time"), t("subject")])
            st.table(df)

    elif st.session_state.page == "hw":
        st.title("📝 Домашние задания и уроки")
        tab_hw, tab_lesson, tab_list = st.tabs(["📝 Задать ДЗ", "📅 Назначить урок", "📋 Список"])

        with tab_hw:
            st.subheader("Новое домашнее задание")
            grp_sel  = st.selectbox("Группа", list(SCHEDULE.keys()) + ["ALL"], key="hw_grp")
            subj_sel = st.text_input("Предмет", placeholder="Программирование", key="hw_subj")
            task_txt = st.text_area("Задание", placeholder="Решить задачи 1–5 из учебника...", key="hw_task")
            due_date = st.date_input("Срок сдачи", key="hw_due")
            if st.button("📤 Задать домашнее задание", use_container_width=True, key="hw_send"):
                if subj_sel and task_txt:
                    st.session_state.homeworks.append({
                        "id":          str(uuid.uuid4())[:8],
                        "group":       grp_sel,
                        "subject":     subj_sel,
                        "task":        task_txt,
                        "due":         due_date.strftime("%d.%m.%Y"),
                        "created_by":  user["name"],
                        "created":     datetime.now().strftime("%d.%m.%Y %H:%M")
                    })
                    st.success("✅ Домашнее задание добавлено!")
                else:
                    st.error("Заполните предмет и задание")

        with tab_lesson:
            st.subheader("Назначить дополнительный урок")
            grp_l   = st.selectbox("Группа", list(SCHEDULE.keys()), key="les_grp")
            subj_l  = st.text_input("Предмет / тема", key="les_subj")
            day_l   = st.selectbox("День", ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота"], key="les_day")
            time_l  = st.time_input("Время", key="les_time")
            if st.button("📅 Добавить урок в расписание", use_container_width=True, key="les_send"):
                if subj_l:
                    SCHEDULE[grp_l].append([day_l, time_l.strftime("%H:%M"), subj_l])
                    st.success(f"✅ Урок «{subj_l}» добавлен в расписание группы {grp_l}!")
                else:
                    st.error("Введите название предмета")

        with tab_list:
            st.subheader("Все домашние задания")
            if not st.session_state.homeworks:
                st.info("Домашних заданий пока нет.")
            else:
                for h in reversed(st.session_state.homeworks):
                    st.markdown(f"""
                    <div class='info-item'>
                        <div class='info-item-title'>{h['subject']} — {h['group']}</div>
                        <div class='info-item-sub'>До: {h['due']} · Задал: {h['created_by']} · {h['created']}</div>
                        <div class='info-item-body'>{h['task']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    elif st.session_state.page == "notif":
        st.title("🔔 Уведомления для студентов")
        grp_n  = st.selectbox("Кому", list(SCHEDULE.keys()) + ["ALL"], key="notif_grp")
        msg_n  = st.text_area("Сообщение", placeholder="Завтра занятие перенесено на 11:00...", key="notif_msg")
        if st.button("📢 Отправить уведомление", use_container_width=True, key="notif_send"):
            if msg_n:
                st.session_state.notifications.append({
                    "id":          str(uuid.uuid4())[:8],
                    "to_group":    grp_n,
                    "message":     msg_n,
                    "created_by":  user["name"],
                    "created":     datetime.now().strftime("%d.%m.%Y %H:%M")
                })
                st.success("✅ Уведомление отправлено!")
            else:
                st.error("Введите сообщение")

        st.markdown("---")
        st.subheader("Отправленные уведомления")
        my_notifs = [n for n in st.session_state.notifications if n["created_by"] == user["name"]]
        if not my_notifs:
            st.info("Вы ещё не отправляли уведомлений.")
        else:
            for n in reversed(my_notifs):
                st.markdown(f"""
                <div class='info-item'>
                    <div class='info-item-title'>📢 {n['message']}</div>
                    <div class='info-item-sub'>Группа: {n['to_group']} · {n['created']}</div>
                </div>
                """, unsafe_allow_html=True)


# ================================================================
# ADMINISTRATOR PAGES
# ================================================================
elif user["role"] == "Administrator":

    if st.session_state.page in ("schedule", "admin"):
        st.title(t("admin_panel"))
        tab1, tab2, tab3, tab4 = st.tabs([t("tab_acc"), t("tab_org"), t("tab_users"), t("tab_create")])

        # ── TAB 1: Account requests ──
        with tab1:
            reqs      = st.session_state.account_requests
            pending_n = sum(1 for r in reqs if r["status"] == "pending")
            st.markdown(f"**Всего заявок: {len(reqs)} · Ожидают: {pending_n}**")
            if not reqs:
                st.info("Заявок пока нет.")
            else:
                for i, r in enumerate(reqs):
                    b_cls  = {"pending":"badge-pending","approved":"badge-approved","rejected":"badge-rejected"}[r["status"]]
                    b_text = {"pending":"⏳ Ожидание","approved":"✅ Одобрено","rejected":"❌ Отклонено"}[r["status"]]
                    with st.expander(f"#{r['id']} — {r['name']} [{r['created']}]"):
                        st.markdown(f"<span class='badge {b_cls}'>{b_text}</span>", unsafe_allow_html=True)
                        st.write(f"**ИИН:** {r['iin']}  |  **Email:** {r['email']}  |  **Телефон:** {r['phone']}")
                        if r["status"] == "pending":
                            ca, cb, cc = st.columns(3)
                            nl  = ca.text_input("Логин",  key=f"lg_{i}")
                            np_ = cb.text_input("Пароль", key=f"pw_{i}")
                            ng  = cc.text_input("Группа", key=f"gp_{i}", placeholder="АИУ-1-25")
                            col_a, col_r = st.columns(2)
                            if col_a.button("✅ Одобрить", key=f"ap_{i}", use_container_width=True):
                                if nl and np_ and ng:
                                    st.session_state.users_db[nl] = {
                                        "password": np_, "role": "Student",
                                        "name": r["name"], "dob": "-",
                                        "phone": r["phone"], "group": ng, "banned": False
                                    }
                                    st.session_state.account_requests[i]["status"] = "approved"
                                    st.success(f"Аккаунт «{nl}» создан!")
                                    st.rerun()
                                else:
                                    st.error("Введите логин, пароль и группу")
                            if col_r.button("❌ Отклонить", key=f"rj_{i}", use_container_width=True):
                                st.session_state.account_requests[i]["status"] = "rejected"
                                st.rerun()

        # ── TAB 2: Org requests ──
        with tab2:
            org_reqs = st.session_state.org_requests
            if not org_reqs:
                st.info("Заявок на организации пока нет.")
            else:
                for i, r in enumerate(org_reqs):
                    b_cls  = {"pending":"badge-pending","approved":"badge-approved","rejected":"badge-rejected"}[r["status"]]
                    b_text = {"pending":"⏳ Ожидание","approved":"✅ Одобрено","rejected":"❌ Отклонено"}[r["status"]]
                    with st.expander(f"#{r['id']} — {r['org_name']} [{r['created']}]"):
                        st.markdown(f"<span class='badge {b_cls}'>{b_text}</span>", unsafe_allow_html=True)
                        st.write(f"**Организация:** {r['org_name']}  |  **БИН:** {r['bin']}  |  **Права:** {r['role']}")
                        if r["status"] == "pending":
                            col_a, col_r = st.columns(2)
                            if col_a.button("✅ Одобрить", key=f"oa_{i}", use_container_width=True):
                                st.session_state.org_requests[i]["status"] = "approved"; st.rerun()
                            if col_r.button("❌ Отклонить", key=f"or_{i}", use_container_width=True):
                                st.session_state.org_requests[i]["status"] = "rejected"; st.rerun()

        # ── TAB 3: All users ──
        with tab3:
            st.markdown("#### 👤 Управление пользователями")
            db = st.session_state.users_db

            search = st.text_input("🔍 Поиск по логину / имени / группе", placeholder="Введите запрос...")

            users_list = list(db.items())
            if search:
                s = search.lower()
                users_list = [(uname, udata) for uname, udata in users_list
                              if s in uname.lower()
                              or s in udata.get("name","").lower()
                              or s in udata.get("group","").lower()]

            if not users_list:
                st.info("Пользователи не найдены.")
            else:
                for uname, udata in users_list:
                    is_banned = udata.get("banned", False)
                    is_admin  = udata.get("role") == "Administrator"

                    badge_html = (
                        f"<span class='badge badge-banned'>{t('banned_badge')}</span>"
                        if is_banned else
                        f"<span class='badge badge-active'>✅ Активен</span>"
                    )

                    with st.expander(f"{'🚫 ' if is_banned else ''}@{uname} — {udata.get('name','-')} [{udata.get('role','-')}]"):
                        st.markdown(badge_html, unsafe_allow_html=True)
                        col_info, col_act = st.columns([3, 2])
                        with col_info:
                            st.write(f"**Группа:** {udata.get('group','-')}")
                            st.write(f"**Телефон:** {udata.get('phone','-')}")
                            st.write(f"**Роль:** {udata.get('role','-')}")
                        with col_act:
                            if not is_admin:
                                if is_banned:
                                    if st.button(t("unban_user"), key=f"unban_{uname}", use_container_width=True):
                                        st.session_state.users_db[uname]["banned"] = False
                                        st.success(f"Пользователь «{uname}» разблокирован.")
                                        st.rerun()
                                else:
                                    if st.button(t("ban_user"), key=f"ban_{uname}", use_container_width=True):
                                        st.session_state.users_db[uname]["banned"] = True
                                        st.warning(f"Пользователь «{uname}» заблокирован.")
                                        st.rerun()

                                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                                if st.button(t("delete_user"), key=f"del_{uname}", use_container_width=True):
                                    del st.session_state.users_db[uname]
                                    st.error(f"Пользователь «{uname}» удалён.")
                                    st.rerun()
                            else:
                                st.caption("Администратора нельзя удалить или заблокировать")

        # ── TAB 4: Create Account (Admin tool) ──
        with tab4:
            st.markdown("#### ➕ Создать новый аккаунт")
            st.markdown("""
            <div style='background:#181818;border:1px solid #2a2a2a;border-radius:12px;
                        padding:12px 16px;margin-bottom:1rem;font-size:13px;color:#777;'>
                Создание аккаунтов для Студентов, Преподавателей и Администраторов.
                Все поля обязательны. ИИН и телефон проходят автоматическую проверку.
            </div>
            """, unsafe_allow_html=True)

            # Role selector with visual badges
            new_role = st.radio(
                "Тип аккаунта",
                ["Student", "Teacher", "Administrator"],
                format_func=lambda r: {
                    "Student":       "🎓 Студент",
                    "Teacher":       "👨‍🏫 Преподаватель",
                    "Administrator": "🛠 Администратор"
                }[r],
                horizontal=True,
                key="new_role_select"
            )

            st.markdown("---")

            col_l, col_r = st.columns(2)

            with col_l:
                new_login = st.text_input("Логин", placeholder="ivan_ivanov", key="new_login")
                new_pass  = st.text_input("Пароль", type="password", placeholder="Минимум 4 символа", key="new_pass")
                new_name  = st.text_input("Полное имя", placeholder="Иванов Иван Иванович", key="new_name")
                new_dob   = st.text_input("Дата рождения", placeholder="ДД.ММ.ГГГГ", key="new_dob")

            with col_r:
                new_iin   = st.text_input("ИИН (12 цифр)", placeholder="123456789012", max_chars=12, key="new_iin")
                # Live IIN hint
                if new_iin:
                    ok_i, msg_i = validate_iin(new_iin)
                    st.markdown(
                        f"<div class='{'val-ok' if ok_i else 'val-err'}'>{'✓ ИИН корректен' if ok_i else '⚠ ' + msg_i}</div>",
                        unsafe_allow_html=True
                    )

                new_phone = st.text_input("Телефон", placeholder="+77001234567", max_chars=13, key="new_phone")
                # Live phone hint
                if new_phone:
                    ok_p, msg_p = validate_phone(new_phone)
                    st.markdown(
                        f"<div class='{'val-ok' if ok_p else 'val-err'}'>{'✓ Номер корректен' if ok_p else '⚠ ' + msg_p}</div>",
                        unsafe_allow_html=True
                    )

                # Group field — only for Student
                if new_role == "Student":
                    new_group = st.selectbox(
                        "Группа",
                        list(SCHEDULE.keys()),
                        key="new_group_sel"
                    )
                elif new_role == "Teacher":
                    new_group = "ALL"
                    st.markdown(
                        "<div style='color:#555;font-size:12px;padding:4px 0;'>Группа: ALL (преподаватель видит все группы)</div>",
                        unsafe_allow_html=True
                    )
                else:
                    new_group = "ALL"
                    st.markdown(
                        "<div style='color:#555;font-size:12px;padding:4px 0;'>Группа: ALL (администратор)</div>",
                        unsafe_allow_html=True
                    )

            st.markdown("")
            if st.button("✅ Создать аккаунт", use_container_width=True, key="create_acc_btn"):
                errors = []

                # — Field presence checks —
                if not new_login:  errors.append("Введите логин")
                elif new_login in st.session_state.users_db:
                    errors.append(f"Логин «{new_login}» уже занят")

                if not new_pass:   errors.append("Введите пароль")
                elif len(new_pass) < 4:
                    errors.append("Пароль должен содержать минимум 4 символа")

                if not new_name:   errors.append("Введите полное имя")
                if not new_dob:    errors.append("Введите дату рождения")

                # — IIN validation —
                if not new_iin:
                    errors.append("Введите ИИН")
                else:
                    ok_i, msg_i = validate_iin(new_iin)
                    if not ok_i: errors.append(msg_i)

                # — Phone validation —
                if not new_phone:
                    errors.append("Введите телефон")
                else:
                    ok_p, msg_p = validate_phone(new_phone)
                    if not ok_p: errors.append(msg_p)

                if errors:
                    for e in errors:
                        st.error(f"⚠️ {e}")
                else:
                    st.session_state.users_db[new_login] = {
                        "password": new_pass,
                        "role":     new_role,
                        "name":     new_name,
                        "dob":      new_dob,
                        "phone":    new_phone,
                        "group":    new_group,
                        "banned":   False,
                        "iin":      new_iin,
                    }
                    role_ru = {"Student": "Студент", "Teacher": "Преподаватель", "Administrator": "Администратор"}[new_role]
                    st.success(f"✅ Аккаунт «{new_login}» ({role_ru}) успешно создан!")
                    st.markdown(f"""
                    <div style='background:#0a1a10;border:1px solid #1a4a2a;border-radius:10px;
                                padding:12px 16px;margin-top:8px;font-size:13px;'>
                        <b style='color:#00e050;'>Данные нового аккаунта:</b><br>
                        <span style='color:#aaa;'>Логин:</span> <b style='color:#e8e8e8;'>{new_login}</b> &nbsp;|&nbsp;
                        <span style='color:#aaa;'>Роль:</span> <b style='color:#e8e8e8;'>{role_ru}</b> &nbsp;|&nbsp;
                        <span style='color:#aaa;'>Группа:</span> <b style='color:#e8e8e8;'>{new_group}</b>
                    </div>
                    """, unsafe_allow_html=True)
