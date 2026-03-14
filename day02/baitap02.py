import os
from adk.agent import LLMAgent
from adk.runner import Runner
from adk.models import GeminiModel
# Import thêm module Session để quản lý trạng thái
from adk.session import Session

def main():
    print("Đang khởi tạo Hệ thống ADK với bộ nhớ (Session)...")

    # 1. Khởi tạo Model
    llm_model = GeminiModel(model_name="gemini-2.5-pro")

    # 2. Khởi tạo Agent
    chat_agent = LLMAgent(
        name="Memory_Assistant",
        model=llm_model,
        system_instruction="Bạn là một người bạn trò chuyện thân thiện và chu đáo. Bạn có trí nhớ rất tốt và luôn nhớ các chi tiết mà người dùng đã chia sẻ trước đó trong cuộc trò chuyện."
    )

    # 3. Khởi tạo Session (Phiên làm việc)
    # Việc gán session_id giúp ADK biết cách gom nhóm các tin nhắn thuộc về cùng một người dùng/ngữ cảnh.
    user_session = Session(session_id="peter_workspace_01")

    # 4. Khởi tạo Runner và gắn Session vào
    # Từ giờ, mọi tin nhắn đi qua Runner này sẽ được tự động lưu vào user_session
    runner = Runner(agent=chat_agent, session=user_session)

    print("\n--- Bắt đầu trò chuyện (Gõ 'thoát' hoặc 'quit' để dừng) ---")
    
    # 5. Thiết lập vòng lặp hội thoại (Chat loop)
    while True:
        user_input = input("\n[Bạn]: ")
        
        # Bắt sự kiện thoát vòng lặp
        if user_input.lower() in ['thoát', 'quit', 'exit']:
            print("Kết thúc phiên làm việc. Tạm biệt!")
            break
            
        # Bỏ qua nếu người dùng không nhập gì mà nhấn Enter
        if not user_input.strip():
            continue

        print("[Agent đang suy nghĩ...]")
        
        # Gửi tin nhắn qua Runner. Nhờ có Session, Runner sẽ tự động 
        # tải lịch sử chat cũ nạp vào Prompt trước khi gửi cho LLM.
        response = runner.run(user_input)
        
        print(f"[Memory_Assistant]: {response.text}")

if __name__ == "__main__":
    main()