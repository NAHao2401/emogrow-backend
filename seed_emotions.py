import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.emotion import Emotion, EmotionFlashcard

def seed_data():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Emotion).first():
            print("Emotions already seeded. Skipping...")
            return

        mock_emotions = [
            ("Vui vẻ", "Cảm xúc khi trẻ cảm thấy hạnh phúc, thoải mái và muốn cười.", "#FFD54F", "😊"),
            ("Buồn", "Cảm xúc khi trẻ cảm thấy không vui, thất vọng hoặc mất mát.", "#64B5F6", "😢"),
            ("Tức giận", "Cảm xúc khi trẻ cảm thấy khó chịu, bực bội hoặc không hài lòng.", "#EF5350", "😡"),
            ("Sợ hãi", "Cảm xúc khi trẻ cảm thấy lo lắng, bất an hoặc sợ một điều gì đó.", "#9575CD", "😨"),
            ("Ngạc nhiên", "Cảm xúc khi trẻ gặp điều bất ngờ hoặc chưa từng nghĩ tới.", "#FFB74D", "😮"),
            ("Lo lắng", "Cảm xúc khi trẻ cảm thấy bồn chồn, hồi hộp hoặc không yên tâm.", "#4DB6AC", "😟"),
            ("Xấu hổ", "Cảm xúc khi trẻ cảm thấy ngại ngùng, lúng túng hoặc mắc cỡ.", "#F48FB1", "😳"),
            ("Tự hào", "Cảm xúc khi trẻ cảm thấy vui vì đã làm được điều tốt hoặc đạt thành quả.", "#81C784", "😊"),
            ("Yêu thương", "Cảm xúc khi trẻ cảm thấy được quan tâm, gần gũi hoặc muốn thể hiện tình cảm.", "#F06292", "🥰"),
            ("Bình tĩnh", "Cảm xúc khi trẻ cảm thấy thoải mái, nhẹ nhàng và không căng thẳng.", "#90CAF9", "😌"),
            ("Mệt mỏi", "Cảm xúc khi trẻ cảm thấy thiếu năng lượng, buồn ngủ hoặc cần nghỉ ngơi.", "#B0BEC5", "😴"),
            ("Cô đơn", "Cảm xúc khi trẻ cảm thấy một mình, thiếu sự chia sẻ hoặc cần được quan tâm.", "#A1887F", "🥺"),
            ("Bối rối", "Cảm xúc khi trẻ chưa hiểu rõ điều gì đó hoặc không biết nên làm gì.", "#CE93D8", "😕"),
            ("Ghen tị", "Cảm xúc khi trẻ cảm thấy không vui vì người khác có điều mình mong muốn.", "#AED581", "😒"),
            ("Hào hứng", "Cảm xúc khi trẻ cảm thấy rất vui, mong chờ hoặc thích thú với điều gì đó.", "#FF8A65", "🤩")
        ]

        emotion_objects = []
        for name, desc, color, emoji in mock_emotions:
            emotion = Emotion(
                name=name,
                description=desc,
                color_code=color,
                emoji=emoji
            )
            db.add(emotion)
            emotion_objects.append(emotion)
            
        db.commit()
        
        # Add some mock flashcards for "Vui vẻ" (id = 1)
        vui_ve_id = emotion_objects[0].emotion_id
        flashcards = [
            EmotionFlashcard(
                emotion_id=vui_ve_id,
                title="Nhận biết nụ cười",
                front_text="Khi con cảm thấy vui, mặt con sẽ trông như thế nào?",
                front_instruction="Hãy làm mặt vui cho bố mẹ xem nhé!",
                back_title="Đúng rồi, đó là nụ cười!",
                back_description="Khi vui, khóe miệng chúng ta cong lên, mắt sáng rỡ.",
                explanation="Vui vẻ là khi con được làm điều mình thích, được ăn món ngon hoặc được đi chơi.",
                example_situation="Giống như lúc con được bố mẹ dẫn đi công viên ấy!",
                difficulty_level=1,
                is_active=True
            ),
            EmotionFlashcard(
                emotion_id=vui_ve_id,
                title="Sẻ chia niềm vui",
                front_text="Khi vui vẻ, con thích làm gì cùng bạn bè?",
                front_instruction="Kể cho bố mẹ nghe một điều vui con từng làm với bạn.",
                back_title="Chia sẻ làm niềm vui nhân đôi!",
                back_description="Khi chơi chung và cười đùa cùng nhau, ai cũng sẽ thấy vui vẻ.",
                explanation="Niềm vui rất dễ lây lan. Khi con cười, người khác cũng muốn cười theo.",
                example_situation="Con có thể chia sẻ đồ chơi với bạn để cả hai cùng vui.",
                difficulty_level=2,
                is_active=True
            )
        ]
        
        for fc in flashcards:
            db.add(fc)
            
        db.commit()
        print("Data seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
