from config import TOKEN
import telebot
from logic import shorten_url
from pydub import AudioSegment
import os
from logic import voice_to_text
import speech_recognition as sr

bot = telebot.TeleBot(TOKEN)
AudioSegment.ffmpeg = 'ffmpeg.exe'
AudioSegment.ffmprobe = 'ffmprobe.exe'
wav_file = 'new_file.wav'

@bot.message_handler(commands = ['help','start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 
                     "Привет я могу расшифровывать голосовые сообщения и записывать их в качестве текста, а так же делать ссылки короче по команде: /url и сама ссылка!")


@bot.message_handler(commands = ['url'])
def url_shorten(message):
    url = telebot.util.extract_arguments(message.text)
    if url:
        shortened_url = shorten_url(url)
        bot.send_message(message.chat.id, f"{shortened_url}")


@bot.message_handler(content_types = ['voice'])
def voice_decoding(message):
    get_file = bot.get_file(message.voice.file_id)
    fname = os.path.basename(get_file.file_path)
    downloaded_file = bot.download_file(get_file.file_path)
    try: 

        with open(fname, 'wb') as f: 
            f.write(downloaded_file)
        AudioSegment.from_file(fname).export(wav_file, format='wav')
        result = voice_to_text(wav_file)
        bot.send_message(message.chat.id, format(result))
    except sr.UnknownValueError as e:
        bot.send_message(message.chat.id, "Прошу прощения, но я не разобрал сообщение...")
    except Exception as e:
        bot.send_message(message.chat.id, "Что-то пошло не так...")
    finally:
        os.remove(fname)
        os.remove(wav_file)
    
































#    try:
#        get_file = bot.get_file(message.voice.file_id)
#        full_path_file = os.path.splitext(get_file.file_path)
#        file_name = os.path.basename(full_path_file)
#        doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, get_file.file_path))
#        with open(file_name+'.oga', 'wb') as f:
#            f.write(doc.content) 
#        overwriting = subprocess.run(['ffmpeg', '-i', file_name+'.oga', file_name+'.wav']) 
#        result = voice_to_text(file_name+'.wav') 
#        bot.send_message(message.chat.id, format(result))
#        return result
#    
#    except Exception as e:
#        bot.send_message(message.chat.id, "Прошу прощения, но я не разобрал сообщение...", e)
        





    




bot.infinity_polling()