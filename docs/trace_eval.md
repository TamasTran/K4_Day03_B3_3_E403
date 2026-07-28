# 📊 BÁO CÁO GIÁM SÁT & ĐÁNH GIÁ (OBSERVABILITY TRACE LOGS)
Dành cho Role 5: Observability & Reviewer

---

## 🎯 1. BẢNG CHẤM ĐIỂM AGENTIC FIT (SCORING MATRIX)

*Đề tài:* Trợ Lý Sàng Lọc Hồ Sơ Tuyển Dụng & Hẹn Phỏng Vấn

| Tiêu chí | Điểm (1-5) | Lý do đánh giá |
| :--- | :---: | :--- |
| 🧠 *Multi-step Reasoning* | 5/5 | Cần suy luận phức tạp: phân tích hồ sơ → so sánh yêu cầu → đánh giá phù hợp → lên kế hoạch phỏng vấn → xử lý từ chối. |
| 🛠️ *Tool Interaction* | 5/5 | Tương tác nhiều công cụ: đọc DB hồ sơ, tra cứu thông tin công việc, gửi email hẹn, kiểm tra lịch interviewer, quản lý calendar. |
| 🔀 *Dynamic Decision* | 5/5 | Quyết định xem hồ sơ phù hợp phụ thuộc nội dung chi tiết. Thời gian hẹn phỏng vấn phụ thuộc lịch có sẵn. Kết quả bước trước quyết định hành động tiếp theo. |
| ⏳ *Long Horizon* | 5/5 | Quy trình dài: sàng lọc sơ bộ → phân tích chi tiết → xếp hạng → hẹn phỏng vấn → gửi thông báo. Yêu cầu duy trì trạng thái qua nhiều bước. |
| *TỔNG ĐIỂM FIT* | *20/20* | *KẾT LUẬN: BÀI TOÁN HOÀN HẢO CHO AGENTIC ARCHITECTURE - CỰC KỲ NÊN DÙNG REACT AGENT!* |

---

## 🔍 2. SO SÁNH PHẢN HỒI (TEST CASE #3)
Môi trường chạy thử:

- Provider: `MockProvider` (offline, không tiêu tốn API key)
- Guardrail vòng lặp: `MAX_ITERATIONS = 5`
- Nguồn test: `config/test_cases.json`

## Test case được tạo như thế nào?

Các test case trong `config/test_cases.json` được nhóm thiết kế thủ công dựa
trên các luồng nghiệp vụ tuyển dụng mà Agent cần xử lý. Mỗi test case có các
trường chính:

- `question`: câu hỏi đầu vào gửi cho Agent.
- `expected_behavior`: chuỗi hành vi và thứ tự gọi tool mong đợi.
- `tools_used`: danh sách tool dự kiến được sử dụng.
- `success_criteria`: dữ liệu hoặc kết quả cần xuất hiện để xem là đạt.
- `trap_reason`: lý do tạo câu bẫy, chỉ có ở các edge case.

Bộ test được chia thành ba nhóm:

1. **Single tool:** kiểm tra Agent chọn đúng một tool để đọc JD hoặc hồ sơ.
2. **Multi-step:** kiểm tra Agent gọi nhiều tool theo đúng thứ tự và tổng hợp
   Observation thành câu trả lời.
3. **Edge case:** dùng ID không tồn tại hoặc slot không khả dụng để kiểm tra
   Agent có dừng an toàn hay không.

## Nguồn dữ liệu chuẩn (ground truth)

Toàn bộ dữ liệu dùng trong Mốc 3 là dữ liệu mock được khai báo trong
`src/tools.py`, không lấy từ API hoặc cơ sở dữ liệu tuyển dụng bên ngoài:

| Dữ liệu | Biến nguồn trong `src/tools.py` |
|---|---|
| Mô tả công việc, kỹ năng và lương | `JOB_DESCRIPTIONS` |
| Hồ sơ và kỹ năng ứng viên | `CANDIDATES` |
| Người phỏng vấn và slot trống | `INTERVIEWERS` |
| Điểm phù hợp của từng cặp ứng viên–công việc | `evaluations` trong `evaluate_candidate_fit()` |
| Thứ hạng ứng viên | `rankings` trong `rank_candidates()` |

Ví dụ, kết quả `CD-001` phù hợp `JOB-2024-001` ở mức `9/10` được xem là đúng
vì cặp này được khai báo trực tiếp trong bảng `evaluations`. Tương tự,
`CD-999` là dữ liệu sai vì mã này không tồn tại trong `CANDIDATES`.

