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
| *TỔNG ĐIỂM FIT* | *20/20* | *KẾT LUẬN: BÀI TOÁN HOÀN HẢO CHO AGENTIC ARCHITECTURE |

---

## 🔍 2. SO SÁNH PHẢN HỒI (TEST CASE #3)

**Câu hỏi:** *"Hãy so sánh: Ứng viên CD-001 có phù hợp với công việc
JOB-2024-001 (Python Developer) không?"*

### 🤖 Chatbot Baseline

**Phản hồi:** *"Để tiến hành so sánh ứng viên CD-001 với công việc
JOB-2024-001 (Python Developer), tôi sẽ cần lấy thông tin mô tả công việc
trước. Xin vui lòng chờ tôi một chút trong khi tôi lấy thông tin này."*

**Nhận xét:** Chatbot chỉ mô tả ý định tra cứu nhưng không thực sự gọi công
cụ, không lấy được hồ sơ, JD hoặc điểm phù hợp. Vì vậy, yêu cầu của người
dùng chưa được giải quyết.

### 🧠 ReAct Agent

**Thought 1:** Cần lấy hồ sơ của ứng viên CD-001.

**Action 1:** `get_candidate_profile["CD-001"]`

**Observation 1:** CD-001 có 4 năm kinh nghiệm Python, 2 năm Django,
1 năm PostgreSQL; có các kỹ năng Python, Django, PostgreSQL, REST API,
Docker và Linux.

**Thought 2:** Cần lấy yêu cầu chính thức của JOB-2024-001 để đối chiếu.

**Action 2:** `get_job_description["JOB-2024-001"]`

**Observation 2:** Vị trí Python Developer yêu cầu 3+ năm kinh nghiệm
Python, Django, PostgreSQL và các kỹ năng REST API, Docker; mức lương
18–25 triệu VNĐ.

**Thought 3:** Đã có hồ sơ và JD, cần dùng công cụ đánh giá mức độ phù hợp.

**Action 3:** `evaluate_candidate_fit["CD-001", "JOB-2024-001"]`

**Observation 3:** Ứng viên đạt 9/10 — RẤT PHÙ HỢP; kinh nghiệm đầy đủ,
kỹ năng khớp 95% và học vấn phù hợp.

**Final Answer:** *"Ứng viên CD-001 rất phù hợp với công việc JOB-2024-001,
với điểm đánh giá 9/10."*

**Nhận xét:** ReAct Agent hoàn thành yêu cầu nhờ kết hợp suy luận tuần tự với
ba công cụ. Kết luận cuối cùng có thể kiểm chứng từ các Observation và không
dựa trên dữ liệu tự suy đoán.

---

## 3. Môi trường và nguồn bằng chứng

Kết quả trong báo cáo này được cập nhật từ log chạy thực tế do nhóm cung cấp:

- Provider: `OpenAIProvider`
- Model: `gpt-4o-mini`
- Số test case: 10
- Guardrail: `MAX_ITERATIONS = 5`
- Tool registry: `AVAILABLE_TOOLS` trong `src/tools.py`
- Đặc tả test: `config/test_cases.json`

Đây là lần chạy có request tới model OpenAI, không phải trace sinh bởi
`MockProvider` hoặc planner offline. Vì output của LLM có tính không xác định,
kết quả có thể thay đổi giữa các lần chạy.

## 4. Test case và ground truth được tạo như thế nào?

Các test case được nhóm thiết kế thủ công từ những luồng nghiệp vụ tuyển dụng
cần kiểm tra. Mỗi phần tử trong `config/test_cases.json` gồm:

- `question`: câu hỏi đầu vào.
- `expected_behavior`: chuỗi hành động mong đợi.
- `tools_used`: các tool dự kiến phải được gọi.
- `success_criteria`: dữ liệu và kết quả cần đạt.
- `trap_reason`: mục tiêu của câu bẫy, nếu có.

Ground truth của bài lab là mock data trong `src/tools.py`:

| Dữ liệu | Nguồn |
|---|---|
| Công việc, kỹ năng, lương | `JOB_DESCRIPTIONS` |
| Hồ sơ ứng viên | `CANDIDATES` |
| Người phỏng vấn và slot trống | `INTERVIEWERS` |
| Điểm phù hợp | `evaluations` trong `evaluate_candidate_fit()` |
| Bảng xếp hạng | `rankings` trong `rank_candidates()` |

Ví dụ, `CD-001` được kỳ vọng đạt `9/10` với `JOB-2024-001` vì cặp này
được khai báo trực tiếp trong `evaluations`. `CD-999` được xem là ID không hợp
lệ vì không tồn tại trong `CANDIDATES`.

“Đúng” trong báo cáo có nghĩa là output nhất quán với mock data và workflow
được mô tả trong test case; không có nghĩa là dữ liệu đã được xác minh với một
hệ thống HR thật.

## 5. Quy tắc đánh giá

- **Đạt:** gọi đủ tool cần thiết, đúng thứ tự nghiệp vụ, Observation khớp mock
  data và Final Answer phản ánh đúng kết quả.
