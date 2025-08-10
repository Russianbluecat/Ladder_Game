# app.py - Hugging Face Spaces 배포용 사다리 게임
import gradio as gr
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import io
import base64
from PIL import Image

# matplotlib 한글 폰트 설정 (한글 깨짐 방지)
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = ['DejaVu Sans']

# 사다리 게임 메인 클래스
class LadderGame:
    def __init__(self, player_count, results_str):
        """
        사다리 게임 초기화
        
        Args:
            player_count (int): 참가자 수 (2-10명)
            results_str (str): 결과 문자열 (쉼표로 구분)
        """
        self.player_count = player_count
        self.players = []
        
        # user1, user2, ... 형식으로 참가자 이름 자동 생성
        for i in range(1, player_count + 1):
            self.players.append(f"user{i}")
        
        # 입력받은 결과 문자열을 파싱하여 리스트로 변환
        self.results = self.parse_results(results_str, player_count)
        
        self.num_players = len(self.players)
        self.ladder_height = 10
        self.horizontal_lines = []
        
    def parse_results(self, results_str, expected_count):
        """
        결과 문자열을 파싱하여 리스트로 변환
        """
        if not results_str or results_str.strip() == "":
            return ['(Empty)'] * expected_count
        
        parts = results_str.split(',')
        results = []
        
        for part in parts:
            trimmed = part.strip()
            if trimmed == '':
                results.append('(Empty)')
            else:
                results.append(trimmed)
        
        # 결과 개수 조정
        while len(results) < expected_count:
            results.append('(Empty)')
            
        if len(results) > expected_count:
            results = results[:expected_count]
        
        return results
        
    def generate_ladder(self):
        """
        사다리의 가로선들을 랜덤하게 생성
        """
        self.horizontal_lines = []
        
        for level in range(1, self.ladder_height):
            for pos in range(self.num_players - 1):
                if random.random() < 0.3:
                    adjacent_exists = any(
                        line['level'] == level and abs(line['position'] - pos) <= 1
                        for line in self.horizontal_lines
                    )
                    if not adjacent_exists:
                        self.horizontal_lines.append({
                            'level': level,
                            'position': pos
                        })
    
    def trace_path(self, start_position):
        """
        특정 시작 위치에서 사다리를 따라 내려가는 경로를 추적
        """
        current_pos = start_position
        path = [(0, current_pos)]
        
        for level in range(1, self.ladder_height + 1):
            for line in self.horizontal_lines:
                if line['level'] == level:
                    if line['position'] == current_pos:
                        current_pos += 1
                        break
                    elif line['position'] == current_pos - 1:
                        current_pos -= 1
                        break
            
            path.append((level, current_pos))
        
        return path
    
    def play_game(self):
        """
        사다리 게임을 실행하고 결과를 반환
        """
        self.generate_ladder()
        
        game_results = {}
        all_paths = {}
        
        for i, player in enumerate(self.players):
            path = self.trace_path(i)
            final_position = path[-1][1]
            result = self.results[final_position]
            
            game_results[player] = result
            all_paths[player] = path
            
        return game_results, all_paths
    
    def create_visualization(self, game_results, all_paths):
        """
        사다리 게임 결과를 시각화하여 PIL Image 객체로 반환
        """
        fig, ax = plt.subplots(1, 1, figsize=(15.6, 4.8))
        
        # 세로선 그리기
        for i in range(self.num_players):
            ax.plot([i, i], [self.ladder_height, 0], 'k-', linewidth=2)
        
        # 가로선 그리기
        for line in self.horizontal_lines:
            level = self.ladder_height - line['level']
            pos = line['position']
            ax.plot([pos, pos + 1], [level, level], 'k-', linewidth=3)
        
        # 참가자 이름 표시
        for i, player in enumerate(self.players):
            ax.text(i, self.ladder_height + 0.7, player, 
                   ha='center', va='center',
                   fontsize=12, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        
        # 결과 표시
        for i, result in enumerate(self.results):
            display_result = result if result != '(Empty)' else 'Empty'
            color = 'lightgray' if result == '(Empty)' else 'lightcoral'
            ax.text(i, -0.7, display_result, 
                   ha='center', va='center',
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor=color))
        
        # 각 참가자의 경로 표시
        colors = ['red', 'blue', 'green', 'orange', 'purple', 
                 'brown', 'pink', 'gray', 'cyan', 'magenta']
        
        for idx, player in enumerate(self.players):
            path = all_paths[player]
            color = colors[idx % len(colors)]
            
            x_coords = [point[1] for point in path]
            y_coords = [self.ladder_height - point[0] for point in path]
            
            ax.plot(x_coords, y_coords, 
                   color=color, linewidth=4, alpha=0.8, label=player)
            
            ax.scatter(x_coords[0], y_coords[0], 
                      color=color, s=100, marker='o', alpha=0.8)
            
            ax.scatter(x_coords[-1], y_coords[-1], 
                      color=color, s=100, marker='s', alpha=0.8)
        
        # 그래프 설정
        ax.set_xlim(-1, self.num_players)
        ax.set_ylim(-1.5, self.ladder_height + 1.5)
        ax.set_title("🎮 Ladder Game Results", fontsize=16, fontweight='bold')
        
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        legend = ax.legend(
            loc='center left',
            bbox_to_anchor=(1.05, 0.5),
            fontsize=10,
            frameon=True,
            fancybox=True,
            shadow=True
        )
        legend.get_frame().set_alpha(0.9)
        
        plt.tight_layout()
        
        # 이미지를 메모리 버퍼에 저장
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buf.seek(0)
        plt.close()
        
        return Image.open(buf)

