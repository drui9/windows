from multiprocessing import Process

def main():
  from bottle import route, run
  @route('/')
  def home():
    return "<h1>Home</h1>"
    
  @route('/hello/<name>')
  def hello(name):
    return f"Hello, {name}!"
  run(host='localhost', port=8080, debug=True)

t = Process(target=main)
t.start()
grammer.runtime['actions']['bottle'] = t
