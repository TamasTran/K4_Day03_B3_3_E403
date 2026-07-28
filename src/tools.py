"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Trợ Lý Sàng Lọc Hồ Sơ Tuyển Dụng & Hẹn Phỏng Vấn
"""

from functools import wraps


def safe_tool(func):
    """Biến mọi exception của tool thành Observation lỗi, không làm sập Agent."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            return f"❌ LỖI: Tool '{func.__name__}' không thể thực thi: {exc}"

    return wrapper

# ============================================================================
# MOCK DATABASE - Giả lập dữ liệu từ HRIS/ATS
# ============================================================================

JOB_DESCRIPTIONS = {
    "JOB-2024-001": {
        "title": "Python Developer",
        "requirements": "3+ năm kinh nghiệm Python, Django, PostgreSQL",
        "skills": ["Python", "Django", "PostgreSQL", "REST API", "Docker"],
        "salary": "18-25 triệu VNĐ",
    },
    "JOB-2024-002": {
        "title": "QA Engineer",
        "requirements": "2+ năm kinh nghiệm testing, automation",
        "skills": ["Selenium", "TestNG", "Manual Testing", "SQL", "Bug Tracking"],
        "salary": "15-20 triệu VNĐ",
    },
    "JOB-2024-003": {
        "title": "Frontend Developer",
        "requirements": "3+ năm React, TypeScript, responsive design",
        "skills": ["React", "TypeScript", "CSS", "Webpack", "Jest"],
        "salary": "16-23 triệu VNĐ",
    },
}

CANDIDATES = {
    "CD-001": {
        "name": "Nguyễn Văn A",
        "experience": "4 năm Python + 2 năm Django, 1 năm PostgreSQL",
        "skills": ["Python", "Django", "PostgreSQL", "REST API", "Docker", "Linux"],
        "education": "Đại học BKHN - Khoa CNTT",
        "applying_for": "JOB-2024-001",
    },
    "CD-002": {
        "name": "Trần Thị B",
        "experience": "2 năm QA manual + 1 năm Selenium automation",
        "skills": ["Selenium", "TestNG", "Manual Testing", "SQL", "Bug Tracking", "Jira"],
        "education": "Trung cấp Công nghệ - Chứng chỉ QA",
        "applying_for": "JOB-2024-002",
    },
    "CD-003": {
        "name": "Lê Minh C",
        "experience": "2.5 năm React + 1.5 năm TypeScript",
        "skills": ["React", "JavaScript", "CSS", "HTML", "Git"],
        "education": "Đại học FPT - Khoa IT",
        "applying_for": "JOB-2024-003",
    },
    "CD-004": {
        "name": "Phạm Thị D",
        "experience": "5 năm Python, 3 năm Django + PostgreSQL",
        "skills": ["Python", "Django", "PostgreSQL", "REST API", "Docker", "AWS", "Kubernetes"],
        "education": "Thạc sĩ - Đại học Bách Khoa",
        "applying_for": "JOB-2024-001",
    },
    "CD-005": {
        "name": "Hoàng Văn E",
        "experience": "1 năm QA automation",
        "skills": ["Selenium", "Python", "TestNG"],
        "education": "Trung cấp - Chứng chỉ QA",
        "applying_for": "JOB-2024-002",
    },
}

INTERVIEWERS = {
    "INT-001": {
        "name": "Trần Hải - Tech Lead",
        "available_slots": ["2024-12-20 09:00", "2024-12-20 14:00", "2024-12-21 10:00", "2024-12-23 15:00"],
    },
    "INT-002": {
        "name": "Ngô Hương - HR Manager",
        "available_slots": ["2024-12-19 13:00", "2024-12-20 10:00", "2024-12-22 11:00"],
    },
}

# ============================================================================
# TOOLS - Các công cụ mà Agent có thể gọi
# ============================================================================


@safe_tool
def get_job_description(job_id: str) -> str:
    """
    Lấy thông tin chi tiết công việc từ hệ thống HRIS.

    Trả về: chức danh, yêu cầu, kỹ năng, mức lương

    Args:
        job_id (str): Mã công việc (Ví dụ: 'JOB-2024-001')

    Returns:
        str: Thông tin chi tiết công việc
    """
    if job_id not in JOB_DESCRIPTIONS:
        return f"❌ LỖI: Không tìm thấy công việc '{job_id}'."

    job = JOB_DESCRIPTIONS[job_id]
    return (
        f"📋 THÔNG TIN CÔNG VIỆC: {job_id}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 Chức danh: {job['title']}\n"
        f"📌 Yêu cầu: {job['requirements']}\n"
        f"💡 Kỹ năng cần thiết: {', '.join(job['skills'])}\n"
        f"💰 Mức lương: {job['salary']}"
    )


