from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from DB import chats, utils, users, ais
from Schema import base_schemas, chat_schemas
from AI import crud

router = APIRouter()

# # 유저 채팅 목록 읽기
@router.get("/user/{user_address}", response_model=chat_schemas.ChatReadList)
def get_chats(user_address: str, db: Session = Depends(utils.get_db)):
    db_chat = chats.get_chats_by_user_address(db, user_address=user_address)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat

# # @router.get("/chats/ai_id/{ai_id}", response_model=schemas.ChatTableOverViewList)
# # def get_chats(ai_id: str, db: Session = Depends(utils.get_db)):
# #     db_chat = chats.get_chats_by_ai_id(db, ai_id=ai_id)
# #     if not db_chat:
# #         raise HTTPException(status_code=404, detail="Chat not found")
# #     return schemas.ChatTableOverViewList(chats=db_chat)

# # 특정 채팅 읽기
@router.get("/messages/{chat_id}", response_model=chat_schemas.ChatMessagesRead)
def get_chat_messages(chat_id: str, db: Session = Depends(utils.get_db)):
    chat_exists = chats.check_chat_exists(db=db, chat_id=chat_id)
    if not chat_exists:
        raise HTTPException(status_code=404, detail="Chat not found")

    res = chats.get_chat_messages(db, chat_id=chat_id)
    return res

# # 챗 생성
@router.post("/", response_model=base_schemas.Chat)
def create_chat(chat: chat_schemas.ChatCreate, db: Session = Depends(utils.get_db)):
    ai_exists = ais.check_ai_exists(db, ai_id=chat.ai_id)
    if not ai_exists:
        raise HTTPException(status_code=404, detail="AI not found")

    chat_id = utils.create_chat_id(chat.user_address, chat.ai_id)
    chat_exist = chats.check_chat_exists(db, chat_id=chat_id)
    if chat_exist:
        raise HTTPException(status_code=400, detail="Chat already exists")

    chatTable = base_schemas.Chat(
        id=chat_id,
        user_address=chat.user_address,
        ai_id= chat.ai_id,
    )
    chat_message_id = utils.create_chat_message_id(chat_id=chat_id)
    chat_message = base_schemas.ChatMessage(
        id= chat_message_id,
        chat_id = chat_id,
        sender_id = chat.ai_id,
        message = "Hello! How Can I assist you?"
    )

    chats.create_chat_message(db=db, chat_message=chat_message)

    return chats.create_chat(db=db, chat=chatTable)


# # # 채팅 내용 생성
# @router.post("/chats/create_contents/{chat_id}", response_model=schemas.ChatMessage)
# def create_chat_content(chat_content: schemas.ChatContentsTableCreateInput, chat_id :str, db: Session = Depends(utils.get_db)):
#     chat_exist = chats.get_chat(db, chat_id=chat_id)
#     if not chat_exist:
#         raise HTTPException(status_code=400, detail="Chat Doesn't exists")

#     chatcontentsid = chat_id + '_' + ctime()

#     chatContentsTable = schemas.ChatContentsTableCreate(
#         chat_contents_id =  chatcontentsid,
#         chat_id =  chat_id,
#         sender_id =  chat_content.sender_id,
#         message =  chat_content.message,
#     )

#     chats.create_chat_content(db=db, chat_content=chatContentsTable)

#     #RAG 답변 생성해서 넣기
#     db_ai = ais.get_ai(db, ai_id=chat_exist.ai_id)

#     token, answer = rag_qa(chat_content.message, chat_exist.ai_id)
#     # token, answer = rag_qa(chat_content.message, "dating_adivce_ai")

#     aiUpdateDB = schemas.AITableUsageUpdate(
#         chat_counts= db_ai.chat_counts + 1,
#         prompt_tokens = db_ai.prompt_tokens + token.prompt_tokens,
#         completion_tokens = db_ai.completion_tokens + token.completion_tokens,
#     )
    
#     ais.update_usage_ai(db=db, ai_id=chat_exist.ai_id, ai_update=aiUpdateDB)


#     chatcontentsid = "AI_" + chat_id + ctime()

#     answerContentsTable = schemas.ChatContentsTableCreate(
#         chat_contents_id =  chatcontentsid,
#         chat_id=  chat_id,
#         sender_id = chat_exist.ai_id,
#         message =  answer,
#     )

#     suiapi.pay_usage(ai=db_ai, tokens=token.prompt_tokens)

#     return chats.create_chat_content(db=db, chat_content=answerContentsTable)