- **Đạt một phần:** kết quả chính hợp lý hoặc guardrail hoạt động, nhưng thiếu
  tool, sai thứ tự hoặc không khớp hoàn toàn `tools_used`.
- **Không đạt:** chưa hoàn thành yêu cầu, tuyên bố hành động đã làm khi tool
  chưa thực thi, gọi tool bằng placeholder hoặc bỏ qua guardrail quan trọng.

---

## 6. Tổng hợp kết quả 10 test case

| TC | Mục tiêu | Tool thực tế | Kết quả | Nhận xét |
|:---:|---|---|:---:|---|
| 1 | Đọc JD | `get_job_description` | ✅ Đạt | Trả đúng yêu cầu, kỹ năng và mức lương. |
| 2 | Đọc hồ sơ | `get_candidate_profile` | ✅ Đạt | Hồ sơ `CD-001` khớp mock data. |
| 3 | So sánh ứng viên–JD | `get_candidate_profile` → `get_job_description` → `evaluate_candidate_fit` | ✅ Đạt | Đúng thứ tự và kết luận `9/10`. |
| 4 | Kiểm tra lịch, tạo lịch, gửi email | `check_interviewer_availability` | ❌ Không đạt | Agent nói “sẽ hẹn” nhưng không gọi `schedule_interview` và `send_email`. |
| 5 | Xếp hạng và mời top 2 | `rank_candidates` → hai lần `get_candidate_profile` → `check_interviewer_availability` | ❌ Không đạt | Gọi tool bằng placeholder `interviewer_id`, nhận lỗi và không gửi lời mời. |
| 6 | Đánh giá, kiểm tra lịch, đặt lịch, gửi email | `get_candidate_profile` → `evaluate_candidate_fit` → `schedule_interview` → `send_email` | ⚠️ Đạt một phần | Hoàn tất lịch và email nhưng bỏ qua `check_interviewer_availability`; email được LLM tự tạo, không có trong hồ sơ. |
| 7 | ID ứng viên không tồn tại | `get_candidate_profile` | ⚠️ Đạt một phần | Guardrail dừng đúng sau lỗi, nhưng khác tool kỳ vọng `evaluate_candidate_fit`. |
| 8 | ID công việc không tồn tại | `rank_candidates` | ✅ Đạt | Dừng đúng sau Observation lỗi. |
| 9 | Slot không khả dụng | `check_interviewer_availability` | ✅ Đạt | Không tạo lịch và đề nghị chọn slot khác. |
| 10 | Từ chối ứng viên đã nhận việc khác | `reject_candidate` | ✅ Đạt | Lý do hợp lý; tool xác nhận email đã tự động gửi. |

**Tổng hợp:** 6 đạt, 2 đạt một phần, 2 không đạt.

---

## 7. Trace các trường hợp cần cải thiện

### Test case 4 — Tuyên bố hành động nhưng chưa thực thi

```text
Action: check_interviewer_availability["INT-001", "2024-12-20"]
Observation: Có slot 2024-12-20 09:00.

Final Answer: Tôi sẽ hẹn phỏng vấn ứng viên CD-001 với Trần Hải
vào lúc 09:00 ngày 20/12/2024.
```

**Đánh giá:** không đạt. Log không có:

```text
Action: schedule_interview[...]
Action: send_email[...]
```

Do đó Final Answer chỉ là lời hứa, không phải xác nhận hành động đã hoàn thành.

### Test case 5 — LLM dùng placeholder làm tham số thật

```text
Action: check_interviewer_availability["interviewer_id", "date_range"]
Observation: ❌ LỖI: Người phỏng vấn 'interviewer_id' không tồn tại.
```

**Đánh giá:** không đạt yêu cầu mời hai ứng viên hàng đầu. Guardrail đã làm
đúng nhiệm vụ là dừng sau lỗi, nhưng LLM đáng lẽ phải hỏi người dùng bổ sung
interviewer và thời gian, không được gọi tool bằng placeholder.

### Test case 6 — Bỏ qua bước kiểm tra lịch

```text
Action: evaluate_candidate_fit["CD-003", "JOB-2024-003"]
Observation: 8/10 — PHÁT TRIỂN.

Action: schedule_interview["CD-003", "INT-002", "2024-12-19 13:00"]
Observation: Đã tạo lịch phỏng vấn.

Action: send_email["leminhc@example.com", ...]
Observation: Email được gửi thành công.
```

**Đánh giá:** đạt một phần. Agent hoàn tất yêu cầu, nhưng không gọi
`check_interviewer_availability` trước `schedule_interview` như workflow và
`tools_used` yêu cầu. Địa chỉ `leminhc@example.com` cũng không xuất hiện trong
`CANDIDATES`, vì vậy đây là dữ liệu do LLM tự tạo.

### Test case 7 — Guardrail khi ứng viên không tồn tại

