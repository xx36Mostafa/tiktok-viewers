import base64
import requests
import re
import pytesseract
import urllib
import random
import string , time
from requests_toolbelt import MultipartEncoder
from rich import print as printf
from rich.console import Console
from rich.panel import Panel
SUCCESS = 0
class tiktok:
    def __init__(self):
        ter = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        pytesseract.pytesseract.tesseract_cmd = ter
        self.session = requests.Session()

    def downloadImage(self,img):
        img_src = 'https://zefoy.com'+img
        headers = {
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }
        response = requests.get(img_src,cookies=self.session.cookies.get_dict(),headers=headers)
        with open('cap.png','wb') as e:
            e.write(response.content)
        text = pytesseract.image_to_string("cap.png")
        text = text.replace("\n","")
        return text

    def login(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            }
        r = self.session.get('https://zefoy.com/', headers=self.headers)
        self.PHPSESSID = r.cookies.get('PHPSESSID')
        match = re.search(r'<img[^>]+src="([^"]+)"', r.text)
        if match:
            img_src = match.group(1)
            input_name = re.search(r'<input[^>]+name="([^"]+)"', r.text).group(1)
            solve = self.downloadImage(img_src)
            data = {
                input_name: solve,
            }
            # printf(f"[bold blue]  ──> Captcha Solve Is: [bold white]{solve}         ")
            r2 = self.session.post('https://zefoy.com/', cookies=self.session.cookies.get_dict(), headers=self.headers, data=data)
            if 'placeholder="Enter Video URL"' in str(r2.text):
                printf(f"[bold green]   ──> LOGIN SUCCESSFUL!           ",end='\r')
                time.sleep(2.5)
                return r2.text
            else:
                printf(f"[bold red]   ──> LOGIN FAILED!              ",end='\r')
                time.sleep(2.5)
                return self.login()
        else:
            self.session.close()
            self.session = requests.Session()
            return self.login()
        
    def delay(self,menit, detik):
        total = (menit * 60 + detik)
        while (total):
            menit, detik = divmod(total, 60)
            printf(f"[bold bright_white]  ──>[bold white] Time[bold green] {menit:02d}:{detik:02d}[bold white] Success:[bold green]{SUCCESS} [bold white]Viewers:[bold green]{SUCCESS*1000} ", end='\r')
            time.sleep(1)
            total -= 1
        return 1

    def antiLogOut(self):
        pass

    def start(self):
        global SUCCESS
        response = self.login()
        if response:
            input_name_test = re.search(r'<input[^>]+name="([^"]+)"', response).group(1)
            boundary = '----WebKitFormBoundary'+ ''.join(random.sample(string.ascii_letters + string.digits, 16))
            # PHPSESSID = self.session.cookies.get('PHPSESSID')
            cookies = {
                'PHPSESSID': self.PHPSESSID,
                'user_agent': 'Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F127.0.6533.100%20Safari%2F537.36',
                'window_size': '1920x284',
                '__gads': 'ID=55ac059df2e6570a:T=1724114824:RT=1724119584:S=ALNI_MZSj7RTUNK79WobpAGWKanpeneSPg',
                '__gpi': 'UID=00000e9cbd65f4d5:T=1724114824:RT=1724119584:S=ALNI_MapKZPbPYarOq1l4WLqoaespqgIDQ',
                '__eoi': 'ID=fb87c25b30e3e8eb:T=1724114824:RT=1724119584:S=AA-Afjbezjpo5mU7zkWAaAWdS3Bc',
                'FCNEC': '%5B%5B%22AKsRol-tf-iHoB244R73hX-vN1889p8fSOEjM3qF2ZlnnYVDNm6WFJSWJs5atp6v9W5U4yqzynyh8TZaTX-yd3wa2MCo37lsix8e_jlk9tYUjDE3Z-ykv6WleDe8QxpLZy3JrG9RqdXpEQuBgE0__szFvmfYa85TVg%3D%3D%22%5D%5D',
            }

            headers = {
                'accept': '*/*',
                'accept-language': 'en-US',
                'content-type': 'multipart/form-data; boundary='+boundary,
                'origin': 'https://zefoy.com',
                'PHPSESSID':self.PHPSESSID,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
                }

            data = MultipartEncoder(
                            {
                                input_name_test: (None, video_url)
                            }, boundary=boundary
                        )
            response_co = self.session.post('https://zefoy.com/c2VuZC9mb2xeb3dlcnNfdGlrdG9V', cookies=cookies, headers=headers, data=data)
            hidden_input_src = base64.b64decode(urllib.parse.unquote(response_co.text[::-1])).decode()
            if 'seconds for your next submit' in hidden_input_src:
                sec = str(hidden_input_src).split('var ltm=')[1].split(';')[0]
                self.delay(0,int(sec))
                # printf(f"[bold RED] Please Wait Message.. Trying Again Now!", end='\r')
                self.start()
            else:
                find_form_videoid = re.search('type="hidden" name="(.*?)" value="(\d+)"', str(hidden_input_src))
                videoid = find_form_videoid.group(2)
                next_post_action = re.search('action="(.*?)"', str(hidden_input_src)).group(1)
                hidden_input_name = re.search(r'<input[^>]+name="([^"]+)"', hidden_input_src).group(1)
                boundary = '----WebKitFormBoundary' \
                + ''.join(random.sample(string.ascii_letters + string.digits, 16))
                headers['content-type'] = 'multipart/form-data; boundary='+boundary
                data = MultipartEncoder(
                                {
                                    hidden_input_name: (None, videoid)
                                }, boundary=boundary
                            )
                response_ttt = requests.post(f'https://zefoy.com/{next_post_action}',cookies=cookies, headers=headers, data=data)
                if response_ttt.content == b'':
                    printf(f"[bold RED] Failed.. Try Again Now!", end='\r')
                    self.start()
                else:
                    SUCCESS += 1
                    printf(Panel(f"""[bold white]Status :[bold green] Successfully...
[bold white]Viewers :[bold red] {SUCCESS*1000}""", width=56, style="bold bright_white", title="[ Success ]"))
                    printf(f"[bold bright_white]   ───>[bold green] TRY SENDING VIEWS AGAIN!           ", end='\r')
                    
if __name__ == '__main__':
    printf(Panel(f"[italic red]Number of Viewers required .. Note: 1 = 1K Viewers!", width=56, style="bold bright_white", title="[ Viewers Required ]", subtitle="╭─────", subtitle_align="left"))
    num = Console().input("[bold bright_white]   ╰─> ")
    printf(Panel(f"[italic white]Please fill in your tiktok video link, make sure the account is not private and the\nlink is correct. Take the video link via browser!", width=56, style="bold bright_white", title="[ Link Video ]", subtitle="╭─────", subtitle_align="left"))
    video_url = Console().input(f"[bold bright_white]   ╰─> ")
    for i in range(int(num)):
        try:
            bot = tiktok()
            bot.start()
        except:
            pass