"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Trợ Lý Sàng Lọc Hồ Sơ Tuyển Dụng & Hẹn Phỏng Vấn
"""

def get_job_description(job_id: str) -> str:
    """
    Lấy thông tin chi tiết công việc từ hệ thống HRIS.

    Args:
        job_id (str): Mã công việc (Ví dụ: 'JOB-2024-001')

    Returns:
        str: Thông tin chi tiết: chức danh, yêu cầu, kỹ năng, mức lương
    """
    jobs = {
        "JOB-2024-001": "Vị trí: Python Developer\nYêu cầu: 3+ năm kinh nghiệm Python, Django, PostgreSQL\nKỹ năng: Backend, Database, REST API\nMức lương: 18-25 triệu VNĐ",
        "JOB-2024-002": "Vị trí: QA Engineer\nYêu cầu: 2+ năm kinh nghiệm testing, automation\nKỹ năng: Selenium, TestNG, Manual Testing\nMức lương: 15-20 triệu VNĐ",
    }
    return jobs.get(job_id, f"LỖI: Không tìm thấy công việc '{job_id}'.")


def get_candidate_profile(candidate_id: str) -> str:
    """
    Lấy hồ sơ ứng viên từ hệ thống HRIS.

    Args:
        candidate_id (str): Mã ứng viên (Ví dụ: 'CD-001')

    Returns:
        str: Thông tin: tên, kinh nghiệm, kỹ năng, học vấn
    """
    candidates = {
        "CD-001": "Tên: Nguyễn Văn A\nKinh nghiệm: 4 năm Python, 2 năm Django\nKỹ năng: Python, Django, PostgreSQL, REST API, Docker\nHọc vấn: Đại học BKHN - Khoa CNTT",
        "CD-002": "Tên: Trần Thị B\nKinh nghiệm: 1 năm QA, 2 năm testing manual\nKỹ năng: Selenium, TestNG, SQL, Bug tracking\nHọc vấn: Trung cấp - Chứng chỉ QA",
    }
    return candidates.get(candidate_id, f"LỖI: Không tìm thấy ứng viên '{candidate_id}'.")


def evaluate_candidate_fit(candidate_id: str, job_id: str) -> str:
    """
    Đánh giá mức độ phù hợp giữa ứng viên và công việc.

    Args:
        candidate_id (str): Mã ứng viên
        job_id (str): Mã công việc

    Returns:
        str: Điểm phù hợp (1-10) và nhận xét chi tiết
    """
    evaluations = {
        ("CD-001", "JOB-2024-001"): "Điểm phù hợp: 9/10 ✅ RẤT PHÙ HỢP\nLý do: Kinh nghiệm đầy đủ, kỹ năng match 95%, học vấn phù hợp.",
        ("CD-002", "JOB-2024-002"): "Điểm phù hợp: 7/10 ⚠️ KHỚP VỮA\nLý do: Kinh nghiệm chưa đủ (3 năm), nhưng kỹ năng cơ bản đủ.",
    }
    key = (candidate_id, job_id)
    return evaluations.get(key, "LỖI: Không thể đánh giá.")


def check_interviewer_availability(interviewer_id: str, date_range: str) -> str:
    """
    Kiểm tra lịch có sẵn của interviewer.

    Args:
        interviewer_id (str): Mã người phỏng vấn
        date_range (str): Khoảng thời gian cần kiểm tra (Ví dụ: '2024-12-20 to 2024-12-25')

    Returns:
        str: Danh sách slot thời gian còn trống
    """
    if "2024-12-2" in date_range:
        return "Lịch có sẵn của INT-001 (2024-12-20 đến 2024-12-25):\n- 20/12 09:00-10:00 ✓\n- 20/12 14:00-15:00 ✓\n- 21/12 10:00-11:00 ✓\n- 23/12 15:00-16:00 ✓"
    return "Không tìm thấy slot trống."


def schedule_interview(candidate_id: str, interviewer_id: str, interview_datetime: str) -> str:
    """
    Tạo lịch phỏng vấn trong hệ thống.

    Args:
        candidate_id (str): Mã ứng viên
        interviewer_id (str): Mã người phỏng vấn
        interview_datetime (str): Ngày giờ phỏng vấn (Ví dụ: '2024-12-20 09:00')

    Returns:
        str: Xác nhận tạo lịch thành công
    """
    return f"✅ Đã tạo lịch phỏng vấn:\nỨng viên: {candidate_id}\nNgười phỏng vấn: {interviewer_id}\nThời gian: {interview_datetime}\nID Cuộc họp: INT-20241220-001"


def send_email(recipient: str, subject: str, body: str) -> str:
    """
    Gửi email thông báo (cho ứng viên hoặc interviewer).

    Args:
        recipient (str): Địa chỉ email người nhận
        subject (str): Chủ đề email
        body (str): Nội dung email

    Returns:
        str: Xác nhận gửi thành công
    """
    return f"✅ Email gửi thành công:\nĐến: {recipient}\nChủ đề: {subject}\nThời gian gửi: 2024-12-19 14:30"


def rank_candidates(job_id: str) -> str:
    """
    Xếp hạng tất cả ứng viên cho một công việc dựa trên điểm phù hợp.

    Args:
        job_id (str): Mã công việc

    Returns:
        str: Danh sách ứng viên được xếp hạng
    """
    if job_id == "JOB-2024-001":
        return "Xếp hạng ứng viên cho JOB-2024-001:\n1. CD-001 (9/10) - ✅ RẤT PHÁT TRIỂN\n2. CD-005 (6/10) - ⚠️ CẦN PHỎNG VẤN\n3. CD-003 (4/10) - ❌ KHÔNG PHÁT TRIỂN"
    return "LỖI: Không tìm thấy công việc."


def reject_candidate(candidate_id: str, reason: str) -> str:
    """
    Từ chối ứng viên và gửi thông báo.

    Args:
        candidate_id (str): Mã ứng viên
        reason (str): Lý do từ chối

    Returns:
        str: Xác nhận từ chối
    """
    return f"✅ Đã cập nhật trạng thái ứng viên {candidate_id} thành 'Từ chối'.\nLý do: {reason}\nEmail thông báo đã gửi."


# Danh sách các tool được đăng ký để Agent sử dụng
AVAILABLE_TOOLS = {
    "get_job_description": get_job_description,
    "get_candidate_profile": get_candidate_profile,
    "evaluate_candidate_fit": evaluate_candidate_fit,
    "check_interviewer_availability": check_interviewer_availability,
    "schedule_interview": schedule_interview,
    "send_email": send_email,
    "rank_candidates": rank_candidates,
    "reject_candidate": reject_candidate,
}
