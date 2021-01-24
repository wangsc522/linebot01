#20201231更換LUIS帳號為wangsc2020
#http://127.0.0.1:8080/prediction?query="8月18日誦心經1部"
#http://127.0.0.1:8080/prediction?query="我要玩猜數字"
#https://westeurope.api.cognitive.microsoft.com/luis/prediction/v3.0/apps/7cf6b3f3-f3d5-49b8-90ea-ad773e5c8ac8/slots/production/predict?subscription-key=741aed7e6b864bed8d60a142eb3d1651&verbose=true&show-all-intents=true&log=true&query=要玩猜數字
#增加21點
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials

#import datetime, json, os, time
import json, os
#import numpy as np
import random
from datetime import datetime, timedelta
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

customIntent={"放棄":"放棄遊戲","我要玩21點":"玩21點","加牌":"加牌","停牌":"停牌"}
'''
ModeIntentTaskMap={
                    "對話":{"放棄遊戲":cancelGame,"註冊":regName,"報名":singup,"玩猜數字":gameGuessNumber,"玩AB猜數字遊戲":gameGuessAB,"玩成語接龍":gameIdiomSolitaire,"玩21點":gamePoker21}
                   } 
'''
#Channel secret a2107f4d8710940b1568c6ae14415089
#b55ecac4-cc57-4dfa-8b02-902326507c54
#Channel access token  rNuJcLVeCoJwBooBW8AhsyoFTKWDN/15SdFP8ObH1SBMAbdtWK0tEQReHXE+8fRo1NtNxt1kX/6KKvqSzytsZy8RvuuFhpjmbi9a+V+eVqt+NJrYwrefxT31ckJGaZt6dtG66trfbDULq4f3bdd60QdB04t89/1O/w1cDnyilFU=

"""
初始化變量撲克牌組
"""
playing_cards = {
    "♠A": 1, "♠2": 2, "♠3": 3, "♠4": 4, "♠5": 5, "♠6": 6, "♠7": 7,
    "♠8": 8, "♠9": 9, "♠10": 10, "♠J": 10, "♠Q": 10, "♠K": 10,
    "♥A": 1, "♥2": 2, "♥3": 3, "♥4": 4, "♥5": 5, "♥6": 6, "♥7": 7,
    "♥8": 8, "♥9": 9, "♥10": 10, "♥J": 10, "♥Q": 10, "♥K": 10,
    "♣A": 1, "♣2": 2, "♣3": 3, "♣4": 4, "♣5": 5, "♣6": 6, "♣7": 7,
    "♣8": 8, "♣9": 9, "♣10": 10, "♣J": 10, "♣Q": 10, "♣K": 10,
    "♦A": 1, "♦2": 2, "♦3": 3, "♦4": 4, "♦5": 5, "♦6": 6, "♦7": 7,
    "♦8": 8, "♦9": 9, "♦10": 10, "♦J": 10, "♦Q": 10, "♦K": 10
}
poker_number = 1
poker_names = list(playing_cards.keys())
A_list = ["♠A", "♥A", "♣A", "♦A"]

VER=0.11

idiomNumber=5000

app = Flask(__name__)
                           
line_bot_api = LineBotApi('rNuJcLVeCoJwBooBW8AhsyoFTKWDN/15SdFP8ObH1SBMAbdtWK0tEQReHXE+8fRo1NtNxt1kX/6KKvqSzytsZy8RvuuFhpjmbi9a+V+eVqt+NJrYwrefxT31ckJGaZt6dtG66trfbDULq4f3bdd60QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a2107f4d8710940b1568c6ae14415089')

#luisAppId = "4fffa055-e22e-46a0-8416-a91ffa832944"
luisAppId = "7cf6b3f3-f3d5-49b8-90ea-ad773e5c8ac8"
#luisAppKey = "e0b8bd8d20c24c799e468488a1e3aa99"
luisAppKey = "0c27389e595549eca99514047420e278"
SLOTName ='staging'
#runtime_endpoint = 'https://wscluis01.cognitiveservices.azure.com/'
runtime_endpoint = 'https://line001-authoring.cognitiveservices.azure.com/'
clientRuntime = LUISRuntimeClient(runtime_endpoint, CognitiveServicesCredentials(luisAppKey))



# 引用必要套件
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
cred = credentials.Certificate('serviceAccountKey.json')
                                
# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred)

# 初始化firestore
db = firestore.client()

@app.route('/', methods=['GET'])
def hello_world():
    target = os.environ.get('TARGET', 'World')
    #doc_ref = db.collection("log").document("lineMessage")
    #doc_ref = db.document(doc_path)
    #doc_ref.set({'message':'http test'})
    #collection_ref = db.document("log/lineMessage/test/{}".format(datetime.now()))
    #collection_ref.add({'message':'http test2','count':collection_ref.count})

    doc_ref = db.document("log/lineMessage/test/{}".format(datetime.now()))
    doc_ref.set({'message':'add now time '})
    return 'Hello {}!\n'.format(target)

@app.route('/ver', methods=['GET'])
def ver():
    return 'ver {} \n'.format(VER)

@app.route('/hi')
def hi():
    #target = os.environ.get('TARGET', 'World')
    return '大家好!\n'
    
@app.route('/prediction', methods=['GET'])
def prediction():
    queryText = request.args.get('query')
    print(queryText)
    queryRequest = { "query" : queryText }
    
    response = clientRuntime.prediction.get_slot_prediction(app_id=luisAppId, slot_name=SLOTName, prediction_request=queryRequest)

    print("意圖: {}".format(response.prediction.top_intent))
    #print("Sentiment: {}".format (response.prediction.sentiment))
    #print("Intents: ")

    #for intent in response.prediction.intents:
     #   print("\t{}".format (json.dumps (intent)))
    print("元素: {}".format (response.prediction.entities))
    return "意圖:{}".format(response.prediction.top_intent)+"；元素:{}".format(response.prediction.entities)

def gameSayHi(playerName):
    return "\n歡迎{}進來玩遊戲，人生得意須盡歡，莫使遊戲無人玩".format(playerName)

def gameQuit(playerName,gameRecord):
    if gameRecord.get("ans"):
        msg="\n您放棄遊戲\n答案為{}".format(gameRecord.get("ans"))
    else:    
        msg="\n您放棄遊戲結束"
    gameRecord["time"]="{}".format(datetime.now())
    gameRecord["gameMode"]="遊戲結束"
    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
    doc_ref.set(gameRecord)
    return msg

def gameGuessNumber(gameID,entities,ans):
    if entities.get("number"):
        maxNumber = entities.get("number")[0]+1
    else:   
        maxNumber = 100
    gameRecord={}
    gameRecord["time"]="{}".format(datetime.now())
    gameRecord['gameID']=gameID
    gameRecord["round"]=0
    gameRecord['gameMode']="玩猜數字"
    gameRecord["modeValidPeriod"]="{}".format(datetime.now()+ timedelta(0,3600))
    gameRecord['max']=maxNumber
    gameRecord['min']=0
    if ans:
        gameRecord['ans']=ans["ans"]
    else:    
        gameRecord['ans']=random.randint(1, maxNumber)
    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
    doc_ref.set(gameRecord)
    return "\n開始玩猜數字\n第1回合,數字範圍0~{},您要猜多少?".format(maxNumber)

def gameGuessAB(gameID,entities,ans):    
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    random.shuffle(items)
    if ans:
        answer=ans
    else:
        answer=""
        if entities.get("number"):
            answerLen = entities.get("number")[0]
        else:   
            answerLen=3
        for i in range(answerLen):
            answer+=str(items[i])
    gameRecord={}
    gameRecord["time"]="{}".format(datetime.now())
    gameRecord['gameID']=gameID
    gameRecord['gameMode']="玩AB猜"
    gameRecord["modeValidPeriod"]="{}".format(datetime.now()+ timedelta(0,3600))
    gameRecord["round"]=0
    gameRecord["len"]=answerLen
    gameRecord["ans"]=answer
    gameRecord["rec"]=""
    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
    doc_ref.set(gameRecord)
    return "\n開始玩AB猜數字\n第1回合您要猜那{}位數?".format(answerLen)

# 模塊化函數
"""
對牌組進行打亂
"""
def random_pokers(rand_poker_list):
    random.shuffle(rand_poker_list)


"""
發牌，兩種函數：
第一個，初始化發牌，一次給2張
第二個，後面叫牌，一次給1張
"""
def get_one_poker(input_poker_list):
    return input_poker_list.pop(random.randint(0, len(input_poker_list)-1))



