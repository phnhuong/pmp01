import os
# Import các module cốt lõi từ kiến trúc ADK
from adk.agent import LLMAgent
from adk.runner import Runner
from adk.models import GeminiModel

# 1. Cấu hình API Key (Nếu bạn chưa set ở môi trường terminal)
# os.environ["GEMINI_API_KEY"] = "MÃ_API_CỦA_BẠN_Ở_ĐÂY"

def main():
    print("Đang khởi tạo hệ thống ADK...")

    # 2. Khởi tạo Model (Bộ não ngôn ngữ)
    # Ở đây chúng ta dùng Gemini, bạn có thể thay bằng ClaudeModel nếu muốn
    llm_model = GeminiModel(model_name="gemini-2.5-pro")

    # 3. Khởi tạo Agent (Tác tử) với System Instruction
    # Đây là lúc chúng ta định hình "tính cách" và "chuyên môn" cho Agent
    tutor_agent = LLMAgent(
        name="OOP_Tutor",
        model=llm_model,
        system_instruction="""Bạn là một chuyên gia lập trình nhiệt tình. 
        Nhiệm vụ của bạn là giải thích các khái niệm lập trình một cách ngắn gọn, 
        dễ hiểu và luôn kèm theo một ví dụ thực tế nhỏ."""
    )

    # 4. Khởi tạo Runner (Động cơ thực thi)
    # Runner sẽ chịu trách nhiệm điều phối luồng vào/ra cho Agent
    runner = Runner(agent=tutor_agent)

    # 5. Gửi yêu cầu và nhận kết quả
    user_query = "Chào bạn, hãy giải thích cho tôi khái niệm OOP là gì nhé."
    print(f"\n[Người dùng]: {user_query}")
    print("[Agent đang suy nghĩ...]\n")

    # Hàm run() sẽ xử lý toàn bộ quá trình gửi câu hỏi đến LLM và trả về kết quả
    response = runner.run(user_query)

    # In kết quả cuối cùng ra màn hình
    print(f"[Agent OOP_Tutor]:\n{response.text}")

if __name__ == "__main__":
    main()