@safe_tool
def get_candidate_profile(candidate_id: str) -> str:
    """
    Lấy hồ sơ ứng viên từ hệ thống HRIS.

    Trả về: kinh nghiệm, kỹ năng, học vấn

    Args:
        candidate_id (str): Mã ứng viên (Ví dụ: 'CD-001')

    Returns:
        str: Thông tin hồ sơ ứng viên
    """
    if candidate_id not in CANDIDATES:
        return f"❌ LỖI: Không tìm thấy ứng viên '{candidate_id}'."

    candidate = CANDIDATES[candidate_id]
    return (
        f"👤 HỒ SƠ ỨNG VIÊN: {candidate_id}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 Tên: {candidate['name']}\n"
        f"⏳ Kinh nghiệm: {candidate['experience']}\n"
        f"💪 Kỹ năng: {', '.join(candidate['skills'])}\n"
        f"🎓 Học vấn: {candidate['education']}\n"
        f"🎯 Đang ứng tuyển: {candidate['applying_for']}"
    )


@safe_tool
def evaluate_candidate_fit(candidate_id: str, job_id: str) -> str:
    """
    Chấm điểm phù hợp (1-10) kèm nhận xét giữa một ứng viên và một vị trí cụ thể.

    Args:
        candidate_id (str): Mã ứng viên
        job_id (str): Mã công việc

    Returns:
        str: Điểm phù hợp (1-10) + nhận xét chi tiết
    """
    if candidate_id not in CANDIDATES:
        return f"❌ LỖI: Ứng viên '{candidate_id}' không tồn tại."
    if job_id not in JOB_DESCRIPTIONS:
        return f"❌ LỖI: Công việc '{job_id}' không tồn tại."

    evaluations = {
        ("CD-001", "JOB-2024-001"): (9, "✅ RẤT PHÙ HỢP", "Kinh nghiệm đầy đủ (4 năm), kỹ năng match 95%, học vấn phù hợp, sẵn sàng."),
        ("CD-002", "JOB-2024-002"): (7, "⚠️ KHỚP VỮA", "Kinh nghiệm chưa đủ (3 năm), nhưng kỹ năng cơ bản đủ, cần training thêm."),
        ("CD-003", "JOB-2024-003"): (8, "✅ PHÁT TRIỂN", "Kinh nghiệm React tốt, TypeScript chưa sâu, có tiềm năng cao."),
        ("CD-004", "JOB-2024-001"): (10, "🌟 XUẤT SẮC", "Kinh nghiệm rất sâu (5 năm), thạc sĩ, thành thạo tất cả kỹ năng."),
        ("CD-005", "JOB-2024-002"): (5, "❌ CHƯA ĐỦ", "Kinh nghiệm quá ít (1 năm), cần nhiều training, không đáp ứng yêu cầu."),
    }

    if (candidate_id, job_id) in evaluations:
        score, status, comment = evaluations[(candidate_id, job_id)]
        return (
            f"📊 ĐÁNH GIÁ PHỤ HỢP: {candidate_id} ↔ {job_id}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⭐ Điểm: {score}/10 {status}\n"
            f"📌 Nhận xét: {comment}"
        )

    return f"⚠️ Chưa có dữ liệu đánh giá cho cặp ({candidate_id}, {job_id})."


@safe_tool
def rank_candidates(job_id: str) -> str:
    """
    Xếp hạng toàn bộ ứng viên đang ứng tuyển cho một vị trí.

    Args:
        job_id (str): Mã công việc

    Returns:
        str: Danh sách ứng viên được xếp hạng (từ cao đến thấp)
    """
    if job_id not in JOB_DESCRIPTIONS:
        return f"❌ LỖI: Công việc '{job_id}' không tồn tại."

    rankings = {
        "JOB-2024-001": [
            ("CD-004", 10, "🌟 XUẤT SẮC"),
            ("CD-001", 9, "✅ RẤT PHÙ HỢP"),
            ("CD-003", 4, "❌ CHƯA PHÁT TRIỂN"),
        ],
        "JOB-2024-002": [
            ("CD-002", 7, "⚠️ KHỚP VỮA"),
            ("CD-005", 5, "❌ CHƯA ĐỦ"),
        ],
        "JOB-2024-003": [
            ("CD-003", 8, "✅ PHÁT TRIỂN"),
            ("CD-001", 3, "❌ KHÔNG KHỚP"),
        ],
    }

    if job_id not in rankings:
        return f"📊 Chưa có ứng viên nào cho công việc {job_id}."

    result = f"🏆 BẢNG XẾP HẠNG ỨNG VIÊN: {job_id}\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    for idx, (cand_id, score, status) in enumerate(rankings[job_id], 1):
        candidate = CANDIDATES[cand_id]
        result += f"{idx}. {cand_id} ({candidate['name']}) - {score}/10 {status}\n"
    return result


