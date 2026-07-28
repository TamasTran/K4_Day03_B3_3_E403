"""
Core Agent App - Role 4: tích hợp Tools + Prompts + Test Cases + Provider.

Ứng dụng này minh họa rõ khác biệt giữa:
- Baseline Chatbot: chỉ trả lời bằng LLM, không gọi tool.
- ReAct Agent: suy luận Thought -> Action -> Observation, gọi tool thật trong tools.py.
"""

import ast
import inspect
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from prompts import CHATBOT_BASELINE_PROMPT
from providers import get_llm_provider
from tools import AVAILABLE_TOOLS


load_dotenv()

try:
    from prompts import MAX_ITERATIONS
except ImportError:
    MAX_ITERATIONS = 3

try:
    from prompts import REACT_SYSTEM_PROMPT
except ImportError:
    REACT_SYSTEM_PROMPT = """Bạn là ReAct Agent cho bài toán tuyển dụng.
Hãy suy luận theo chuỗi Thought -> Action -> Observation.
Khi cần dùng dữ liệu thật, hãy gọi tool; khi đã đủ thông tin, trả lời Final Answer."""

Action = Tuple[str, List[Any]]


def load_test_cases() -> List[Dict[str, Any]]:
    """Đọc bộ test cases từ config/test_cases.json."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")

    if not os.path.exists(config_path):
        config_path = "test_cases.json"

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def print_box(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def build_tool_summary() -> str:
    """Tạo mô tả tool ngắn gọn từ AVAILABLE_TOOLS để đưa vào prompt."""
    lines = []
    for name, func in AVAILABLE_TOOLS.items():
        params = ", ".join(inspect.signature(func).parameters.keys())
        first_doc_line = (inspect.getdoc(func) or "").splitlines()[0]
        lines.append(f"- {name}[{params}]: {first_doc_line}")
    return "\n".join(lines)


def build_react_prompt(user_query: str, scratchpad: str = "") -> str:
    """Ghép input mỗi vòng ReAct; system prompt được truyền riêng cho provider."""
    return f"""
DANH SÁCH TOOL THỰC TẾ CỦA ỨNG DỤNG:
{build_tool_summary()}

YÊU CẦU:
- Chỉ gọi tool có trong danh sách trên.
- Mỗi vòng lặp chỉ đưa ra đúng 1 Action hoặc Final Answer.
- Dùng cú pháp: Action: tool_name["arg1", "arg2"]
- Nếu Observation báo lỗi, hãy dừng và trả lời lịch sự, không gọi bước tiếp theo.
- Không tự bịa dữ liệu hồ sơ, lịch phỏng vấn, điểm đánh giá hoặc email.

CÂU HỎI NGƯỜI DÙNG:
{user_query}