# 결과 입력을 관리하는 함수들
def add_result_to_list(new_input, current_results, results_state, player_count):
    """
    새로운 입력을 결과 리스트에 추가하는 함수 (엔터 키로 트리거)
    """
    max_count = int(player_count)
    
    if len(results_state) >= max_count:
        return "", current_results, results_state, f"⚠️ 이미 {max_count}개가 모두 입력되었습니다!"
    
    # 새 결과 추가
    if new_input.strip() == "":
        results_state.append("(Empty)")
        added_text = "(Empty)"
    else:
        results_state.append(new_input.strip())
        added_text = new_input.strip()
    
    # 결과 문자열 업데이트
    if current_results.strip() == "":
        updated_results = added_text
    else:
        updated_results = current_results + ", " + added_text
    
    # 상태 메시지 생성
    remaining = max_count - len(results_state)
    if remaining > 0:
        status_msg = f"✅ '{added_text}' 추가! 남은 개수: {remaining}"
    else:
        status_msg = f"🎉 모든 {max_count}개 결과 입력 완료!"
    
    return "", updated_results, results_state, status_msg

def clear_all_results():
    """
    모든 결과를 초기화하는 함수
    """
    return "", "", [], "🗑️ 모든 결과가 초기화되었습니다!"

def run_ladder_game_with_state(player_count, results_state):
    """
    상태 기반 사다리 게임 실행 함수
    """
    try:
        if not results_state or len(results_state) == 0:
            return None, "❌ 결과를 먼저 입력해주세요!"
        
        results_str = ", ".join(results_state)
        
        game = LadderGame(int(player_count), results_str)
        game_results, all_paths = game.play_game()
        
        img = game.create_visualization(game_results, all_paths)
        
        result_text = "🎊 **Game Results:**\n" + "**" + "-" * 30 + "**\n"
        for player in game.players:
            result = game_results[player]
            display_result = result if result != '(Empty)' else 'Empty'
            result_text += f"**{player} ➡️ {display_result}**\n"
        
        return img, result_text
        
    except Exception as e:
        return None, f"❌ Error occurred: {str(e)}"