@safe_tool
def check_interviewer_availability(interviewer_id: str, date_range: str) -> str:
    """
    Xem các khung giờ còn trống của người phỏng vấn trong một khoảng thời gian.

    Args:
        interviewer_id (str): Mã người phỏng vấn
        date_range (str): Khoảng thời gian cần kiểm tra (Ví dụ: '2024-12-20 to 2024-12-25')

    Returns:
        str: Danh sách slot thời gian còn trống
    """
    if interviewer_id not in INTERVIEWERS:
        return f"❌ LỖI: Người phỏng vấn '{interviewer_id}' không tồn tại."

    interviewer = INTERVIEWERS[interviewer_id]
    slots = interviewer["available_slots"]

    result = (
        f"📅 LỊCH CÓ SẴN: {interviewer_id} ({interviewer['name']})\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⏱️ Khoảng thời gian: {date_range}\n"
    )

    if slots:
        result += f"✅ Các slot trống:\n"
        for slot in slots:
            result += f"  • {slot}\n"
    else:
        result += "❌ Không có slot trống trong khoảng thời gian này.\n"

    return result


@safe_tool
def schedule_interview(candidate_id: str, interviewer_id: str, interview_datetime: str) -> str:
    """
    Tạo lịch phỏng vấn chính thức trong hệ thống.

    Args:
        candidate_id (str): Mã ứng viên
        interviewer_id (str): Mã người phỏng vấn
        interview_datetime (str): Ngày giờ phỏng vấn (Ví dụ: '2024-12-20 09:00')

    Returns:
        str: Xác nhận tạo lịch thành công + ID cuộc họp
    """
    if candidate_id not in CANDIDATES:
        return f"❌ LỖI: Ứng viên '{candidate_id}' không tồn tại."
    if interviewer_id not in INTERVIEWERS:
        return f"❌ LỖI: Người phỏng vấn '{interviewer_id}' không tồn tại."

    candidate = CANDIDATES[candidate_id]
    interviewer = INTERVIEWERS[interviewer_id]

    return (
        f"✅ ĐÃ TẠO LỊCH PHỎNG VẤN\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Ứng viên: {candidate_id} ({candidate['name']})\n"
        f"👨‍💼 Người phỏng vấn: {interviewer_id} ({interviewer['name']})\n"
        f"📅 Thời gian: {interview_datetime}\n"
        f"🎫 ID Cuộc họp: INT-{interview_datetime.replace(' ', '-').replace(':', '')}\n"
        f"💬 Email xác nhận sẽ được gửi cho cả hai bên."
    )


@safe_tool
def send_email(recipient: str, subject: str, body: str) -> str:
    """
    Gửi email thông báo cho ứng viên hoặc người phỏng vấn.

    Args:
        recipient (str): Địa chỉ email người nhận (hoặc candidate_id/interviewer_id)
        subject (str): Chủ đề email
        body (str): Nội dung email

    Returns:
        str: Xác nhận gửi email thành công
    """
    return (
        f"📧 EMAIL ĐƯỢC GỬI THÀNH CÔNG\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📮 Đến: {recipient}\n"
        f"📌 Chủ đề: {subject}\n"
        f"📝 Nội dung: {body[:100]}...\n"
        f"⏱️ Thời gian gửi: 2024-12-19 14:30"
    )


@safe_tool
def reject_candidate(candidate_id: str, reason: str) -> str:
    """
    Cập nhật trạng thái "Từ chối" cho một ứng viên kèm lý do.
    Hệ thống sẽ tự gửi email thông báo.

    Args:
        candidate_id (str): Mã ứng viên
        reason (str): Lý do từ chối

    Returns:
        str: Xác nhận cập nhật trạng thái + email gửi
    """
    if candidate_id not in CANDIDATES:
        return f"❌ LỖI: Ứng viên '{candidate_id}' không tồn tại."

    candidate = CANDIDATES[candidate_id]
    return (
        f"✅ CẬP NHẬT TRẠNG THÁI TỪ CHỐI\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Ứng viên: {candidate_id} ({candidate['name']})\n"
        f"❌ Trạng thái: Từ chối\n"
        f"📋 Lý do: {reason}\n"
        f"📧 Email thông báo đã tự động gửi đến ứng viên.\n"
        f"💬 Nội dung: 'Cảm ơn bạn đã ứng tuyển. Thật tiếc chúng tôi không thể tiếp tục với hồ sơ của bạn lần này.'"
    )


# ============================================================================
# TOOL REGISTRY - Đăng ký các tool cho Agent sử dụng
# ============================================================================

AVAILABLE_TOOLS = {
    "get_job_description": get_job_description,
    "get_candidate_profile": get_candidate_profile,
    "evaluate_candidate_fit": evaluate_candidate_fit,
    "rank_candidates": rank_candidates,
    "check_interviewer_availability": check_interviewer_availability,
    "schedule_interview": schedule_interview,
    "send_email": send_email,
    "reject_candidate": reject_candidate,
}