TRACE HIỆN TẠI:
{scratchpad}
""".strip()


def run_baseline_chatbot(user_query: str, provider) -> str:
    """Chạy chatbot baseline không có quyền gọi tool."""
    print(f"\n💬 [CHATBOT BASELINE] User: {user_query}")
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"🤖 Baseline Answer:\n{response}")
    return response


def _extract_ids(text: str, pattern: str) -> List[str]:
    return list(dict.fromkeys(re.findall(pattern, text, flags=re.IGNORECASE)))


def _extract_datetime(text: str) -> Optional[str]:
    match = re.search(r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}", text)
    return match.group(0) if match else None


def _extract_date(text: str) -> Optional[str]:
    match = re.search(r"\d{4}-\d{2}-\d{2}", text)
    return match.group(0) if match else None


def build_offline_plan(user_query: str) -> List[Action]:
    """
    Planner tối giản để demo ReAct ổn định khi dùng MockProvider/offline.
    Luật được viết theo bộ test cases trong config/test_cases.json.
    """
    q = user_query.lower()
    candidates = _extract_ids(user_query, r"CD-\d{3}")
    jobs = _extract_ids(user_query, r"JOB-\d{4}-\d{3}")
    interviewers = _extract_ids(user_query, r"INT-\d{3}")
    dt = _extract_datetime(user_query)
    date = _extract_date(user_query)

    candidate_id = candidates[0].upper() if candidates else None
    job_id = jobs[0].upper() if jobs else None
    interviewer_id = interviewers[0].upper() if interviewers else None

    if "nhận lời" in q or "nhan loi" in q or "từ chối" in q or "tu choi" in q:
        return [
            (
                "reject_candidate",
                [
                    candidate_id or "CD-004",
                    "Ứng viên vừa nhận lời từ công ty khác",
                ],
            )
        ]

    if "xếp hạng" in q or "xep hang" in q:
        plan: List[Action] = [("rank_candidates", [job_id or "JOB-2024-001"])]
        if job_id == "JOB-2024-001" and ("2 ứng viên" in q or "2 ung vien" in q):
            plan.extend(
                [
                    ("schedule_interview", ["CD-004", "INT-001", "2024-12-20 09:00"]),
                    (
                        "send_email",
                        [
                            "CD-004",
                            "Mời phỏng vấn Python Developer",
                            "Bạn là một trong 2 ứng viên hàng đầu cho JOB-2024-001. Lịch phỏng vấn: 2024-12-20 09:00.",
                        ],
                    ),
                    ("schedule_interview", ["CD-001", "INT-001", "2024-12-20 14:00"]),
                    (
                        "send_email",
                        [
                            "CD-001",
                            "Mời phỏng vấn Python Developer",
                            "Bạn là một trong 2 ứng viên hàng đầu cho JOB-2024-001. Lịch phỏng vấn: 2024-12-20 14:00.",
                        ],
                    ),
                ]
            )
        return plan

    if ("hồ sơ" in q or "ho so" in q) and candidate_id and "phù hợp" not in q:
        return [("get_candidate_profile", [candidate_id])]

    if (
        ("công việc" in q or "cong viec" in q or "yêu cầu" in q or "yeu cau" in q)
        and job_id
        and not any(word in q for word in ["so sánh", "so sanh", "phù hợp", "phu hop"])
    ):
        return [("get_job_description", [job_id])]

    schedule_intent = any(
        phrase in q
        for phrase in ["hẹn", "hen ", "tạo lịch", "tao lich", "lên lịch", "len lich"]
    )
    explicit_evaluation_request = any(word in q for word in ["đánh giá", "danh gia", "so sánh", "so sanh"])

    if schedule_intent and not explicit_evaluation_request:
        check_range = dt or ("2024-12-20 to 2024-12-25" if date == "2024-12-20" else (date or "2024-12-20"))
        return [
            ("check_interviewer_availability", [interviewer_id or "INT-001", check_range]),
            ("schedule_interview", [candidate_id or "CD-001", interviewer_id or "INT-001", dt or "2024-12-20 09:00"]),
            (
                "send_email",
                [
                    candidate_id or "CD-001",
                    "Xác nhận lịch phỏng vấn",
                    f"Lịch phỏng vấn đã được tạo vào {dt or '2024-12-20 09:00'}.",
                ],
            ),
        ]

    if any(word in q for word in ["đánh giá", "danh gia", "phù hợp", "phu hop", "so sánh", "so sanh"]):
        if candidate_id == "CD-999":
            return [("evaluate_candidate_fit", [candidate_id, job_id or "JOB-2024-001"])]

        plan = []
        if "so sánh" in q or "so sanh" in q:
            plan.extend(
                [
                    ("get_candidate_profile", [candidate_id or "CD-001"]),
                    ("get_job_description", [job_id or "JOB-2024-001"]),
                ]
            )
        plan.append(("evaluate_candidate_fit", [candidate_id or "CD-001", job_id or "JOB-2024-001"]))

        if "hẹn phỏng vấn" in q or "hen phong van" in q:
            plan.extend(
                [
                    ("check_interviewer_availability", [interviewer_id or "INT-002", dt or date or "2024-12-19"]),
                    ("schedule_interview", [candidate_id or "CD-003", interviewer_id or "INT-002", dt or "2024-12-19 13:00"]),
                    (
                        "send_email",
                        [
                            candidate_id or "CD-003",
                            "Xác nhận lịch phỏng vấn",
                            f"Lịch phỏng vấn đã được xác nhận vào {dt or '2024-12-19 13:00'}.",
                        ],
                    ),
                ]
            )
        return plan

    if schedule_intent:
        check_range = dt or ("2024-12-20 to 2024-12-25" if date == "2024-12-20" else (date or "2024-12-20"))
        return [
            ("check_interviewer_availability", [interviewer_id or "INT-001", check_range]),
            ("schedule_interview", [candidate_id or "CD-001", interviewer_id or "INT-001", dt or "2024-12-20 09:00"]),
            (
                "send_email",
                [
                    candidate_id or "CD-001",
                    "Xác nhận lịch phỏng vấn",
                    f"Lịch phỏng vấn đã được tạo vào {dt or '2024-12-20 09:00'}.",
                ],
            ),
        ]

    return []


def parse_action(llm_output: str) -> Optional[Action]:
    """Parse Action từ output dạng tool['a'] hoặc tool['a', 'b']."""
    match = re.search(
        r"Action\s*:\s*([a-zA-Z_][\w]*)\s*(?:\[([^\r\n]*)\]|\(([^\r\n]*)\))",
        llm_output,
    )
    if not match:
        return None

    tool_name = match.group(1)
    raw_args = (match.group(2) if match.group(2) is not None else match.group(3)).strip()

    try:
        parsed = ast.literal_eval(f"[{raw_args}]")
    except Exception:
        parsed = [raw_args.strip().strip("\"'")]

    return tool_name, parsed


def is_tool_error(observation: str) -> bool:
    """Nhận diện lỗi thật từ tool, tránh nhầm icon ❌ trong trạng thái nghiệp vụ."""
    return "LỖI" in observation.upper()


def execute_tool(tool_name: str, args: List[Any]) -> Tuple[str, bool]:
    """Gọi tool an toàn, trả về (observation, has_error)."""
    if tool_name not in AVAILABLE_TOOLS:
        valid_tools = ", ".join(AVAILABLE_TOOLS.keys())
        return f"❌ LỖI: Tool '{tool_name}' không tồn tại. Tool hợp lệ: {valid_tools}", True

    tool = AVAILABLE_TOOLS[tool_name]
    expected_params = list(inspect.signature(tool).parameters.keys())
    if len(args) != len(expected_params):
        return (
            f"❌ LỖI: Tool '{tool_name}' cần {len(expected_params)} tham số "
            f"({', '.join(expected_params)}), nhưng nhận {len(args)} tham số: {args}",
            True,
        )

    try:
        observation = tool(*args)
    except Exception as exc:
        return f"❌ LỖI khi chạy tool '{tool_name}': {exc}", True

    has_error = is_tool_error(observation)
    return observation, has_error


def should_stop_after_observation(tool_name: str, observation: str, requested_args: List[Any]) -> Optional[str]:
    """Guardrail nghiệp vụ: dừng khi tool báo lỗi hoặc lịch yêu cầu không khả dụng."""
    if is_tool_error(observation):
        return "Tool báo lỗi nên Agent dừng lại để tránh thao tác sai dữ liệu."

    if tool_name == "check_interviewer_availability" and len(requested_args) >= 2:
        requested_range = str(requested_args[1])
        requested_time = requested_range if re.search(r"\d{2}:\d{2}", requested_range) else None
        available_slots = re.findall(r"•\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})", observation)
        if requested_time and available_slots and requested_time not in available_slots:
            return "Slot yêu cầu không có trong lịch trống nên Agent không tạo lịch phỏng vấn."

    return None


def make_final_answer(user_query: str, observations: List[str], stop_reason: Optional[str] = None) -> str:
    """Tổng hợp câu trả lời cuối cùng từ observation của tools."""
    if stop_reason:
        return f"{stop_reason}\n\nThông tin đã kiểm tra:\n" + "\n\n".join(observations)

    if not observations:
        return (
            "Tôi chưa xác định được tool phù hợp cho yêu cầu này. "
            "Bạn có thể cung cấp mã ứng viên (CD-xxx), mã công việc (JOB-xxxx-xxx) hoặc mã interviewer (INT-xxx)."
        )

    return "Đã hoàn thành yêu cầu. Kết quả:\n\n" + "\n\n".join(observations)


def run_react_agent(
    user_query: str,
    provider,
    prefer_llm_actions: Optional[bool] = None,
) -> str:
    """
    Chạy ReAct Agent có guardrail.

    Provider thật (OpenAI/Gemini/Anthropic/OpenRouter) luôn tự sinh Thought và
    Action. Planner xác định chỉ được dùng cho MockProvider để chạy demo offline.
    """
    print(f"\n🧠 [REACT AGENT] User: {user_query}")

    is_mock_provider = provider.__class__.__name__ == "MockProvider"
    if prefer_llm_actions is None:
        use_llm_actions = not is_mock_provider
    else:
        use_llm_actions = prefer_llm_actions

    offline_plan = build_offline_plan(user_query)
    observations: List[str] = []
    scratchpad = ""
    stop_reason: Optional[str] = None

    # MAX_ITERATIONS là giới hạn cứng cho cả planner offline lẫn LLM planner.
    max_steps = MAX_ITERATIONS if use_llm_actions else min(
        MAX_ITERATIONS, max(1, len(offline_plan))
    )
    guardrail_triggered = False

    for step in range(1, max_steps + 1):
        print(f"\n--- 🔄 ReAct Step {step}/{max_steps} ---")

        action: Optional[Action] = None
        if use_llm_actions:
            llm_output = provider.generate(
                build_react_prompt(user_query, scratchpad),
                system_prompt=REACT_SYSTEM_PROMPT,
            )
            print(llm_output)
            if "Final Answer:" in llm_output:
                final = llm_output.split("Final Answer:", 1)[1].strip()
                print(f"\n🏁 Final Answer:\n{final}")
                return final
            action = parse_action(llm_output)

        if not use_llm_actions and action is None and step <= len(offline_plan):
            action = offline_plan[step - 1]
            print(f"Thought: Chọn tool phù hợp cho bước {step} dựa trên yêu cầu và dữ liệu đã có.")
            print(f"Action: {action[0]}{action[1]}")

        if action is None:
            if use_llm_actions:
                stop_reason = (
                    "Provider không trả về Action hoặc Final Answer đúng định dạng; "
                    "Agent dừng để tránh thực thi hành động không xác định."
                )
            break

        tool_name, args = action
        observation, has_error = execute_tool(tool_name, args)
        observations.append(observation)
        print(f"Observation:\n{observation}")

        scratchpad += f"\nAction: {tool_name}{args}\nObservation: {observation}\n"

        stop_reason = should_stop_after_observation(tool_name, observation, args)
        if has_error or stop_reason:
            break

        if step == MAX_ITERATIONS:
            has_remaining_work = use_llm_actions or step < len(offline_plan)
            if has_remaining_work:
                guardrail_triggered = True
                stop_reason = (
                    f"Guardrail đã dừng Agent sau {MAX_ITERATIONS} vòng lặp "
                    "để tránh chạy quá giới hạn an toàn."
                )

    if guardrail_triggered:
        print(f"\n🛡️ GUARDRAIL TRIGGERED: {stop_reason}")

    final_answer = make_final_answer(user_query, observations, stop_reason)
    print(f"\n🏁 Final Answer:\n{final_answer}")
    return final_answer


def run_demo(test_cases: List[Dict[str, Any]], provider) -> None:
    """Chạy demo trên toàn bộ test cases để Role 5 lấy trace log."""
    for test in test_cases:
        print_box(f"TEST CASE #{test.get('id')}: {test.get('category')}")
        print(f"🎯 Expected Tools: {', '.join(test.get('tools_used', []))}")
        print(f"❓ Question: {test.get('question')}")

        run_baseline_chatbot(test["question"], provider)
        run_react_agent(test["question"], provider)


def run_interactive(provider) -> None:
    """Chế độ nhập câu hỏi thủ công."""
    print("\nNhập câu hỏi tuyển dụng của bạn. Gõ 'exit' để thoát.")
    while True:
        user_query = input("\nUser> ").strip()
        if user_query.lower() in {"exit", "quit", "q"}:
            break
        run_react_agent(user_query, provider)


if __name__ == "__main__":
    print_box("🏫 ĐẠI HỌC VINUNI - LAB 3: CHATBOT VS REACT AGENT")

    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider: {provider.__class__.__name__} (Model: {model_name})")
    print(f"🛠️ Tools loaded: {', '.join(AVAILABLE_TOOLS.keys())}")

    tests = load_test_cases()
    print(f"✅ Đã tải {len(tests)} test cases từ config/test_cases.json")

    selected = os.getenv("TEST_CASE_ID")
    if selected:
        selected_tests = [t for t in tests if str(t.get("id")) == selected]
        if not selected_tests:
            print(f"❌ Không tìm thấy TEST_CASE_ID={selected}")
            sys.exit(1)
        run_demo(selected_tests, provider)
    elif os.getenv("INTERACTIVE", "0") == "1":
        run_interactive(provider)
    else:
        run_demo(tests, provider)