def init_get_poker(input_poker_list):
    return [input_poker_list.pop(random.randint(0, len(input_poker_list)-1)),
            input_poker_list.pop(random.randint(0, len(input_poker_list)-1))]


"""
計算手中牌的分數
輸入：手牌
返回值：分數
"""
def score_count(hand_poker):
    score = 0
    for i in hand_poker:
        score += playing_cards.get(i)

    # 判斷有沒有A
    for i in hand_poker:
        if i in A_list:
            if score + 10 <= 21:
                score = score + 10
            else:
                break

    return score

"""
勝負判斷函數
輸入：玩家和電腦分數
輸出：輸贏情況，並且返回比分，用於加入總比分
"""
def judge_win_lose(your_score, pc_score):
    if your_score > 21 and pc_score > 21:
        return 0
    elif your_score <= 21 and pc_score > 21:
        return 1
    elif your_score > 21 and pc_score <= 21:
        return -1
    else:
        if your_score > pc_score:
            return 1
        elif your_score == pc_score:
            return 0
        else:
            return -1
    
def gamePoker21(gameID,entities,ans):
    msg=""
    # 總分情況（玩家: 電腦）
    #total_score = np.array([0, 0])
    total_score = [0, 0]
    # 初始化玩家和電腦的手牌
    your_hand_poker = []
    pc_hand_poker = []
    poker_list = poker_names * poker_number
    # 先洗牌
    random_pokers(poker_list)
    
    # 初始化兩張牌
    your_init_poker = init_get_poker(poker_list)
    pc_init_poker = init_get_poker(poker_list)

    #計算點數
    your_score = score_count(your_init_poker)
    pc_score = score_count(pc_init_poker)

    # 判斷有沒有21點

    # 遊戲提示
    msg=msg+"\n********現在是第{}局遊戲********".format(1)
    msg=msg+"\n你的手牌是：{}和{},共{}點\n電腦的手牌是：{}和？".format(your_init_poker[0], your_init_poker[1],your_score,pc_init_poker[0] )
    # 加入手牌
    your_hand_poker.extend(your_init_poker)
    pc_hand_poker.extend(pc_init_poker)
    gameRecord={}
    gameRecord["time"]="{}".format(datetime.now())
    gameRecord['gameID']=gameID
    gameRecord['gameMode']="玩21點"
    gameRecord["modeValidPeriod"]="{}".format(datetime.now()+ timedelta(0,3600))
    gameRecord["round"]=1
    gameRecord["your_hand_poker"]=your_hand_poker
    gameRecord["pc_hand_poker"]=pc_hand_poker
    gameRecord["poker_list"]=poker_list
    #gameRecord["total_score"]=total_score.tolist()
    gameRecord["total_score"]=total_score
    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
    doc_ref.set(gameRecord)
    return msg

def playPoker21NewGame(gameRecord,msg,input_poker_list):
    gameRecord["round"]+=1
    # 初始化兩張牌
    your_init_poker = init_get_poker(input_poker_list)
    pc_init_poker = init_get_poker(input_poker_list)

    #計算點數
    your_score = score_count(your_init_poker)
    pc_score = score_count(pc_init_poker)

    # 判斷有沒有21點

    # 遊戲提示
    msg+="\n********現在是第{}局遊戲********".format(gameRecord["round"])
    msg=msg+"\n你的手牌是：{}和{},共{}點\n電腦的手牌是：{}和？".format(your_init_poker[0], your_init_poker[1],your_score,pc_init_poker[0] )
    # 加入手牌
    #your_hand_poker.extend(your_init_poker)
    #pc_hand_poker.extend(pc_init_poker)
    gameRecord["your_hand_poker"]=your_init_poker
    gameRecord["pc_hand_poker"]=pc_init_poker
    #gameRecord["your_hand_poker"]=your_hand_poker
    #gameRecord["pc_hand_poker"]=pc_hand_poker
    return gameRecord,msg
    
