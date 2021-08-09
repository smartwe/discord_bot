import discord, bs4, youtube_dl, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
from alive import alive
from weathercatcher import wc

alive()
client = discord.Client()

commands = ["*명령어","*검색","*재생","*정지","*일시정지","*다시자생","*삭제"]

def url_def(text):
  chrome_options = Options()
  chrome_options.add_argument("headless")
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  driver = webdriver.Chrome(options=chrome_options)
  driver.get('https://www.youtube.com/results?search_query=' + text)
  source = driver.page_source
  bs = bs4.BeautifulSoup(source, 'lxml')
  entire = bs.find('a', {'id': 'video-title'})
  driver.quit()
  rink = entire.get('href')
  url = 'https://www.youtube.com' + rink
  return url


def text_split(set_text):
  test2_size = len(set_text)
  test2_size = int(test2_size)
  text = set_text[1]
  for i in range(2, test2_size):
    text = text + " " + set_text[i]
  return text


def lct(text):
  if text == "":
    return "서울"
  else:
    return text

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,activity=discord.Game("*명령어"))

@client.event
async def on_message(message):
    global voice
    channel = message.channel


    def voice_ch():
      for vc in client.voice_clients:
            if vc.guild == message.guild:
                voice = vc
      return voice

    if message.content.startswith("*미세먼지"):
      location = message.content.lstrip("*미세먼지 ")
      location = lct(location)
      try:
        mese = wc.current_fdust(location)
        await channel.send("현재 " + location + "의 미세먼지 지수는 " + mese + " 입니다")
      except:
        await channel.send("해외 도시는 미세먼지 측정이 안됩니다!(아니면 다시 시도해보세요!)")

    if message.content.startswith("*기온"):
      location = message.content.lstrip("*기온 ")
      location = lct(location)
      temp = wc.current_temp(location)
      await channel.send("현재 "+ location + "의 기온은 " + temp + "℃ 입니다") 

    if message.content.startswith("*날씨정보"):
      location = message.content.lstrip("*날씨세부정보 ")
      location = lct(location)
      detail = wc.current_details(location)
      await channel.send("현재 " + location + "은(는) " + detail)

    if message.content.startswith("*초미세먼지"):
      location = message.content.lstrip("*초미세먼지 ")
      location = lct(location)
      try:
        ufdust = wc.current_ufdust(location)
        await channel.send("현재 " + location + "의 초미세먼지 지수는 " + ufdust + " 입니다")
      except:
        await channel.send("해외 도시는 초미세먼지 측정이 안됩니다!(아니면 다시 시도해보세요!)")
    
    if message.content.startswith("*오존"):
      location = message.content.lstrip("*오존 ")
      location = lct(location)
      try:
        ozone= wc.current_ozoneindex(location)
        await channel.send("현재 " + location + "의 오존 농도는 " + ozone + " 입니다")
      except:
        await channel.send("해외 도시는 오존농도 측정이 안됩니다!(아니면 다시 시도해보세요!)")
 
    if message.content == "*퇴장":
        voice = voice_ch()
        try:
          await voice.disconnect()     
          await channel.send("음성 채널을 나갔습니다!")
        except:
          await channel.send("음성 채널에 입장해주세요!")

    if message.content == "*일시정지":
      voice = voice_ch()
      try:
        voice.pause()
        await channel.send("음악을 정지 합니다")
      except:
        await channel.send("음악을 재생하고 있지 않습니다!")

    if message.content == "*다시재생":
      voice = voice_ch()
      try:
        voice.resume()
        await channel.send("음악을 다시 재생합니다")
      except:
        await channel.send("일시정지 상태가 아닙니다")

    if message.content == "*정지":
      voice = voice_ch()
      try:
        voice.stop()
        await channel.send("음악 재생을 중단 합니다")
      except:
        await channel.send("음악을 재생하고 있지 않습니다!")

    if message.content.startswith("*재생"):
        test1 = message.content.replace(" ","").lstrip("*재생 ")
        test2 = message.content.split(" ")
        url_list = []
        url_test = "" 
        for i in test1:
          url_list.append(i)
        for i in range(8):
          try:
            url_test = url_test + url_list[i]
          except:
            break
        if url_test == "https://":
          url = test1 
        else:
          text = text_split(test2)
          url = url_def(text)
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        ydl_ops = {"format": "bestaudio", 'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}
        with youtube_dl.YoutubeDL(ydl_ops) as ydl:
          info = ydl.extract_info(url, download=False)
          URL = info['formats'][0]['url']
          title = info.get('title', None)
        coin = 0
        try:
          vc = message.author.voice.channel
          await vc.connect()
        except:
          coin += 1 
        try:
          voice = voice_ch()
          voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
          await channel.send(title + "을(를) 재생합니다!")
        except:
          if coin == 1:
            await channel.send("음성 채널에 입장하여 주세요!")
          else:
            await channel.send("오류 발생!")
    if message.content == "*뭐할까":
        try_list = [
            "게임 하는 것은 어떠신가요?", "오늘은 영화를 보세요!", "취미를 찾아보세요!",
            "저의 숨겨진 기능을 찾아보는 것은 어떠세요?", "아무거나 도전해보세요!", "프로그래밍 하시죠!"
        ]
        num = randint(0, 6)
        await channel.send(try_list[num])

    if message.content.startswith("*삭제"):
        str_size = message.content.split(" ")
        text = int(text_split(str_size))
        if text <= 100:
            await channel.send("메세지를 삭제합니다")
            await message.channel.purge(limit=text + 2)
            massage_ = await message.channel.send("{} 메세지가 삭제되었습니다".format(message.author.mention))
            sleep(1.5)
            await massage_.delete()
        else:
            await channel.send("100이하만 가능합니다")

    if message.content.startswith("*검색"):
      text1 = message.content.replace(" ","").lstrip("*검색 ")
      text2 = message.content.split(" ")
      if text1 == "":
        await channel.send("검색할 내용을 입력해 주세요!")
      else:
        text = text_split(text2)
        url = url_def(text)
        await channel.send(url)

    if message.content == "*명령어":
        embed = discord.Embed(title="명령어 목록", colour=discord.Color.red())
        embed.add_field(name="*검색",
            value="유튜브 영상 검색 기능 입니다\n사용법 : *검색 + 영상 이름")
        embed.add_field(name="*삭제", value="메세지를 지정한 숫자만큼 삭제합니다", inline=False)
        embed.add_field(name="*뭐할까", value="무엇을 할지 랜덤으로 추천해 드립니다", inline=False)
        embed.add_field(name="기상 관련 명령어", value="`*기온`, `*미세먼지`, `*초미세먼지`, `*오존`, `*날씨정보`\n 사용법 : 기상 관련 명령어 + 도시", inline=False)
        embed.add_field(name="*재생", value="음악을 재생합니다. 예) *재생 링크", inline=True)
        embed.add_field(name="재생 관련 명령어", value="`*정지`, `*일시정지`, `*다시재생`, `*퇴장`")
        await channel.send(embed=embed)

client.run(os.environ['token'])
