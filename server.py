from flask import Flask,request,redirect
 
app = Flask(__name__)
 
nextid = 4
topics = [
    {'id': 1, 'title': 'html', 'body': 'html is ...'},
    {'id': 2, 'title': 'css', 'body': 'css is ...'},
    {'id': 3, 'title': 'javascript', 'body': 'javascript is ...'}
]

def template(contents,content,id=None):#id=None는 이 함수가 
    #호출될 때 id 값이 전달되지 않으면 기본적으로 None이 되도록 설정한 것입니다.
    contextui = ''
    if id != None:
        contextui = f'''
<li><a href="/update/{id}/">update</a></li>
    ''' 
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
             {content}
             <ul>
             <li><a href="/create/">create</a></li>
             {contextui}
             </ul>
        </body>
    </html>
    '''

def getcontent():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags

 
@app.route('/')
def index():
    return template(getcontent(),"<h2>welcome</h2>hello,WEB")
 
@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']  
            break
    return template(getcontent(),f'<h2>{title}</h2>{body}',id)

@app.route('/create/', methods=["GET","POST"]) # GET,POST 요청만 받을것을 정의함.(쓰지않았을때의 기본은 GET방식)
def create():
    print("request method :",request.method)
    if request.method == 'GET':
        content = """
        <form action="/create/" method="POST"> 
            <p><input type="text" name ="title" placeholder = "제목"></p>
            <p><textarea name="body" placeholder = "내용을 입력하세요"></textarea></p>
            <p><input type="submit" value="create"></p>
        </form>
        """
        return template(getcontent(),content)
    elif request.method == 'POST':
        global nextid
        title = request.form["title"] #html 폼에서 입력한 username 정보 가져옴
        body = request.form['body']
        newtopic = {'id':nextid,'title':title,'body':body}
        topics.append(newtopic)
        nextid += 1
        url = '/read/' + str(nextid) +'/'
        return redirect(url) #redirect 함수는 클라이언트를 새로운 위치로 자동으로 이동시킴

@app.route('/update/<int:id>/', methods=["GET","POST"]) 
def update(id):
    if request.method == 'GET':
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']  
                break
        content = f"""
            <form action="/update/{id}" method="POST"> 
                <p><input type="text" name ="title" placeholder = "제목" value={title} ></p>
                <p><textarea name="body" placeholder = "내용을 입력하세요">{body}</textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
            """

        return template(getcontent(),content)
    
    elif request.method == 'POST':
        titles = request.form["title"]
        bodyes = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = titles
                topic['body'] = bodyes
                break
        url = '/read/' + str(id) +'/'
        return redirect(url)

app.run(debug=True)