from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import pandas as pd

from agent.core import run_agent

from tools.platform import (
    send_whatsapp_broadcast,
    compose_email
)

app = FastAPI()

# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# GLOBAL EXCEL STORAGE
# =========================================

uploaded_df = None

# =========================================
# CHAT MODEL
# =========================================

class ChatRequest(BaseModel):
    text: str

# =========================================
# NORMAL BROADCAST MODEL
# =========================================

class BroadcastRequest(BaseModel):

    type: str

    recipients: list[str]

    subject: str = ""

    message: str

# =========================================
# SMART BROADCAST MODEL
# =========================================

class SmartBroadcastRequest(BaseModel):

    query: str

    type: str

    message: str

    subject: str = ""

# =========================================
# CHAT ROUTE
# =========================================

@app.post("/chat")
async def chat(data: ChatRequest):

    try:

        result = run_agent(data.text)

        return {

            "response": result

        }

    except Exception as e:

        return {

            "response":
            f"Error: {str(e)}"

        }

# =========================================
# EXCEL UPLOAD
# =========================================

@app.post("/upload-excel")
async def upload_excel(

    file: UploadFile = File(...)

):

    global uploaded_df

    try:

        uploaded_df = pd.read_excel(
            file.file
        )

        print("\n📄 EXCEL DATA:")
        print(uploaded_df)

        return {

            "response":
            "Excel uploaded successfully",

            "columns":
            uploaded_df.columns.tolist(),

            "rows":
            len(uploaded_df)

        }

    except Exception as e:

        return {

            "response":
            f"Upload failed: {str(e)}"

        }

# =========================================
# NORMAL BROADCAST
# =========================================

@app.post("/broadcast")
async def broadcast(data: BroadcastRequest):

    print("\n====================")
    print("📢 BROADCAST REQUEST")
    print("====================")

    print("TYPE:", data.type)
    print("RECIPIENTS:", data.recipients)
    print("SUBJECT:", data.subject)
    print("MESSAGE:", data.message)

    # =====================================
    # WHATSAPP
    # =====================================

    if data.type == "whatsapp":

        result = send_whatsapp_broadcast(

            data.recipients,

            data.message

        )

        return {

            "response": result

        }

    # =====================================
    # EMAIL
    # =====================================

    elif data.type == "email":

        result = compose_email(

            data.recipients,

            data.subject,

            data.message

        )

        return {

            "response": result

        }

    return {

        "response":
        "Unknown broadcast type"

    }

# =========================================
# SMART BROADCAST
# =========================================

@app.post("/smart-broadcast")
async def smart_broadcast(

    data: SmartBroadcastRequest

):

    global uploaded_df

    try:

        if uploaded_df is None:

            return {

                "response":
                "No Excel uploaded"

            }

        query = data.query.lower()

        print(
            f"\n🔍 SEARCH QUERY: {query}"
        )

        # =================================
        # FILTER DATAFRAME
        # =================================

        filtered_df = uploaded_df[

            uploaded_df.apply(

                lambda row:

                row.astype(str)

                .str.lower()

                .str.contains(query)

                .any(),

                axis=1

            )

        ]

        print("\n📄 FILTERED DATA:")
        print(filtered_df)

        # =================================
        # WHATSAPP
        # =================================

        if data.type == "whatsapp":

            recipients = filtered_df[
                "Phone Number"
            ].astype(str).tolist()

            print(
                "\n📞 RECIPIENTS:"
            )

            print(recipients)

            result = send_whatsapp_broadcast(

                recipients,

                data.message

            )

            return {

                "response": result,

                "matched":
                len(recipients)

            }

        # =================================
        # EMAIL
        # =================================

        elif data.type == "email":

            recipients = filtered_df[
                "Email ID"
            ].astype(str).tolist()

            print(
                "\n📧 RECIPIENTS:"
            )

            print(recipients)

            result = compose_email(

                recipients,

                data.subject,

                data.message

            )

            return {

                "response": result,

                "matched":
                len(recipients)

            }

        return {

            "response":
            "Invalid type"

        }

    except Exception as e:

        return {

            "response":
            f"Error: {str(e)}"

        }