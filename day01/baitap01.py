import os
from pathlib import Path
try:
    # Try to auto-load .env from project root if python-dotenv is installed
    from dotenv import load_dotenv
    project_root = Path(__file__).resolve().parent.parent
    dotenv_path = project_root / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
except Exception:
    # `python-dotenv` not installed; fall back to a simple .env parser
    try:
        project_root = Path(__file__).resolve().parent.parent
        dotenv_path = project_root / ".env"
        if dotenv_path.exists():
            with open(dotenv_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        os.environ.setdefault(k, v)
    except Exception:
        # If fallback fails, continue and rely on environment variables
        pass
# Import các module chính thức từ Google ADK
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.models import Gemini
from google.adk.sessions import InMemorySessionService
from google.genai import types

# 1. Cấu hình API Key (Nếu bạn chưa set ở môi trường terminal)
# os.environ["GEMINI_API_KEY"] = "MÃ_API_CỦA_BẠN_Ở_ĐÂY"

def main():
    print("Đang khởi tạo hệ thống ADK...")
    # Kiểm tra API key cho Gemini/Google GenAI
    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        print("\nLỗi: chưa cấu hình API key cho Google GenAI.")
        print("Thiết lập biến môi trường GEMINI_API_KEY hoặc GOOGLE_API_KEY rồi chạy lại.")
        print("Ví dụ (bash): export GEMINI_API_KEY=\"MÃ_API_CỦA_BẠN\"")
        return

    # 2. Khởi tạo Model (Bộ não ngôn ngữ)
    # Use a model with available quota for more testing capacity
    llm_model = Gemini(model="gemini-2.5-flash-lite")

    # 3. Khởi tạo Agent với instruction (ADK sử dụng pydantic models)
    tutor_agent = LlmAgent(
        name="OOP_Tutor",
        model=llm_model,
        instruction=(
            "Bạn là một chuyên gia lập trình nhiệt tình. "
            "Nhiệm vụ của bạn là giải thích các khái niệm lập trình một cách ngắn gọn, "
            "dễ hiểu và luôn kèm theo một ví dụ thực tế nhỏ."
        ),
    )

    # 4. Khởi tạo Runner với InMemory session service (dùng cho development)
    session_service = InMemorySessionService()
    runner = Runner(app_name="pmp01", agent=tutor_agent, session_service=session_service, auto_create_session=True)

    # 5. Gửi yêu cầu và nhận kết quả (Runner.run trả về generator các Event)
    user_query = "Chào bạn, hãy giải thích cho tôi khái niệm OOP là gì nhé."
    print(f"\n[Người dùng]: {user_query}")
    print("[Agent đang suy nghĩ...]\n")

    content = types.Content(role='user', parts=[types.Part(text=user_query)])
    events = runner.run(user_id="user", session_id="default", new_message=content)

    # Gom text từ các event trả về
    final_text = ""
    for ev in events:
        if getattr(ev, 'content', None) and ev.content.parts:
            for part in ev.content.parts:
                if getattr(part, 'text', None):
                    final_text += part.text

    print(f"[Agent OOP_Tutor]:\n{final_text}")

if __name__ == "__main__":
    main()