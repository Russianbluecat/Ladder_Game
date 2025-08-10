---
title: Interactive Ladder Game
emoji: 🎮
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# 🎮 Interactive Ladder Game

A fun interactive ladder game where you can input results one by one and watch the magic happen!
사다리타기 게임을 웹으로 구현해보고 싶었어 
Claude가 많이 코드에 기여해줬어. 내가 했지만 재밋따 

## ✨ Features

- **Real-time Input**: Type results and press Enter to add them instantly
- **Visual Results**: Beautiful visualization of the ladder game with colored paths
- **Multiple Players**: Support for 2-10 participants
- **Empty Results**: Just press Enter for empty/blank results
- **Korean Support**: Works perfectly with Korean text

## 🎯 How to Use

1. **Select Participants**: Choose 2-10 players using the slider
2. **Add Results**: 
   - Type a result (e.g., "Winner", "당첨", etc.)
   - Press **Enter** to add it
   - Just press **Enter** for empty results
3. **Run Game**: Click "Run Game!" when all results are added
4. **View Results**: See the beautiful ladder visualization and final results!

## 💡 Example Usage

- Type "Winner" → Press Enter → Shows "Winner"
- Type "Loser" → Press Enter → Shows "Winner, Loser" 
- Just press Enter → Shows "Winner, Loser, (Empty)"

## 🛠️ Technical Details

- Built with **Gradio** for the web interface
- Uses **Matplotlib** for ladder visualization  
- **PIL** for image processing
- Real-time state management with Gradio State

## 🎨 Features

- Animated path tracing for each player
- Color-coded results for easy identification
- Responsive design that works on mobile and desktop
- Korean/English bilingual support

---

**Enjoy the game!** 🎊