Do đó, “đúng” trong báo cáo này có nghĩa là kết quả của Agent nhất quán với
mock data và quy tắc nghiệp vụ của bài lab; nó không có nghĩa là dữ liệu đã
được xác minh với một hệ thống HR thật.

## Cách xác định pass/fail

Luồng đối chiếu được sử dụng:

```text
question trong test_cases.json
        ↓
Agent chọn Thought và Action
        ↓
AVAILABLE_TOOLS gọi hàm tương ứng
        ↓
Tool đọc mock data trong tools.py
        ↓
Observation được trả về Agent
        ↓
Đối chiếu tool đã gọi, dữ liệu trả về và hành vi dừng
```

Một test được xem là đạt khi:

- Agent chọn đúng tool cần thiết và không gọi tool ngoài danh sách.
- Các ID, điểm số, kỹ năng và slot trong Observation khớp mock data.
- Luồng nhiều bước thực hiện đúng thứ tự nghiệp vụ.
- Agent dừng khi Observation chứa `LỖI`.
- Với câu bẫy lịch, Agent không gọi `schedule_interview` hoặc `send_email`
  sau khi nhận thấy slot yêu cầu không khả dụng.

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
4. Trong luồng qua `run_react_agent`, slot không khả dụng làm Agent dừng trước
   hành động tạo lịch.
5. ReAct loop không được vượt quá `MAX_ITERATIONS`.

## Kiểm thử tự động

Chạy:

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

Bộ test dùng `ScriptedProvider` để mô phỏng đường đi của provider thật qua
vòng `LLM Action -> Tool Observation -> LLM Final Answer`; không có request
API thật trong unit test. Planner viết sẵn chỉ được dùng với `MockProvider` để
thử offline. Output LLM sai định dạng cũng làm Agent dừng an toàn.

## Kết quả xác minh Mốc 3

Ngày chạy: 2026-07-28.

```text
Ran 5 tests in 0.002s
OK
```

Ba kịch bản được chạy lại trực tiếp bằng `MockProvider`:

- Test case 3: gọi tuần tự `get_candidate_profile` → `get_job_description` →
  `evaluate_candidate_fit`, kết luận `9/10 - RẤT PHÙ HỢP`.
- Test case 7: Observation báo `LỖI` với `CD-999`; Agent dừng ngay và không gọi
  thêm tool.
- Test case 9: slot `2024-12-25 15:00` không xuất hiện trong lịch trống; Agent
  dừng trước `schedule_interview` và `send_email`.

Ngoài ra, `app.py`, `prompts.py`, `tools.py` và `providers.py` đều vượt qua
kiểm tra biên dịch bằng `python -m py_compile`. Chế độ offline có thể chạy ngay
cả khi máy chưa cài `python-dotenv`; các provider online vẫn dùng `.env` khi
dependency này có mặt.

## Giới hạn của kết quả đánh giá

`config/test_cases.json` hiện đóng vai trò bộ đặc tả và dữ liệu đầu vào cho
demo. Hàm `run_demo()` có hiển thị `tools_used`, nhưng chưa tự động so sánh
danh sách tool thực tế với danh sách mong đợi và chưa tự diễn giải toàn bộ
chuỗi `success_criteria`. Năm unit test trong `tests/test_react_agent.py` mới
là các kiểm tra có assertion tự động.

Ngoài ra, guardrail slot hiện nằm trong `run_react_agent`. Nếu gọi trực tiếp
`schedule_interview()` thì tool chưa tự kiểm tra thời điểm có thuộc
`INTERVIEWERS[interviewer_id]["available_slots"]` hay không. Tool
`check_interviewer_availability()` cũng chưa lọc danh sách theo `date_range`.
Vì vậy kết luận “đạt” của test case 9 chỉ áp dụng cho luồng Agent hiện tại,
không chứng minh rằng riêng từng tool đã an toàn trước mọi cách gọi.

Các kiểm tra nên bổ sung:

- So sánh tự động tool thực tế với `tools_used` của cả 10 test case.
- Kiểm tra `success_criteria` bằng assertion thay vì chỉ đọc log.
- Kiểm tra gọi thẳng `schedule_interview` với slot không hợp lệ và slot trùng.
- Kiểm tra lọc lịch theo ngày hoặc khoảng ngày.
- Kiểm tra email, lý do từ chối và các tham số rỗng.
- Kiểm tra Agent dừng chính xác tại `MAX_ITERATIONS`.
- Chạy integration test riêng cho provider API khi có API key.
