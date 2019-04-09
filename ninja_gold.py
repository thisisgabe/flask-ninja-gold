from flask import Flask, render_template, request, redirect, session
import random, datetime
app = Flask(__name__)
app.secret_key = 'ilikecoolstuffthatisfuntodo'

def build_data():
   data = {}
   #load the number of coins
   if 'number_coins' not in session:
      print('number_coins does not exist, creating...')
      session["number_coins"] = 0
      print(session["number_coins"])
   data["number_coins"] = session["number_coins"]
   #load the activity log
   if 'activity_log' not in session:
      print('activity_log does not exist, creating...')
      data["activity_log"] = []
      session["activity_log"] = []
   else:
      data["activity_log"] = reversed(session["activity_log"])
   # return the data
   return data

def add_to_log(string, color):
   d = datetime.datetime.today()
   value = string + ' ' + d.strftime("%B %d %Y %H:%M:%S")
   session["activity_log"].append({
      'color': color,
      'text': value
   })
   print('added to activity log')
   print(value)

def updateScore(request):
   if not request.form["building_type"]:
      return
   switcher = {
      0: 'farm',
      1: 'cave',
      2: 'house',
      3: 'casino'
   }

   building = switcher.get(int(request.form["building_type"]), 'invalid')

   if building == 'farm':
      num = random.randrange(10, 21)
      session["number_coins"] += num
      add_to_log(f'visited the farm and acquired {num} coins. yay!!!', 'green')

   elif building == 'cave':
      num = random.randrange(5, 11)
      session["number_coins"] += num
      add_to_log(f'visited the cave and acquired {num} coins. yay!!!', 'green')
   elif building == 'house':
      num = random.randrange(2, 6)
      session["number_coins"] += num
      add_to_log(f'visited the house and acquired {num} coins. yay!!!', 'green')
   elif building == 'casino':
      num = random.randrange(-50, 51)
      session["number_coins"] += num
      if num > 0:
         add_to_log(f'visited the casino and acquired {num} coins. yay!!!', 'green')
      elif num < 0:
         add_to_log(f'visited the casino and got swindled for {num} coins. booo!!!', 'red')
      else:
         add_to_log("we had water at the casino and came out even. ~~neutral-ness intensifies~~", '')
   else:
      add_to_log('what the heck just happened???', '')

@app.route('/')
def main():
   return render_template("index.html", game_info=build_data())

@app.route('/destroy_session')
def destroy_session():
   print("destroying session")
   session.clear()
   return redirect('/')

@app.route('/process_money', methods=['POST'])
def index():
   print('user submitted form')
   print(request.form)
   updateScore(request)
   return redirect('/')

if __name__ == "__main__":
   app.run(debug=True)