def playPoker21Hit(playerName,command,gameRecord):
    print(gameRecord)
    #input_poker_list=gameRecord["input_poker_list"]

    #new_poker = get_one_poker(input_poker_list)
    new_poker = get_one_poker(gameRecord["poker_list"])
    gameRecord["your_hand_poker"].append(new_poker)
    your_score = score_count(gameRecord["your_hand_poker"])
    msg=""
    msg="你當前的手牌爲：{} 共{}點".format(gameRecord["your_hand_poker"],your_score)
    if your_score > 21:
        msg+="\n你的手牌超過21點，你輸了"
        gameRecord["total_score"][1]+=1
        msg+="\n當前總比分爲：(玩家:電腦)>>>>{}:{}".format(gameRecord["total_score"][0], gameRecord["total_score"][1])
        gameRecord,msg=playPoker21NewGame(gameRecord,msg,gameRecord["poker_list"])
    #gameRecord["input_poker_list"]=input_poker_list
    gameRecord["time"]="{}".format(datetime.now())
    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
    doc_ref.set(gameRecord)
    return msg

def playPoker21Stand(playerName,command,gameRecord):
    poker_list=gameRecord["poker_list"]
    your_hand_poker=gameRecord["your_hand_poker"]
    pc_hand_poker=gameRecord["pc_hand_poker"]

    pc_score = score_count(pc_hand_poker)
    your_score = score_count(your_hand_poker)
    while (your_score > pc_score) and (pc_score<18):
        new_poker = get_one_poker(poker_list)
        pc_hand_poker.append(new_poker)
        pc_score = score_count(pc_hand_poker)
    msg="此時電腦的手牌是:{}".format(pc_hand_poker)
    judgment=judge_win_lose(your_score, pc_score)
    if judgment==-1:
        msg+="\n你的手牌點數比電腦低，你輸了"
        gameRecord["total_score"][1]+=1
    elif judgment==1:
        msg+="\n你的手牌點數比電腦高，你贏了"
        gameRecord["total_score"][0]+=1
    elif judgment==0:
        msg+="\n你的手牌點數和電腦一樣，平手"
    msg+="\n當前總比分爲：(玩家:電腦)>>>>{}:{}".format(gameRecord["total_score"][0], gameRecord["total_score"][1])
    if len(gameRecord["poker_list"]) < 15:
        msg+="\n不好意思，剩餘撲克數過少，只有{}張，遊戲結束".format(len(gameRecord["poker_list"]))
        msg+="\n這盤遊戲最終比分爲：(玩家:電腦)>>>>{}:{}".format(gameRecord["total_score"][0], gameRecord["total_score"][1])
        if total_score[0] > total_score[1]:
            msg+="\n你最終贏得了勝利"
        elif total_score[0] < total_score[1]:
            msg+="\n你最終輸掉了遊戲"
        else:
            msg+="\n你和電腦五五開"
        gameRecord['gameMode']="遊戲結束"
    else:
        gameRecord,msg=playPoker21NewGame(gameRecord,msg,gameRecord["poker_list"])

    #gameRecord["input_poker_list"]=input_poker_list
    gameRecord["time"]="{}".format(datetime.now())
    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
    doc_ref.set(gameRecord)

    return msg

    
def gameIdiomSolitaire(gameID,entities,ans):
    if ans:
        idiomData=ans 
    else:   
        docs=db.collection("idiom").where("no","==",random.randint(1,idiomNumber )).get()
        if docs:
            idiomData=docs[0].to_dict()
        else:
            idiomData={}
    if idiomData:        
        gameRecord={}
        gameRecord["time"]="{}".format(datetime.now())
        gameRecord['gameID']=gameID
        gameRecord['gameMode']="玩成語接龍"
        gameRecord["modeValidPeriod"]="{}".format(datetime.now()+ timedelta(0,3600))
        gameRecord["round"]=0
        gameRecord["idiom"]=idiomData["idiom"]
        gameRecord["last"]=idiomData["phonetic"][-1:][0]
        gameRecord["used"]=[idiomData["idiom"]]
        doc_ref = db.document("lineMessage/{}".format(datetime.now()))
        doc_ref.set(gameRecord)
        msg="\n開始從[{}]玩成語接龍，您要接那句成語?".format(idiomData["idiom"])
    else:
        msg="\n無法出題!!!"
    return msg