```text
Action: get_candidate_profile["CD-999"]
Observation: ❌ LỖI: Không tìm thấy ứng viên 'CD-999'.

Final Answer: Tool báo lỗi nên Agent dừng lại để tránh thao tác sai dữ liệu.
```

**Đánh giá:** guardrail đạt vì không có tool nào được gọi sau lỗi. Tuy nhiên,
tool thực tế khác `evaluate_candidate_fit` trong đặc tả test nên case này chỉ
được đánh dấu đạt một phần khi chấm nghiêm theo `tools_used`.

### Test case 9 — Phanh xung đột lịch

```text
Action: check_interviewer_availability["INT-001", "2024-12-25"]
Observation: Chỉ có các slot từ 2024-12-20 đến 2024-12-23.

Final Answer: Lịch phỏng vấn 2024-12-25 15:00 không có sẵn.
Bạn có muốn chọn một khoảng thời gian khác không?
```

**Đánh giá:** đạt về quyết định an toàn; `schedule_interview` và `send_email`
không được gọi.

---

## 8. Guardrail được xác nhận từ log

1. Observation chứa `LỖI` làm Agent dừng ngay ở test 5, 7 và 8.
2. Agent không tạo lịch khi nhận thấy slot không khả dụng ở test 9.
3. Action gọi tool không tồn tại hoặc tham số sai được chuyển thành chuỗi lỗi
   thay vì làm ứng dụng crash.
4. ReAct loop không chạy quá `MAX_ITERATIONS = 5`.

Guardrail chưa được xác nhận đầy đủ:

- Test 6 cho thấy LLM có thể gọi thẳng `schedule_interview` mà không kiểm tra
  lịch trước.
- `schedule_interview()` chưa tự kiểm tra slot có nằm trong
  `INTERVIEWERS[interviewer_id]["available_slots"]`.
- `check_interviewer_availability()` hiện hiển thị toàn bộ slot và chưa lọc
  đúng theo `date_range`.
- `send_email()` chấp nhận địa chỉ do LLM tự tạo mà không kiểm tra dữ liệu.

---

## 9. So sánh tổng quát giữa Baseline và ReAct

Trong log, Baseline Chatbot thường nói sẽ “tra cứu”, “kiểm tra” hoặc “thực
hiện xếp hạng”, nhưng không có Action và Observation. Vì vậy Baseline không
thực sự truy cập dữ liệu tool.

ReAct Agent tạo được trace kiểm chứng gồm `Thought → Action → Observation`,
nhưng vẫn có thể:

- Dừng quá sớm và chỉ hứa sẽ thực hiện hành động như test 4.
- Tự tạo placeholder hoặc dữ liệu chưa tồn tại như test 5 và test 6.
- Bỏ qua một bước bắt buộc trong workflow.

Điều này cho thấy ReAct có khả năng thực thi cao hơn Baseline, nhưng cần
guardrail ở cấp code thay vì chỉ dựa vào system prompt.

---

## 10. Kiểm thử tự động và giới hạn đánh giá

Unit test chạy bằng:

```powershell
python -m unittest discover -s tests -v
```

Kết quả gần nhất:

```text
Ran 5 tests in 0.002s
OK
```

Năm unit test dùng `MockProvider` hoặc `ScriptedProvider`; chúng không thay thế
integration test với OpenAI. Ngược lại, log OpenAI cung cấp bằng chứng
integration thực tế nhưng chưa được chấm bằng assertion tự động.

`run_demo()` hiện chỉ in `tools_used`; chưa ghi lại và tự so sánh tool thực tế
với tool kỳ vọng. Vì vậy việc chương trình chạy hết 10 case mà không crash
không đồng nghĩa cả 10 case đều đạt.

Các kiểm tra cần bổ sung:

- Ghi lại tool call thực tế và so sánh với `tools_used`.
- Tự động kiểm tra `success_criteria`.
- Cấm `schedule_interview` nếu chưa có Observation xác nhận slot.
- Cấm placeholder như `"interviewer_id"` và `"date_range"`.
- Xác minh email phải có trong dữ liệu ứng viên hoặc do người dùng cung cấp.
- Kiểm tra hành động có tác động thực chỉ được báo thành công sau Observation.
- Bổ sung test cho giới hạn `MAX_ITERATIONS` và luồng cần hơn năm bước.

---

## 11. Kết luận

Trace OpenAI cho thấy Agent xử lý tốt các yêu cầu đọc dữ liệu, đánh giá ứng
viên và các edge case ID không tồn tại hoặc lịch không khả dụng. Tuy nhiên,
luồng có tác động thực chưa ổn định: test 4 không tạo lịch, test 5 dùng
placeholder sai, và test 6 bỏ qua kiểm tra lịch đồng thời tự tạo email.

Kết quả Mốc 3 nên được ghi nhận là **đạt phần lõi ReAct và guardrail lỗi cơ
bản, nhưng chưa đạt hoàn toàn workflow scheduling/email**. Ưu tiên tiếp theo
là đưa các quy tắc bắt buộc vào code và tool validation, thay vì chỉ mô tả
trong prompt.
