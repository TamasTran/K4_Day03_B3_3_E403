# Trace đánh giá ReAct Agent — Mốc 3

Môi trường chạy thử:

- Provider: `MockProvider` (offline, không tiêu tốn API key)
- Guardrail vòng lặp: `MAX_ITERATIONS = 5`
- Nguồn test: `config/test_cases.json`

## Test case 3 — Chuỗi suy luận nhiều tool

Yêu cầu: so sánh ứng viên `CD-001` với công việc `JOB-2024-001`.

```text
Thought: Cần lấy hồ sơ ứng viên trước khi đánh giá.
Action: get_candidate_profile["CD-001"]
Observation: CD-001 có 4 năm Python, 2 năm Django, PostgreSQL,
REST API, Docker và đang ứng tuyển JOB-2024-001.

Thought: Cần lấy yêu cầu chính thức của công việc để đối chiếu.
Action: get_job_description["JOB-2024-001"]
Observation: Vị trí Python Developer yêu cầu 3+ năm Python,
Django, PostgreSQL, REST API và Docker.

Thought: Đã có hồ sơ và JD, có thể dùng tool đánh giá.
Action: evaluate_candidate_fit["CD-001", "JOB-2024-001"]
Observation: Điểm phù hợp 9/10 — RẤT PHÙ HỢP; kinh nghiệm đầy đủ,
kỹ năng khớp 95% và học vấn phù hợp.

Final Answer: CD-001 phù hợp với JOB-2024-001 ở mức 9/10.
```

Kết quả: đạt; Agent gọi đúng thứ tự ba tool và chỉ kết luận từ Observation.

## Test case 7 — Ứng viên không tồn tại

```text
Thought: Cần kiểm tra mức độ phù hợp của ứng viên với công việc.
Action: evaluate_candidate_fit["CD-999", "JOB-2024-001"]
Observation: ❌ LỖI: Ứng viên "CD-999" không tồn tại.

Final Answer: Tool báo lỗi nên Agent dừng lại để tránh thao tác sai dữ liệu.
```

Kết quả: đạt guardrail; không gọi thêm tool sau Observation lỗi.

## Test case 9 — Xung đột lịch

Yêu cầu: đặt lịch `2024-12-25 15:00` với `INT-001`.

```text
Thought: Phải kiểm tra lịch trống trước khi tạo lịch.
Action: check_interviewer_availability["INT-001", "2024-12-25 15:00"]
Observation: Các slot còn trống là 2024-12-20 09:00,
2024-12-20 14:00, 2024-12-21 10:00 và 2024-12-23 15:00.

Final Answer: Slot yêu cầu không có trong lịch trống nên Agent
không tạo lịch phỏng vấn.
```

Kết quả: đạt guardrail; `schedule_interview` và `send_email` không được gọi.

## Phanh an toàn đã xác nhận

1. Tool không tồn tại hoặc sai số tham số được chuyển thành Observation lỗi.
2. Exception phát sinh bên trong tool được `safe_tool` bắt và trả về chuỗi lỗi.
3. Observation chứa `LỖI` làm Agent dừng ngay.
4. Slot không khả dụng làm Agent dừng trước hành động tạo lịch.
5. ReAct loop không được vượt quá `MAX_ITERATIONS`.

## Kiểm thử tự động

Chạy:

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

Bộ test xác nhận provider thật đi qua vòng `LLM Action -> Tool Observation ->
LLM Final Answer`; planner viết sẵn chỉ được dùng với `MockProvider` để thử
offline. Output LLM sai định dạng cũng làm Agent dừng an toàn.