def playIdiomSolitaire(playerName,idiom,gameRecord):
    idiomLast = gameRecord["last"]
    docs=db.collection("idiom").where("idiom","==",idiom).where("first","==",idiomLast).get()
    if docs:
        idiomData=docs[0].to_dict()
        gameRecord["time"]="{}".format(datetime.now())
        gameRecord["idiom"] = idiomData["idiom"]
        gameRecord["last"] = idiomData["phonetic"][-1:][0]
        gameRecord["round"]+=1
        gameRecord["used"]+=[idiomData["idiom"]]
        msg="\n已經猜了{}".format(gameRecord["used"])
        if gameRecord["round"]==10:
           msg=msg+",猜10個了,真是超強的!!!" 
    else:
        msg="\n不能接{}!!!".format(idiom)
    gameRecord["time"]="{}".format(datetime.now())
    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
    doc_ref.set(gameRecord)
    return msg

def playGuessNumber(playerName,guessNumber,gameRecord):
    if guessNumber.isdigit():
        guessNumber=int(guessNumber)
        if (guessNumber>gameRecord['min']) and (guessNumber<gameRecord['max']) :
            gameRecord["round"]=gameRecord["round"]+1
            gameRecord["time"]="{}".format(datetime.now())
            gameRecord["guessNumber"]=guessNumber
            if guessNumber==gameRecord['ans']:
                gameRecord["gameMode"]="遊戲結束"
                msg="\n第{}回合猜中了".format(gameRecord['round'])
                doc_ref = db.document("lineMessage/{}".format(datetime.now()))
                doc_ref.set(gameRecord)
            else:
                #msg="\n{},{},{}".format(gameRecord['max'],gameRecord['min'],guessNumber,gameRecord['ans'])
                if (guessNumber > gameRecord['ans']) and (guessNumber < gameRecord['max']):
                #if (guessNumber > gameRecord['ans']) :
                    gameRecord["max"]=guessNumber
                if (guessNumber < gameRecord['ans']) and (guessNumber > gameRecord['min']):
                #if (guessNumber < gameRecord['ans']) :
                    gameRecord["min"]=guessNumber
                msg="\n猜錯囉，{}請加油！！！\n第{}回合,數字範圍{}~{}".format(playerName,gameRecord['round']+1,gameRecord['min'],gameRecord['max'])
                doc_ref = db.document("lineMessage/{}".format(datetime.now()))
                doc_ref.set(gameRecord)
        else:
            msg="\n猜的數字不在範圍內，雖然只是遊戲，但{}仍請用心猜，這次老闆招待，不算次數！！！\n第{}回合,數字範圍{}~{}".format(playerName,gameRecord['round']+1,gameRecord['min'],gameRecord['max'])
    else:    
        msg="\n{}不是整數".format(guessNumber)    
    return msg

def playGuessAB(playerName,guessNumber,gameRecord):
    answerLen = gameRecord["len"]
    if (not guessNumber.isdigit()) or (len(guessNumber)!=answerLen):  #cheak all input is digit
        #msg="\n猜的數字不符合規定，雖然只是遊戲，但{}仍請用心猜，這次老闆招待，不算次數！！！".format(playerName)
        msg="\n猜的數字不符合規定，雖然只是遊戲，但{}仍請用心猜，這次老闆招待，不算次數！！！".format(playerName)
        #msg=msg+"{}{}{}".format(guessNumber.isdigit(),len(guessNumber),answerLen)
    else:
        gameRecord["round"]=gameRecord["round"]+1
        gameRecord["time"]="{}".format(datetime.now())
        gameRecord["guessNumber"]=guessNumber
        a_count=0 # initial A count
        b_count=0 # initial B count
        answer = gameRecord["ans"]
        
        if guessNumber==answer:
            msg="\n第{}回合猜中了".format(gameRecord['round'])
            gameRecord["gameMode"]="遊戲結束"
            doc_ref = db.document("lineMessage/{}".format(datetime.now()))
            doc_ref.set(gameRecord)
        else:    
            for i in range(answerLen):
                for j in range(answerLen):
                    if i==j and guessNumber[i]==answer[j]:
                        a_count+=1
                    elif guessNumber[i]==answer[j]:
                        b_count+=1
            gameRecord["rec"]=gameRecord["rec"]+"\n第{}回合猜{}:{}A{}B".format(gameRecord['round'],guessNumber,a_count,b_count)
            gameRecord["a_count"]=a_count
            gameRecord["b_count"]=b_count
            msg="\n沒猜中，{}請加油！！！{}".format(playerName,gameRecord["rec"])            
            doc_ref = db.document("lineMessage/{}".format(datetime.now()))
            doc_ref.set(gameRecord)
    return msg
                
