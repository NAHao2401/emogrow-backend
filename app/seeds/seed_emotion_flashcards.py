from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.emotion import Emotion, EmotionFlashcard


def seed_emotion_flashcards(db: Session):
    flashcard_data = {
        "Vui vẻ": [
            {
                "title": "Cảm xúc vui vẻ",
                "front_text": "Con đang vui vẻ",
                "front_instruction": "Chạm để lật",
                "back_title": "Vui vẻ",
                "back_description": "Vui vẻ là khi con cảm thấy hạnh phúc, thoải mái và muốn cười.",
                "explanation": "Con có thể cảm thấy vui khi được ba mẹ khen, được chơi cùng bạn hoặc hoàn thành một việc tốt.",
                "example_situation": "Con cảm thấy vui khi được cô giáo khen vì đã xếp đồ chơi gọn gàng.",
                "audio_url": "/audio/flashcards/happy_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Khi con cười",
                "front_text": "Khi nào con cảm thấy muốn cười?",
                "front_instruction": "Hãy nghĩ rồi chạm để xem",
                "back_title": "Niềm vui",
                "back_description": "Khi vui, khuôn mặt con thường tươi tắn và con muốn chia sẻ với người khác.",
                "explanation": "Nụ cười giúp con thể hiện rằng con đang cảm thấy dễ chịu và hạnh phúc.",
                "example_situation": "Con cười thật tươi khi được ba mẹ dẫn đi công viên.",
                "audio_url": "/audio/flashcards/happy_02.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Chia sẻ niềm vui",
                "front_text": "Con có thể làm gì khi vui?",
                "front_instruction": "Chạm để lật",
                "back_title": "Chia sẻ cảm xúc vui",
                "back_description": "Khi vui, con có thể kể cho ba mẹ, bạn bè hoặc cô giáo nghe.",
                "explanation": "Chia sẻ niềm vui giúp mọi người hiểu con hơn và cùng vui với con.",
                "example_situation": "Con nói với mẹ: 'Hôm nay con rất vui vì con vẽ được bức tranh đẹp.'",
                "audio_url": "/audio/flashcards/happy_03.mp3",
                "difficulty_level": 2,
            },
        ],

        "Buồn": [
            {
                "title": "Cảm xúc buồn",
                "front_text": "Con đang buồn",
                "front_instruction": "Chạm để lật",
                "back_title": "Buồn",
                "back_description": "Buồn là khi con cảm thấy không vui, thất vọng hoặc muốn khóc.",
                "explanation": "Buồn là cảm xúc bình thường. Con có thể nói với người lớn để được an ủi.",
                "example_situation": "Con buồn khi món đồ chơi yêu thích bị hỏng.",
                "audio_url": "/audio/flashcards/sad_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Khi con muốn khóc",
                "front_text": "Con có thể làm gì khi muốn khóc?",
                "front_instruction": "Chạm để lật",
                "back_title": "Nói ra nỗi buồn",
                "back_description": "Khi muốn khóc, con có thể ôm ba mẹ hoặc nói: 'Con đang buồn.'",
                "explanation": "Khóc không xấu. Khóc giúp con giải tỏa cảm xúc trong lòng.",
                "example_situation": "Con khóc vì bạn không chơi cùng, rồi cô giáo đến hỏi chuyện và an ủi con.",
                "audio_url": "/audio/flashcards/sad_02.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Buồn rồi sẽ qua",
                "front_text": "Nỗi buồn có ở mãi không?",
                "front_instruction": "Hãy đoán rồi chạm để lật",
                "back_title": "Cảm xúc thay đổi",
                "back_description": "Nỗi buồn có thể qua đi khi con được lắng nghe, nghỉ ngơi hoặc làm điều con thích.",
                "explanation": "Không cảm xúc nào ở mãi. Con có thể bình tĩnh và nhờ người lớn giúp đỡ.",
                "example_situation": "Con buồn vì thua trò chơi, sau đó con thử lại và cảm thấy khá hơn.",
                "audio_url": "/audio/flashcards/sad_03.mp3",
                "difficulty_level": 2,
            },
        ],

        "Tức giận": [
            {
                "title": "Cảm xúc tức giận",
                "front_text": "Con đang tức giận",
                "front_instruction": "Chạm để lật",
                "back_title": "Tức giận",
                "back_description": "Tức giận là khi con cảm thấy khó chịu, bực bội hoặc không hài lòng.",
                "explanation": "Con có thể tức giận, nhưng không nên đánh bạn, la hét hoặc ném đồ.",
                "example_situation": "Con tức giận khi bạn giành đồ chơi của con.",
                "audio_url": "/audio/flashcards/angry_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Hít thở khi tức giận",
                "front_text": "Con nên làm gì khi tức giận?",
                "front_instruction": "Chạm để lật",
                "back_title": "Bình tĩnh lại",
                "back_description": "Khi tức giận, con có thể hít sâu, đếm từ 1 đến 5 và nói cảm xúc của mình.",
                "explanation": "Hít thở giúp cơ thể con dịu lại trước khi nói hoặc hành động.",
                "example_situation": "Con hít sâu rồi nói: 'Con không thích khi bạn lấy đồ của con.'",
                "audio_url": "/audio/flashcards/angry_02.mp3",
                "difficulty_level": 2,
            },
            {
                "title": "Nói thay vì đánh",
                "front_text": "Khi tức giận, con có nên đánh bạn không?",
                "front_instruction": "Chạm để lật",
                "back_title": "Không làm đau người khác",
                "back_description": "Con không nên đánh bạn. Con có thể dùng lời nói để nói điều mình không thích.",
                "explanation": "Nói ra cảm xúc giúp người khác hiểu con mà không làm ai bị đau.",
                "example_situation": "Con nói với bạn: 'Bạn làm mình buồn, mình muốn lấy lại đồ chơi.'",
                "audio_url": "/audio/flashcards/angry_03.mp3",
                "difficulty_level": 2,
            },
        ],

        "Sợ hãi": [
            {
                "title": "Cảm xúc sợ hãi",
                "front_text": "Con đang sợ",
                "front_instruction": "Chạm để lật",
                "back_title": "Sợ hãi",
                "back_description": "Sợ hãi là khi con cảm thấy lo lắng, bất an hoặc muốn tránh xa điều gì đó.",
                "explanation": "Sợ hãi giúp con nhận ra điều con thấy không an toàn. Con có thể tìm người lớn để được bảo vệ.",
                "example_situation": "Con sợ khi nghe tiếng sấm lớn ngoài trời.",
                "audio_url": "/audio/flashcards/fear_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Tìm người giúp đỡ",
                "front_text": "Khi sợ, con có thể tìm ai?",
                "front_instruction": "Chạm để lật",
                "back_title": "Nhờ người lớn",
                "back_description": "Khi sợ, con có thể gọi ba mẹ, cô giáo hoặc người lớn đáng tin cậy.",
                "explanation": "Người lớn có thể giúp con cảm thấy an toàn hơn.",
                "example_situation": "Con sợ bóng tối nên gọi mẹ đến bật đèn ngủ.",
                "audio_url": "/audio/flashcards/fear_02.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Con có thể can đảm",
                "front_text": "Sợ hãi có nghĩa là con yếu đuối không?",
                "front_instruction": "Chạm để lật",
                "back_title": "Can đảm",
                "back_description": "Sợ hãi không có nghĩa là yếu đuối. Ai cũng có lúc cảm thấy sợ.",
                "explanation": "Can đảm là khi con biết mình sợ nhưng vẫn thử đối mặt từng chút một với sự giúp đỡ.",
                "example_situation": "Con sợ phát biểu, nhưng con thử nói một câu ngắn trước lớp.",
                "audio_url": "/audio/flashcards/fear_03.mp3",
                "difficulty_level": 2,
            },
        ],

        "Ngạc nhiên": [
            {
                "title": "Cảm xúc ngạc nhiên",
                "front_text": "Con đang ngạc nhiên",
                "front_instruction": "Chạm để lật",
                "back_title": "Ngạc nhiên",
                "back_description": "Ngạc nhiên là khi con gặp điều bất ngờ hoặc chưa từng nghĩ tới.",
                "explanation": "Ngạc nhiên có thể làm con mở to mắt, há miệng hoặc muốn hỏi thêm.",
                "example_situation": "Con ngạc nhiên khi thấy ba mẹ chuẩn bị bánh sinh nhật cho con.",
                "audio_url": "/audio/flashcards/surprised_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Điều bất ngờ",
                "front_text": "Điều gì làm con bất ngờ?",
                "front_instruction": "Chạm để lật",
                "back_title": "Bất ngờ",
                "back_description": "Một điều bất ngờ có thể làm con vui, tò mò hoặc hơi bối rối.",
                "explanation": "Con có thể hỏi: 'Chuyện gì xảy ra vậy ạ?' để hiểu rõ hơn.",
                "example_situation": "Cô giáo mang một hộp quà vào lớp và con rất tò mò.",
                "audio_url": "/audio/flashcards/surprised_02.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Ngạc nhiên vui và ngạc nhiên lo",
                "front_text": "Ngạc nhiên lúc nào cũng vui không?",
                "front_instruction": "Chạm để lật",
                "back_title": "Nhiều kiểu ngạc nhiên",
                "back_description": "Có lúc ngạc nhiên làm con vui, có lúc làm con lo hoặc chưa hiểu chuyện gì.",
                "explanation": "Con có thể nói ra cảm xúc của mình để người lớn giải thích thêm.",
                "example_situation": "Con ngạc nhiên khi nghe tiếng động lớn và hỏi mẹ đó là tiếng gì.",
                "audio_url": "/audio/flashcards/surprised_03.mp3",
                "difficulty_level": 2,
            },
        ],

        "Lo lắng": [
            {
                "title": "Cảm xúc lo lắng",
                "front_text": "Con đang lo lắng",
                "front_instruction": "Chạm để lật",
                "back_title": "Lo lắng",
                "back_description": "Lo lắng là khi con cảm thấy bồn chồn, hồi hộp hoặc không yên tâm.",
                "explanation": "Con có thể lo khi sắp làm điều mới hoặc chưa biết chuyện gì sẽ xảy ra.",
                "example_situation": "Con lo lắng trước khi vào lớp học mới.",
                "audio_url": "/audio/flashcards/worried_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Nói con đang lo",
                "front_text": "Khi lo lắng, con nên nói gì?",
                "front_instruction": "Chạm để lật",
                "back_title": "Chia sẻ lo lắng",
                "back_description": "Con có thể nói: 'Con đang lo lắng, ba mẹ giúp con được không?'",
                "explanation": "Nói ra giúp người lớn biết con cần được trấn an.",
                "example_situation": "Con nói với cô: 'Con lo vì con chưa biết làm bài này.'",
                "audio_url": "/audio/flashcards/worried_02.mp3",
                "difficulty_level": 2,
            },
            {
                "title": "Làm từng bước nhỏ",
                "front_text": "Làm sao để bớt lo?",
                "front_instruction": "Chạm để lật",
                "back_title": "Từng bước một",
                "back_description": "Con có thể hít thở, hỏi người lớn và làm từng bước nhỏ.",
                "explanation": "Khi chia việc khó thành việc nhỏ, con sẽ cảm thấy dễ làm hơn.",
                "example_situation": "Con lo khi phải dọn phòng, mẹ giúp con bắt đầu bằng việc cất đồ chơi trước.",
                "audio_url": "/audio/flashcards/worried_03.mp3",
                "difficulty_level": 2,
            },
        ],

        "Xấu hổ": [
            {
                "title": "Cảm xúc xấu hổ",
                "front_text": "Con đang xấu hổ",
                "front_instruction": "Chạm để lật",
                "back_title": "Xấu hổ",
                "back_description": "Xấu hổ là khi con cảm thấy ngại ngùng, lúng túng hoặc mắc cỡ.",
                "explanation": "Xấu hổ là cảm xúc bình thường khi con làm sai hoặc bị chú ý quá nhiều.",
                "example_situation": "Con xấu hổ khi đọc nhầm trước lớp.",
                "audio_url": "/audio/flashcards/shy_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Ai cũng có lúc mắc lỗi",
                "front_text": "Mắc lỗi có đáng xấu hổ mãi không?",
                "front_instruction": "Chạm để lật",
                "back_title": "Mắc lỗi là bình thường",
                "back_description": "Ai cũng có lúc mắc lỗi. Con có thể sửa lỗi và thử lại.",
                "explanation": "Mắc lỗi giúp con học thêm điều mới.",
                "example_situation": "Con làm đổ nước, sau đó con xin lỗi và lau bàn.",
                "audio_url": "/audio/flashcards/shy_02.mp3",
                "difficulty_level": 2,
            },
            {
                "title": "Khi con ngại nói",
                "front_text": "Con có thể làm gì khi ngại nói?",
                "front_instruction": "Chạm để lật",
                "back_title": "Nói từ từ",
                "back_description": "Khi ngại, con có thể nói chậm, nói nhỏ trước hoặc nhờ người lớn hỗ trợ.",
                "explanation": "Con không cần phải nói thật nhanh. Con có thể tập từng chút một.",
                "example_situation": "Con ngại chào khách, mẹ đứng cạnh và con nói: 'Con chào cô ạ.'",
                "audio_url": "/audio/flashcards/shy_03.mp3",
                "difficulty_level": 2,
            },
        ],

        "Tự hào": [
            {
                "title": "Cảm xúc tự hào",
                "front_text": "Con đang tự hào",
                "front_instruction": "Chạm để lật",
                "back_title": "Tự hào",
                "back_description": "Tự hào là khi con cảm thấy vui vì mình đã cố gắng hoặc làm được điều tốt.",
                "explanation": "Con có thể tự hào khi hoàn thành việc khó, giúp đỡ người khác hoặc tiến bộ hơn.",
                "example_situation": "Con tự hào vì đã tự mặc quần áo mà không cần ba mẹ giúp.",
                "audio_url": "/audio/flashcards/proud_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Con đã cố gắng",
                "front_text": "Tự hào có cần phải thắng không?",
                "front_instruction": "Chạm để lật",
                "back_title": "Tự hào vì cố gắng",
                "back_description": "Con có thể tự hào vì đã cố gắng, dù kết quả chưa hoàn hảo.",
                "explanation": "Sự cố gắng rất đáng quý. Mỗi lần thử là một lần con tiến bộ.",
                "example_situation": "Con chưa tô màu thật đẹp, nhưng con đã kiên nhẫn hoàn thành bức tranh.",
                "audio_url": "/audio/flashcards/proud_02.mp3",
                "difficulty_level": 2,
            },
            {
                "title": "Nói lời tự hào",
                "front_text": "Con có thể nói gì khi tự hào?",
                "front_instruction": "Chạm để lật",
                "back_title": "Con làm được rồi",
                "back_description": "Con có thể nói: 'Con đã cố gắng và con làm được rồi!'",
                "explanation": "Nói lời tích cực giúp con tự tin hơn.",
                "example_situation": "Con nói: 'Con tự hào vì hôm nay con biết chia sẻ đồ chơi với bạn.'",
                "audio_url": "/audio/flashcards/proud_03.mp3",
                "difficulty_level": 2,
            },
        ],

        "Yêu thương": [
            {
                "title": "Cảm xúc yêu thương",
                "front_text": "Con cảm thấy yêu thương",
                "front_instruction": "Chạm để lật",
                "back_title": "Yêu thương",
                "back_description": "Yêu thương là khi con cảm thấy gần gũi, quan tâm và muốn chăm sóc ai đó.",
                "explanation": "Con có thể thể hiện yêu thương bằng lời nói, cái ôm hoặc hành động tốt.",
                "example_situation": "Con ôm mẹ và nói: 'Con yêu mẹ.'",
                "audio_url": "/audio/flashcards/love_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Thể hiện yêu thương",
                "front_text": "Con có thể làm gì để thể hiện yêu thương?",
                "front_instruction": "Chạm để lật",
                "back_title": "Hành động yêu thương",
                "back_description": "Con có thể nói lời tốt đẹp, giúp đỡ, chia sẻ hoặc ôm người thân.",
                "explanation": "Yêu thương không chỉ là lời nói mà còn là hành động quan tâm.",
                "example_situation": "Con lấy khăn cho em khi em bị đổ nước.",
                "audio_url": "/audio/flashcards/love_02.mp3",
                "difficulty_level": 2,
            },
            {
                "title": "Quan tâm bạn bè",
                "front_text": "Khi bạn buồn, con có thể làm gì?",
                "front_instruction": "Chạm để lật",
                "back_title": "Yêu thương bạn bè",
                "back_description": "Con có thể hỏi thăm bạn, chia sẻ đồ chơi hoặc gọi cô giáo giúp.",
                "explanation": "Quan tâm đến bạn giúp bạn cảm thấy được yêu thương và không cô đơn.",
                "example_situation": "Con hỏi bạn: 'Bạn có sao không? Mình chơi cùng bạn nhé.'",
                "audio_url": "/audio/flashcards/love_03.mp3",
                "difficulty_level": 2,
            },
        ],

        "Bình tĩnh": [
            {
                "title": "Cảm xúc bình tĩnh",
                "front_text": "Con đang bình tĩnh",
                "front_instruction": "Chạm để lật",
                "back_title": "Bình tĩnh",
                "back_description": "Bình tĩnh là khi con cảm thấy nhẹ nhàng, thoải mái và không vội vàng.",
                "explanation": "Bình tĩnh giúp con suy nghĩ rõ hơn và xử lý mọi việc tốt hơn.",
                "example_situation": "Con bình tĩnh xếp hàng chờ đến lượt chơi cầu trượt.",
                "audio_url": "/audio/flashcards/calm_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Hít thở chậm",
                "front_text": "Làm sao để bình tĩnh hơn?",
                "front_instruction": "Chạm để lật",
                "back_title": "Thở chậm",
                "back_description": "Con có thể hít vào thật chậm, thở ra thật nhẹ và đếm từ 1 đến 5.",
                "explanation": "Hít thở chậm giúp cơ thể con thư giãn.",
                "example_situation": "Con chuẩn bị tiêm phòng, con hít thở chậm để bớt sợ.",
                "audio_url": "/audio/flashcards/calm_02.mp3",
                "difficulty_level": 2,
            },
            {
                "title": "Bình tĩnh khi chờ đợi",
                "front_text": "Khi phải chờ, con nên làm gì?",
                "front_instruction": "Chạm để lật",
                "back_title": "Chờ đợi bình tĩnh",
                "back_description": "Con có thể ngồi yên, quan sát xung quanh hoặc nói chuyện nhẹ nhàng.",
                "explanation": "Chờ đợi là cơ hội để con luyện sự kiên nhẫn.",
                "example_situation": "Con ngồi chờ mẹ thanh toán ở siêu thị mà không chạy lung tung.",
                "audio_url": "/audio/flashcards/calm_03.mp3",
                "difficulty_level": 2,
            },
        ],

        "Mệt mỏi": [
            {
                "title": "Cảm xúc mệt mỏi",
                "front_text": "Con đang mệt",
                "front_instruction": "Chạm để lật",
                "back_title": "Mệt mỏi",
                "back_description": "Mệt mỏi là khi cơ thể con thiếu năng lượng, buồn ngủ hoặc muốn nghỉ ngơi.",
                "explanation": "Khi mệt, con nên nghỉ ngơi, uống nước hoặc nói với người lớn.",
                "example_situation": "Con mệt sau khi chạy chơi ngoài sân quá lâu.",
                "audio_url": "/audio/flashcards/tired_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Cơ thể cần nghỉ",
                "front_text": "Khi mệt, cơ thể con cần gì?",
                "front_instruction": "Chạm để lật",
                "back_title": "Nghỉ ngơi",
                "back_description": "Cơ thể con cần được nghỉ, ngủ đủ và ăn uống đầy đủ.",
                "explanation": "Nghỉ ngơi giúp con có lại năng lượng để học và chơi.",
                "example_situation": "Con thấy buồn ngủ nên nằm nghỉ một lát.",
                "audio_url": "/audio/flashcards/tired_02.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Nói khi con mệt",
                "front_text": "Con nên nói gì khi thấy mệt?",
                "front_instruction": "Chạm để lật",
                "back_title": "Xin nghỉ ngơi",
                "back_description": "Con có thể nói: 'Con mệt rồi, con muốn nghỉ một chút.'",
                "explanation": "Nói ra giúp người lớn biết cơ thể con đang cần chăm sóc.",
                "example_situation": "Con nói với cô giáo rằng con hơi mệt và muốn ngồi nghỉ.",
                "audio_url": "/audio/flashcards/tired_03.mp3",
                "difficulty_level": 2,
            },
        ],

        "Cô đơn": [
            {
                "title": "Cảm xúc cô đơn",
                "front_text": "Con đang cô đơn",
                "front_instruction": "Chạm để lật",
                "back_title": "Cô đơn",
                "back_description": "Cô đơn là khi con cảm thấy một mình, thiếu người chơi cùng hoặc cần được quan tâm.",
                "explanation": "Khi cô đơn, con có thể tìm người thân, cô giáo hoặc bạn bè để chia sẻ.",
                "example_situation": "Con cô đơn khi các bạn chơi nhóm mà con chưa được tham gia.",
                "audio_url": "/audio/flashcards/lonely_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Rủ bạn chơi cùng",
                "front_text": "Khi muốn chơi cùng bạn, con có thể nói gì?",
                "front_instruction": "Chạm để lật",
                "back_title": "Kết nối với bạn",
                "back_description": "Con có thể nói: 'Bạn cho mình chơi cùng được không?'",
                "explanation": "Mời bạn chơi cùng là một cách tốt để con bớt cô đơn.",
                "example_situation": "Con đến gần nhóm bạn và hỏi: 'Mình chơi xếp hình cùng được không?'",
                "audio_url": "/audio/flashcards/lonely_02.mp3",
                "difficulty_level": 2,
            },
            {
                "title": "Con không một mình",
                "front_text": "Khi cô đơn, con có thể tìm ai?",
                "front_instruction": "Chạm để lật",
                "back_title": "Có người bên con",
                "back_description": "Con có thể tìm ba mẹ, ông bà, cô giáo hoặc một người bạn thân.",
                "explanation": "Có nhiều người yêu thương và sẵn sàng lắng nghe con.",
                "example_situation": "Con nói với mẹ: 'Hôm nay con thấy cô đơn vì không ai chơi với con.'",
                "audio_url": "/audio/flashcards/lonely_03.mp3",
                "difficulty_level": 2,
            },
        ],

        "Bối rối": [
            {
                "title": "Cảm xúc bối rối",
                "front_text": "Con đang bối rối",
                "front_instruction": "Chạm để lật",
                "back_title": "Bối rối",
                "back_description": "Bối rối là khi con chưa hiểu rõ điều gì đó hoặc chưa biết nên làm gì.",
                "explanation": "Khi bối rối, con có thể dừng lại, hỏi người lớn hoặc nhờ giải thích thêm.",
                "example_situation": "Con bối rối khi không biết phải cất đồ chơi vào hộp nào.",
                "audio_url": "/audio/flashcards/confused_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Hỏi khi chưa hiểu",
                "front_text": "Khi chưa hiểu, con nên làm gì?",
                "front_instruction": "Chạm để lật",
                "back_title": "Đặt câu hỏi",
                "back_description": "Con có thể hỏi: 'Cô ơi, con chưa hiểu, cô chỉ lại cho con được không?'",
                "explanation": "Hỏi là cách tốt để con học thêm và bớt bối rối.",
                "example_situation": "Con không hiểu luật chơi nên hỏi cô giáo hướng dẫn lại.",
                "audio_url": "/audio/flashcards/confused_02.mp3",
                "difficulty_level": 2,
            },
            {
                "title": "Làm rõ từng bước",
                "front_text": "Bối rối thì có thể làm từng bước không?",
                "front_instruction": "Chạm để lật",
                "back_title": "Từng bước rõ ràng",
                "back_description": "Con có thể chia việc khó thành các bước nhỏ để dễ hiểu hơn.",
                "explanation": "Làm từng bước giúp con biết mình nên bắt đầu từ đâu.",
                "example_situation": "Con bối rối khi dọn bàn, mẹ nói: 'Trước tiên con cất bút màu nhé.'",
                "audio_url": "/audio/flashcards/confused_03.mp3",
                "difficulty_level": 2,
            },
        ],

        "Ghen tị": [
            {
                "title": "Cảm xúc ghen tị",
                "front_text": "Con đang ghen tị",
                "front_instruction": "Chạm để lật",
                "back_title": "Ghen tị",
                "back_description": "Ghen tị là khi con cảm thấy không vui vì người khác có điều con cũng muốn.",
                "explanation": "Ghen tị là cảm xúc bình thường, nhưng con không nên làm đau hoặc nói xấu người khác.",
                "example_situation": "Con ghen tị khi bạn có món đồ chơi mới.",
                "audio_url": "/audio/flashcards/jealous_01.mp3",
                "difficulty_level": 2,
            },
            {
                "title": "Nói điều con muốn",
                "front_text": "Khi ghen tị, con có thể nói gì?",
                "front_instruction": "Chạm để lật",
                "back_title": "Nói ra mong muốn",
                "back_description": "Con có thể nói: 'Con cũng muốn được chơi món đó.'",
                "explanation": "Nói ra mong muốn giúp người lớn hiểu con, thay vì con giận dỗi hoặc giành đồ.",
                "example_situation": "Con nói với bạn: 'Bạn cho mình chơi thử khi bạn chơi xong nhé.'",
                "audio_url": "/audio/flashcards/jealous_02.mp3",
                "difficulty_level": 2,
            },
            {
                "title": "Vui cho người khác",
                "front_text": "Con có thể vui khi bạn có điều tốt không?",
                "front_instruction": "Chạm để lật",
                "back_title": "Chúc mừng bạn",
                "back_description": "Con có thể chúc mừng bạn và nhớ rằng con cũng có những điều đặc biệt của riêng mình.",
                "explanation": "Biết vui cho người khác giúp con có mối quan hệ tốt hơn với bạn bè.",
                "example_situation": "Bạn được cô khen, con vỗ tay chúc mừng bạn.",
                "audio_url": "/audio/flashcards/jealous_03.mp3",
                "difficulty_level": 3,
            },
        ],

        "Hào hứng": [
            {
                "title": "Cảm xúc hào hứng",
                "front_text": "Con đang hào hứng",
                "front_instruction": "Chạm để lật",
                "back_title": "Hào hứng",
                "back_description": "Hào hứng là khi con cảm thấy rất vui, mong chờ hoặc thích thú với điều gì đó.",
                "explanation": "Hào hứng giúp con có nhiều năng lượng để tham gia hoạt động.",
                "example_situation": "Con hào hứng khi biết hôm nay lớp sẽ đi dã ngoại.",
                "audio_url": "/audio/flashcards/excited_01.mp3",
                "difficulty_level": 1,
            },
            {
                "title": "Hào hứng nhưng vẫn chờ lượt",
                "front_text": "Khi rất hào hứng, con có cần chờ lượt không?",
                "front_instruction": "Chạm để lật",
                "back_title": "Vui và biết chờ",
                "back_description": "Dù rất hào hứng, con vẫn nên chờ đến lượt và lắng nghe hướng dẫn.",
                "explanation": "Biết chờ giúp con vui chơi an toàn và không làm phiền người khác.",
                "example_situation": "Con rất muốn chơi cầu trượt nhưng vẫn xếp hàng chờ đến lượt.",
                "audio_url": "/audio/flashcards/excited_02.mp3",
                "difficulty_level": 2,
            },
            {
                "title": "Chia sẻ sự hào hứng",
                "front_text": "Con có thể nói gì khi hào hứng?",
                "front_instruction": "Chạm để lật",
                "back_title": "Nói niềm mong chờ",
                "back_description": "Con có thể nói: 'Con rất mong được tham gia hoạt động này!'",
                "explanation": "Nói ra sự hào hứng giúp người khác biết con đang rất thích thú.",
                "example_situation": "Con nói với ba: 'Con rất háo hức được đi sở thú ngày mai.'",
                "audio_url": "/audio/flashcards/excited_03.mp3",
                "difficulty_level": 2,
            },
        ],
    }

    created_count = 0
    skipped_count = 0
    missing_emotions = []

    try:
        for emotion_name, flashcards in flashcard_data.items():
            emotion = (
                db.query(Emotion)
                .filter(Emotion.name == emotion_name)
                .first()
            )

            if emotion is None:
                missing_emotions.append(emotion_name)
                continue

            for item in flashcards:
                existed = (
                    db.query(EmotionFlashcard)
                    .filter(
                        EmotionFlashcard.emotion_id == emotion.emotion_id,
                        EmotionFlashcard.title == item["title"],
                    )
                    .first()
                )

                if existed:
                    skipped_count += 1
                    continue

                flashcard = EmotionFlashcard(
                    emotion_id=emotion.emotion_id,
                    title=item["title"].strip(),
                    front_text=item["front_text"].strip(),
                    front_instruction=item.get("front_instruction", "Chạm để lật"),
                    back_title=item.get("back_title"),
                    back_description=item.get("back_description"),
                    explanation=item.get("explanation"),
                    example_situation=item.get("example_situation"),
                    audio_url=item.get("audio_url"),
                    difficulty_level=item.get("difficulty_level", 1),
                    is_active=True,
                )

                db.add(flashcard)
                created_count += 1

        db.commit()

        print("Seed emotion flashcards completed.")
        print(f"Created: {created_count}")
        print(f"Skipped existing: {skipped_count}")

        if missing_emotions:
            print("Missing emotions:")
            for name in missing_emotions:
                print(f"- {name}")

    except SQLAlchemyError as e:
        db.rollback()
        print("Seed emotion flashcards failed.")
        print(e)
        raise