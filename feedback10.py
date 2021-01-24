#20201231更換LUIS帳號為wangsc2020
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials

#import datetime, json, os, time
import json, os
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



#Channel secret a2107f4d8710940b1568c6ae14415089
#b55ecac4-cc57-4dfa-8b02-902326507c54
#Channel access token  rNuJcLVeCoJwBooBW8AhsyoFTKWDN/15SdFP8ObH1SBMAbdtWK0tEQReHXE+8fRo1NtNxt1kX/6KKvqSzytsZy8RvuuFhpjmbi9a+V+eVqt+NJrYwrefxT31ckJGaZt6dtG66trfbDULq4f3bdd60QdB04t89/1O/w1cDnyilFU=

VER=0.10

idiomNumber=5000

app = Flask(__name__)
                           
line_bot_api = LineBotApi('rNuJcLVeCoJwBooBW8AhsyoFTKWDN/15SdFP8ObH1SBMAbdtWK0tEQReHXE+8fRo1NtNxt1kX/6KKvqSzytsZy8RvuuFhpjmbi9a+V+eVqt+NJrYwrefxT31ckJGaZt6dtG66trfbDULq4f3bdd60QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a2107f4d8710940b1568c6ae14415089')

#luisAppId = "4fffa055-e22e-46a0-8416-a91ffa832944"
luisAppId = "7cf6b3f3-f3d5-49b8-90ea-ad773e5c8ac8"
#luisAppKey = "e0b8bd8d20c24c799e468488a1e3aa99"
luisAppKey = "0c27389e595549eca99514047420e278"
SLOTName ='staging'
runtime_endpoint = 'https://wscluis01.cognitiveservices.azure.com/'
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
    doc_ref = db.document("log/lineMessage/test/{}".format(datetime.now()))
    #collection_ref.add({'message':'http test2','count':collection_ref.count})
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
#@app.route("/", methods=['GET'])
#http://127.0.0.1:8080/prediction?query="8月18日誦心經1部"
#http://127.0.0.1:8080/prediction?query="我要玩猜數字"
#https://westeurope.api.cognitive.microsoft.com/luis/prediction/v3.0/apps/7cf6b3f3-f3d5-49b8-90ea-ad773e5c8ac8/slots/production/predict?subscription-key=741aed7e6b864bed8d60a142eb3d1651&verbose=true&show-all-intents=true&log=true&query=要玩猜數字
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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    logMsg={}
    logMsg['message'] = event.message.text
    #用EVENT取得訊息
    queryRequest = { "query" : event.message.text }
    logMsg['query']="{}".format(queryRequest)
    response = clientRuntime.prediction.get_slot_prediction(app_id=luisAppId, slot_name=SLOTName, prediction_request=queryRequest)
    entities=response.prediction.entities
    logMsg['意圖']="{}".format(entities)
    userID=event.source.user_id
    logMsg['userID']=userID
    profile = line_bot_api.get_profile(userID)
    logMsg['姓名']=profile.display_name
    intent=response.prediction.top_intent
    logMsg['intent']="{}".format(intent)
    
    
    #於LINE回應分析結果
    try:
        message=""
        #message="意圖:{}".format(response.prediction.top_intent)+"\n元素:{}".format(response.prediction.entities)+"\n回報人: {}".format(profile.display_name)
        #message="意圖:{}".format(response.prediction.top_intent)+"\n元素:{}".format(response.prediction.entities)+"\n回報人: {}".format(profile.display_name+event.source.user_id)
        #message="意圖:{}".format(response.prediction.top_intent)
        #message=message+"\n來源類別:{}".format(event.source.type)
        groupMode="對話"
        if "group" == event.source.type:
            groupId=event.source.group_id
            #message=message+"\n群組編號:{}".format(event.source.group_id)
            #doc_ref = db.collection("lineMessage")
            #doc_ref = db.collection(u'cities').document(u'SF')
            try:
                #docs = db.collection("lineMessage").where('groupMode', 'in', ["玩成語接龍","玩猜數字"]).stream()
                docs = db.collection("lineMessage").where("modeValidPeriod",">","{}".format(datetime.now())).where('groupID', '==',groupId).where('groupMode', 'in', ["玩成語接龍","玩猜數字","對話","玩AB猜數字遊戲","遊戲結束"]).stream()
                #query = db.collection("lineMessage").where("modeValidPeriod",">","{}".format(datetime.now())).where('groupID', '==',groupId).where('groupMode', 'in', ["玩成語接龍","玩猜數字"]).order_by('time').limit_to_last(1).stream()
                #docs = query.get()
                #if docs:
                #    message=message+"\n發現狀態"+"\n{}".format(docs)+"\n{}".format(type(docs))
                for doc in docs:
                    #message=message+"\n發現狀態"
                    #message=message+"\ndocID={}".format(doc.id)
                    gameRecord=doc.to_dict()
                    #message=message+"\ntime={}".format(gameRecord['time'])
                    groupMode='{}'.format(gameRecord['groupMode'])
                    #groupMode="玩猜數字"
                    #message=message+'\nDocument data: {}'.format(gameRecord)
            except Exception as e:
                message=message+"狀態讀取錯誤={}".format(e)
                groupMode="對話"
                logMsg['groupMode']="對話"
            #message=message+"\nhello"    
        else:
            groupId=""
            groupMode="對話"
        logMsg['groupID']= groupId 
        #message=message+'\n狀態:'+groupMode+"\n遊戲紀錄{}".format(gameRecord)
        message=message+'\n狀態:'+groupMode
        if '打招呼' in intent:
            message=message+"{}".format(event)+"\n歡迎{}進來玩遊戲，人生得意須盡歡，莫使遊戲無人玩".format(logMsg['姓名'])
        elif "放棄遊戲" in intent:
            #message=message+"\n放棄遊戲".format(gameRecord['round']-1)
            if gameRecord.get("ans"):
                message=message+"\n遊戲結束\n答案為{}".format(gameRecord.get("ans"))
            doc_ref = db.document("lineMessage/{}".format(datetime.now()))
            doc_ref.set({"time":"{}".format(datetime.now()),'groupID':groupId,'groupMode':"遊戲結束","modeValidPeriod":"{}".format(gameRecord["modeValidPeriod"])})
        elif groupMode in ["對話","遊戲結束"]: 
            if '註冊' in intent:
                doc_ref = db.document("lineData/{}".format(userID))
                doc_ref.set({'registered':response.prediction.entities["姓名"][0][0],'userID':userID,"time":"{}".format(datetime.now())})
            elif '報名' in intent:
                doc_ref = db.document("lineData/{}".format(userID))
                doc_ref.set({'Sign up': response.prediction.entities["課程"][0][0],"time":"{}".format(datetime.now())})
            elif '玩猜數字' in intent:
                if groupId:
                    logMsg['groupMode']= intent
                    #doc_ref = db.document("lineData/{}".format(userID))
                    if entities.get("number"):
                        maxNumber = entities.get("number")[0]+1
                    else:   
                        maxNumber = 100
                    
                    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
                    doc_ref.set({"time":"{}".format(datetime.now()),'groupID':groupId,'groupMode':"玩猜數字","modeValidPeriod":"{}".format(datetime.now()+ timedelta(0,120)),"round":1,"max":maxNumber,"min":0,"ans":random.randint(1, maxNumber)})
                    message=message+"\n開始玩猜數字\n第1回合,數字範圍0~{},您要猜多少?".format(maxNumber)
                else:
                    message=message+"\n要在群組才成玩猜數字"
            elif '玩AB猜數字遊戲' in intent:
                if groupId:
                    logMsg['groupMode']= intent
                    #doc_ref = db.document("lineData/{}".format(userID))
                    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
                    random.shuffle(items)
                    answer=''
                    if entities.get("number"):
                        answerLen = entities.get("number")[0]
                    else:   
                        answerLen=3
                    for i in range(answerLen):
                        answer+=str(items[i])
                    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
                    doc_ref.set({"time":"{}".format(datetime.now()),'groupID':groupId,'groupMode':"玩AB猜數字遊戲","modeValidPeriod":"{}".format(datetime.now()+ timedelta(0,600)),"round":1,"len":answerLen,"ans":answer,"rec":""})
                    message=message+"\n開始玩AB猜數字\n第1回合您要猜那{}位數?".format(answerLen)
                else:
                    message=message+"\n要在群組才成玩AB猜數字遊戲"
            elif '玩成語接龍' in intent:
                if groupId:
                    logMsg['groupMode']= intent
                    #doc_ref = db.document("lineData/{}".format(userID))
                    docs=db.collection("idiom").where("no","==",random.randint(1,idiomNumber )).get()
                    idiomData=docs[0].to_dict()
                    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
                    doc_ref.set({"time":"{}".format(datetime.now()),'groupID': groupId,'groupMode':"玩成語接龍","modeValidPeriod":"{}".format(datetime.now()+ timedelta(0,6000)),"idiom":idiomData["idiom"],"last":idiomData["phonetic"][-1:][0],"round":0,"used":[idiomData["idiom"]]})
                    message=message+"\n開始從{}玩成語接龍，您要接那句成語?".format(idiomData["idiom"])
                else:
                    message=message+"\n要在群組才成玩成語接龍"
        elif groupMode=="玩成語接龍":
            try:
                
                idiom=event.message.text
                
                idiomLast = gameRecord["last"]
                
                docs=db.collection("idiom").where("idiom","==",idiom).where("first","==",idiomLast).get()
                if docs:
                    idiomData=docs[0].to_dict()
                    gameRecord["idiom"] = idiomData["idiom"]
                    gameRecord["last"] = idiomData["phonetic"][-1:][0]
                    gameRecord["round"]+=1
                    gameRecord["used"]+=[idiomData["idiom"]]
                    message=message+"\n已經猜了{}".format(gameRecord["used"])
                    if gameRecord["round"]==10:
                       message=message+",猜10個了,真是超強的!!!" 
                else:
                    message=message+"\n不能接{}!!!".format(idiom)
                gameRecord["time"]="{}".format(datetime.now())
                doc_ref = db.document("lineMessage/{}".format(datetime.now()))
                doc_ref.set(gameRecord)
                #doc_ref.set({"time":"{}".format(datetime.now()),'groupID': groupId,'groupMode':"玩成語接龍","modeValidPeriod":"{}".format(gameRecord["modeValidPeriod"]),"idiom":idiom,"last":idiomData["phonetic"][-1:],"round":gameRecord["round"],"used":gameRecord["used"]})
            except Exception as e:
                message=message+"\n{}".format(e)    
        elif groupMode=="玩猜數字": 
        #else:
            try:
                guessNumber=int(event.message.text)
            except:
                guessNumber=0
            if (guessNumber>gameRecord['min']) and (guessNumber<gameRecord['max']) :
                gameRecord["round"]=gameRecord["round"]+1
                if guessNumber==gameRecord['ans']:
                    message=message+"\n第{}回合猜中了".format(gameRecord['round']-1)
                    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
                    doc_ref.set({"time":"{}".format(datetime.now()),'groupID':groupId,'groupMode':"遊戲結束","modeValidPeriod":"{}".format(gameRecord["modeValidPeriod"]),"round":gameRecord["round"],"max":gameRecord["max"],"min":gameRecord["min"],"ans":gameRecord["ans"]})
                else:
                    message=message+"\n{},{},{}".format(gameRecord['max'],gameRecord['min'],guessNumber,gameRecord['ans'])
                    if (guessNumber > gameRecord['ans']) and (guessNumber < gameRecord['max']):
                    #if (guessNumber > gameRecord['ans']) :
                        gameRecord["max"]=guessNumber
                    if (guessNumber < gameRecord['ans']) and (guessNumber > gameRecord['min']):
                    #if (guessNumber < gameRecord['ans']) :
                        gameRecord["min"]=guessNumber
                    message=message+"\n猜錯囉，{}請加油！！！\n第{}回合,數字範圍{}~{}".format(logMsg['姓名'],gameRecord['round'],gameRecord['min'],gameRecord['max'])
                    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
                    doc_ref.set({"time":"{}".format(datetime.now()),'groupID':groupId,'groupMode':"玩猜數字","modeValidPeriod":"{}".format(gameRecord["modeValidPeriod"]),"round":gameRecord["round"],"max":gameRecord["max"],"min":gameRecord["min"],"ans":gameRecord["ans"]})
            else:
                message=message+"\n猜的數字不在範圍內，雖然只是遊戲，但{}仍請用心猜，這次老闆招待，不算次數！！！\n第{}回合,數字範圍{}~{}".format(logMsg['姓名'],gameRecord['round'],gameRecord['min'],gameRecord['max'])
        elif groupMode=="玩AB猜數字遊戲": 
            #message=message+"\n記錄:{}".format(gameRecord)
            guessNumber=event.message.text
            a_count=0 # initial A count
            b_count=0 # initial B count
            answer = gameRecord["ans"]
            answerLen = gameRecord["len"]
            rec=gameRecord["rec"]
            if (not guessNumber.isdigit()) or (len(guessNumber)!=answerLen):  #cheak all input is digit
                message=message+"\n猜的數字不符合規定，雖然只是遊戲，但{}仍請用心猜，這次老闆招待，不算次數！！！".format(logMsg['姓名'])
            else:
                if guessNumber==answer:
                    message=message+"\n第{}回合猜中了".format(gameRecord['round'])
                    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
                    doc_ref.set({"time":"{}".format(datetime.now()),'groupID':groupId,'groupMode':"遊戲結束","modeValidPeriod":"{}".format(gameRecord["modeValidPeriod"]),"round":gameRecord["round"],"ans":gameRecord["ans"]})
                else:    
                    for i in range(answerLen):
                        for j in range(answerLen):
                            if i==j and guessNumber[i]==answer[j]:
                                a_count+=1
                            elif guessNumber[i]==answer[j]:
                                b_count+=1
                    rec=rec+"\n第{}回合猜{}:{}A{}B".format(gameRecord['round'],guessNumber,a_count,b_count)
                    #message=message+"\n猜錯囉，{}請加油！！！\n第{}回合猜{}:{}A{}B".format(logMsg['姓名'],gameRecord['round'],guessNumber,a_count,b_count)            
                    message=message+"\n猜錯囉，{}請加油！！！{}".format(logMsg['姓名'],rec)            
                    gameRecord["round"]=gameRecord["round"]+1
                    doc_ref = db.document("lineMessage/{}".format(datetime.now()))
                    doc_ref.set({"time":"{}".format(datetime.now()),'groupID':groupId,'groupMode':"玩AB猜數字遊戲","modeValidPeriod":"{}".format(gameRecord["modeValidPeriod"]),"round":gameRecord["round"],"len":gameRecord["len"],"a_count":a_count,"b_count":b_count,"ans":gameRecord["ans"],"rec":rec})
        elif 'None' in intent:
            message=message+"\n歡迎{}來玩遊戲，但我不知道您要我做什麼？".format(logMsg['姓名'])
        
    except Exception as e:
        #print(e)
        message="{}{}".format(e)

    finally:
        #將訊息及結果寫入FIREBASE
        #doc_ref = db.document("lineMessage/{}".format(datetime.now()))
        doc_ref = db.document("lineMessage/{}".format(datetime.now()))
        #doc_ref = db.document("log/lineMessage/test/{}".format(datetime.now()))
        #doc_ref.set({'intent':"{}".format(intent),'message': event.message.text,'result':"{}".format(response.prediction.entities),'name':profile.display_name,'userID':userID})
        doc_ref.set(logMsg)
        line_bot_api.reply_message(
            event.reply_token,
            #TextSendMessage("版本{}\n".format(VER)+message+"\n狀態:{}".format(groupMode)))
            TextSendMessage("版本{}\n".format(VER)+message))
    
if __name__ == "__main__":
    app.run(debug=True,host='127.0.0.1',port=int(os.environ.get('PORT', 8080)))
    #app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))