#entities=response.prediction.entities
def assignTasks(eventText,playerName,userID,gameID,intent,entities,logMsg,ans={}):  
    try:
        message=""
        gameMode="對話"
        logMsg['gameID']= gameID 
        try:
            docs = db.collection("lineMessage").where("modeValidPeriod",">","{}".format(datetime.now())).where('gameID', '==',gameID).where('gameMode', 'in', ["玩成語接龍","玩猜數字","對話","玩AB猜","遊戲結束","玩21點"]).get()
        except Exception as e:
            message=message+"狀態讀取錯誤={}".format(e)
            gameMode="對話"
            logMsg['gameMode']=gameMode
            docs=[]
        #message=message+"{}".format(docs[-1:])
        if docs:
            gameRecord=docs[-1:][0].to_dict()
            if "遊戲結束" == gameRecord['gameMode']:
                gameMode="對話" 
            else:
                gameMode=gameRecord['gameMode']
        else:
            gameMode="對話"
        #message=message+'\n之前狀態:'+gameMode
        logMsg['gameMode']= intent
        if '打招呼' in intent:
            message=message+gameSayHi(playerName)
        elif "放棄遊戲" in intent:
            msg=gameQuit(playerName,gameRecord)
            message=message+msg
        elif gameMode in ["對話"]: 
            if '註冊' in intent:
                doc_ref = db.document("lineData/{}".format(userID))
                doc_ref.set({'registered':entities["姓名"][0][0],'userID':userID,"time":"{}".format(datetime.now())})
            elif '報名' in intent:
                doc_ref = db.document("lineData/{}".format(userID))
                doc_ref.set({'Sign up':entities["課程"][0][0],"time":"{}".format(datetime.now())})
            elif '玩猜數字' in intent:
                message=message+gameGuessNumber(gameID,entities,ans)
            elif '玩AB猜' in intent:
                message=message+gameGuessAB(gameID,entities,ans)
            elif '玩成語接龍' in intent:
                message=message+gameIdiomSolitaire(gameID,entities,ans)
            elif '玩21點' in intent:
                message=message+gamePoker21(gameID,entities,ans)
        elif gameMode=="玩成語接龍":
            try:
                message=message+playIdiomSolitaire(playerName,eventText,gameRecord)
            except Exception as e:
                message=message+"\n執行玩成語接龍時發生[{}]錯誤".format(e)    
        elif gameMode=="玩猜數字": 
            try:
                #print("eT:"+eventText)
                message=message+playGuessNumber(playerName,eventText,gameRecord)
            except Exception as e:
                message=message+"\n執行玩猜數字時發生[{}]錯誤".format(e)        
        elif gameMode=="玩AB猜數字遊戲": 
            try:
                message=message+playGuessAB(playerName,eventText,gameRecord)
            except Exception as e:
                message=message+"\n執行玩AB猜數字遊戲時發生[{}]錯誤".format(e)  
        elif gameMode=="玩21點": 
            '''
            try:
                if '加牌' in intent:
                    message=message+playPoker21Hit(playerName,eventText,gameRecord)
                elif '停牌' in intent:
                    message=message+playPoker21Stand(playerName,eventText,gameRecord)
            except Exception as e:
                message=message+"\n執行玩21點遊戲時發生[{}]錯誤".format(e)  
            '''    
            if '加牌' in intent:
                message=message+playPoker21Hit(playerName,eventText,gameRecord)
            elif '停牌' in intent:
                message=message+playPoker21Stand(playerName,eventText,gameRecord)
        elif 'None' in intent:
            message=message+"\n歡迎{}來玩遊戲，但我不知道您要我做什麼？".format(logMsg['姓名'])
    except Exception as e:
        #print(e)
        message=message+"\nassignTasks[{}]".format(e)

    finally:
        #將訊息及結果寫入FIREBASE
        doc_ref = db.document("lineMessage/{}".format(datetime.now()))
        doc_ref.set(logMsg)
    return message 


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def analysisIntent(sentence):
    #print(sentence)
    top_intent=customIntent.get(sentence["query"])
    if top_intent:
        entities={}
    else:
        r=clientRuntime.prediction.get_slot_prediction(app_id=luisAppId, slot_name=SLOTName, prediction_request=sentence)
        entities=r.prediction.entities
        top_intent=r.prediction.top_intent 
    return entities,top_intent

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    logMsg={}
    logMsg['message'] = event.message.text
    #用EVENT取得訊息
    
    #logMsg['query']="{}".format(event.message.text)
    entities,intent=analysisIntent({ "query" : event.message.text })
    #response = clientRuntime.prediction.get_slot_prediction(app_id=luisAppId, slot_name=SLOTName, prediction_request=queryRequest)
    #entities=response.prediction.entities
    logMsg['意圖']="{}".format(entities)
    userID=event.source.user_id
    logMsg['userID']=userID
    profile = line_bot_api.get_profile(userID)
    logMsg['姓名']=profile.display_name
    #intent=response.prediction.top_intent
    logMsg['intent']="{}".format(intent)
    #assignTasks(eventText,playerName,userID,gameID,intent,entities):
    #gameId=event.source.group_id 必需判斷 source.type分{user,userId},{roomId,room}
    try:
        if "group" == event.source.type:
            gameID=event.source.group_id
            #gameId=event["source"]["groupId"]
        elif "user" == event.source.type:
            gameID=event.source.user_id
            #gameId=event["source"]["userId"]
        elif "room" == event.source.type: 
            gameID=event.source.room_id
            #gameId=event["source"]["roomId"]
        else:
            gameID=""
        if gameID:    
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("版本{}{}".format(VER,
                    assignTasks(event.message.text,profile.display_name,event.source.user_id,gameID,intent,entities,logMsg))))
                    #assignTasks(eventText,playerName,userID,gameID,intent,entities)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("無法取得GameID!!!"))
    except Exception as e:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("{}".format(e)))
