from app.db.session import engine
from sqlalchemy import text

sql = """
INSERT INTO emotions (name, description, color_code, emoji, audio_url, animation_url)
VALUES
('Vui vẻ', 'Cảm xúc khi trẻ cảm thấy hạnh phúc, thoải mái và muốn cười.', '#FFD54F', '😊', NULL, NULL),
('Buồn', 'Cảm xúc khi trẻ cảm thấy không vui, thất vọng hoặc mất mát.', '#64B5F6', '😢', NULL, NULL),
('Tức giận', 'Cảm xúc khi trẻ cảm thấy khó chịu, bực bội hoặc không hài lòng.', '#EF5350', '😡', NULL, NULL),
('Sợ hãi', 'Cảm xúc khi trẻ cảm thấy lo lắng, bất an hoặc sợ một điều gì đó.', '#9575CD', '😨', NULL, NULL),
('Ngạc nhiên', 'Cảm xúc khi trẻ gặp điều bất ngờ hoặc chưa từng nghĩ tới.', '#FFB74D', '😮', NULL, NULL),
('Lo lắng', 'Cảm xúc khi trẻ cảm thấy bồn chồn, hồi hộp hoặc không yên tâm.', '#4DB6AC', '😟', NULL, NULL),
('Xấu hổ', 'Cảm xúc khi trẻ cảm thấy ngại ngùng, lúng túng hoặc mắc cỡ.', '#F48FB1', '😳', NULL, NULL),
('Tự hào', 'Cảm xúc khi trẻ cảm thấy vui vì đã làm được điều tốt hoặc đạt thành quả.', '#81C784', '😊', NULL, NULL),
('Yêu thương', 'Cảm xúc khi trẻ cảm thấy được quan tâm, gần gũi hoặc muốn thể hiện tình cảm.', '#F06292', '🥰', NULL, NULL),
('Bình tĩnh', 'Cảm xúc khi trẻ cảm thấy thoải mái, nhẹ nhàng và không căng thẳng.', '#90CAF9', '😌', NULL, NULL),
('Mệt mỏi', 'Cảm xúc khi trẻ cảm thấy thiếu năng lượng, buồn ngủ hoặc cần nghỉ ngơi.', '#B0BEC5', '😴', NULL, NULL),
('Cô đơn', 'Cảm xúc khi trẻ cảm thấy một mình, thiếu sự chia sẻ hoặc cần được quan tâm.', '#A1887F', '🥺', NULL, NULL),
('Bối rối', 'Cảm xúc khi trẻ chưa hiểu rõ điều gì đó hoặc không biết nên làm gì.', '#CE93D8', '😕', NULL, NULL),
('Ghen tị', 'Cảm xúc khi trẻ cảm thấy không vui vì người khác có điều mình mong muốn.', '#AED581', '😒', NULL, NULL),
('Hào hứng', 'Cảm xúc khi trẻ cảm thấy rất vui, mong chờ hoặc thích thú với điều gì đó.', '#FF8A65', '🤩', NULL, NULL);
"""

with engine.begin() as conn:
    conn.execute(text(sql))
    print("Successfully inserted new standard emotions!")
