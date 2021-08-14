import discord, bs4, youtube_dl, os, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
from weathercatcher import wc

client = discord.Client()

commands = ["명령어", "검색", "뭐할까", "재생", "정지", "일시정지", "다시재생", "퇴장", "삭제", "미세먼지", "기온", "오존", "날씨정보"]


def download(url, file_name):
    with open(file_name, "wb") as file:   # open in binary mode
        response = requests.get(url)               # get request
        file.write(response.content) 


def tierfinder(word):
    if word.find('tier/1.svg') != -1:
        return "브론즈 5"
    elif word.find('tier/2.svg') != -1:
        return "브론즈 4"
    elif word.find('tier/3.svg') != -1:
        return "브론즈 3"
    elif word.find('tier/4.svg') != -1:
        return "브론즈 2"
    elif word.find('tier/5.svg') != -1:
        return "브론즈 1"
    elif word.find('tier/6.svg') != -1:
        return "실버 5"
    elif word.find('tier/7.svg') != -1:
        return "실버 4"
    elif word.find('tier/8.svg') != -1:
        return "실버 3"
    elif word.find('tier/9.svg') != -1:
        return "실버 2"
    elif word.find('tier/10.svg') != -1:
        return "실버 1"
    elif word.find('tier/11.svg') != -1:
        return "골드 5"
    elif word.find('tier/12.svg') != -1:
        return "골드 4"
    elif word.find('tier/13.svg') != -1:
        return "골드 3"
    elif word.find('tier/14.svg') != -1:
        return "골드 2"
    elif word.find('tier/15.svg') != -1:
        return "골드 1"
    elif word.find('tier/16.svg') != -1:
        return "플래티넘 5"
    elif word.find('tier/17.svg') != -1:
        return "플래티넘 4"
    elif word.find('tier/18.svg') != -1:
        return "플래티넘 3"
    elif word.find('tier/19.svg') != -1:
        return "플래티넘 2"
    elif word.find('tier/20.svg') != -1:
        return "플래티넘 1"
    elif word.find('tier/21.svg') != -1:
        return "다이아몬드 5"
    elif word.find('tier/22.svg') != -1:
        return "다이아몬드 4"
    elif word.find('tier/23.svg') != -1:
        return "다이아몬드 3"
    elif word.find('tier/24.svg') != -1:
        return "다이아몬드 2"
    elif word.find('tier/25.svg') != -1:
        return "다이아몬드 1"
    elif word.find('tier/26.svg') != -1:
        return "루비 5"
    elif word.find('tier/27.svg') != -1:
        return "루비 4"
    elif word.find('tier/28.svg') != -1:
        return "루비 3"
    elif word.find('tier/29.svg') != -1:
        return "루비 2"
    elif word.find('tier/30.svg') != -1:
        return "루비 1"
    elif word.find('tier/31.svg') != -1:
        return "마스터"
    else:
        return "언랭크"


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
    #await client.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.listening, name = "*명령어"))
    await client.change_presence(status=discord.Status.online,activity=discord.Game("[*명령어] 기능 추가"))

@client.event
async def on_message(message):
    global voice
    channel = message.channel


    def voice_ch():
      for vc in client.voice_clients:
            if vc.guild == message.guild:
                voice = vc
      return voice

    if message.content== "*ps":
        await channel.send("0:봇 사용\n1:기능 추가")

    if message.content.startswith("*ps0811"):
      text = message.content.lstrip("*ps0811")
      print(text)
      if text == " 0":
        await client.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.listening, name = "*명령어"))
        await channel.send("바뀜!")
      elif text == " 1":
        await client.change_presence(status=discord.Status.online,activity=discord.Game("[*명령어] 기능 추가"))
        await channel.send("바뀜!")

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
    if message.content.startswith("*백준문제"):
      id = message.content.lstrip("*백준문제 ")
      boj = requests.get("https://www.acmicpc.net/problem/" + id)
      html = boj.text
      soup = bs4.BeautifulSoup(html, "html.parser")
      q = soup.select_one("#problem_description > p").text
      inq = soup.select_one("#problem_input > p").text
      outq = soup.select_one("#problem_output > p").text
      embed = discord.Embed(title = "[boj 정보]", color = discord.Color.blue())
      embed.add_field(name = "문제", value = q, inline=False)
      embed.add_field(name = "입력", value = inq, inline=False)
      embed.add_field(name = "출력", value = outq, inline=False)
      await channel.send(embed = embed)

    if message.content.startswith("*백준 "):
      id = message.content.lstrip("*백준 ")
      boj = requests.get("https://www.acmicpc.net/user/" + id)
      html = boj.text
      soup = bs4.BeautifulSoup(html, "html.parser")
      rank = soup.find('img' , {'class' : 'solvedac-tier'}).text
      status = soup.find('blockquote' , {'class' : 'no-mathjax'}).text
      bojrank = soup.select_one("#statics > tbody > tr:nth-child(1) > td").text
      cq1 = soup.select_one("#u-solved").text
      wq1 = soup.select_one("#u-result-6").text
      wq2 = soup.select_one("body > div.wrapper > div.container.content > div.row > div:nth-child(2) > div > div.col-md-9 > div:nth-child(2) > div.panel-body").text
      src = rank.attrs['src']
      download(src,"image.svg")
      os.system("cairosvg image.svg -o image.png")
      image = discord.File("image.png", filename="rank.png")
      embed = discord.Embed(title = "[boj 정보]", color = discord.Color.blue())
      embed.add_field(name = "상태매세지", value = status, inline=False)
      embed.add_field(name = "백준 랭크", value = bojrank, inline=False)
      embed.add_field(name = "맞은 문제수", value = cq1, inline=False)
      embed.add_field(name = "틀린 횟수", value = wq1, inline = False)
      embed.add_field(name = "틀린 문제", value = wq2, inline = False)
      embed.set_thumbnail(url = "attachment://rank.png")
      await channel.send(embed=embed, file=image)

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

    if message.content == "*명령어정보":
      await channel.send(commands)

client.run(os.environ['token'])