def create_interface():
    """
    Gradio Blocks를 사용하여 실시간 입력 사다리 게임 인터페이스 생성
    """
    with gr.Blocks(
        title="🎮 Interactive Ladder Game", 
        theme=gr.themes.Soft(),
        css="""
        #result_text textarea {
            font-size: 16px !important;
            font-weight: bold !important;
            line-height: 1.4 !important;
        }
        #status_msg textarea {
            font-size: 14px !important;
            font-weight: bold !important;
        }
        """
    ) as demo:
        
        # 상태 관리를 위한 변수
        results_state = gr.State([])
        
        # 상단 제목 및 설명
        gr.Markdown("""
        # 🎮 Interactive Ladder Game
        
        Real-time input mode: Enter results one by one and see them accumulate!
        
        ### 📝 How to use:
        1. **Number of participants**: Select 2-10 people
        2. **Add results**: Type each result and press **Enter** to add
        3. **Empty result**: Just press Enter without typing to add empty space
        4. Click **Run Game** when all results are entered!
        
        ### 💡 Example flow:
        - Type "Winner" → Press Enter → "Winner" appears in results
        - Type "Loser" → Press Enter → "Winner, Loser" appears in results
        - Just press Enter → "Winner, Loser, (Empty)" appears in results
        """)
        
        # 메인 레이아웃
        with gr.Row():
            # 왼쪽: 입력 컨트롤
            with gr.Column(scale=1):
                # 참가자 수 선택
                player_count = gr.Slider(
                    minimum=2, maximum=10, step=1, value=4,
                    label="🧑‍🤝‍🧑 Number of Participants"
                )
                
                # 실시간 입력창
                input_box = gr.Textbox(
                    label="🎯 Enter Result (Press Enter to add)",
                    placeholder="Type a result and press Enter...",
                    lines=1
                )
                
                # 입력된 결과들 표시창
                results_display = gr.Textbox(
                    label="📝 Current Results",
                    lines=4,
                    interactive=False,
                    placeholder="Results will appear here as you add them..."
                )
                
                # 상태 메시지
                status_msg = gr.Textbox(
                    label="📢 Status",
                    lines=2,
                    interactive=False,
                    elem_id="status_msg",
                    value="Ready to input results!"
                )
                
                # 컨트롤 버튼들
                with gr.Row():
                    clear_btn = gr.Button("🗑️ Clear All", variant="secondary")
                    run_btn = gr.Button("🎲 Run Game!", variant="primary", size="lg")
            
            # 오른쪽: 결과 표시
            with gr.Column(scale=2):
                with gr.Row():
                    # 게임 결과 이미지
                    game_image = gr.Image(
                        label="🎨 Ladder Game Results",
                        type="pil",
                        height=350
                    )
                    
                    # 결과 텍스트
                    result_text = gr.Textbox(
                        label="📋 Game Results",
                        lines=12,
                        max_lines=15,
                        elem_id="result_text"
                    )
        
        # 빠른 예시 버튼들
        gr.Markdown("### 🎯 Quick Setup Examples:")
        with gr.Row():
            example1_btn = gr.Button("4P: Win/Lose", size="sm")
            example2_btn = gr.Button("5P: With Empty", size="sm")
            example3_btn = gr.Button("한글 예시", size="sm")
        
        # 이벤트 연결
        
        # 엔터 키 입력시 결과 추가
        input_box.submit(
            fn=add_result_to_list,
            inputs=[input_box, results_display, results_state, player_count],
            outputs=[input_box, results_display, results_state, status_msg]
        )
        
        # 초기화 버튼
        clear_btn.click(
            fn=clear_all_results,
            outputs=[input_box, results_display, results_state, status_msg]
        )
        
        # 게임 실행 버튼
        run_btn.click(
            fn=run_ladder_game_with_state,
            inputs=[player_count, results_state],
            outputs=[game_image, result_text]
        )
        
        # 예시 버튼들
        def set_example1():
            return "", "Winner, Loser, Coffee, Cleaning", ["Winner", "Loser", "Coffee", "Cleaning"], "✅ 예시 1 로드됨!"
        
        def set_example2():
            return "", "1st, 2nd, (Empty), Lose, Retry", ["1st", "2nd", "(Empty)", "Lose", "Retry"], "✅ 예시 2 로드됨!"
            
        def set_example3():
            return "", "당첨, 꽝, 커피, 청소", ["당첨", "꽝", "커피", "청소"], "✅ 한글 예시 로드됨!"
        
        example1_btn.click(
            fn=set_example1,
            outputs=[input_box, results_display, results_state, status_msg]
        )
        
        example2_btn.click(
            fn=set_example2,
            outputs=[input_box, results_display, results_state, status_msg]
        )
        
        example3_btn.click(
            fn=set_example3,
            outputs=[input_box, results_display, results_state, status_msg]
        )
    
    return demo

# 메인 실행 부분 (Hugging Face Spaces용)
if __name__ == "__main__":
    print("🎮 Starting Interactive Ladder Game...")
    
    # Gradio 앱 생성
    demo = create_interface()
    
    # Hugging Face Spaces에서 자동 배포
    demo.launch()