def test(note):
    print(note)
    msg=""
    testDatas=[
            {"eventText":"放棄","result":"","ans":{}}
            #,{"eventText":"玩猜數字","result":"","ans":{"ans":32}}
            #,{"eventText":"50","result":"","ans":{}}
            #,{"eventText":"20","result":"","ans":{}}
            #,{"eventText":"30","result":"","ans":{}}
            #,{"eventText":"40","result":"","ans":{}}
            #,{"eventText":"41","result":"","ans":{}}
            #,{"eventText":"32","result":"","ans":{}}
            #,{"eventText":"放棄","result":"","ans":{}}
            ,{"eventText":"我要玩21點","result":"","ans":{}}
            ,{"eventText":"加牌","result":"","ans":{}}
            ,{"eventText":"停牌","result":"","ans":{}}
            ,{"eventText":"加牌","result":"","ans":{}}
            ,{"eventText":"加牌","result":"","ans":{}}
            ,{"eventText":"停牌","result":"","ans":{}}
            ,{"eventText":"加牌","result":"","ans":{}}
            ,{"eventText":"加牌","result":"","ans":{}}
            ,{"eventText":"加牌","result":"","ans":{}}
            ,{"eventText":"加牌","result":"","ans":{}}
            ,{"eventText":"停牌","result":"","ans":{}}
            ,{"eventText":"放棄","result":"","ans":{}}
              ]
    #testDatas=[{"eventText":"玩猜數字","result":""}]
    #r=assignTasks(eventText,playerName,userID,gameID,intent,entities,logMsg)
    for data in testDatas:
        #print("測試資料:{}".format(data))
        entities,intent=analysisIntent({ "query" : data["eventText"] })
        #print("意圖:{},元素:{}".format(intent,entities))
        r=assignTasks(data["eventText"],"test1","test1:userID0001","test1:gameID0001",intent,entities,{},data["ans"])
        #print("結果:{}".format(r))
        msg+="測試資料:{}\n結果:{}\n".format(data,r)
    return msg

            
if __name__ == "__main__":
    import argparse

    #sys.argv = ['doc04.py', '--data','datasets/sentiment', '--init', 'n','--model','albert','--epoch','3']
    #sys.argv = ['doc05.py', '--data','20200416','--epoch','3']
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", required=False, help="Test Mode")
    args = parser.parse_args()
    #print(args)
    if args.test:
        print("{}".format(test(args.test)))
    else:
        app.run(debug=True,host='127.0.0.1',port=int(os.environ.get('PORT', 8080)))
    #app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))